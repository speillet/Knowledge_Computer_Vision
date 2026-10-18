"""Petits cas contrôlés, Python 3.9+ sans dépendance ; pas des pipelines CV complets."""
import json
import math


def otsu_threshold(values):
    """Seuil Otsu d'intensités entières 0..255 ; premier maximum en cas d'égalité."""
    if not values or any(type(x) is not int or not 0 <= x <= 255 for x in values):
        raise ValueError("Il faut des intensités entières non vides entre 0 et 255.")
    histogram = [0] * 256
    for value in values:
        histogram[value] += 1
    n = len(values)
    total = sum(values)
    left_n = left_sum = 0
    best_score, threshold = -1.0, None
    for t in range(255):
        left_n += histogram[t]
        left_sum += t * histogram[t]
        right_n = n - left_n
        if not left_n or not right_n:
            continue
        mean_difference = left_sum / left_n - (total - left_sum) / right_n
        score = left_n * right_n * mean_difference ** 2
        if score > best_score:
            best_score, threshold = score, t
    if threshold is None:
        raise ValueError("Le cas constant ne définit pas deux classes non vides.")
    return threshold


def project(point, fx, fy, cx, cy):
    """Pinhole idéal en repère caméra, sans distorsion ; point devant la caméra."""
    x, y, z = point
    if not all(math.isfinite(v) for v in (x, y, z, fx, fy, cx, cy)) or z <= 0:
        raise ValueError("Coordonnées finies et profondeur positive attendues.")
    return fx * x / z + cx, fy * y / z + cy


def nearest_indices_1d(source, target, translation=0):
    """Association pédagogique 1D ; ne constitue pas un ICP complet."""
    if not source or not target:
        raise ValueError("Deux ensembles non vides sont nécessaires.")
    if not all(math.isfinite(x) for x in [*source, *target, translation]):
        raise ValueError("Les coordonnées doivent être finies.")
    return [min(range(len(target)), key=lambda j: abs(p + translation - target[j]))
            for p in source]


def main():
    values = [0, 0, 1, 1, 9, 9, 10, 10]
    shifted = [x + 20 for x in values]
    threshold = otsu_threshold(values)
    shifted_threshold = otsu_threshold(shifted)
    point = (1, 2, 10)
    original = project(point, 500, 600, 320, 240)
    # Resize x0.5 puis crop (20,30), exprimé dans le nouveau repère pixel.
    transformed = project(point, 250, 300, 140, 90)
    print(json.dumps({
        'otsu_threshold': threshold,
        'otsu_brightness_shift_threshold': shifted_threshold,
        'mask_preserved_under_shift': [x > threshold for x in values]
        == [x > shifted_threshold for x in shifted],
        'projection_original': original,
        'projection_resized_cropped': transformed,
        'nearest_bad_initialisation': nearest_indices_1d([0, 1, 3], [10, 11, 13], 0),
        'nearest_good_initialisation': nearest_indices_1d([0, 1, 3], [10, 11, 13], 10),
        'stereo_depth_m_d20': 1000 * 0.2 / 20,
        'stereo_depth_m_d10': 1000 * 0.2 / 10,
        'eight_streams_frames_s': 8 * 30,
        'amdahl_gain': 1 / (0.9 + 0.1 / 2),
    }, indent=2))


if __name__ == '__main__':
    main()
