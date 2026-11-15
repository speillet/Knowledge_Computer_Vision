"""Recompute the constructed example of CV-WATERSHED-006 (reference 91-otsu-distance-watershed).

Stdlib only. Run with: python3 -I docs/revues/2026-11-15-accepted-proposals/checks/91-otsu-distance-watershed.py
What is recomputed: a line-by-line Python port of OpenCV 4.13.0 `cv::watershed`
(modules/imgproc/src/segmentation.cpp, tag 4.13.0) is run on a constructed BGR image, and
compared with a priority flood of -D (lowest value first, ties by entry time), the relief
of Beucher and Meyer's thalweg lines (1993, Sec. VI.B) and of scikit-image's documented
call `watershed(-distance, markers, mask=image)` (v0.25.2, _watershed.py L99-L100,
L143-L149, L208). Conventions fixed by the sources:
- priority of a pixel reached from a labelled 4-neighbour = max over B, G, R of the absolute
  difference between the two pixels, 0..255 (segmentation.cpp L151-L159);
- CV_8UC3 image and CV_32SC1 markers required (L161); one-pixel frame set to -1, negative
  inputs reset to 0 (L179-L193); initial queue entry with the smallest difference to an
  adjacent marker (L183-L223);
- 256 FIFO queues, lowest index first; a pixel whose labelled 4-neighbours carry two
  labels becomes -1 and does not propagate (L239-L293); a newly labelled pixel pushes its
  unlabelled 4-neighbours with their difference to it (L295-L323);
- markers as in the 4.13.0 tutorial: sure foreground D > alpha max D, sure background =
  mask dilated 3 times by 3x3, labels shifted by one, unknown = 0
  (doc/py_tutorials/py_imgproc/py_watershed/py_watershed.markdown L80-L121).
D is the exact Euclidean distance from each foreground pixel centre to the nearest
background pixel centre (what DIST_L2 with DIST_MASK_PRECISE computes). The scene is a
project construction; no OpenCV or scikit-image call is executed.
"""

import heapq
import math
from collections import deque

W, H = 80, 50
C1, R1 = (25, 25), 20          # large coin
C2, R2 = (55, 25), 14          # small coin, centres 30 px apart
GREY, DARK, LIGHT = (60, 60, 60), (0, 0, 0), (230, 230, 230)
RIM = (15.0, 17.0)             # dark rim of the large coin, radius in [15, 17) px
ALPHA = 0.7                    # the tutorial's value
N4 = ((-1, 0), (1, 0), (0, -1), (0, 1))


def inside(x, y, c, r):
    return (x - c[0]) ** 2 + (y - c[1]) ** 2 <= r * r


def scene(rim):
    img = [[LIGHT] * W for _ in range(H)]
    fg = [[0] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            a, b = inside(x, y, C1, R1), inside(x, y, C2, R2)
            if a or b:
                fg[y][x], img[y][x] = 1, GREY
                if rim and a and not b and RIM[0] <= math.hypot(x - C1[0], y - C1[1]) < RIM[1]:
                    img[y][x] = DARK
    return img, fg


def distance(fg):
    bg = [(x, y) for y in range(H) for x in range(W) if not fg[y][x]]
    return [[math.sqrt(min((x - u) ** 2 + (y - v) ** 2 for u, v in bg)) if fg[y][x] else 0.0
             for x in range(W)] for y in range(H)]


def dilate3(m, iterations):
    for _ in range(iterations):
        m = [[int(any(m[v][u] for v in range(max(0, y - 1), min(H, y + 2))
                      for u in range(max(0, x - 1), min(W, x + 2))))
              for x in range(W)] for y in range(H)]
    return m


def components8(b):
    lab, k = [[0] * W for _ in range(H)], 0
    for y in range(H):
        for x in range(W):
            if b[y][x] and not lab[y][x]:
                k += 1
                lab[y][x], stack = k, [(x, y)]
                while stack:
                    u, v = stack.pop()
                    for du in (-1, 0, 1):
                        for dv in (-1, 0, 1):
                            p, q = u + du, v + dv
                            if 0 <= p < W and 0 <= q < H and b[q][p] and not lab[q][p]:
                                lab[q][p] = k
                                stack.append((p, q))
    return lab, k


def c_diff(a, b):
    """segmentation.cpp L151-L159: highest absolute channel difference."""
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))


def cv_watershed(img, markers):
    """Port of cv::watershed, OpenCV 4.13.0 segmentation.cpp L88-L325."""
    m = [row[:] for row in markers]
    WSHED, IN_QUEUE = -1, -2
    q = [deque() for _ in range(256)]
    for x in range(W):
        m[0][x] = m[H - 1][x] = WSHED
    for y in range(1, H - 1):
        m[y][0] = m[y][W - 1] = WSHED
        for x in range(1, W - 1):
            if m[y][x] < 0:
                m[y][x] = 0
            if m[y][x] == 0 and any(m[y + dy][x + dx] > 0 for dx, dy in N4):
                idx = min(c_diff(img[y][x], img[y + dy][x + dx]) for dx, dy in N4 if m[y + dy][x + dx] > 0)
                q[idx].append((x, y))
                m[y][x] = IN_QUEUE
    active = next((i for i in range(256) if q[i]), None)
    if active is None:
        return m
    while True:
        if not q[active]:
            active = next((i for i in range(active + 1, 256) if q[i]), None)
            if active is None:
                break
        x, y = q[active].popleft()
        lab = 0
        for dx, dy in N4:
            t = m[y + dy][x + dx]
            if t > 0:
                lab = t if lab == 0 else (lab if t == lab else WSHED)
        assert lab != 0
        m[y][x] = lab
        if lab == WSHED:
            continue
        for dx, dy in N4:
            if m[y + dy][x + dx] == 0:
                t = c_diff(img[y][x], img[y + dy][x + dx])
                q[t].append((x + dx, y + dy))
                active = min(active, t)
                m[y + dy][x + dx] = IN_QUEUE
    return m


def flood(relief, markers, mask):
    """Priority flood: lowest relief value first, ties by entry time; no dam line."""
    lab = [row[:] for row in markers]
    heap, age = [], 0
    for y in range(H):
        for x in range(W):
            if lab[y][x] > 0:
                for dx, dy in N4:
                    u, v = x + dx, y + dy
                    if 0 <= u < W and 0 <= v < H and mask[v][u] and lab[v][u] == 0:
                        heapq.heappush(heap, (relief[v][u], age, u, v, lab[y][x]))
                        age += 1
    while heap:
        _, _, x, y, label = heapq.heappop(heap)
        if lab[y][x]:
            continue
        lab[y][x] = label
        for dx, dy in N4:
            u, v = x + dx, y + dy
            if 0 <= u < W and 0 <= v < H and mask[v][u] and lab[v][u] == 0:
                heapq.heappush(heap, (relief[v][u], age, u, v, label))
                age += 1
    return lab


def run(rim):
    img, fg = scene(rim)
    d = distance(fg)
    dmax = max(max(row) for row in d)
    sure_fg = [[int(d[y][x] > ALPHA * dmax) for x in range(W)] for y in range(H)]
    sure_bg = dilate3(fg, 3)
    cc, k = components8(sure_fg)
    markers = [[0 if (sure_bg[y][x] and not sure_fg[y][x]) else cc[y][x] + 1 for x in range(W)] for y in range(H)]
    cv_labels = cv_watershed(img, markers)
    seeds = [[cc[y][x] + 1 if cc[y][x] else 0 for x in range(W)] for y in range(H)]
    neg_d = [[-v for v in row] for row in d]
    d_labels = flood(neg_d, seeds, fg)
    return img, d, dmax, k, markers, cv_labels, d_labels


checks = 0
only_large = [(x, y) for y in range(H) for x in range(W) if inside(x, y, C1, R1) and not inside(x, y, C2, R2)]

img0, d0, dmax0, k0, markers0, cv0, neg0 = run(rim=False)
img1, d1, dmax1, k1, markers1, cv1, neg1 = run(rim=True)

# Check 1: geometry -- max D = sqrt(401) = 20.02 px at the large centre, sqrt(197) = 14.04 px at
# the small one, and a neck (saddle of D on the centre row) of 9.0 px at x = 43-44.
row = [d0[25][x] for x in range(W)]
assert abs(dmax0 - math.sqrt(401)) < 1e-12 and abs(row[55] - math.sqrt(197)) < 1e-12
neck_x = min(range(30, 55), key=lambda x: row[x])
assert neck_x in (43, 44) and abs(row[neck_x] - 9.0) < 1e-12; checks += 1

# Check 2: one seed per coin with the tutorial's alpha = 0.7; the small coin's seed is a single
# pixel, because its maximum 14.04 barely exceeds 0.7 * 20.02 = 14.02.
seed_small = sum(markers0[y][x] == 3 for y in range(H) for x in range(W))
assert k0 == k1 == 2 and seed_small == 1 and math.sqrt(197) > ALPHA * dmax0 > 14.0; checks += 1

# Check 3: the rim does not change D or the markers (they come from the binary mask only).
assert d0 == d1 and markers0 == markers1; checks += 1

# Check 4: priorities are colour differences: grey-grey 0 across the contact, grey-rim 60,
# grey-background 170 (segmentation.cpp L151-L159).
assert (c_diff(GREY, GREY), c_diff(GREY, DARK), c_diff(GREY, LIGHT)) == (0, 60, 170); checks += 1

# Check 5: without the rim, cv::watershed and the -D flood agree: the dam between the coins
# on the centre row sits at the neck (x = 44), and no pixel of the large coin gets label 3.
assert cv0[25][44] == -1 and cv0[25][43] == 2 and cv0[25][45] == 3
assert neg0[25][43] == 2 and neg0[25][44] == 3
assert sum(cv0[y][x] == 3 for x, y in only_large) == 0; checks += 1

# Check 6: with the rim, the small coin's label crosses the uniform contact at priority 0 and
# runs round the outer ring of the large coin: 235 of its 1,216 own pixels (19%) get label 3,
# e.g. x = 6-8 on the centre row, at the far side of the large coin.
taken = sum(cv1[y][x] == 3 for x, y in only_large)
assert len(only_large) == 1216 and taken == 235 and abs(taken / len(only_large) - 0.193) < 1e-3
assert [cv1[25][x] for x in (6, 7, 8)] == [3, 3, 3]; checks += 1

# Check 7: flooding -D with the same seeds ignores colours: identical labels with and without
# the rim, and no pixel of the large coin goes to the small coin.
assert neg0 == neg1 and sum(neg1[y][x] == 3 for x, y in only_large) == 0; checks += 1

# Check 8: OpenCV writes -1 on the image frame (segmentation.cpp L179-L193).
assert all(cv1[0][x] == -1 and cv1[H - 1][x] == -1 for x in range(W)); checks += 1

# Check 9: passing D itself, scaled to 0..255 and replicated in three channels, does not flood -D:
# the port floods differences of D between neighbours, about 12-13 per pixel along the cone
# slope but 0 across the saddle, so the neck is the cheapest place to cross. The small coin's
# label takes 899 of the large coin's 1,216 own pixels.
scale = 255.0 / dmax0
d_image = [[(round(d0[y][x] * scale),) * 3 for x in range(W)] for y in range(H)]
cv_d = cv_watershed(d_image, markers0)
steps = [c_diff(d_image[25][x], d_image[25][x + 1]) for x in range(10, 50)]
assert set(steps[:10]) <= {12, 13} and c_diff(d_image[25][43], d_image[25][44]) == 0
assert sum(cv_d[y][x] == 3 for x, y in only_large) == 899; checks += 1

print(f"91-otsu-distance-watershed (CV-WATERSHED-006): {checks} checks passed "
      f"(neck D = {row[neck_x]:.1f} px at x = {neck_x}; with rim, {taken}/{len(only_large)} "
      f"large-coin pixels labelled as the small coin by the cv::watershed port, 0 by the -D flood)")
