"""Recompute the constructed examples of CV-SORT-009 (reference 111-sort).

Stdlib only. Run with: python3 -I docs/revues/2026-11-15-accepted-proposals/checks/111-sort.py
What is recomputed: the IoU budget of two equal boxes shifted by d, and a pure-Python port of
the pinned SORT update loop run on constructed single-object sequences.
Conventions fixed by the sources:
- abewley/sort at commit 2236dff5019565958b84df7d871d41cc1db58ac7, sort.py:
  iou_batch L47-L63; box <-> [u, v, s, r] L66-L91; KalmanBoxTracker L99-L121 (F, H,
  R[2:,2:] *= 10, P[4:,4:] *= 1000 then P *= 10, Q[-1,-1] *= 0.01, Q[4:,4:] *= 0.01, only
  x[:4] set from the box); update L123-L131; predict and hit_streak reset L133-L145;
  associate_detections_to_trackers with the > threshold shortcut and the < threshold
  rejection L154-L196; Sort defaults max_age=1, min_hits=3, iou_threshold=0.3 L200;
  update loop, output rule and deletion L210-L253.
- filterpy at commit 5df4e095fac07684a05c495bd72d3424f7c68c9c, kalman_filter.py L397-L403:
  x = 0, P = Q = I, R = I by default, so a new track's velocities are exactly 0; update with
  the Joseph-form covariance L553-L554.
- Bewley et al. 2016 (arXiv 1602.00763) Sec. 3.3: detections are matched to predicted boxes
  by IoU and pairs below IoU_min are rejected; Sec. 3.4: a new tracker starts from the box
  "with the velocity set to zero" and a large velocity covariance.
The sequences (box sizes, speeds, frame rates) are project constructions.
"""

import itertools


def iou(a, b):
    """sort.py L47-L63 for one pair of [x1, y1, x2, y2] boxes."""
    w = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    h = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = w * h
    return inter / ((a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter)


def to_z(b):
    w, h = b[2] - b[0], b[3] - b[1]
    return [b[0] + w / 2.0, b[1] + h / 2.0, w * h, w / h]


def to_box(x):
    w = (x[2] * x[3]) ** 0.5
    h = x[2] / w
    return [x[0] - w / 2.0, x[1] - h / 2.0, x[0] + w / 2.0, x[1] + h / 2.0]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(r) for r in zip(*a)]


def inverse(m):
    n = len(m)
    a = [row[:] + [float(i == j) for j in range(n)] for i, row in enumerate(m)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(a[r][c]))
        a[c], a[p] = a[p], a[c]
        piv = a[c][c]
        a[c] = [v / piv for v in a[c]]
        for r in range(n):
            if r != c:
                f = a[r][c]
                a[r] = [v - f * w for v, w in zip(a[r], a[c])]
    return [row[n:] for row in a]


def eye(n, d=1.0):
    return [[d if i == j else 0.0 for j in range(n)] for i in range(n)]


F = [[1, 0, 0, 0, 1, 0, 0], [0, 1, 0, 0, 0, 1, 0], [0, 0, 1, 0, 0, 0, 1], [0, 0, 0, 1, 0, 0, 0],
     [0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1]]
Hm = [[1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0]]


class Track:
    count = 0

    def __init__(self, box):
        """sort.py L99-L121 with filterpy defaults L397-L403."""
        self.R = eye(4)
        self.R[2][2] = self.R[3][3] = 10.0
        self.P = eye(7)
        for i in range(4, 7):
            self.P[i][i] *= 1000.0
        self.P = [[v * 10.0 for v in row] for row in self.P]
        self.Q = eye(7)
        self.Q[6][6] *= 0.01
        for i in range(4, 7):
            self.Q[i][i] *= 0.01
        self.x = to_z(box) + [0.0, 0.0, 0.0]          # velocities stay 0
        self.time_since_update = 0
        self.id = Track.count
        Track.count += 1
        self.hits = self.hit_streak = self.age = 0
        self.last_gain = None

    def predict(self):
        if self.x[6] + self.x[2] <= 0:
            self.x[6] = 0.0
        self.x = [sum(F[i][k] * self.x[k] for k in range(7)) for i in range(7)]
        fp = matmul(F, self.P)
        self.P = [[a + b for a, b in zip(r1, r2)] for r1, r2 in zip(matmul(fp, transpose(F)), self.Q)]
        self.age += 1
        if self.time_since_update > 0:
            self.hit_streak = 0
        self.time_since_update += 1
        return to_box(self.x)

    def update(self, box):
        self.time_since_update = 0
        self.hits += 1
        self.hit_streak += 1
        z = to_z(box)
        pht = matmul(self.P, transpose(Hm))
        s = [[a + b for a, b in zip(r1, r2)] for r1, r2 in zip(matmul(Hm, pht), self.R)]
        k = matmul(pht, inverse(s))
        y = [z[i] - sum(Hm[i][j] * self.x[j] for j in range(7)) for i in range(4)]
        self.x = [self.x[i] + sum(k[i][j] * y[j] for j in range(4)) for i in range(7)]
        ikh = [[eye(7)[i][j] - sum(k[i][m] * Hm[m][j] for m in range(4)) for j in range(7)] for i in range(7)]
        krk = matmul(matmul(k, self.R), transpose(k))
        self.P = [[a + b for a, b in zip(r1, r2)]                 # Joseph form, filterpy L553-L554
                  for r1, r2 in zip(matmul(matmul(ikh, self.P), transpose(ikh)), krk)]
        self.last_gain = k


def associate(dets, preds, thr=0.3):
    """sort.py L154-L196; the optimal assignment is found by enumeration (tiny sizes here)
    instead of lap or scipy, which return the same maximum-IoU assignment."""
    if not preds:
        return [], list(range(len(dets)))
    m = [[iou(d, p) for p in preds] for d in dets]
    a = [[int(v > thr) for v in row] for row in m]
    if dets and max(sum(r) for r in a) == 1 and max(sum(c) for c in zip(*a)) == 1:
        pairs = [(i, j) for i in range(len(dets)) for j in range(len(preds)) if a[i][j]]
    else:
        k = min(len(dets), len(preds))
        candidates = ([list(zip(rows, cols))
                       for rows in itertools.permutations(range(len(dets)), k)
                       for cols in itertools.combinations(range(len(preds)), k)] if k else [[]])
        pairs = max(candidates, key=lambda c: sum(m[i][j] for i, j in c))
    matches = [(i, j) for i, j in pairs if m[i][j] >= thr]
    matched = {i for i, _ in matches}
    return matches, [i for i in range(len(dets)) if i not in matched]


class Sort:
    def __init__(self, max_age=1, min_hits=3, iou_threshold=0.3):
        self.max_age, self.min_hits, self.thr = max_age, min_hits, iou_threshold
        self.trackers, self.frame_count = [], 0

    def update(self, dets):
        """sort.py L210-L253; returns [(box, id + 1)] as the reference does."""
        self.frame_count += 1
        preds = [t.predict() for t in self.trackers]
        matches, unmatched = associate(dets, preds, self.thr)
        for i, j in matches:
            self.trackers[j].update(dets[i])
        for i in unmatched:
            self.trackers.append(Track(dets[i]))
        out = []
        for t in reversed(list(self.trackers)):
            if t.time_since_update < 1 and (t.hit_streak >= self.min_hits or self.frame_count <= self.min_hits):
                out.append((to_box(t.x), t.id + 1))
            if t.time_since_update > self.max_age:
                self.trackers.remove(t)
        return out


def run(speeds, w=16.0, h=16.0, x0=100.0, y0=200.0):
    """One object detected in every frame; speeds[k] is its displacement before frame k + 2."""
    Track.count = 0
    tracker, x, outputs = Sort(), x0, []
    boxes = [[x, y0, x + w, y0 + h]]
    for v in speeds:
        x += v
        boxes.append([x, y0, x + w, y0 + h])
    for b in boxes:
        outputs.append(tracker.update([b]))
    return outputs, Track.count, tracker, boxes


checks = 0

# Check 1: equal boxes shifted by d along x: IoU = (w - d) / (w + d); IoU >= 0.3 <=> d <= 0.538 w.
w = 16.0
for d in (0.0, 4.0, 8.6, 10.0):
    assert abs(iou([0, 0, w, w], [d, 0, d + w, w]) - (w - d) / (w + d)) < 1e-12
d_max = (1 - 0.3) / (1 + 0.3)
assert abs(d_max - 0.5385) < 1e-4; checks += 1

# Check 2: a diagonal shift is stricter -- (dx, dy) = (0.4 w, 0.4 w) already gives IoU 0.2195.
assert abs(iou([0, 0, w, w], [0.4 * w, 0.4 * w, 1.4 * w, 1.4 * w]) - 0.36 / 1.64) < 1e-12; checks += 1

# Check 3: a new track predicts exactly its birth box (zero velocity, F x = x), so its first match
# faces the IoU between two consecutive detections.
Track.count = 0
t = Track([100.0, 200.0, 116.0, 216.0])
assert t.x[4:] == [0.0, 0.0, 0.0]
pred = t.predict()
assert max(abs(a - b) for a, b in zip(pred, [100.0, 200.0, 116.0, 216.0])) < 1e-9; checks += 1

# Check 4: 16 px box moving 10 px per frame (d/w = 0.625): consecutive IoU 6/26 = 0.231 < 0.3.
# SORT creates a new internal track at every one of the 20 frames and returns nothing after the
# first min_hits = 3 frames, where each output carries a different ID.
out30, n_tracks30, _, boxes30 = run([10.0] * 19)
assert abs(iou(boxes30[0], boxes30[1]) - 6 / 26) < 1e-12
assert n_tracks30 == 20 and [o[0][1] for o in out30[:3]] == [1, 2, 3] and all(o == [] for o in out30[3:]); checks += 1

# Check 5: the same object at twice the frame rate (5 px per frame, d/w = 0.3125, IoU 11/21 = 0.524)
# keeps one ID, output in all 40 frames.
out60, n_tracks60, _, boxes60 = run([5.0] * 39)
assert abs(iou(boxes60[0], boxes60[1]) - 11 / 21) < 1e-12
assert n_tracks60 == 1 and all(o and o[0][1] == 1 for o in out60); checks += 1

# Check 6: the first update learns the velocity: gains 0.9999 (centre) and 0.9988 (velocity), so
# the velocity becomes 0.9988 * 5 = 4.99 px/frame and the third prediction overlaps at IoU > 0.99.
Track.count = 0
s = Sort()
s.update([[100.0, 200.0, 116.0, 216.0]])
s.update([[105.0, 200.0, 116.0 + 5.0, 216.0]])
trk = s.trackers[0]
assert abs(trk.last_gain[0][0] - 10011 / 10012) < 1e-9 and abs(trk.last_gain[4][0] - 10000 / 10012) < 1e-9
assert abs(trk.x[4] - 5.0 * 10000 / 10012) < 1e-9
assert iou(trk.predict(), [110.0, 200.0, 126.0, 216.0]) > 0.99; checks += 1

# Check 7: what fails is the birth, not the speed: born at 5 px/frame and accelerating by
# 0.5 px/frame^2 to 10 px/frame (d/w = 0.625), then holding that speed, the object keeps ID 1 in
# every frame, whereas a track born at 10 px/frame never survives (check 4).
ramp = [5.0 + 0.5 * k for k in range(11)] + [10.0] * 19
out_ramp, n_ramp, _, _ = run(ramp)
assert n_ramp == 1 and all(o and o[0][1] == 1 for o in out_ramp) and max(ramp) / 16.0 == 0.625; checks += 1

# Check 8: lowering iou_threshold to 0.2 admits the 10 px/frame birth (IoU 0.231), one ID throughout;
# it also widens the gate for every other pair, which is the price of this remedy.
Track.count = 0
s2, ids = Sort(iou_threshold=0.2), set()
for b in boxes30:
    for _, tid in s2.update([b]):
        ids.add(tid)
assert Track.count == 1 and ids == {1}; checks += 1

print(f"111-sort (CV-SORT-009): {checks} checks passed "
      f"(d_max/w = {d_max:.4f}; 16 px box at 10 px/frame: {n_tracks30} tracks in 20 frames, "
      f"IoU {6 / 26:.3f}; at 5 px/frame: {n_tracks60} track, IoU {11 / 21:.3f})")
