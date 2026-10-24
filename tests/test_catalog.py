from pathlib import Path
import tempfile
import unittest
from scripts.sync_catalog import collect, partition_targets


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


    def test_promoted_targets_are_kept_separate_from_open_work(self):
        pending = {'id': 'APP-001', 'connexe': 'CV-EXISTING'}
        completed = {'id': 'APP-002', 'fiche': 'CV-EXISTING'}
        opened, drafted = partition_targets([pending, completed], {'CV-EXISTING'})
        self.assertEqual(opened, [pending])
        self.assertEqual(drafted, [completed])

    def test_unknown_reference_cannot_close_a_coverage_target(self):
        with self.assertRaisesRegex(ValueError, 'Fiche de couverture absente'):
            partition_targets([{'id': 'APP-001', 'fiche': 'CV-MISSING'}], set())

    def test_duplicate_coverage_id_cannot_silently_disappear(self):
        with self.assertRaisesRegex(ValueError, 'dupliquée'):
            partition_targets([{'id': 'APP-001'}, {'id': 'APP-001'}], set())


if __name__ == '__main__':
    unittest.main()
