"""Check the integration of English card headers with the review inventory."""

import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "card_inventory",
    ROOT / ".agents/skills/revue-cartes/scripts/inventaire_cartes.py",
)
inventory = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inventory)


class EnglishCardInventory(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.vault = Path(self.temp.name)
        (self.vault / "00-Accueil.md").write_text("# Fixture vault\n")
        topic = self.vault / "40-features-matching"
        (topic / "references").mkdir(parents=True)
        (topic / "references/41-test.md").write_text("# Fixture reference\n")
        self.path = topic / "41-test.md"

    def write_card(self, detail):
        self.path.write_text(
            "# Fixture flashcards\n\n"
            "TARGET DECK: CV::Pilote::40-features-matching\n\n"
            "## CV-TEST-001\n\n"
            "Objective: Explain a mechanism. Family: understanding. Provenance: agent.\n\n"
            "START\nCV-Pilote\nID: CV-TEST-001\n"
            "Question: Which mechanism applies?\n"
            "Reponse: **Expected answer**: A test mechanism.\n\n"
            f"**Further explanation**: {detail}\n\n"
            "**Blocking errors**: Confusing the coordinate frames.\n"
            "Source: [[40-features-matching/references/41-test|Reference]] ; "
            "[Source](https://example.org/primary).\n"
            "Tags: cv::pilote cv::d04 famille::comprehension "
            "cv_id::CV-TEST-001 provenance::agent pole::B\n"
            "<!--ID: 1234567890-->\nEND\n"
        )

    def test_english_headers_retain_export_checks_and_stable_identity(self):
        self.write_card("A fixture sentence for counting lexical words. " * 30)
        data = inventory.inventory(self.vault)
        card = data["fichiers"][0]["cartes"][0]
        self.assertEqual(data["anomalies"], [])
        self.assertTrue(data["controles_export"])
        self.assertEqual(card["famille_entete"], "comprehension")
        self.assertEqual(card["guid"], inventory.expected_guid("CV-TEST-001"))
        self.assertEqual(card["commentaire_plugin"], "1234567890")
        self.assertEqual(card["poles"], ["B"])
        self.assertFalse(card["sous_plancher"])
        self.assertIsNone(card["conversion"])
        self.assertIn("understanding", inventory.render(data))

    def test_short_english_answer_is_flagged(self):
        self.write_card("A short fixture.")
        data = inventory.inventory(self.vault)
        self.assertTrue(data["fichiers"][0]["cartes"][0]["sous_plancher"])
        self.assertTrue(any("below the threshold" in issue for issue in data["anomalies"]))

    def test_unsupported_export_syntax_is_flagged(self):
        self.write_card("A fixture sentence for counting lexical words. " * 30 + "\n# Invalid heading")
        data = inventory.inventory(self.vault)
        self.assertIsNotNone(data["fichiers"][0]["cartes"][0]["conversion"])
        self.assertTrue(any("package conversion rejected" in issue for issue in data["anomalies"]))

    def test_legacy_inventory_comment_comparison_remains_compatible(self):
        self.write_card("A fixture sentence for counting lexical words. " * 30)
        after = inventory.inventory(self.vault)
        before = {"fichiers": [{"cartes": [
            {"id": "CV-TEST-001", "identite_anki": "1234567890"},
        ]}]}
        self.assertEqual(inventory.compare(before, after), [])
        before["fichiers"][0]["cartes"][0]["identite_anki"] = "9876543210"
        self.assertEqual(len(inventory.compare(before, after)), 1)
        self.assertIn("Plugin identity comment changed", inventory.compare(before, after)[0])


if __name__ == "__main__":
    unittest.main()
