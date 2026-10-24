"""Construit le paquet Anki CV-Pilote.apkg depuis les cartes du vault.

Le paquet s'importe directement dans AnkiDroid. Le GUID de chaque note est
dérivé de l'ID pédagogique : une nouvelle importation met à jour la note au
lieu de la dupliquer, tant que l'ID et le type de note restent inchangés.

La conversion Markdown → HTML couvre le sous-ensemble décrit dans
docs/export-apkg.md ; les constructions refusées citent l'ID de la carte.
Seule la construction dépend de genanki :

    uv run --no-project --with genanki==0.13.1 python scripts/build_apkg.py

La vérification (--verifier) et la comparaison (--comparer) n'utilisent que
la bibliothèque standard.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import html
from importlib import metadata
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import tempfile
from urllib.parse import quote
import zipfile

if __package__:
    from .check_vault import DECK_ROOT, FIELDS, MODEL, SECTION_BY_FOLDER, check_vault, wiki_target
else:
    from check_vault import DECK_ROOT, FIELDS, MODEL, SECTION_BY_FOLDER, check_vault, wiki_target

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = "CV-Pilote.apkg"
MANIFEST_NAME = "CV-Pilote-manifest.json"
DEFAULT_FICHE_URL = "https://github.com/speillet/Knowledge_Computer_Vision/blob/main/vault/"
FIELD_SEPARATOR = "\x1f"


class ConversionError(ValueError):
    """Syntaxe Markdown non prise en charge dans une carte."""


class BuildError(RuntimeError):
    """Vault invalide ou paquet impossible à construire."""


def parse_cards(vault):
    """Cartes des fichiers thématiques, dans l'ordre des fichiers et des blocs."""
    vault = Path(vault).resolve()
    cards = []
    for path in sorted(vault.glob("*/*.md")):
        if path.parent.name not in SECTION_BY_FOLDER or path.name == "00-index.md":
            continue
        text = path.read_text(encoding="utf-8")
        decks = re.findall(r"^TARGET DECK: (.+)$", text, re.M)
        for block in re.finditer(r"^START\n(.*?)\nEND$", text, re.M | re.S):
            lines = block[1].splitlines()
            fields, current, tags = {}, None, []
            for line in lines[1:]:
                if line.startswith("Tags: "):
                    tags = line[6:].split()
                    current = None
                    continue
                if re.fullmatch(r"<!--ID: \d+-->", line):
                    continue
                field = re.match(r"^(ID|Question|Reponse|Source): (.*)$", line)
                if field:
                    current = field[1]
                    fields[current] = field[2]
                elif current:
                    fields[current] += "\n" + line
            cards.append({
                "id": fields.get("ID", "").strip(),
                "deck": decks[0] if decks else None,
                "fields": {name: fields.get(name, "").strip() for name in FIELDS},
                "tags": tags,
                "file": path,
            })
    return cards


def _inline(text):
    """Échappe le texte puis applique gras et italique ; garde les marqueurs \x00n\x00."""
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return re.sub(r"(?<![\w*])\*(?=\S)(.+?)(?<=\S)\*(?![\w*])", r"<i>\1</i>", text)


def md_to_html(text, *, card_path, vault, fiche_url=DEFAULT_FICHE_URL, media=None):
    """Convertit le Markdown d'un champ de carte en HTML pour Anki.

    Formules : `$…$` devient `\\(…\\)` et `$$…$$` devient `\\[…\\]`, les seuls
    délimiteurs MathJax d'Anki. Les images locales sont ajoutées à `media`
    et référencées par leur nom de fichier. Les wikilinks pointent vers la
    fiche publiée sous `fiche_url` ; sans URL, seul leur libellé est gardé.
    """
    vault = Path(vault).resolve()
    stash = []

    def keep(fragment):
        stash.append(fragment)
        return f"\x00{len(stash) - 1}\x00"

    def code_block(match):
        return keep(f"<pre><code>{html.escape(match[1], quote=False)}</code></pre>")

    def image(match):
        target = (Path(card_path).parent / match[2]).resolve()
        if not target.is_relative_to(vault) or not target.is_file():
            raise ConversionError(f"image absente ou hors vault : {match[2]}")
        if media is not None:
            media.add(target)
        return keep(f'<img src="{html.escape(target.name)}" alt="{html.escape(match[1])}">')

    def wikilink(match):
        target = wiki_target(match[1])
        label = match[1].split("|", 1)[1] if "|" in match[1] else Path(target).name
        if not fiche_url:
            return keep(_inline(label))
        url = fiche_url + quote(target) + ".md"
        return keep(f'<a href="{html.escape(url)}">{_inline(label)}</a>')

    def link(match):
        return keep(f'<a href="{html.escape(match[2])}">{_inline(match[1])}</a>')

    text = re.sub(r"^```[^\n]*\n(.*?)\n```[ \t]*$", code_block, text, flags=re.M | re.S)
    text = re.sub(r"`([^`\n]+)`",
                  lambda m: keep(f"<code>{html.escape(m[1], quote=False)}</code>"), text)
    text = re.sub(r"\$\$(.+?)\$\$",
                  lambda m: keep("\\[" + html.escape(m[1].strip(), quote=False) + "\\]"),
                  text, flags=re.S)
    text = re.sub(r"\$([^$\n]+?)\$",
                  lambda m: keep("\\(" + html.escape(m[1], quote=False) + "\\)"), text)
    if "$" in text:
        raise ConversionError("délimiteur de formule `$` orphelin")
    for line in text.splitlines():
        if re.match(r"\s*(#{1,6} |\||> )", line):
            raise ConversionError(f"syntaxe non prise en charge (titre, tableau ou citation) : {line.strip()[:40]}")
    text = re.sub(r"!\[([^\]\n]*)\]\(([^\s)]+)\)", image, text)
    text = re.sub(r"\[\[([^\]\n]+)\]\]", wikilink, text)
    text = re.sub(r"\[([^\]\n]+)\]\(([^\s)]+)\)", link, text)
    text = _inline(text)

    blocks = []
    for block in re.split(r"\n[ \t]*\n", text.strip()):
        runs = []
        for line in block.split("\n"):
            bullet = re.match(r"\s*[-*] (.*)", line)
            number = re.match(r"\s*\d+\. (.*)", line)
            kind = "ul" if bullet else "ol" if number else "p"
            content = (bullet or number)[1] if kind != "p" else line
            if runs and runs[-1][0] == kind:
                runs[-1][1].append(content)
            else:
                runs.append((kind, [content]))
        for kind, lines in runs:
            if kind == "p":
                joined = "<br>".join(lines)
                if re.fullmatch(r"\x00\d+\x00", joined) and stash[int(joined[1:-1])].startswith("<pre>"):
                    blocks.append(joined)
                else:
                    blocks.append(f"<p>{joined}</p>")
            else:
                items = "".join(f"<li>{item}</li>" for item in lines)
                blocks.append(f"<{kind}>{items}</{kind}>")
    result = "".join(blocks)
    while "\x00" in result:
        result = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m[1])], result)
    return result


def convert_card(card, vault, fiche_url=DEFAULT_FICHE_URL, media=None):
    """Champs HTML d'une carte ; une erreur de conversion cite son ID."""
    converted = {"ID": html.escape(card["id"])}
    for name in FIELDS[1:]:
        try:
            converted[name] = md_to_html(card["fields"][name], card_path=card["file"],
                                         vault=vault, fiche_url=fiche_url, media=media)
        except ConversionError as error:
            raise ConversionError(f"{card['id']}, champ {name} : {error}") from None
    return converted


def deck_id(name):
    """ID de deck stable, dérivé du nom complet du deck."""
    return int(hashlib.sha256(name.encode("utf-8")).hexdigest()[:12], 16)


def expected_guid(card_id):
    """GUID genanki 0.13.1, relu sans dépendance : SHA-256 puis base 91.

    Algorithme vérifié dans genanki/util.py ; les valeurs de compatibilité
    du paquet initial sont figées dans les tests.
    """
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&()*+,-./:;<=>?@[]^_`{|}~"
    value = int.from_bytes(hashlib.sha256(f"{MODEL}__{card_id}".encode()).digest()[:8], "big")
    digits = []
    while value:
        value, remainder = divmod(value, len(alphabet))
        digits.append(alphabet[remainder])
    return "".join(reversed(digits))


def fingerprint(fields, tags):
    payload = json.dumps([fields, sorted(tags)], ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def load_model(anki_dir=ROOT / "anki"):
    anki_dir = Path(anki_dir)
    spec = json.loads((anki_dir / "model.json").read_text(encoding="utf-8"))
    if spec["name"] != MODEL or spec["fields"] != FIELDS or spec["deckRoot"] != DECK_ROOT:
        raise BuildError("anki/model.json ne correspond pas au contrat du contrôleur")
    if len(spec["templates"]) != 1 or not isinstance(spec.get("modelId"), int):
        raise BuildError("anki/model.json doit avoir un seul gabarit et un modelId entier")
    template = spec["templates"][0]
    return {
        "id": spec["modelId"],
        "templates": [{
            "name": template["name"],
            "qfmt": (anki_dir / template["front"]).read_text(encoding="utf-8"),
            "afmt": (anki_dir / template["back"]).read_text(encoding="utf-8"),
        }],
        "css": (anki_dir / spec["css"]).read_text(encoding="utf-8"),
    }


def git_commit(root=ROOT):
    """Commit courant, suffixé de -modifie si vault, anki ou scripts diffèrent de HEAD."""
    try:
        commit = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], check=True,
                                capture_output=True, text=True).stdout.strip()
        dirty = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--",
                                "vault", "anki", "scripts"], check=True,
                               capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    return commit + ("-modifie" if dirty else "")


def build_package(vault=ROOT / "vault", out_dir=ROOT / "dist", fiche_url=DEFAULT_FICHE_URL,
                  timestamp=None, anki_dir=ROOT / "anki"):
    """Écrit le paquet et son manifeste dans out_dir ; retourne le manifeste."""
    import genanki

    vault, out_dir = Path(vault).resolve(), Path(out_dir)
    errors, counts = check_vault(vault)
    if errors:
        raise BuildError("contrôle du vault en échec :\n" + "\n".join(errors))
    spec = load_model(anki_dir)
    model = genanki.Model(spec["id"], MODEL, fields=[{"name": name} for name in FIELDS],
                          templates=spec["templates"], css=spec["css"])
    decks, media, entries = {}, set(), {}
    for card in parse_cards(vault):
        fields = convert_card(card, vault, fiche_url, media)
        guid = genanki.guid_for(MODEL, card["id"])
        note = genanki.Note(model=model, fields=[fields[name] for name in FIELDS],
                            tags=card["tags"], guid=guid)
        if card["deck"] not in decks:
            decks[card["deck"]] = genanki.Deck(deck_id(card["deck"]), card["deck"])
        decks[card["deck"]].add_note(note)
        entries[card["id"]] = {"guid": guid, "deck": card["deck"],
                               "empreinte": fingerprint(fields, card["tags"])}
    if len(entries) != counts["cartes"]:
        raise BuildError(f"{len(entries)} cartes lues pour {counts['cartes']} contrôlées")
    out_dir.mkdir(parents=True, exist_ok=True)
    package = genanki.Package(list(decks.values()), media_files=sorted(str(p) for p in media))
    package.write_to_file(str(out_dir / PACKAGE_NAME), timestamp=timestamp)
    built_at = datetime.fromtimestamp(timestamp, timezone.utc) if timestamp else datetime.now(timezone.utc)
    manifest = {
        "paquet": PACKAGE_NAME,
        "genere_le": built_at.isoformat(timespec="seconds"),
        "commit": git_commit(),
        "genanki": metadata.version("genanki"),
        "modele": {"nom": MODEL, "id": spec["id"]},
        "comptes": {"notes": len(entries), "decks": len(decks), "medias": len(media)},
        "medias": sorted(p.name for p in media),
        "cartes": dict(sorted(entries.items())),
    }
    (out_dir / MANIFEST_NAME).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def verify_package(apkg, expected_decks=None):
    """Relit ZIP/SQLite ; expected_decks associe chaque ID au deck du vault."""
    errors = []
    with zipfile.ZipFile(apkg) as archive, tempfile.TemporaryDirectory() as temp:
        names = set(archive.namelist())
        if "collection.anki2" not in names or "media" not in names:
            return ["collection.anki2 ou media absent du paquet"], {}
        media = json.loads(archive.read("media"))
        for index in media:
            if index not in names:
                errors.append(f"média {media[index]} déclaré mais absent du zip")
        archive.extract("collection.anki2", temp)
        connection = sqlite3.connect(Path(temp) / "collection.anki2")
        try:
            notes = connection.execute("SELECT id, guid, flds, tags, mid FROM notes").fetchall()
            cards = connection.execute("SELECT nid, did, ord FROM cards").fetchall()
            deck_json, model_json = connection.execute("SELECT decks, models FROM col").fetchone()
            decks, models = json.loads(deck_json), json.loads(model_json)
        finally:
            connection.close()
    guids = [note[1] for note in notes]
    if len(guids) != len(set(guids)):
        errors.append("GUID dupliqués dans le paquet")
    ids = []
    cards_by_note = {}
    note_ids = {note[0] for note in notes}
    for nid, did, ordinal in cards:
        cards_by_note.setdefault(nid, []).append((did, ordinal))
        if nid not in note_ids:
            errors.append(f"carte liée à une note absente : {nid}")
    model_id = json.loads((ROOT / "anki/model.json").read_text(encoding="utf-8"))["modelId"]
    media_names = set(media.values())
    for nid, guid, flds, tags, mid in notes:
        fields = flds.split(FIELD_SEPARATOR)
        if len(fields) != len(FIELDS):
            errors.append(f"note à {len(fields)} champs au lieu de {len(FIELDS)}")
            continue
        ids.append(fields[0])
        card_id = html.unescape(fields[0])
        if guid != expected_guid(card_id):
            errors.append(f"{card_id} : GUID différent de l'identité pédagogique")
        model = models.get(str(mid), {})
        if (mid != model_id or model.get("name") != MODEL
                or [field["name"] for field in model.get("flds", [])] != FIELDS
                or len(model.get("tmpls", [])) != 1):
            errors.append(f"{card_id} : modèle différent du contrat")
        note_cards = cards_by_note.get(nid, [])
        if len(note_cards) != 1:
            errors.append(f"{card_id} : {len(note_cards)} cartes au lieu d'une")
        else:
            did, ordinal = note_cards[0]
            deck_name = decks.get(str(did), {}).get("name", "")
            if ordinal != 0:
                errors.append(f"{card_id} : gabarit de carte différent de Rappel")
            if (not deck_name.startswith(DECK_ROOT + "::")
                    or expected_decks is not None and deck_name != expected_decks.get(card_id)):
                errors.append(f"{card_id} : sous-deck différent du vault")
        if f"cv_id::{html.unescape(fields[0])}" not in tags.split():
            errors.append(f"{fields[0]} : tag cv_id absent ou différent de l'ID")
        prose = re.sub(r"<pre>.*?</pre>|<code>.*?</code>", "", "".join(fields), flags=re.S)
        if "$" in prose:
            errors.append(f"{fields[0]} : délimiteur `$` non converti")
        for source in re.findall(r'<img src="([^"]+)"', "".join(fields)):
            if html.unescape(source) not in media_names:
                errors.append(f"{fields[0]} : média {source} absent du paquet")
    if len(ids) != len(set(ids)):
        errors.append("IDs pédagogiques dupliqués dans le paquet")
    if expected_decks is not None and set(ids) != set(expected_decks):
        errors.append(f"IDs du paquet différents du vault : {len(ids)} contre {len(expected_decks)}")
    deck_names = sorted(deck["name"] for deck in decks.values()
                        if deck["name"].startswith(DECK_ROOT + "::"))
    summary = {"notes": len(notes), "cartes": len(cards), "decks": deck_names,
               "medias": sorted(media_names)}
    return errors, summary


def compare_manifests(old, new):
    """Cartes ajoutées, modifiées et retirées entre deux manifestes."""
    before, after = old.get("cartes", {}), new.get("cartes", {})
    return {
        "ajoutees": sorted(after.keys() - before.keys()),
        "modifiees": sorted(card for card in after.keys() & before.keys()
                            if after[card]["empreinte"] != before[card]["empreinte"]),
        "retirees": sorted(before.keys() - after.keys()),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--vault", type=Path, default=ROOT / "vault")
    parser.add_argument("--sortie", type=Path, default=ROOT / "dist",
                        help="dossier du paquet et du manifeste (défaut : dist/)")
    parser.add_argument("--lien-fiches", default=DEFAULT_FICHE_URL,
                        help="URL de base des fiches ; chaîne vide pour garder le libellé seul")
    parser.add_argument("--verifier", type=Path, metavar="APKG",
                        help="vérifier un paquet existant sans le reconstruire")
    parser.add_argument("--comparer", type=Path, metavar="MANIFESTE",
                        help="comparer un manifeste antérieur au manifeste de --sortie")
    args = parser.parse_args()

    if args.comparer:
        old = json.loads(args.comparer.read_text(encoding="utf-8"))
        new = json.loads((args.sortie / MANIFEST_NAME).read_text(encoding="utf-8"))
        print(json.dumps(compare_manifests(old, new), ensure_ascii=False, indent=2))
        return 0
    if args.verifier:
        expected = {card["id"]: card["deck"] for card in parse_cards(args.vault)}
        errors, summary = verify_package(args.verifier, expected)
    else:
        try:
            manifest = build_package(args.vault, args.sortie, args.lien_fiches)
        except ModuleNotFoundError as error:
            print(f"{error}. Lancer : uv run --no-project --with genanki==0.13.1 "
                  "python scripts/build_apkg.py", file=sys.stderr)
            return 2
        except (BuildError, ConversionError) as error:
            print(error, file=sys.stderr)
            return 1
        expected = {key: value["deck"] for key, value in manifest["cartes"].items()}
        errors, summary = verify_package(args.sortie / PACKAGE_NAME, expected)
        summary["paquet"] = str(args.sortie / PACKAGE_NAME)
        summary["commit"] = manifest["commit"]
    for error in errors:
        print(error, file=sys.stderr)
    summary["decks"] = len(summary.get("decks", []))
    print(json.dumps({"resultat": "ECHEC" if errors else "OK", **summary}, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
