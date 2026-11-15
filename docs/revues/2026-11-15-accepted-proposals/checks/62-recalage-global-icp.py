"""Recompute the constructed examples of CV-ICP-006 (reference 62-recalage-global-icp).

Stdlib only. Run with: python3 -I docs/revues/2026-11-15-accepted-proposals/checks/62-recalage-global-icp.py
Conventions taken from Gelfand, Ikemoto, Rusinkiewicz and Levoy 2003, "Geometrically
Stable Sampling for the ICP Algorithm":
- eq. 4: C = sum_i a_i a_i^T with a_i = [p_i x n_i ; n_i] (rotation first), a 6x6 matrix;
- eq. 5: the alignment error grows by dE = x^T C x for a small motion x = [dr ; dt];
- Sec. 2.2: an eigenvector with a small eigenvalue is a motion along which the surfaces slide;
- Sec. 3.1: stability measure c = lambda_1 / lambda_6, computed after moving the centroid of
  the points to the origin and scaling them to a mean distance of 1.
The corridor, the two-plane scene and the door frame are project constructions; points
are noise-free samples with exact normals. No registration is run.
"""

import math


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def stability_matrix(scene):
    """C = sum a a^T, a = [p x n ; n] (Gelfand et al., eq. 4)."""
    c = [[0.0] * 6 for _ in range(6)]
    for p, n in scene:
        a = list(cross(p, n)) + list(n)
        for i in range(6):
            for j in range(6):
                c[i][j] += a[i] * a[j]
    return c


def eigen(m, sweeps=100):
    """Cyclic Jacobi; returns (eigenvalue, unit eigenvector) pairs, largest first."""
    n = len(m)
    a = [row[:] for row in m]
    v = [[float(i == j) for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-26 * sum(a[i][i] ** 2 for i in range(n)):
            break
        for p in range(n):
            for q in range(p + 1, n):
                if a[p][q] == 0.0:
                    continue
                th = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = math.copysign(1.0, th) / (abs(th) + math.sqrt(th * th + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    pairs = [(a[i][i], [v[k][i] for k in range(n)]) for i in range(n)]
    return sorted(pairs, key=lambda e: -e[0])


def normalize(scene):
    """Gelfand et al. Sec. 3.1: centroid to the origin, mean distance to 1."""
    pts = [p for p, _ in scene]
    c = [sum(p[i] for p in pts) / len(pts) for i in range(3)]
    q = [tuple(p[i] - c[i] for i in range(3)) for p in pts]
    s = sum(math.sqrt(sum(x * x for x in p)) for p in q) / len(q)
    return [(tuple(x / s for x in p), n) for p, (_, n) in zip(q, scene)]


def transform(scene, scale=1.0, shift=(0.0, 0.0, 0.0)):
    return [(tuple(scale * (p[i] + shift[i]) for i in range(3)), n) for p, n in scene]


def grid(a, b, step):
    k = int(round((b - a) / step))
    return [a + i * step for i in range(k + 1)]


def condition(ev):
    return ev[0][0] / ev[-1][0]


def is_axis(vec, k, tol=1e-6):
    """True when vec is +/- the k-th basis vector (0-2 rotations, 3-5 translations)."""
    return abs(abs(vec[k]) - 1.0) < tol and all(abs(x) < tol for i, x in enumerate(vec) if i != k)


checks = 0
h = 0.1                                   # sampling step (m)
L, W, H = 10.0, 2.0, 2.5                  # corridor along x: length, width, height (m)
X, Y, Z = grid(0, L, h), grid(0, W, h), grid(0, H, h)
floor = [((x, y, 0.0), (0.0, 0.0, 1.0)) for x in X for y in Y]
ceiling = [((x, y, H), (0.0, 0.0, -1.0)) for x in X for y in Y]
wall_a = [((x, 0.0, z), (0.0, 1.0, 0.0)) for x in X for z in Z]
wall_b = [((x, W, z), (0.0, -1.0, 0.0)) for x in X for z in Z]
corridor = floor + ceiling + wall_a + wall_b
two_planes = floor + wall_a
# Door frame: two vertical strips 2 m high whose normals face along the corridor (+/- x).
door = [((xd, -0.05, z), (sx, 0.0, 0.0)) for xd, sx in ((4.5, 1.0), (5.4, -1.0)) for z in grid(0, 2.0, h)]
corridor_door = corridor + door

# Check 1: sizes of the constructed scenes.
assert (len(floor), len(wall_a), len(corridor), len(door)) == (2121, 2626, 9494, 42); checks += 1

# Check 2: floor + one wall (two planes) -> exactly one zero eigenvalue after normalization;
# its eigenvector is the pure translation along the intersection line x = n_floor x n_wall.
ev2 = eigen(stability_matrix(normalize(two_planes)))
assert abs(ev2[-1][0]) < 1e-9 * ev2[0][0] and ev2[-2][0] > 1e-2 * ev2[0][0]
n_line = cross((0.0, 0.0, 1.0), (0.0, 1.0, 0.0))
assert is_axis(ev2[-1][1], 3) and abs(abs(n_line[0]) - 1.0) < 1e-12; checks += 1

# Check 3: corridor (floor, ceiling, two walls) -> one zero eigenvalue, pure translation along
# the axis; the rotation about the axis is the weakest constrained motion but is not free.
ev_c = eigen(stability_matrix(normalize(corridor)))
assert abs(ev_c[-1][0]) < 1e-9 * ev_c[0][0] and is_axis(ev_c[-1][1], 3)
assert is_axis(ev_c[-2][1], 0) and 0.09 < ev_c[-2][0] / ev_c[0][0] < 0.11; checks += 1

# Check 4: an exact null direction does not depend on units or origin (C' = M C M^T with M
# invertible), but every other eigenvalue does: raw mm inflates the largest one ~10^6 times.
ev_c_mm = eigen(stability_matrix(transform(corridor, 1000.0)))
ev_c_m = eigen(stability_matrix(corridor))
assert is_axis(ev_c_mm[-1][1], 3) and abs(ev_c_mm[-1][0]) < 1e-9 * ev_c_mm[0][0]
assert 0.9e6 < ev_c_mm[0][0] / ev_c_m[0][0] < 1.1e6; checks += 1

# Check 5: door frame -> the smallest eigenvalue becomes non-zero; after normalization the
# condition number is about 125 and the weakest eigenvector is still close to the axis translation.
ev_d = eigen(stability_matrix(normalize(corridor_door)))
kappa_norm = condition(ev_d)
assert 124.5 < kappa_norm < 125.5 and abs(ev_d[-1][1][3]) > 0.999; checks += 1

# Check 6: the same scan without normalization: ~4,500 in metres with the origin at the corridor
# entrance, ~4.4e9 in millimetres -- the raw number mixes geometry, unit and origin.
kappa_m = condition(eigen(stability_matrix(corridor_door)))
kappa_mm = condition(eigen(stability_matrix(transform(corridor_door, 1000.0))))
assert 4400 < kappa_m < 4500 and 4.3e9 < kappa_mm < 4.4e9; checks += 1

# Check 7: in a map frame whose origin lies 100 m and 50 m away, the raw weakest eigenvector is a
# rotation about the distant origin almost cancelled by a translation (|t_x| < 0.01), not the
# corridor translation, and its eigenvalue is far below the pure t_x value.
ev_far = eigen(stability_matrix(transform(corridor_door, 1.0, (100.0, 50.0, 0.0))))
tx_value = sum(n[0] ** 2 for _, n in corridor_door)          # x^T C x for x = pure t_x
assert abs(tx_value - 42.0) < 1e-9
assert abs(ev_far[-1][1][3]) < 0.01 and ev_far[-1][0] < tx_value / 10
assert 5.0e7 < condition(ev_far) < 5.3e7; checks += 1

# Check 8: normalization removes unit dependence exactly (metres and millimetres agree).
kappa_norm_mm = condition(eigen(stability_matrix(normalize(transform(corridor_door, 1000.0)))))
assert abs(kappa_norm_mm - kappa_norm) < 1e-6 * kappa_norm; checks += 1

# Check 9: eq. 5 reading -- sliding 0.05 m along the bare corridor changes the linearized error
# by 0; the same slide with the door frame costs 42 * 0.05^2 = 0.105 m^2, while a 0.05 m vertical
# slide costs (number of floor + ceiling points) * 0.05^2.
def delta_e(scene, x):
    c = stability_matrix(scene)
    return sum(x[i] * c[i][j] * x[j] for i in range(6) for j in range(6))


slide = [0, 0, 0, 0.05, 0, 0]
assert abs(delta_e(corridor, slide)) < 1e-12
assert abs(delta_e(corridor_door, slide) - 0.105) < 1e-9
assert abs(delta_e(corridor, [0, 0, 0, 0, 0, 0.05]) - 2 * len(floor) * 0.0025) < 1e-9; checks += 1

print(f"62-recalage-global-icp (CV-ICP-006): {checks} checks passed "
      f"(door: normalized c = {kappa_norm:.1f}, raw m = {kappa_m:.0f}, raw mm = {kappa_mm:.3g}; "
      f"corridor rotation/largest = {ev_c[-2][0] / ev_c[0][0]:.3f})")
