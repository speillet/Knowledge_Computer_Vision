from importlib.util import find_spec
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
import zipfile

from scripts.build_apkg import (ConversionError, MANIFEST_NAME, PACKAGE_NAME, compare_manifests,
                                deck_id, expected_guid, md_to_html, parse_cards, verify_package)
from scripts.simulate_anki_import import check_reimport


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

Objectif : tester le paquet. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-TEST-001
Question: Que vaut $x_i<1$ & pourquoi ?
Reponse: **Noyau attendu** : réponse avec `code_$`.

**Approfondissement** :
- premier point ;
- second point.

**Erreurs bloquantes** : contresens.
Source: [[40-features-matching/references/41-test|Fiche test]] ; [source](https://example.org/primary).
Tags: cv::pilote cv::d04 famille::comprehension cv_id::CV-TEST-001 provenance::agent pole::B
END
"""
URL = "https://example.org/vault/"


class ImportSimulation(unittest.TestCase):
    def test_initial_package_guids_remain_compatible(self):
        self.assertEqual(expected_guid("CV-ACQUISITION-001"), "IZ]LO~1#G9")
        self.assertEqual(expected_guid("CV-ACQUISITION-002"), "n0uAINY9H|")
        self.assertEqual(expected_guid("CV-ACQUISITION-003"), "Rd~h)QoIr~")

    def test_style_import_fails_when_update_or_history_is_lost(self):
        successful = {"doublons": False, "ids_de_notes_conserves": True,
                      "mise_a_jour_appliquee": True, "historique_conserve": True,
                      "css_mis_a_jour": True}
        self.assertEqual(check_reimport(successful), [])
        for key in successful:
            with self.subTest(key=key):
                broken = {**successful, key: not successful[key]}
                self.assertEqual(len(check_reimport(broken)), 1)


class Conversion(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.vault = Path(self.temp.name)
        self.card = self.vault / "40-features-matching/41-test.md"
        self.card.parent.mkdir(parents=True)

    def convert(self, text, media=None):
        return md_to_html(text, card_path=self.card, vault=self.vault, fiche_url=URL, media=media)

    def test_math_uses_anki_delimiters_and_escapes_html(self):
        html = self.convert(r"Si $a_i<b|c$ & $$\|x\|_2$$ alors.")
        self.assertIn(r"\(a_i&lt;b|c\)", html)
        self.assertIn(r"\[\|x\|_2\]", html)
        self.assertIn("&amp;", html)
        self.assertNotIn("$", html)

    def test_code_keeps_dollars_and_markup_literal(self):
        html = self.convert("Voir `a**b**$`.\n\n```python\nx = '<b>' + \"$\"\n```")
        self.assertIn("<code>a**b**$</code>", html)
        self.assertIn("<pre><code>x = '&lt;b&gt;' + \"$\"</code></pre>", html)
        self.assertNotIn("<p><pre>", html)

    def test_paragraph_followed_by_list(self):
        html = self.convert("**Titre** :\n- un ;\n- deux.\n\nSuite *nuancée*.")
        self.assertEqual(html, "<p><b>Titre</b> :</p><ul><li>un ;</li><li>deux.</li></ul>"
                               "<p>Suite <i>nuancée</i>.</p>")

    def test_links_wikilinks_and_images(self):
        (self.vault / "99-Ressources").mkdir()
        svg = self.vault / "99-Ressources/schema.svg"
        svg.write_text("<svg/>", encoding="utf-8")
        media = set()
        html = self.convert("![Schéma](../99-Ressources/schema.svg) [[40-features-matching/references/41-test|Fiche]] "
                            "[article](https://example.org/a?b=1&c=2)", media)
        self.assertIn('<img src="schema.svg" alt="Schéma">', html)
        self.assertIn(f'<a href="{URL}40-features-matching/references/41-test.md">Fiche</a>', html)
        self.assertIn('<a href="https://example.org/a?b=1&amp;c=2">article</a>', html)
        self.assertEqual(media, {svg.resolve()})

    def test_wikilink_without_url_keeps_label(self):
        html = md_to_html("[[40-features-matching/references/41-test|Fiche]]", card_path=self.card,
                          vault=self.vault, fiche_url="")
        self.assertEqual(html, "<p>Fiche</p>")

    def test_unsupported_syntax_is_refused(self):
        for text in ["| a | b |", "# Titre", "> citation", "prix $5", "![x](absente.svg)"]:
            with self.subTest(text=text), self.assertRaises(ConversionError):
                self.convert(text)


class Helpers(unittest.TestCase):
    def test_deck_id_is_stable_and_distinct(self):
        self.assertEqual(deck_id("CV::Pilote::40-features-matching"),
                         deck_id("CV::Pilote::40-features-matching"))
        self.assertNotEqual(deck_id("CV::Pilote::40-features-matching"),
                            deck_id("CV::Pilote::50-calibration-geometrie"))
        self.assertLess(deck_id("CV::Pilote::40-features-matching"), 2 ** 53)

    def test_compare_manifests(self):
        old = {"cartes": {"A": {"empreinte": "1"}, "B": {"empreinte": "2"}, "C": {"empreinte": "3"}}}
        new = {"cartes": {"A": {"empreinte": "1"}, "B": {"empreinte": "9"}, "D": {"empreinte": "4"}}}
        self.assertEqual(compare_manifests(old, new),
                         {"ajoutees": ["D"], "modifiees": ["B"], "retirees": ["C"]})


class VaultFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.vault = Path(self.temp.name) / "vault"
        (self.vault / "40-features-matching/references").mkdir(parents=True)
        (self.vault / "40-features-matching/references/41-test.md").write_text(NOTE, encoding="utf-8")
        self.card = self.vault / "40-features-matching/41-test.md"
        self.card.write_text(CARD, encoding="utf-8")

    def test_parse_cards(self):
        cards = parse_cards(self.vault)
        self.assertEqual([card["id"] for card in cards], ["CV-TEST-001"])
        self.assertEqual(cards[0]["deck"], "CV::Pilote::40-features-matching")
        self.assertIn("pole::B", cards[0]["tags"])
        self.assertTrue(cards[0]["fields"]["Reponse"].endswith("**Erreurs bloquantes** : contresens."))

    @unittest.skipUnless(find_spec("genanki"), "genanki absent : uv run --no-project --with genanki==0.13.1")
    def test_rebuild_keeps_guid_and_updates_content(self):
        from scripts.build_apkg import build_package

        out = Path(self.temp.name) / "dist"
        first = build_package(self.vault, out, URL, timestamp=1_700_000_000)
        self.card.write_text(CARD.replace("contresens.", "contresens corrigé."), encoding="utf-8")
        second = build_package(self.vault, out, URL, timestamp=1_700_000_100)
        self.assertEqual(first["cartes"]["CV-TEST-001"]["guid"], second["cartes"]["CV-TEST-001"]["guid"])
        self.assertEqual(compare_manifests(first, second)["modifiees"], ["CV-TEST-001"])
        expected = {"CV-TEST-001": "CV::Pilote::40-features-matching"}
        errors, summary = verify_package(out / PACKAGE_NAME, expected)
        self.assertEqual(errors, [])
        self.assertEqual(summary["decks"], ["CV::Pilote::40-features-matching"])
        with zipfile.ZipFile(out / PACKAGE_NAME) as archive, tempfile.TemporaryDirectory() as temp:
            archive.extract("collection.anki2", temp)
            connection = sqlite3.connect(Path(temp) / "collection.anki2")
            fields, mod = connection.execute("SELECT flds, mod FROM notes").fetchone()
            connection.close()
        self.assertIn("contresens corrigé.", fields)
        self.assertEqual(mod, 1_700_000_100)
        manifest = json.loads((out / MANIFEST_NAME).read_text(encoding="utf-8"))
        self.assertEqual(manifest["comptes"], {"notes": 1, "decks": 1, "medias": 0})

    @unittest.skipUnless(find_spec("genanki"), "genanki absent : uv run --no-project --with genanki==0.13.1")
    def test_verifier_rejects_broken_card_links_and_note_identity(self):
        from scripts.build_apkg import build_package

        out = Path(self.temp.name) / "dist"
        build_package(self.vault, out, URL)
        expected = {"CV-TEST-001": "CV::Pilote::40-features-matching"}
        with zipfile.ZipFile(out / PACKAGE_NAME) as archive:
            original = {name: archive.read(name) for name in archive.namelist()}
        for mutation in (
            "DELETE FROM cards", "UPDATE cards SET nid=-1", "UPDATE cards SET ord=1",
            "UPDATE cards SET did=1", "UPDATE notes SET mid=0",
            "UPDATE notes SET guid='brokenGuid'",
        ):
            with self.subTest(mutation=mutation):
                database = out / "broken.anki2"
                database.write_bytes(original["collection.anki2"])
                with sqlite3.connect(database) as connection:
                    connection.execute(mutation)
                connection.close()
                package = out / "broken.apkg"
                with zipfile.ZipFile(package, "w") as archive:
                    for name, data in original.items():
                        archive.writestr(name, database.read_bytes() if name == "collection.anki2" else data)
                errors, _ = verify_package(package, expected)
                self.assertTrue(errors, mutation)


if __name__ == "__main__":
    unittest.main()
