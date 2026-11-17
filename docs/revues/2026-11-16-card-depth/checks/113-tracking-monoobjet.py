"""Recompute the constructed numbers added to CV-SOT-001 and CV-SOT-002 and the coordinates
of the template-drift figure of reference 113-tracking-monoobjet (2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/113-tracking-monoobjet.py
Update rule m_t = (1 - eta) m_{t-1} + eta m_hat_t: MOSSE eqs. 10-12 and KCF Sec. VIII-A.
Rates: MOSSE 0.125 (Sec. 3.4); KCF 0.075 raw, 0.02 HOG (Table II); OpenCV TrackerKCF 0.075;
OpenCV legacy TrackerMOSSE 0.2. SiamFC speed: 86 frames/s with 3 scales (Sec. 4.1).
The two-appearance template and the tracking rule below are a project toy model.
"""

import math
import os
import xml.dom.minidom

checks = 0


def close(a, b, tol=1e-4):
    return abs(a - b) <= tol


# --- CV-SOT-001: cost of a bank of single-object trackers ------------------------------------
targets, scales, fps_one = 20, 3, 86.0
assert targets * scales == 60                  # search-crop embeddings per frame
assert close(fps_one / targets, 4.3)            # linear extrapolation, no batching (constructed)
checks += 1

# --- CV-SOT-002: toy model of a template shared by target and distractor ---------------------
# Unit appearance vectors a (target) and d (distractor) with similarity c = a.d < 1.
# Template m = (1 - s) a + s d. Responses: target (1 - s) + s c, distractor (1 - s) c + s.
for c in (0.0, 0.3, 0.8, 0.95):
    for s in (0.0, 0.2, 0.49, 0.51, 0.8, 1.0):
        r_target, r_distr = (1 - s) + s * c, (1 - s) * c + s
        assert close(r_distr - r_target, (2 * s - 1) * (1 - c), 1e-12)   # sign set by s - 1/2 only
        assert (r_distr > r_target) == (s > 0.5)
checks += 1


def share_after_occlusion(eta, length):
    """Distractor share after `length` updates made on the distractor, starting from s = 0."""
    s = 0.0
    for _ in range(length):
        s = (1 - eta) * s + eta
    return s


def run(eta, occlusion, frames, gated=False):
    """Simulate the share: on the distractor during the occlusion, then on whichever answers more."""
    s, trace = 0.0, [0.0]
    for t in range(1, frames + 1):
        if t <= occlusion:
            on_distractor = True
            if gated:                      # weak peak: the update is skipped
                trace.append(s)
                continue
        else:
            on_distractor = s > 0.5
        s = (1 - eta) * s + eta * (1.0 if on_distractor else 0.0)
        trace.append(s)
    return trace


for eta, share, half in ((0.02, 0.18, 34.3), (0.075, 0.54, 8.9), (0.125, 0.74, 5.2), (0.2, 0.89, 3.1)):
    assert close(share_after_occlusion(eta, 10), 1 - (1 - eta) ** 10, 1e-12)
    assert round(1 - (1 - eta) ** 10, 2) == share
    assert round(math.log(0.5) / math.log(1 - eta), 1) == half
checks += 1

# Tipping point: the occlusion locks the tracker on the distractor iff it lasts more than the
# model's half-life in updates. eta = 0.075: 8 frames recover, 9 lock; eta = 0.02: 34 vs 35.
for eta, last_safe in ((0.075, 8), (0.02, 34)):
    assert run(eta, last_safe, 400)[-1] < 0.01 and run(eta, last_safe + 1, 400)[-1] > 0.99
assert close(run(0.075, 10, 40)[10], 0.5414, 1e-4) and close(run(0.075, 10, 40)[40], 0.9558, 1e-4)
assert close(run(0.02, 10, 40)[10], 0.1829, 1e-4) and close(run(0.02, 10, 40)[40], 0.0998, 1e-4)
assert all(v == 0.0 for v in run(0.075, 10, 40, gated=True))
checks += 1

# --- Figure: polylines drawn at x = 70 + 11 k, y = 410 - 300 s -------------------------------
here = os.path.dirname(os.path.abspath(__file__))
svg = os.path.normpath(os.path.join(here, "..", "..", "..", "..", "vault", "99-Ressources",
                                    "cv-sot-template-drift.svg"))
dom = xml.dom.minidom.parse(svg)
lines = {p.getAttribute("id"): p.getAttribute("points") for p in dom.getElementsByTagName("polyline")}
for pid, trace in (("sd-eta0075", run(0.075, 10, 40)), ("sd-eta002", run(0.02, 10, 40))):
    pts = [tuple(map(float, q.split(","))) for q in lines[pid].split()]
    assert len(pts) == 41
    for k, (x, y) in enumerate(pts):
        assert close(x, 70 + 11 * k, 1e-9) and close(y, 410 - 300 * trace[k], 0.06)
assert lines["sd-gated"] == "70,410 510,410"
crossing = math.log(0.5) / math.log(0.925)
circles = [(float(c.getAttribute("cx")), float(c.getAttribute("cy"))) for c in dom.getElementsByTagName("circle")]
assert (180.0, 247.6) in circles and (180.0, 355.1) in circles
assert any(close(cx, 70 + 11 * crossing, 0.05) and cy == 260 for cx, cy in circles)
checks += 1

print(f"113-tracking-monoobjet (CV-SOT-001, CV-SOT-002, figure): {checks} checks passed")
