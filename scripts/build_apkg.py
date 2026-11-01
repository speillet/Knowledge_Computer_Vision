"""Build CV-Pilote.apkg from the vault and preserve stable note identities.

Importing a newer package updates existing notes when pedagogical IDs and the
note type remain unchanged. The Markdown-to-HTML subset is documented in
/docs/export-apkg.md. Unsupported constructs identify the affected card.

Only building requires genanki:
    uv run --no-project --with genanki==0.13.1 python scripts/build_apkg.py

Verification (--verify) and comparison (--compare) use the standard library.
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
DEFAULT_FICHE_URL = 'https://github.com/speillet/Knowledge_Computer_Vision/blob/main/vault/'
FIELD_SEPARATOR = "\x1f"


class ConversionError(ValueError):
    """Markdown syntax not supported in a flashcard."""


class BuildError(RuntimeError):
    """vault invalid or package impossible to build."""


def parse_cards(vault):
    """flashcards thematic files, in order of files and blocks."""
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
    """Escape the text and apply bold and italic; preserve the null-delimited placeholders."""
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return re.sub(r"(?<![\w*])\*(?=\S)(.+?)(?<=\S)\*(?![\w*])", r"<i>\1</i>", text)


def md_to_html(text, *, card_path, vault, fiche_url=DEFAULT_FICHE_URL, media=None):
    """Converts the Markdown of a field from flashcard to HTML for Anki.

Formulas: `$…$` becomes `\\(…\\)` and `$$…$$` becomes `\\[…\\]`, the only MathJax delimiters of Anki. Local images are added to `media` and referenced by their filename. Wikilinks point to the reference note published under `fiche_url`; without a URL, only their label is kept.

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
            raise ConversionError(f"absent or out of vault: {match[2]}")
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
        raise ConversionError('`$` orphan delimiter')
    for line in text.splitlines():
        if re.match(r"\s*(#{1,6} |\||> )", line):
            raise ConversionError(f"unsupported syntax (heading, table, or quotation): {line.strip()[:40]}")
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
    """HTML fields of a flashcard; a conversion error cites its ID."""
    converted = {"ID": html.escape(card["id"])}
    for name in FIELDS[1:]:
        try:
            converted[name] = md_to_html(card["fields"][name], card_path=card["file"],
                                         vault=vault, fiche_url=fiche_url, media=media)
        except ConversionError as error:
            raise ConversionError(f"{card['id']}, field {name} : {error}") from None
    return converted


def deck_id(name):
    """Stable deck ID, derived from the deck's full name."""
    return int(hashlib.sha256(name.encode("utf-8")).hexdigest()[:12], 16)


def expected_guid(card_id):
    """GUID genanki 0.13.1, read without dependency: SHA-256 then base 91.

Checked algorithm in genanki/util.py; the compatibility values of the initial packet are fixed in the tests.

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
        raise BuildError("anki/model.json does not match the controller's contract")
    if len(spec["templates"]) != 1 or not isinstance(spec.get("modelId"), int):
        raise BuildError('anki/model.json must have a single template and an integer modelId')
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
    """Commit current, suffixed to -modifies if vault, anki or scripts differ from HEAD."""
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
    """Writes the packet and its manifest in out_dir; returns the manifest."""
    import genanki

    vault, out_dir = Path(vault).resolve(), Path(out_dir)
    errors, counts = check_vault(vault)
    if errors:
        raise BuildError('check of vault failed:\n' + "\n".join(errors))
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
        raise BuildError(f"{len(entries)} flashcards read for {counts['cartes']} Controlled")
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
    """Read ZIP/SQLite; expected_decks matches each ID to the vault deck."""
    errors = []
    with zipfile.ZipFile(apkg) as archive, tempfile.TemporaryDirectory() as temp:
        names = set(archive.namelist())
        if "collection.anki2" not in names or "media" not in names:
            return ['collection.anki2 or media missing from package'], {}
        media = json.loads(archive.read("media"))
        for index in media:
            if index not in names:
                errors.append(f"Media {media[index]} declared but absent from the zip")
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
        errors.append('Duplicate GUID in the package')
    ids = []
    cards_by_note = {}
    note_ids = {note[0] for note in notes}
    for nid, did, ordinal in cards:
        cards_by_note.setdefault(nid, []).append((did, ordinal))
        if nid not in note_ids:
            errors.append(f"flashcard linked to an absent note: {nid}")
    model_id = json.loads((ROOT / "anki/model.json").read_text(encoding="utf-8"))["modelId"]
    media_names = set(media.values())
    for nid, guid, flds, tags, mid in notes:
        fields = flds.split(FIELD_SEPARATOR)
        if len(fields) != len(FIELDS):
            errors.append(f"Note to {len(fields)} Fields instead of {len(FIELDS)}")
            continue
        ids.append(fields[0])
        card_id = html.unescape(fields[0])
        if guid != expected_guid(card_id):
            errors.append(f"{card_id} : GUID different from pedagogical identity")
        model = models.get(str(mid), {})
        if (mid != model_id or model.get("name") != MODEL
                or [field["name"] for field in model.get("flds", [])] != FIELDS
                or len(model.get("tmpls", [])) != 1):
            errors.append(f"{card_id} : different model of the contract")
        note_cards = cards_by_note.get(nid, [])
        if len(note_cards) != 1:
            errors.append(f"{card_id} : {len(note_cards)} flashcards instead of one")
        else:
            did, ordinal = note_cards[0]
            deck_name = decks.get(str(did), {}).get("name", "")
            if ordinal != 0:
                errors.append(f"{card_id} : flashcard template different from Recall")
            if (not deck_name.startswith(DECK_ROOT + "::")
                    or expected_decks is not None and deck_name != expected_decks.get(card_id)):
                errors.append(f"{card_id} : sub-deck different from vault")
        if f"cv_id::{html.unescape(fields[0])}" not in tags.split():
            errors.append(f"{fields[0]} : cv_id tag absent or different from ID")
        prose = re.sub(r"<pre>.*?</pre>|<code>.*?</code>", "", "".join(fields), flags=re.S)
        if "$" in prose:
            errors.append(f"{fields[0]} `$` delimiter not converted")
        for source in re.findall(r'<img src="([^"]+)"', "".join(fields)):
            if html.unescape(source) not in media_names:
                errors.append(f"{fields[0]} Media {source} Absent from package")
    if len(ids) != len(set(ids)):
        errors.append('Duplicate educational IDs in the package')
    if expected_decks is not None and set(ids) != set(expected_decks):
        errors.append(f"Package IDs different from vault: {len(ids)} contre {len(expected_decks)}")
    deck_names = sorted(deck["name"] for deck in decks.values()
                        if deck["name"].startswith(DECK_ROOT + "::"))
    summary = {"notes": len(notes), "cartes": len(cards), "decks": deck_names,
               "medias": sorted(media_names)}
    return errors, summary


def compare_manifests(old, new):
    """flashcards added, modified and removed between two manifests."""
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
    parser.add_argument("--output", "--sortie", dest="sortie", metavar="DIRECTORY", type=Path, default=ROOT / "dist",
                        help='package and manifest folder (default: dist/)')
    parser.add_argument("--reference-url", "--lien-fiches", dest="lien_fiches", metavar="URL", default=DEFAULT_FICHE_URL,
                        help='Base URL of reference notes; empty string to keep label alone')
    parser.add_argument("--verify", "--verifier", dest="verifier", type=Path, metavar="APKG",
                        help='Check an existing package without rebuilding it')
    parser.add_argument("--compare", "--comparer", dest="comparer", type=Path, metavar="MANIFEST",
                        help='compare an earlier manifest with the manifest in --output')
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
            print(f"{error}. Run: uv run --no-project --with genanki==0.13.1 "
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
