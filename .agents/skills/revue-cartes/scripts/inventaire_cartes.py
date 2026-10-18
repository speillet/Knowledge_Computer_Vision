"""Inventaire en lecture seule des cartes du vault, pour le skill revue-cartes.

Liste, par fichier de cartes : deck, IDs, familles, objectifs, provenance,
présence d'une identité Anki, longueur des réponses et sources. Calcule aussi
les familles absentes et le prochain ID libre par préfixe. Avec --comparer,
compare l'inventaire courant à un JSON produit avant modification.

Ce script ne remplace pas scripts/check_vault.py : il décrit le contenu pour
l'audit, sans juger la conformité complète du format. Bibliothèque standard,
Python 3.9+.
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
HEADER = re.compile(r"Objectif : (.*?) Famille : (\S+?)\. Provenance : (\S+?)\.")
URL = re.compile(r"https?://[^\s)>\]]+")
WIKILINK = re.compile(r"\[\[([^\]|#]+)")
SYNC = re.compile(r"<!--ID: (\d+)-->")


def words(text):
    return len(re.findall(r"\w+", text))


def parse_card_file(path, root):
    """Retourne la description d'un fichier de cartes et ses anomalies."""
    text = path.read_text(encoding="utf-8")
    rel = str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
    anomalies = []
    decks = re.findall(r"^TARGET DECK: (.+)$", text, re.M)
    if len(decks) != 1:
        anomalies.append(f"{rel}: {len(decks)} ligne(s) TARGET DECK au lieu d'une")
    starts = len(re.findall(r"^START$", text, re.M))
    ends = len(re.findall(r"^END$", text, re.M))
    blocks = list(re.finditer(r"^START\n(.*?)\nEND$", text, re.M | re.S))
    if not (starts == ends == len(blocks)):
        anomalies.append(f"{rel}: START={starts}, END={ends}, blocs complets={len(blocks)}")

    cards, previous_end = [], 0
    for block in blocks:
        header = text[previous_end:block.start()]
        previous_end = block.end()
        lines = block[1].splitlines()
        fields, current, tags, sync_ids = {}, None, [], []
        if not lines or lines[0] != MODEL:
            anomalies.append(f"{rel}: bloc sans modèle {MODEL}")
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
            anomalies.append(f"{rel}: {identity or 'bloc sans ID'} : champ(s) absent(s) {', '.join(missing)}")
        head = HEADER.search(header)
        if identity and f"## {identity}\n" not in header:
            anomalies.append(f"{rel}: {identity} : titre ## absent avant le bloc")
        if not head:
            anomalies.append(f"{rel}: {identity or 'bloc sans ID'} : ligne Objectif/Famille/Provenance absente")
        family_tags = [t[len("famille::"):] for t in tags if t.startswith("famille::")]
        domain_tags = [t[len("cv::"):] for t in tags if re.fullmatch(r"cv::d\d{2}", t)]
        source = fields.get("Source", "")
        cards.append({
            "id": identity,
            "famille": family_tags[0] if len(family_tags) == 1 else None,
            "famille_entete": head[2] if head else None,
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
            anomalies.append(f"{rel}: {identity} : famille du tag ({card['famille']}) "
                             f"différente de l'en-tête ({card['famille_entete']})")
        if len(sync_ids) > 1:
            anomalies.append(f"{rel}: {identity} : plusieurs identités Anki")

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
    vault = next((p for p in [target, *target.parents] if (p / "00-Accueil.md").is_file()), root)
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
                anomalies.append(f"ID dupliqué {card['id']} : {seen[card['id']]} et {description['fichier']}")
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
    """Différences d'IDs pédagogiques et d'identités Anki entre deux inventaires."""
    def index(data):
        return {c["id"]: c for f in data["fichiers"] for c in f["cartes"]}
    old, new = index(before), index(after)
    lines = []
    for identity in sorted(old.keys() - new.keys()):
        lines.append(f"ID disparu : {identity}")
    for identity in sorted(new.keys() - old.keys()):
        lines.append(f"ID ajouté : {identity}")
    for identity in sorted(old.keys() & new.keys()):
        if old[identity]["identite_anki"] != new[identity]["identite_anki"]:
            lines.append(f"Identité Anki modifiée pour {identity} : "
                         f"{old[identity]['identite_anki']} -> {new[identity]['identite_anki']}")
    return lines


def render(data):
    out = [f"Vault : {data['racine_vault']}",
           f"Fichiers de cartes : {data['totaux']['fichiers']} ; cartes : {data['totaux']['cartes']}"]
    for deck, count in sorted(data["totaux"]["decks"].items(), key=lambda item: str(item[0])):
        out.append(f"  {deck} : {count}")
    for description in data["fichiers"]:
        out.append("")
        out.append(f"## {description['fichier']} ({description['deck']})")
        for card in description["cartes"]:
            anki = "anki" if card["identite_anki"] else "-"
            out.append(f"- {card['id']} | {card['famille']} | {card['mots_reponse']} mots | "
                       f"{anki} | {card['objectif']}")
        out.append(f"Familles absentes : {', '.join(description['familles_absentes']) or 'aucune'}")
    out.append("")
    out.append("Prochains IDs libres : " + ", ".join(data["prochain_id"].values()))
    out.append("Anomalies : " + ("aucune" if not data["anomalies"] else ""))
    out.extend(f"- {problem}" for problem in data["anomalies"])
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("chemin", nargs="?", type=Path, default=Path("vault"),
                        help="fichier de cartes ou dossier (défaut : vault)")
    parser.add_argument("--json", action="store_true", help="sortie JSON complète")
    parser.add_argument("--comparer", type=Path,
                        help="JSON d'un inventaire antérieur à comparer")
    args = parser.parse_args()
    try:
        data = inventory(args.chemin)
    except FileNotFoundError as error:
        print(f"Chemin introuvable : {error}", file=sys.stderr)
        return 2
    if args.comparer:
        differences = compare(json.loads(args.comparer.read_text(encoding="utf-8")), data)
        print("\n".join(differences) if differences else "Aucune différence d'ID ni d'identité Anki.")
        return 1 if differences else 0
    print(json.dumps(data, ensure_ascii=False, indent=2) if args.json else render(data))
    return 1 if data["anomalies"] else 0


if __name__ == "__main__":
    sys.exit(main())
