import json
import unittest
from unittest.mock import patch

from scripts.learning_path import ROOT, render_path, validate_order
from scripts.sync_catalog import collect


class LearningPath(unittest.TestCase):
    def setUp(self):
        self.entries = [{'id': 'A', 'prerequis': '[]'},
                        {'id': 'B', 'prerequis': '["A"]'}]

    def test_prerequisite_must_precede_dependent_topic(self):
        self.assertEqual(validate_order(self.entries, [{'sujets': ['A', 'B']}]), [])
        self.assertIn('B must follow A', validate_order(self.entries, [{'sujets': ['B', 'A']}]))

    def test_cycle_cannot_have_a_valid_order(self):
        self.entries[0]['prerequis'] = '["B"]'
        self.assertTrue(validate_order(self.entries, [{'sujets': ['A', 'B']}]))

    def test_missing_duplicate_or_unknown_topic_is_rejected(self):
        for topics, expected in [(['A'], 'missing'), (['A', 'A', 'B'], 'Duplicate'),
                                 (['A', 'B', 'C'], 'Unknown')]:
            with self.subTest(topics=topics):
                errors = validate_order(self.entries, [{'sujets': topics}])
                self.assertTrue(any(expected in error for error in errors))

    def test_unknown_prerequisite_is_rejected(self):
        self.entries[1]['prerequis'] = '["MISSING"]'
        self.assertIn('B: unknown prerequisite MISSING',
                      validate_order(self.entries, [{'sujets': ['A', 'B']}]))

    def test_repository_path_covers_all_existing_topics_in_dependency_order(self):
        steps = json.loads((ROOT / 'scripts/learning_path.json').read_text())['etapes']
        self.assertEqual(validate_order(collect(ROOT / 'vault'), steps), [])

    def test_rendered_counts_follow_content_backlog_and_threshold(self):
        entries = [{**entry, 'title': entry['id'], 'ref': entry['id'] + '.md',
                    'cards_path': entry['id'] + '-cards.md', 'card_ids': []}
                   for entry in self.entries]
        steps = [{'sujets': ['A', 'B'], 'titre': 'Example',
                  'objectif': 'Understand', 'preuve': 'Explain'}]
        first = render_path(entries, steps, 17)
        self.assertIn('2 existing subjects', first)
        self.assertIn('The 17', first)
        with patch('scripts.learning_path.MIN_ANSWER_WORDS', 210):
            second = render_path(entries, steps, 16)
        self.assertIn('The 16', second)
        self.assertNotIn('The 17', second)
        self.assertIn('210 lexical words', second)


if __name__ == '__main__':
    unittest.main()
