"""Recalculate constructed examples; this is not a CV or device benchmark."""

import json
import math


def main():
    checks = []

    def check(card, quantity, expression, actual, expected, tolerance=1e-9):
        if not math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance):
            raise AssertionError((card, quantity, actual, expected))
        checks.append({"card": card, "quantity": quantity,
                       "expression": expression, "actual": actual,
                       "expected": expected, "tolerance": tolerance})

    check("CV-SVD-001", "weak-direction parameter change", "1e-6 / 1e-6", 1e-6 / 1e-6, 1)
    check("CV-SVD-003", "common correlated residual cost, rho=0.5, a=1",
          "2 / (1 + 0.5)", 2 / 1.5, 4 / 3)
    check("CV-SVD-003", "opposite correlated residual cost, rho=0.5, a=1",
          "2 / (1 - 0.5)", 2 / 0.5, 4)
    check("CV-ACQUISITION-001", "exposure budget, ms", "1000 / 800", 1000 / 800, 1.25)
    check("CV-ACQUISITION-002", "SNR at 25 electrons", "25 / sqrt(25+25)",
          25 / math.sqrt(50), 3.5355339059327373)
    check("CV-ACQUISITION-002", "SNR at 50 electrons", "50 / sqrt(50+25)",
          50 / math.sqrt(75), 5.773502691896257)
    check("CV-ACQUISITION-002", "SNR improvement factor", "(50/sqrt(75))/(25/sqrt(50))",
          (50 / math.sqrt(75)) / (25 / math.sqrt(50)), 1.632993161855452)
    check("CV-CAPTEURS-001", "rolling-shutter skew, px", "1000 * 0.020", 1000 * 0.020, 20)
    check("CV-CAPTEURS-002", "drift after ten minutes, ms", "20e-6 * 600 * 1000",
          20e-6 * 600 * 1000, 12)
    check("CV-CAPTEURS-002", "drift displacement at 2 m/s, mm", "2 * 0.012 * 1000",
          2 * 0.012 * 1000, 24)
    check("CV-IMAGERIES-001", "anisotropic step length, mm", "sqrt(0.5**2 + 3**2)",
          math.hypot(0.5, 3), 3.0413812651491097)
    check("CV-IMAGERIES-002", "new longitudinal sampling, mm/line", "750 / 5000",
          750 / 5000, 0.15)
    check("CV-IMAGERIES-002", "part length with stale scale, mm", "(30/0.15)*0.1",
          (30 / 0.15) * 0.1, 20)
    check("CV-FILTRES-001", "mean of an impulse neighborhood", "(8*10 + 250)/9",
          (8 * 10 + 250) / 9, 36.666666666666664)
    check("CV-ORB-001", "sample shift from orientation error, px", "15 * radians(5)",
          15 * math.radians(5), 1.3089969389957472)
    check("CV-ORB-002", "Hamming distance, 0 versus 128", "popcount(128)",
          bin(128).count("1"), 1)
    check("CV-ORB-002", "Hamming distance, 0 versus 3", "popcount(3)",
          bin(3).count("1"), 2)
    for w, expected in [(0.5, 72), (0.25, 1177), (0.3, 567)]:
        check("CV-FAST-BRIEF-005 / CV-HOMOGRAPHIE-004", f"RANSAC budget, w={w}",
              f"ceil(log(0.01)/log(1-{w}**4))",
              math.ceil(math.log(0.01) / math.log1p(-(w ** 4))), expected)
    check("CV-HOMOGRAPHIE-007", "near disparity, px", "800 * 0.1 / 2", 800 * 0.1 / 2, 40)
    check("CV-HOMOGRAPHIE-007", "far disparity, px", "800 * 0.1 / 10", 800 * 0.1 / 10, 8)
    check("CV-ZHANG-004", "target scale bias, percent", "(20/19.8-1)*100",
          (20 / 19.8 - 1) * 100, 1.0101010101010166)
    check("CV-ZHANG-005", "resize then crop principal point, px", "0.5*320-20",
          0.5 * 320 - 20, 140)
    check("CV-ZHANG-005", "crop then resize principal point, px", "0.5*(320-20)",
          0.5 * (320 - 20), 150)
    check("CV-FISHEYE-001", "fisheye radius at 60 degrees", "radians(60)",
          math.radians(60), 1.0471975511965976)
    check("CV-FISHEYE-001", "pinhole radius at 60 degrees", "tan(radians(60))",
          math.tan(math.radians(60)), 1.7320508075688767)
    check("CV-FISHEYE-003", "radially imbalanced RMS, px", "sqrt((90*0.2**2+10*2**2)/100)",
          math.sqrt((90 * 0.2 ** 2 + 10 * 2 ** 2) / 100), 0.6603029607687671)
    check("CV-STEREO-002", "near bound, m", "200/2.5", 200 / 2.5, 80)
    check("CV-STEREO-002", "far bound, m", "200/1.5", 200 / 1.5, 133.33333333333334)
    check("CV-STEREO-003", "unconverted fixed-point depth scale", "20/320", 20 / 320, 1 / 16)
    check("CV-VIO-004", "orientation age error, degrees", "100*0.020", 100 * 0.020, 2)
    check("CV-CLIP-002", "original softmax", "19/(19+1)", 19 / 20, 0.95)
    check("CV-CLIP-002", "softmax after competing top label", "19/(19+19+1)",
          19 / 39, 0.48717948717948717)
    check("CV-OCR-002", "micro CER, percent", "100/101", 100 / 101, 0.9900990099009901)
    check("CV-DETECTEURS-004", "scaled object width, px", "12*(640/1920)", 12 / 3, 4)
    check("CV-DETECTEURS-004", "scaled object height, px", "9*(640/1920)", 9 / 3, 3)
    check("CV-DETECTEURS-004", "vertical padding per side, px", "(640-1080/3)/2",
          (640 - 1080 / 3) / 2, 140)
    check("CV-DETECTEURS-009", "GIoU with unit gap", "-(3-2)/3", -(3 - 2) / 3, -1 / 3)
    check("CV-DETECTEURS-009", "GIoU with two-unit gap", "-(4-2)/4", -(4 - 2) / 4, -0.5)
    for logit in [-2.0, 0.0, 2.0]:
        def focal(value):
            probability = 1 / (1 + math.exp(-value))
            return -(1 - probability) ** 2 * math.log(probability)

        probability = 1 / (1 + math.exp(-logit))
        analytic = (1 - probability) ** 2 * (
            2 * probability * math.log(probability) - (1 - probability))
        step = 1e-5
        numeric = (focal(logit + step) - focal(logit - step)) / (2 * step)
        check("CV-DETECTEURS-008", f"focal logit gradient at z={logit}",
              "analytic derivative versus central finite difference, gamma=2",
              analytic, numeric, tolerance=1e-7)
    check("CV-VIDEO-002", "event hit probability", "0.1/1", 0.1 / 1, 0.1)
    check("CV-VIDEO-003", "five-frame lookahead at 30 Hz, ms", "5/30*1000",
          5 / 30 * 1000, 166.66666666666666)
    check("CV-SORT-003", "posterior variance, px squared", "(1-25/34)*25",
          (1 - 25 / 34) * 25, 225 / 34)
    check("CV-IOU-AP-004", "AP101", "(51+50*(2/3))/101",
          (51 + 50 * (2 / 3)) / 101, 0.834983498349835)
    check("CV-IOU-AP-006", "one-pixel shift IoU", "9/11", 9 / 11, 0.8181818181818182)
    check("CV-IOU-AP-006", "two-pixel shift IoU", "8/12", 8 / 12, 2 / 3)
    check("CV-IOU-AP-007", "precision at low prevalence", "99/(99+999)",
          99 / 1098, 0.09016393442622951)
    check("CV-METRIQUES-TEMPS-002", "mean per-threshold HOTA example",
          "(sqrt(1*0.25)+sqrt(0.25*1))/2", (math.sqrt(0.25) + math.sqrt(0.25)) / 2, 0.5)
    check("CV-METRIQUES-TEMPS-002", "incorrect recombination example",
          "sqrt(0.625*0.625)", math.sqrt(0.625 * 0.625), 0.625)
    check("CV-METRIQUES-APPLIQUEES-004", "empty-dominated mean Dice", "99/100", 99 / 100, 0.99)
    check("CV-PIPELINE-002", "buffer fill time, seconds", "400/(240-200)", 400 / (240 - 200), 10)
    check("CV-QUANT-004", "ideal total speedup", "1/(0.8+0.2/2)", 1 / (0.8 + 0.2 / 2), 10 / 9)
    check("CV-DEPLOIEMENT-001", "total time with overhead", "0.9+0.1/2+0.05",
          0.9 + 0.1 / 2 + 0.05, 1)
    check("CV-CANNY-HOUGH-002", "ROI vertical line full-image rho, px",
          "20 + 100*cos(0) + 50*sin(0)", 20 + 100 * math.cos(0) + 50 * math.sin(0), 120)
    check("CV-BA-002", "camera-pair connections from a five-camera track",
          "5*(5-1)/2", 5 * 4 / 2, 10)
    check("CV-BA-002", "camera-pair connection from a two-camera track",
          "2*(2-1)/2", 2 * 1 / 2, 1)
    print(json.dumps({"date": "2026-11-08", "environment": "Python standard library",
                      "scope": "constructed arithmetic only; no CV implementation run",
                      "passed": len(checks), "checks": checks}, indent=2))


if __name__ == "__main__":
    main()
