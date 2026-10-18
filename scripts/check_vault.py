"""Contrôles du contrat documentaire du pilote, sans dépendance externe.

Le sous-ensemble pris en charge : répertoires thématiques de vault_sections.json,
front matter plat, liens Markdown simples, wikilinks depuis la racine et blocs
START/END du modèle CV-Pilote.
Ce contrôleur n'est ni un parseur Markdown général ni un synchroniseur Anki.
"""

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

MODEL = "CV-Pilote"
DECK_ROOT = "CV::Pilote"
SECTIONS = json.loads((Path(__file__).with_name("vault_sections.json")).read_text(encoding="utf-8"))
SECTION_BY_FOLDER = {section["dossier"]: section for section in SECTIONS}
FIELDS = ["ID", "Question", "Reponse", "Source"]
FAMILIES = {"comprehension", "raisonnement", "algorithme", "comparaison",
            "diagnostic", "pratique", "evaluation", "conception"}
RUBRICS = ["Noyau attendu", "Approfondissement", "Erreurs bloquantes"]
META_FIELDS = {"id", "type", "domaine", "priorite", "profondeur", "statut",
               "provenance", "revision", "tags", "poles"}


def parse_poles(value):
    """Liste YAML simple de lettres, avec guillemets facultatifs ; pas du YAML général."""
    if not value.startswith("[") or not value.endswith("]"):
        return None
    values = [item.strip().strip("\"'") for item in value[1:-1].split(",")]
    if not values or any(item not in "ABCDEF" or len(item) != 1 for item in values):
        return None
    return values if len(values) == len(set(values)) else None


def without_fences(text):
    return re.sub(r"^```[^\n]*\n.*?^```\s*$", "", text, flags=re.M | re.S)


def wiki_target(link):
    return link.split("|", 1)[0].split("#", 1)[0]


def check_vault(root):
    """Retourne erreurs et compteurs ; les échecs scientifiques sont hors portée."""
    root = Path(root).resolve()
    errors = []
    files = sorted(root.rglob("*.md"))
    files = [p for p in files if ".obsidian" not in p.relative_to(root).parts]
    notes, pedagogical_ids, sync_ids = {}, set(), set()
    counts = {"markdown": len(files), "fiches": 0, "cartes": 0}

    def fail(path, message):
        errors.append(f"{path.relative_to(root)}: {message}")

    def check_target(path, target, wiki=False):
        if urlsplit(target).scheme or target.startswith("#"):
            return
        local = unquote(target.split("#", 1)[0])
        if not local:
            return
        candidate = (root / local if wiki else path.parent / local).resolve()
        if wiki and not candidate.suffix:
            candidate = candidate.with_suffix(".md")
        if not candidate.is_relative_to(root) or not candidate.is_file():
            fail(path, f"lien local absent ou hors vault : {target}")

    for path in files:
        text = path.read_text(encoding="utf-8")
        clean = without_fences(text)
        is_card_file = (path.parent.parent == root and path.parent.name in SECTION_BY_FOLDER
                        and path.name != "00-index.md")
        if not is_card_file and re.search(r"^START$", text, re.M):
            fail(path, "bloc START hors d'un fichier de cartes thématique")
        if any(line.rstrip() != line for line in text.splitlines()):
            fail(path, "espaces en fin de ligne")
        if len(re.findall(r"^```", text, re.M)) % 2:
            fail(path, "bloc de code non fermé")
        if clean.count("$$") % 2:
            fail(path, "formule display non fermée")
        for match in re.finditer(r"!?\[[^\]\n]*\]\(([^\s)]+)\)", clean):
            check_target(path, match[1])
        for match in re.finditer(r"^\[[^\]]+\]:\s*(\S+)", clean, re.M):
            check_target(path, match[1])
        for match in re.finditer(r"\[\[([^\]]+)\]\]", clean):
            check_target(path, wiki_target(match[1]), wiki=True)
        definitions = {m[1].casefold() for m in
                       re.finditer(r"^\[([^\]]+)\]:", clean, re.M)}
        for match in re.finditer(r"\[[^\]]+\]\[([^\]]+)\]", clean):
            if match[1].casefold() not in definitions:
                fail(path, f"référence Markdown absente : {match[1]}")
        if (path.parent.name != "references" or path.parent.parent.name not in SECTION_BY_FOLDER
                or path.parent.parent.parent != root):
            continue
        counts["fiches"] += 1
        front = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        meta = dict(re.findall(r"^(\w+):\s*(.+)$", front[1], re.M)) if front else {}
        if not META_FIELDS <= meta.keys():
            fail(path, "métadonnées de fiche incomplètes")
        if parse_poles(meta.get("poles", "")) is None:
            fail(path, "pôles de fiche attendus : lettres uniques A à F dans une liste non vide")
        if not re.fullmatch(r"d(?:0[1-9]|1[0-4])", meta.get("domaine", "")):
            fail(path, "domaine attendu entre d01 et d14")
        if meta.get("domaine") != SECTION_BY_FOLDER[path.parent.parent.name]["domaine"]:
            fail(path, "domaine de fiche différent de son répertoire thématique")
        if meta.get("provenance") not in {"agent", "apprenant", "mixte"}:
            fail(path, "provenance de rédaction absente ou invalide")
        if meta.get("id") in pedagogical_ids:
            fail(path, "identifiant de fiche dupliqué")
        pedagogical_ids.add(meta.get("id"))
        notes[path] = meta
        if not re.search(r"https://", text):
            fail(path, "source HTTPS absente")

    media_names = set()
    media_suffixes = {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif"}
    for media in root.rglob("*"):
        if media.is_file() and media.suffix.lower() in media_suffixes and ".obsidian" not in media.relative_to(root).parts:
            name = media.name.casefold()
            if name in media_names:
                fail(media, "basename de média dupliqué")
            media_names.add(name)

    card_ids = set()
    card_files = [path for path in files if path.parent.parent == root
                  and path.parent.name in SECTION_BY_FOLDER and path.name != "00-index.md"]
    for path in card_files:
        text = path.read_text(encoding="utf-8")
        decks = re.findall(r"^TARGET DECK: (.+)$", text, re.M)
        section = SECTION_BY_FOLDER[path.parent.name]
        expected_deck = f"{DECK_ROOT}::{section['dossier']}"
        if decks != [expected_deck]:
            fail(path, f"un seul deck cible {expected_deck} est attendu pour cette thématique")
        blocks = list(re.finditer(r"^START\n(.*?)\nEND$", text, re.M | re.S))
        if len(blocks) != len(re.findall(r"^START$", text, re.M)) or len(blocks) != len(re.findall(r"^END$", text, re.M)):
            fail(path, "marqueurs START/END non équilibrés")
        previous_end = 0
        for block in blocks:
            counts["cartes"] += 1
            header = text[previous_end:block.start()]
            previous_end = block.end()
            lines = block[1].splitlines()
            if not lines or lines[0] != MODEL:
                fail(path, f"modèle attendu : {MODEL}")
                continue
            fields, current, tags = {}, None, None
            block_sync_count = 0
            for line in lines[1:]:
                if line.startswith("Tags: "):
                    if tags is not None:
                        fail(path, "Tags répété")
                    tags = line[6:].split()
                    continue
                sync = re.fullmatch(r"<!--ID: (\d+)-->", line)
                if tags is not None:
                    if sync:
                        block_sync_count += 1
                        if block_sync_count > 1 or line != lines[-1]:
                            fail(path, "une seule identité Anki, immédiatement avant END")
                        if sync[1] in sync_ids:
                            fail(path, "identité Anki dupliquée")
                        sync_ids.add(sync[1])
                    else:
                        fail(path, "seule l'identité Anki est permise après Tags")
                    continue
                field = re.match(r"^(ID|Question|Reponse|Source): (.*)$", line)
                if field:
                    current = field[1]
                    if current in fields:
                        fail(path, f"champ répété : {current}")
                    fields[current] = field[2]
                elif current:
                    fields[current] += "\n" + line
                else:
                    fail(path, "texte avant le premier champ")
            if list(fields) != FIELDS or any(not v.strip() for v in fields.values()):
                fail(path, "champs absents, vides ou dans le mauvais ordre")
            identity = fields.get("ID", "")
            if not re.fullmatch(r"CV-[A-Z0-9-]+-\d{3}", identity):
                fail(path, "identifiant pédagogique invalide")
            if identity in card_ids:
                fail(path, f"identifiant de carte dupliqué : {identity}")
            card_ids.add(identity)
            if f"## {identity}\n" not in header or not all(word in header for word in ("Objectif :", "Famille :", "Provenance :")):
                fail(path, f"{identity} : objectif/famille/provenance hors bloc absent")
            tags = tags or []
            families = [t.removeprefix("famille::") for t in tags if t.startswith("famille::")]
            if len(families) != 1 or families[0] not in FAMILIES:
                fail(path, f"{identity} : famille absente ou inconnue")
            required_tags = {"cv::pilote", f"cv_id::{identity}", "provenance::agent"}
            if not required_tags <= set(tags):
                fail(path, f"{identity} : tags d'identité/provenance incomplets")
            for rubric in RUBRICS:
                if f"**{rubric}**" not in fields.get("Reponse", ""):
                    fail(path, f"{identity} : rubrique absente : {rubric}")
            source = fields.get("Source", "")
            parents = re.findall(r"\[\[([^\]]+)\]\]", source)
            parent = root / (wiki_target(parents[0]) + ".md") if len(parents) == 1 else None
            if parent not in notes:
                fail(path, f"{identity} : fiche parente absente ou ambiguë")
            elif f"cv::{notes[parent].get('domaine')}" not in tags:
                fail(path, f"{identity} : domaine différent de sa fiche")
            elif notes[parent].get("domaine") != section["domaine"]:
                fail(path, f"{identity} : carte rangée dans une autre thématique que sa fiche")
            if parent in notes:
                expected_poles = parse_poles(notes[parent].get("poles", ""))
                actual_poles = [tag.removeprefix("pole::") for tag in tags if tag.startswith("pole::")]
                if (expected_poles is None or set(actual_poles) != set(expected_poles)
                        or len(actual_poles) != len(set(actual_poles))):
                    fail(path, f"{identity} : étiquettes de pôle différentes de la fiche")
                for tag in tags:
                    if tag.startswith("cas_pole::"):
                        parts = tag.split("::")
                        if (len(parts) != 3 or parts[1] not in actual_poles
                                or parts[2] not in {"conception", "diagnostic"}
                                or parts[2] not in families):
                            fail(path, f"{identity} : étiquette de cas métier invalide")
            if "https://" not in source:
                fail(path, f"{identity} : source externe absente")
    if not counts["fiches"] or not counts["cartes"]:
        errors.append("Le vault doit contenir des fiches et des cartes.")
    return errors, counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault", nargs="?", type=Path,
                        default=Path(__file__).resolve().parents[1] / "vault")
    args = parser.parse_args()
    errors, counts = check_vault(args.vault)
    model_path = Path(__file__).resolve().parents[1] / "anki" / "model.json"
    model = json.loads(model_path.read_text(encoding="utf-8"))
    if (model["name"] != MODEL or model["fields"] != FIELDS
            or len(model["templates"]) != 1 or model["deckRoot"] != DECK_ROOT):
        errors.append("Le manifeste Anki ne correspond pas au contrat du contrôleur.")
    for error in errors:
        print(error, file=sys.stderr)
    print(json.dumps({"resultat": "ECHEC" if errors else "OK", **counts}, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
