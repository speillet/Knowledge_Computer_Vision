"""Simule import, révision et ré-importation du paquet avec le moteur d'Anki.

    uv run --no-project --python 3.12 --with anki==26.9.3 --with genanki==0.13.1 \\
        python scripts/simulate_anki_import.py

Tout se passe dans un dossier temporaire : copie du vault et des gabarits,
collection Anki jetable. Ni le dépôt ni une collection personnelle ne sont
modifiés. La simulation ne remplace pas l'essai sur AnkiDroid : elle ne dit
rien du rendu ni de la version installée sur le téléphone.
"""

import argparse
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
import time

if __package__:
    from .build_apkg import FIELD_SEPARATOR, MODEL, PACKAGE_NAME, ROOT, build_package
else:
    from build_apkg import FIELD_SEPARATOR, MODEL, PACKAGE_NAME, ROOT, build_package

MARKER = "[simulation]"


def check_reimport(result):
    """Refuse une réimportation incomplète, avec ou sans changement du style."""
    failures = []
    if result["doublons"]:
        failures.append("doublons après ré-importation")
    for key, message in (
        ("ids_de_notes_conserves", "notes recréées au lieu d'être mises à jour"),
        ("mise_a_jour_appliquee", "contenu modifié non mis à jour"),
        ("historique_conserve", "historique de révision modifié"),
        ("css_mis_a_jour", "style modifié non mis à jour"),
    ):
        if key in result and not result[key]:
            failures.append(message)
    return failures


def import_package(col, path):
    """Importe comme le dialogue par défaut : mises à jour « si plus récent »."""
    from anki.collection import ImportAnkiPackageOptions, ImportAnkiPackageRequest

    enum = ImportAnkiPackageOptions.DESCRIPTOR.fields_by_name["update_notes"].enum_type
    if_newer = enum.values_by_name["IMPORT_ANKI_PACKAGE_UPDATE_CONDITION_IF_NEWER"].number
    options = ImportAnkiPackageOptions(merge_notetypes=False, update_notes=if_newer,
                                       update_notetypes=if_newer, with_scheduling=False,
                                       with_deck_configs=False)
    col.import_anki_package(ImportAnkiPackageRequest(package_path=str(path), options=options))


def notes_by_id(col):
    """ID pédagogique → (id de note, champs)."""
    rows = col.db.all("SELECT id, flds FROM notes")
    return {flds.split(FIELD_SEPARATOR)[0]: (nid, flds) for nid, flds in rows}


def review(col, note_id):
    """Répond « Bien » à la carte de la note, comme une révision réelle."""
    from anki.scheduler.v3 import CardAnswer

    card = col.get_card(col.card_ids_of_note(note_id)[0])
    card.start_timer()
    states = col._backend.get_scheduling_states(card.id)
    col.sched.answer_card(col.sched.build_answer(card=card, states=states,
                                                 rating=CardAnswer.GOOD))


def scheduling(col, note_id):
    card = col.get_card(col.card_ids_of_note(note_id)[0])
    revlog = col.db.scalar("SELECT count() FROM revlog WHERE cid = ?", card.id)
    return {"carte": card.id, "type": card.type, "queue": card.queue, "due": card.due,
            "ivl": card.ivl, "reps": card.reps, "lapses": card.lapses, "revlog": revlog}


def mark_card(vault, card_id):
    """Modifie la rubrique Erreurs bloquantes d'une carte dans la copie du vault."""
    for path in vault.glob("*/*.md"):
        text = path.read_text(encoding="utf-8")
        pattern = rf"(^ID: {re.escape(card_id)}\n(?:.*\n)*?\*\*Erreurs bloquantes\*\* : )"
        changed, count = re.subn(pattern, rf"\1{MARKER} ", text, count=1, flags=re.M)
        if count:
            path.write_text(changed, encoding="utf-8")
            return
    raise ValueError(f"carte {card_id} introuvable")


def build(vault, anki_dir, out_dir):
    time.sleep(1.1)  # date de modification des notes à la seconde : garantir « plus récent »
    build_package(vault, out_dir, timestamp=time.time(), anki_dir=anki_dir)
    return out_dir / PACKAGE_NAME


def simulate(vault, anki_dir, reviewed=3):
    from anki.collection import Collection

    report, failures = {}, []
    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)
        work_vault = shutil.copytree(vault, temp / "vault")
        work_anki = shutil.copytree(anki_dir, temp / "anki")
        (temp / "col").mkdir()
        col = Collection(str(temp / "col" / "collection.anki2"))
        try:
            initial_package = build(work_vault, work_anki, temp / "a")
            import_package(col, initial_package)
            first = notes_by_id(col)
            total = len(first)
            report["import_initial"] = {"notes": total, "cartes": col.card_count()}
            if col.card_count() != total:
                failures.append("nombre de cartes différent du nombre de notes")

            import_package(col, initial_package)
            unchanged = notes_by_id(col)
            report["reimport_sans_modification"] = {
                "notes": len(unchanged),
                "cartes": col.card_count(),
                "notes_et_contenu_conserves": first == unchanged,
            }
            if first != unchanged or col.card_count() != total:
                failures.append("identités, contenu ou nombre modifiés sans correction")

            chosen = sorted(first)[:reviewed]
            for card_id in chosen:
                review(col, first[card_id][0])
            before = {card_id: scheduling(col, first[card_id][0]) for card_id in chosen}

            mark_card(work_vault, chosen[0])
            import_package(col, build(work_vault, work_anki, temp / "b"))
            second = notes_by_id(col)
            after = {card_id: scheduling(col, second[card_id][0]) for card_id in chosen}
            report["reimport_contenu"] = {
                "notes": len(second),
                "doublons": len(second) != total or col.card_count() != total,
                "ids_de_notes_conserves": all(second[k][0] == first[k][0] for k in first),
                "carte_modifiee": chosen[0],
                "mise_a_jour_appliquee": MARKER in second[chosen[0]][1],
                "historique_conserve": before == after,
                "avant": before, "apres": after,
            }
            failures.extend(check_reimport(report["reimport_contenu"]))

            css = work_anki / "style.css"
            css.write_text(css.read_text(encoding="utf-8") + "\n/* simulation */\n", encoding="utf-8")
            mark_card(work_vault, chosen[1])
            import_package(col, build(work_vault, work_anki, temp / "c"))
            third = notes_by_id(col)
            report["reimport_type_de_note_modifie"] = {
                "notes": len(third),
                "doublons": len(third) != total or col.card_count() != total,
                "ids_de_notes_conserves": all(third[k][0] == first[k][0] for k in first),
                "css_mis_a_jour": "/* simulation */" in col.models.by_name(MODEL)["css"],
                "carte_modifiee": chosen[1],
                "mise_a_jour_appliquee": MARKER in third[chosen[1]][1],
                "historique_conserve": all(scheduling(col, third[k][0]) == after[k] for k in chosen),
            }
            failures.extend(check_reimport(report["reimport_type_de_note_modifie"]))
        finally:
            col.close()
    return report, failures


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--vault", type=Path, default=ROOT / "vault")
    parser.add_argument("--anki", type=Path, default=ROOT / "anki")
    args = parser.parse_args()
    try:
        report, failures = simulate(args.vault, args.anki)
    except ModuleNotFoundError as error:
        print(f"{error}. Lancer : uv run --no-project --python 3.12 --with anki==26.9.3 "
              "--with genanki==0.13.1 python scripts/simulate_anki_import.py", file=sys.stderr)
        return 2
    for failure in failures:
        print(failure, file=sys.stderr)
    print(json.dumps({"resultat": "ECHEC" if failures else "OK", **report},
                     ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
