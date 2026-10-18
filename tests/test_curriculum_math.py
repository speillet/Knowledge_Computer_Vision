import unittest
from examples.curriculum_math import nearest_indices_1d, otsu_threshold, project


class CurriculumExamples(unittest.TestCase):
    def test_otsu_and_brightness_shift_keep_partition(self):
        values = [0, 0, 1, 1, 9, 9, 10, 10]
        self.assertEqual(otsu_threshold(values), 1)
        shifted = [x + 20 for x in values]
        self.assertEqual(otsu_threshold(shifted), 21)
        self.assertEqual([x > 1 for x in values], [x > 21 for x in shifted])

    def test_otsu_rejects_undefined_or_invalid_contract(self):
        for values in [[], [1, 1], [-1, 2], [0, 256], [0.2, 3]]:
            with self.subTest(values=values), self.assertRaises(ValueError):
                otsu_threshold(values)

    def test_resize_crop_intrinsics_match_pixel_transform(self):
        original = project((1, 2, 10), 500, 600, 320, 240)
        transformed = project((1, 2, 10), 250, 300, 140, 90)
        self.assertEqual(original, (370, 360))
        self.assertEqual(transformed, (165, 150))
        self.assertEqual(transformed, (original[0] * .5 - 20, original[1] * .5 - 30))

    def test_projection_requires_positive_depth(self):
        with self.assertRaises(ValueError):
            project((1, 2, 0), 500, 500, 0, 0)

    def test_association_depends_on_initialisation(self):
        self.assertEqual(nearest_indices_1d([0, 1, 3], [10, 11, 13], 0), [0, 0, 0])
        self.assertEqual(nearest_indices_1d([0, 1, 3], [10, 11, 13], 10), [0, 1, 2])


if __name__ == '__main__':
    unittest.main()
