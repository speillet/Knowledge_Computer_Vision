"""Read-only inventory of the flashcards of the vault, for the skill revue-cartes.

List, by flashcards file: deck, IDs, families, objectives, provenance, presence of an identity Anki, length of answers and sources. Also calculates missing families and the next free ID by prefix. With --comparer, compare the current inventory to a product JSON before modification.

This script does not replace scripts/check_vault.py: it describes the contents for the audit, without judging the complete conformity of the format. Standard library, Python 3.9+.
"""

import argparse
import json
from pathlib import Path
import re
import sys

MODEL = "CV-Pilote"
FIELDS = ["ID", "Question", "Reponse", "Source"]
FAMILIES = ["comprehension", "raisonnement", "algorithme", "comparaison",
            "diagnostic", "pratique", "evaluation", "conception"]
HEADER = re.compile(r"Objective: (.*?) Family: (\S+?)\. Provenance: (\S+?)\.")
FAMILY_TAGS = {
    "understanding": "comprehension", "reasoning": "raisonnement",
    "algorithm": "algorithme", "comparison": "comparaison", "diagnosis": "diagnostic",
    "practice": "pratique", "evaluation": "evaluation", "design": "conception",
}
URL = re.compile(r"https?://[^\s)>\]]+")
WIKILINK = re.compile(r"\[\[([^\]|#]+)")
SYNC = re.compile(r"<!--ID: (\d+)-->")


def words(text):
    return len(re.findall(r"\w+", text))


def parse_card_file(path, root):
    """Returns the description of a flashcards file and its anomalies."""
    text = path.read_text(encoding="utf-8")
    rel = str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
    anomalies = []
    decks = re.findall(r"^TARGET DECK: (.+)$", text, re.M)
    if len(decks) != 1:
        anomalies.append(f"{rel}: {len(decks)} line(s) TARGET DECK instead of a")
    starts = len(re.findall(r"^START$", text, re.M))
    ends = len(re.findall(r"^END$", text, re.M))
    blocks = list(re.finditer(r"^START\n(.*?)\nEND$", text, re.M | re.S))
    if not (starts == ends == len(blocks)):
        anomalies.append(f"{rel}: START={starts}, END={ends}, complete blocks={len(blocks)}")

    cards, previous_end = [], 0
    for block in blocks:
        header = text[previous_end:block.start()]
        previous_end = block.end()
        lines = block[1].splitlines()
        fields, current, tags, sync_ids = {}, None, [], []
        if not lines or lines[0] != MODEL:
            anomalies.append(f"{rel}: block without model {MODEL}")
        for line in lines[1:]:
            if line.startswith("Tags: "):
                tags = line[6:].split()
                current = None
                continue
            sync = SYNC.fullmatch(line)
            if sync:
                sync_ids.append(sync[1])
                continue
            field = re.match(r"^(ID|Question|Reponse|Source): (.*)$", line)
            if field:
                current = field[1]
                fields[current] = field[2]
            elif current:
                fields[current] += "\n" + line
        identity = fields.get("ID", "").strip()
        missing = [name for name in FIELDS if not fields.get(name, "").strip()]
        if missing:
            anomalies.append(f"{rel}: {identity or 'Block without ID'} : field(s) absent {', '.join(missing)}")
        head = HEADER.search(header)
        if identity and f"## {identity}\n" not in header:
            anomalies.append(f"{rel}: {identity} missing ## heading before block")
        if not head:
            anomalies.append(f"{rel}: {identity or 'Block without ID'} : Objective/Family/Provenance line absent")
        family_tags = [t[len("famille::"):] for t in tags if t.startswith("famille::")]
        domain_tags = [t[len("cv::"):] for t in tags if re.fullmatch(r"cv::d\d{2}", t)]
        source = fields.get("Source", "")
        cards.append({
            "id": identity,
            "famille": family_tags[0] if len(family_tags) == 1 else None,
            "famille_entete": FAMILY_TAGS.get(head[2], head[2]) if head else None,
            "objectif": head[1] if head else None,
            "provenance": head[3] if head else None,
            "domaine": domain_tags[0] if len(domain_tags) == 1 else None,
            "identite_anki": sync_ids[0] if len(sync_ids) == 1 else None,
            "mots_question": words(fields.get("Question", "")),
            "mots_reponse": words(fields.get("Reponse", "")),
            "fiches": sorted(set(WIKILINK.findall(source))),
            "urls": sorted(set(URL.findall(source))),
            "tags": tags,
        })
        card = cards[-1]
        if card["famille"] and card["famille_entete"] and card["famille"] != card["famille_entete"]:
            anomalies.append(f"{rel}: {identity} The Tag Family ({card['famille']}) "
                             f"different from the header ({card['famille_entete']})")
        if len(sync_ids) > 1:
            anomalies.append(f"{rel}: {identity} : several identities Anki")

    covered = sorted({c["famille"] for c in cards if c["famille"]})
    return {
        "fichier": rel,
        "deck": decks[0] if len(decks) == 1 else None,
        "cartes": cards,
        "familles_couvertes": covered,
        "familles_absentes": [f for f in FAMILIES if f not in covered],
    }, anomalies


def inventory(target):
    target = target.resolve()
    if not target.exists():
        raise FileNotFoundError(target)
    root = target if target.is_dir() else target.parent
    vault = next((p for p in [target, *target.parents] if (p / '00-Accueil.md').is_file()), root)
    candidates = [target] if target.is_file() else sorted(target.rglob("*.md"))
    files, anomalies = [], []
    for path in candidates:
        if ".obsidian" in path.parts:
            continue
        if not re.search(r"^START$", path.read_text(encoding="utf-8"), re.M):
            continue
        description, problems = parse_card_file(path, vault)
        files.append(description)
        anomalies.extend(problems)

    seen, next_ids, decks = {}, {}, {}
    for description in files:
        decks[description["deck"]] = decks.get(description["deck"], 0) + len(description["cartes"])
        for card in description["cartes"]:
            if card["id"] in seen:
                anomalies.append(f"Duplicate ID {card['id']} : {seen[card['id']]} and {description['fichier']}")
            seen[card["id"]] = description["fichier"]
            match = re.fullmatch(r"(.+)-(\d{3})", card["id"])
            if match:
                prefix, number = match[1], int(match[2])
                next_ids[prefix] = max(next_ids.get(prefix, 1), number + 1)
    return {
        "racine_vault": str(vault),
        "fichiers": files,
        "totaux": {"fichiers": len(files), "cartes": len(seen), "decks": decks},
        "prochain_id": {prefix: f"{prefix}-{n:03d}" for prefix, n in sorted(next_ids.items())},
        "anomalies": anomalies,
    }


def compare(before, after):
    """Differences in educational IDs and Anki identities between two inventories."""
    def index(data):
        return {c["id"]: c for f in data["fichiers"] for c in f["cartes"]}
    old, new = index(before), index(after)
    lines = []
    for identity in sorted(old.keys() - new.keys()):
        lines.append(f"ID removed : {identity}")
    for identity in sorted(new.keys() - old.keys()):
        lines.append(f"ID added: {identity}")
    for identity in sorted(old.keys() & new.keys()):
        if old[identity]["identite_anki"] != new[identity]["identite_anki"]:
            lines.append(f"Identity Anki modified for {identity} : "
                         f"{old[identity]['identite_anki']} -> {new[identity]['identite_anki']}")
    return lines


def render(data):
    out = [f"Vault : {data['racine_vault']}",
           f"Files from flashcards: {data['totaux']['fichiers']} ; flashcards {data['totaux']['cartes']}"]
    for deck, count in sorted(data["totaux"]["decks"].items(), key=lambda item: str(item[0])):
        out.append(f"  {deck} : {count}")
    for description in data["fichiers"]:
        out.append("")
        out.append(f"## {description['fichier']} ({description['deck']})")
        for card in description["cartes"]:
            anki = "anki" if card["identite_anki"] else "-"
            out.append(f"- {card['id']} | {next((label for label, tag in FAMILY_TAGS.items() if tag == card['famille']), card['famille'])} | {card['mots_reponse']} words | "
                       f"{anki} | {card['objectif']}")
        out.append(f"Absent families: {', '.join(next((label for label, tag in FAMILY_TAGS.items() if tag == family), family) for family in description['familles_absentes']) or 'none'}")
    out.append("")
    out.append('Next free IDs: ' + ", ".join(data["prochain_id"].values()))
    out.append('Anomalies: ' + ("none" if not data["anomalies"] else ""))
    out.extend(f"- {problem}" for problem in data["anomalies"])
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("chemin", metavar="PATH", nargs="?", type=Path, default=Path("vault"),
                        help='flashcards file or folder (default: vault)')
    parser.add_argument("--json", action="store_true", help='Complete JSON output')
    parser.add_argument("--compare", "--comparer", dest="comparer", metavar="MANIFEST", type=Path,
                        help='JSON of an earlier inventory to compare')
    args = parser.parse_args()
    try:
        data = inventory(args.chemin)
    except FileNotFoundError as error:
        print(f"Path not found: {error}", file=sys.stderr)
        return 2
    if args.comparer:
        differences = compare(json.loads(args.comparer.read_text(encoding="utf-8")), data)
        print("\n".join(differences) if differences else 'No difference in ID or Anki identity.')
        return 1 if differences else 0
    print(json.dumps(data, ensure_ascii=False, indent=2) if args.json else render(data))
    return 1 if data["anomalies"] else 0


if __name__ == "__main__":
    sys.exit(main())
