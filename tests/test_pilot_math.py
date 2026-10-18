import math
import unittest

from examples.pilot_math import ap101_from_labels, hard_nms, iou, kalman_scalar, ransac_trials


class GeometryExamples(unittest.TestCase):
    def setUp(self):
        self.boxes = [(0, 0, 10, 10), (2, 0, 12, 10), (20, 0, 30, 10)]

    def test_continuous_iou_and_translation(self):
        self.assertAlmostEqual(iou(self.boxes[0], self.boxes[1]), 2 / 3)
        self.assertEqual(iou(self.boxes[0], self.boxes[2]), 0)
        self.assertEqual(iou(self.boxes[0], self.boxes[0]), 1)
        shifted = [tuple(x + 100 for x in box) for box in self.boxes]
        self.assertAlmostEqual(iou(shifted[0], shifted[1]), 2 / 3)

    def test_nms_controlled_threshold_variation(self):
        self.assertEqual(hard_nms(self.boxes, [0.9, 0.8, 0.7], 0.5), [0, 2])
        self.assertEqual(hard_nms(self.boxes, [0.9, 0.8, 0.7], 0.7), [0, 1, 2])

    def test_nms_strict_boundary_and_tie(self):
        same = [self.boxes[0], self.boxes[0]]
        self.assertEqual(hard_nms(same, [1, 1], 1), [0, 1])
        self.assertEqual(hard_nms(same, [1, 1], 0.5), [0])
        self.assertEqual(hard_nms([], [], 0.5), [])

    def test_reject_invalid_contracts(self):
        for box in [(1, 0, 0, 10), (0, 0, 0, 1), (0, 0, math.nan, 1)]:
            with self.subTest(box=box), self.assertRaises(ValueError):
                iou(box, self.boxes[0])
        with self.assertRaises(ValueError):
            hard_nms(self.boxes, [0.9], 0.5)
        with self.assertRaises(ValueError):
            hard_nms(self.boxes, [1, 1, 1], -0.1)


class EstimationExamples(unittest.TestCase):
    def test_ransac_budget_meets_nominal_probability(self):
        for ratio, expected in [(0.5, 72), (0.8, 9)]:
            budget = ransac_trials(ratio, 4, 0.99)
            self.assertEqual(budget, expected)
            self.assertGreaterEqual(1 - (1 - ratio ** 4) ** budget, 0.99)
            self.assertLess(1 - (1 - ratio ** 4) ** (budget - 1), 0.99)
        self.assertEqual(ransac_trials(1, 4, 0.99), 1)

    def test_ransac_invalid_probability(self):
        for args in [(0, 4, 0.99), (0.5, 0, 0.99), (0.5, 4, 1), (math.nan, 4, 0.99)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                ransac_trials(*args)

    def test_less_certain_measurement_has_less_influence(self):
        position, variance, gain = kalman_scalar(100, 25, 110, 9)
        self.assertAlmostEqual(position, 107.3529411764706)
        self.assertAlmostEqual(variance, 225 / 34)
        self.assertAlmostEqual(gain, 25 / 34)
        self.assertEqual(kalman_scalar(100, 25, 110, 100)[0], 102)
        with self.assertRaises(ValueError):
            kalman_scalar(100, -1, 110, 9)


class EvaluationExamples(unittest.TestCase):
    def test_duplicate_order_changes_interpolated_ap(self):
        self.assertAlmostEqual(ap101_from_labels([1, 0, 1], 2), (51 + 50 * 2 / 3) / 101)
        self.assertEqual(ap101_from_labels([1, 1, 0], 2), 1)

    def test_unreachable_recall_is_zero(self):
        self.assertAlmostEqual(ap101_from_labels([1], 2), 51 / 101)
        self.assertEqual(ap101_from_labels([], 2), 0)
        self.assertEqual(ap101_from_labels([0, 0], 2), 0)

    def test_ap_requires_valid_ground_truth_and_matching(self):
        for labels, count in [([1], 0), ([1, 1], 1), ([2], 2)]:
            with self.subTest(labels=labels, count=count), self.assertRaises(ValueError):
                ap101_from_labels(labels, count)


if __name__ == "__main__":
    unittest.main()
