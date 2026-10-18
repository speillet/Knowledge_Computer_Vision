from pathlib import Path
import tempfile
import unittest

from scripts.check_vault import check_vault


NOTE = """---
id: CV-TEST
type: methode
domaine: d04
poles: [B]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 1
tags: [cv/d04]
---
# Fiche témoin
Source : https://example.org/primary
"""
CARD = """# Cartes témoin

TARGET DECK: CV::Pilote::40-features-matching

## CV-TEST-001

Objectif : tester le contrat. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-TEST-001
Question: Question autonome ?
Reponse: **Noyau attendu** : réponse.

**Approfondissement** : détail.

**Erreurs bloquantes** : contresens.
Source: [[40-features-matching/references/41-test|Fiche]] ; [source](https://example.org/primary).
Tags: cv::pilote cv::d04 famille::comprehension cv_id::CV-TEST-001 provenance::agent pole::B
END
"""


class VaultContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "40-features-matching/references").mkdir(parents=True)
        self.note = self.root / "40-features-matching/references/41-test.md"
        self.card = self.root / "40-features-matching/41-test.md"
        self.note.write_text(NOTE, encoding="utf-8")
        self.card.write_text(CARD, encoding="utf-8")

    def assert_error(self, fragment):
        errors, _ = check_vault(self.root)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_valid_minimal_contract(self):
        errors, counts = check_vault(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(counts, {"markdown": 2, "fiches": 1, "cartes": 1})

    def test_duplicate_pedagogical_identity(self):
        (self.card.parent / "Copy.md").write_text(CARD, encoding="utf-8")
        self.assert_error("identifiant de carte dupliqué")

    def test_orphan_card_and_broken_media(self):
        self.card.write_text(CARD.replace("40-features-matching/references/41-test", "40-features-matching/references/41-missing")
                             + "\n![schéma](missing.svg)\n", encoding="utf-8")
        self.assert_error("fiche parente absente")
        self.assert_error("lien local absent")

    def test_missing_end_marker(self):
        self.card.write_text(CARD.replace("\nEND", ""), encoding="utf-8")
        self.assert_error("START/END non équilibrés")

    def test_model_fields_and_rubric(self):
        self.card.write_text(CARD.replace("Reponse:", "Back:"), encoding="utf-8")
        self.assert_error("champs absents")
        self.card.write_text(CARD.replace("**Erreurs bloquantes**", "**Détails**"), encoding="utf-8")
        self.assert_error("rubrique absente")

    def test_domain_disagrees_with_parent(self):
        self.card.write_text(CARD.replace("cv::d04", "cv::d11"), encoding="utf-8")
        self.assert_error("domaine différent")

    def test_poles_must_be_known_unique_and_present(self):
        for value in ["[]", "[G]", "[B, B]", "B", "[AB]"]:
            with self.subTest(value=value):
                self.note.write_text(NOTE.replace("[B]", value), encoding="utf-8")
                self.assert_error("pôles de fiche attendus")

    def test_card_poles_must_match_parent(self):
        for replacement in ["", "pole::A", "pole::B pole::B", "pole::B pole::G"]:
            with self.subTest(replacement=replacement):
                self.card.write_text(CARD.replace(" pole::B", " " + replacement).replace(" \n", "\n"), encoding="utf-8")
                self.assert_error("étiquettes de pôle différentes")

    def test_case_pole_requires_matching_family_and_pole(self):
        self.card.write_text(CARD.replace("pole::B\n", "pole::B cas_pole::A::diagnostic\n"), encoding="utf-8")
        self.assert_error("cas métier invalide")

    def test_deck_must_match_topic_folder(self):
        self.card.write_text(CARD.replace("CV::Pilote::40-features-matching",
                                         "CV::Pilote::50-calibration-geometrie"), encoding="utf-8")
        self.assert_error("deck cible CV::Pilote::40-features-matching")

    def test_card_and_reference_must_share_topic(self):
        folder = self.root / "50-calibration-geometrie"
        folder.mkdir()
        self.card.unlink()
        (folder / "51-test.md").write_text(
            CARD.replace("TARGET DECK: CV::Pilote::40-features-matching",
                         "TARGET DECK: CV::Pilote::50-calibration-geometrie"), encoding="utf-8")
        self.assert_error("autre thématique que sa fiche")

    def test_reference_domain_must_match_topic(self):
        self.note.write_text(NOTE.replace("domaine: d04", "domaine: d05"), encoding="utf-8")
        self.assert_error("domaine de fiche différent")

    def test_root_scan_rejects_start_examples_in_guides(self):
        (self.root / "Guide.md").write_text("```text\nSTART\nCV-Pilote\nEND\n```\n", encoding="utf-8")
        self.assert_error("bloc START hors")

    def test_sync_identity_is_preserved_but_must_be_unique(self):
        synced = CARD.replace("\nEND", "\n<!--ID: 1234567890-->\nEND")
        self.card.write_text(synced, encoding="utf-8")
        self.assertEqual(check_vault(self.root)[0], [])
        (self.card.parent / "Copy.md").write_text(
            synced.replace("CV-TEST-001", "CV-TEST-002"), encoding="utf-8")
        self.assert_error("identité Anki dupliquée")

    def test_no_vault_escape(self):
        self.card.write_text(CARD + "\n[externe local](../../../private.md)\n", encoding="utf-8")
        self.assert_error("hors vault")

    def test_multiple_sync_comments_in_one_card_are_invalid(self):
        self.card.write_text(CARD.replace("\nEND", "\n<!--ID: 123-->\n<!--ID: 456-->\nEND"), encoding="utf-8")
        self.assert_error("une seule identité Anki")

    def test_unique_media_basename(self):
        for folder in ["a", "b"]:
            target = self.root / "99-Ressources" / folder
            target.mkdir(parents=True)
            (target / "schema.svg").write_text("<svg/>", encoding="utf-8")
        self.assert_error("basename de média dupliqué")

    def test_media_collision_outside_attachment_folder(self):
        for folder in ["99-Ressources", "40-features-matching"]:
            target = self.root / folder
            target.mkdir(exist_ok=True)
            (target / "schema.svg").write_text("<svg/>", encoding="utf-8")
        self.assert_error("basename de média dupliqué")


if __name__ == "__main__":
    unittest.main()
