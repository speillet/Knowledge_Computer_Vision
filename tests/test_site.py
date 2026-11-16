import base64
import json
from pathlib import Path
import re
import tempfile
import unittest

from scripts.check_site import check, served_file
from scripts.prepare_site import content_path, convert_links, stage


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
# Fixture reference

Source: https://example.org/primary
"""
CARD = r"""# Flashcards — Fixture

TARGET DECK: CV::Pilote::40-features-matching

## CV-TEST-001

Objective: Explain uncertainty. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-TEST-001
Question: Why is $\sigma_i^2$ positive for a "noisy" measurement?
Reponse: **Expected answer**: it is a variance.

**Further explanation**: values are in squared units, with $x_i<1$.

**Blocking errors**: confusing variance and standard deviation.
Source: [[40-features-matching/references/41-test|Reference note]]; [primary](https://example.org/primary).
Tags: cv::pilote cv::d04 famille::comprehension cv_id::CV-TEST-001 provenance::agent pole::B
END
"""


class ReadingPages(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.vault = self.root / "vault"
        self.website = self.root / "website"
        self.source = Path("40-features-matching/41-test.md")
        reference = self.vault / "40-features-matching/references/41-test.md"
        reference.parent.mkdir(parents=True)
        reference.write_text(NOTE, encoding="utf-8")
        (self.vault / self.source).write_text(CARD, encoding="utf-8")
        (self.vault / "00-Accueil.md").write_text("# Home\n", encoding="utf-8")

    def test_reading_view_keeps_content_identity_math_and_sources(self):
        originals = {p: p.read_bytes() for p in self.vault.rglob("*") if p.is_file()}
        _, count = stage(self.vault, self.website)
        text = (self.website / "content" / self.source).read_text(encoding="utf-8")
        self.assertEqual(count, 1)
        self.assertIn('id="CV-TEST-001"', text)
        self.assertIn('objective="Explain uncertainty."', text)
        question = base64.b64decode(re.search(r'question="([^"]+)"', text)[1]).decode("utf-8")
        self.assertEqual(question, r'Why is $\sigma_i^2$ positive for a "noisy" measurement?')
        self.assertIn(r"$x_i<1$", text)
        self.assertIn('relref "/40-features-matching/references/41-test.md"', text)
        self.assertIn("**Sources:**", text)
        self.assertIn('"search":', text)
        self.assertNotIn("\nSTART\n", text)
        self.assertNotIn("TARGET DECK:", text)
        self.assertEqual(originals, {p: p.read_bytes() for p in self.vault.rglob("*") if p.is_file()})

    def test_rebuild_replaces_stale_pages_and_preserves_website_configuration(self):
        stage(self.vault, self.website)
        stale = self.website / "content/stale.md"
        stale.write_text("old", encoding="utf-8")
        config = self.website / "config.toml"
        config.write_text("preserve", encoding="utf-8")
        stage(self.vault, self.website)
        self.assertFalse(stale.exists())
        self.assertEqual(config.read_text(encoding="utf-8"), "preserve")

    def test_invalid_vault_does_not_erase_previous_reading_pages(self):
        stage(self.vault, self.website)
        previous = (self.website / "content" / self.source).read_bytes()
        (self.vault / self.source).write_text(CARD.replace("\nEND", ""), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Invalid vault"):
            stage(self.vault, self.website)
        self.assertEqual((self.website / "content" / self.source).read_bytes(), previous)

    def test_links_images_code_and_diagrams(self):
        media = self.vault / "99-Ressources/image.svg"
        media.parent.mkdir()
        media.write_text("<svg/>", encoding="utf-8")
        pages = {self.source, Path("40-features-matching/references/41-test.md")}
        original = ('[Reference](references/41-test.md#example)\n'
                    '![Image](../99-Ressources/image.svg)\n'
                    '`[literal](missing.md)`\n'
                    '```python\nprint("[literal](missing.md)")\n```\n'
                    '```mermaid\ngraph LR\nA-->B\n```')
        converted = convert_links(original, self.source, self.vault, pages)
        self.assertIn('relref "/40-features-matching/references/41-test.md#example"', converted)
        self.assertIn('vault-asset "99-Ressources/image.svg"', converted)
        self.assertIn('print("[literal](missing.md)")', converted)
        self.assertIn('`[literal](missing.md)`', converted)
        self.assertIn("{{< mermaid >}}\ngraph LR\nA-->B\n{{< /mermaid >}}", converted)
        stage(self.vault, self.website)
        self.assertEqual((self.website / "static/vault/99-Ressources/image.svg").read_bytes(), media.read_bytes())

    def test_missing_link_and_vault_escape_are_rejected(self):
        for url in ["missing.md", "../../../outside.md"]:
            with self.subTest(url=url), self.assertRaisesRegex(ValueError, "missing local link"):
                convert_links(f"[bad]({url})", self.source, self.vault, {self.source})

    def test_home_and_domain_indexes_keep_their_role(self):
        self.assertEqual(content_path(Path("00-Accueil.md")), Path("_index.md"))
        self.assertEqual(content_path(Path("40-features-matching/00-index.md")), Path("40-features-matching/_index.md"))


class PublishedLinks(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.site = Path(temp.name)
        (self.site / "index.html").write_text('<a href="/project/topic/#cv-test-001">Card</a>', encoding="utf-8")
        (self.site / "topic").mkdir()
        self.topic = self.site / "topic/index.html"
        self.topic.write_text('<details id="cv-test-001"><summary>Question</summary>Answer</details>', encoding="utf-8")
        (self.site / "index.json").write_text(json.dumps([{"permalink": "/project/topic/"}]), encoding="utf-8")

    def test_project_subpath_links_and_search_targets(self):
        self.assertEqual(check(self.site, "/project/")[0], [])
        self.topic.write_text("<p>No card</p>", encoding="utf-8")
        self.assertTrue(any("missing anchor" in e for e in check(self.site, "/project/")[0]))
        (self.site / "index.json").write_text('[{"permalink":"/project/absent/"}]', encoding="utf-8")
        self.assertTrue(any("index.json: missing page" in e for e in check(self.site, "/project/")[0]))

    def test_missing_build_and_search_index_fail(self):
        (self.site / "index.json").unlink()
        self.assertTrue(any("Missing search index" in e for e in check(self.site, "/project/")[0]))
        (self.site / "index.html").unlink()
        self.assertTrue(check(self.site, "/project/")[0])

    def test_encoded_parent_traversal_cannot_leave_the_site(self):
        self.assertIsNone(served_file(self.site, "/project/", "/project/%2e%2e/outside.html"))


if __name__ == "__main__":
    unittest.main()
