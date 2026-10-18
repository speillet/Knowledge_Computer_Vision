"""Expériences arithmétiques du pilote ; Python 3.9+, bibliothèque standard.

Conventions : boîtes continues xyxy, NMS globale avec test strict IoU > seuil.
L'AP est un cas analytique à un seuil, sans crowd/ignore, pas l'évaluateur COCO.
La correction Kalman est scalaire, pas une réimplémentation de SORT.
"""

import json
import math


def _valid_box(box):
    if len(box) != 4 or not all(math.isfinite(x) for x in box):
        raise ValueError("Une boîte contient quatre coordonnées finies.")
    if box[2] <= box[0] or box[3] <= box[1]:
        raise ValueError("Une boîte doit avoir une aire strictement positive.")


def iou(a, b):
    """IoU de deux boîtes continues dans le même repère, sans +1."""
    _valid_box(a)
    _valid_box(b)
    width = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    height = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    intersection = width * height
    area_a = (a[2] - a[0]) * (a[3] - a[1])
    area_b = (b[2] - b[0]) * (b[3] - b[1])
    return intersection / (area_a + area_b - intersection)


def hard_nms(boxes, scores, threshold):
    """Indices conservés ; score décroissant, indice croissant en cas d'égalité."""
    if len(boxes) != len(scores):
        raise ValueError("Il faut un score par boîte.")
    if not math.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("Le seuil IoU doit appartenir à [0, 1].")
    if not all(math.isfinite(score) for score in scores):
        raise ValueError("Les scores doivent être finis.")
    for box in boxes:
        _valid_box(box)
    remaining = sorted(range(len(boxes)), key=lambda i: (-scores[i], i))
    kept = []
    while remaining:
        best = remaining.pop(0)
        kept.append(best)
        remaining = [i for i in remaining
                     if iou(boxes[best], boxes[i]) <= threshold]
    return kept


def ransac_trials(inlier_ratio, sample_size, confidence):
    """Budget nominal de tirages indépendants ; ne vérifie pas la géométrie."""
    if not 0 < inlier_ratio <= 1 or not 0 < confidence < 1:
        raise ValueError("Proportion dans ]0,1], confiance dans ]0,1[.")
    if type(sample_size) is not int or sample_size < 1:
        raise ValueError("La taille minimale est un entier positif.")
    success = inlier_ratio ** sample_size
    if success == 1:
        return 1
    if success == 0:
        raise ValueError("Probabilité trop petite pour cette précision numérique.")
    return math.ceil(math.log1p(-confidence) / math.log1p(-success))


def kalman_scalar(prediction, prior_variance, measurement, measurement_variance):
    """Correction linéaire scalaire : position, variance et gain."""
    values = (prediction, prior_variance, measurement, measurement_variance)
    if not all(math.isfinite(x) for x in values):
        raise ValueError("Les paramètres doivent être finis.")
    if prior_variance < 0 or measurement_variance <= 0:
        raise ValueError("Variance a priori >= 0 et variance de mesure > 0.")
    gain = prior_variance / (prior_variance + measurement_variance)
    position = prediction + gain * (measurement - prediction)
    variance = (1 - gain) * prior_variance
    return position, variance, gain


def ap101_from_labels(labels, ground_truth_count):
    """AP101 après appariement déjà fait, labels ordonnés TP=1/FP=0.

    Une catégorie, un seuil IoU, aucune annotation ignorée. L'appariement,
    maxDets et les moyennes multiseuils/catégories sont hors de cette fonction.
    """
    if type(ground_truth_count) is not int or ground_truth_count < 1:
        raise ValueError("Il faut au moins une GT valide dans ce cas analytique.")
    if any(label not in (0, 1) for label in labels):
        raise ValueError("Les labels doivent être 0 ou 1.")
    if sum(labels) > ground_truth_count:
        raise ValueError("Un TP ne peut pas compter plusieurs fois une GT.")
    points = []
    tp = 0
    for rank, label in enumerate(labels, 1):
        tp += label
        points.append((tp / ground_truth_count, tp / rank))
    sampled = [max((precision for recall, precision in points if recall >= k / 100),
                   default=0.0) for k in range(101)]
    return sum(sampled) / 101


def main():
    boxes = [(0, 0, 10, 10), (2, 0, 12, 10), (20, 0, 30, 10)]
    scores = [0.9, 0.8, 0.7]
    print(json.dumps({
        "iou_A_B": iou(boxes[0], boxes[1]),
        "nms_threshold_0.5": hard_nms(boxes, scores, 0.5),
        "nms_threshold_0.7": hard_nms(boxes, scores, 0.7),
        "ransac_w_0.5": ransac_trials(0.5, 4, 0.99),
        "ransac_w_0.8": ransac_trials(0.8, 4, 0.99),
        "kalman_R_9": kalman_scalar(100, 25, 110, 9),
        "kalman_R_100": kalman_scalar(100, 25, 110, 100),
        "ap101_TP_FP_TP": ap101_from_labels([1, 0, 1], 2),
        "ap101_TP_only": ap101_from_labels([1], 2),
        "ap101_TP_TP_FP": ap101_from_labels([1, 1, 0], 2),
    }, indent=2))


if __name__ == "__main__":
    main()
