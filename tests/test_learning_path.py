import json
import unittest

from scripts.learning_path import ROOT, validate_order
from scripts.sync_catalog import collect


class LearningPath(unittest.TestCase):
    def setUp(self):
        self.entries = [{'id': 'A', 'prerequis': '[]'},
                        {'id': 'B', 'prerequis': '["A"]'}]

    def test_prerequisite_must_precede_dependent_topic(self):
        self.assertEqual(validate_order(self.entries, [{'sujets': ['A', 'B']}]), [])
        self.assertIn('B doit suivre A', validate_order(self.entries, [{'sujets': ['B', 'A']}]))

    def test_cycle_cannot_have_a_valid_order(self):
        self.entries[0]['prerequis'] = '["B"]'
        self.assertTrue(validate_order(self.entries, [{'sujets': ['A', 'B']}]))

    def test_missing_duplicate_or_unknown_topic_is_rejected(self):
        for topics, expected in [(['A'], 'absent'), (['A', 'A', 'B'], 'dupliqué'),
                                 (['A', 'B', 'C'], 'inconnu')]:
            with self.subTest(topics=topics):
                errors = validate_order(self.entries, [{'sujets': topics}])
                self.assertTrue(any(expected in error for error in errors))

    def test_unknown_prerequisite_is_rejected(self):
        self.entries[1]['prerequis'] = '["MISSING"]'
        self.assertIn('B : prérequis inconnu MISSING',
                      validate_order(self.entries, [{'sujets': ['A', 'B']}]))

    def test_repository_path_covers_all_existing_topics_in_dependency_order(self):
        steps = json.loads((ROOT / 'scripts/learning_path.json').read_text())['etapes']
        self.assertEqual(validate_order(collect(ROOT / 'vault'), steps), [])


if __name__ == '__main__':
    unittest.main()
