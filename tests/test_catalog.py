from pathlib import Path
import tempfile
import unittest
from scripts.sync_catalog import collect


class CatalogCases(unittest.TestCase):
    def test_case_is_linked_to_its_own_card_not_previous_card(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / '40-features-matching'
            (folder / 'references').mkdir(parents=True)
            (folder / 'references/41-test.md').write_text(
                '---\nid: CV-TEST\ndomaine: d04\npoles: [B]\n---\n# Test\n', encoding='utf-8')
            (folder / '41-test.md').write_text(
                'START\nCV-Pilote\nID: CV-TEST-001\nTags: pole::B\nEND\n\n'
                'START\nCV-Pilote\nID: CV-TEST-002\nTags: pole::B cas_pole::B::diagnostic\nEND\n', encoding='utf-8')
            entries = collect(root)
            self.assertEqual(entries[0]['cases'], [('B', 'diagnostic', 'CV-TEST-002')])
            self.assertEqual(entries[0]['card_ids'], ['CV-TEST-001', 'CV-TEST-002'])


if __name__ == '__main__':
    unittest.main()
