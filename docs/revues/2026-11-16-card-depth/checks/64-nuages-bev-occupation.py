"""Recompute the constructed numbers added to CV-BEV-003 and CV-BEV-004 and the grid of the
figure cv-bev-occupancy-implicit.svg (reference 64-nuages-bev-occupation, revision 8,
2026-11-16).

Stdlib only. Run from the repository root with:
    python3 -I docs/revues/2026-11-16-card-depth/checks/64-nuages-bev-occupation.py
OctoMap sensor model: Hornung et al. 2013, Sec. 3.1 (unknown = never initialized), Sec. 3.2
(log-odds update, clamping) and Sec. 5.1 (l_occ = 0.85, l_free = -0.4, ray casting from the
sensor origin to each end point); octomap v1.10.0 insertPointCloud updates each voxel once per
scan with occupied preferred over free (OccupancyOcTreeBase.h L78-L97). Occupancy-network
threshold tau = 0.2: Mescheder et al. 2019, Sec. 4.2. The scan, the pallet, the 30 deg/s turn,
the 50 ms offset and the 100 ms sweep are constructed.
"""

import math
import pathlib
import xml.dom.minidom

checks = 0


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def logit(p):
    return math.log(p / (1 - p))


def prob(l):
    return 1 / (1 + math.exp(-l))


# --- CV-BEV-003: what one scan writes, and the network's surface level ---------------------
# Check 1: one free update gives P = 0.4, one return P = 0.7 from the 0.5 prior; the clamps
# -2 and 3.5 correspond to 0.12 and 0.97.
assert close(prob(-0.4), 0.401, 1e-3) and close(prob(0.85), 0.701, 1e-3)
assert close(prob(-2.0), 0.119, 1e-3) and close(prob(3.5), 0.971, 1e-3)
checks += 1
# Check 2: with tau = 0.2, a query at f = 0.3 is inside the extracted mesh although f < 0.5.
tau, f = 0.2, 0.3
assert f >= tau and f < 0.5
checks += 1

# --- CV-BEV-004: timing signatures (reference worked example D) -----------------------------
omega, dt = math.radians(30.0), 0.050
lat20, lat5 = 20 * math.tan(omega * dt), 5 * math.tan(omega * dt)
# Check 3: 1.5 deg of rotation moves a static point 0.52 m at 20 m (3.3 cells of 0.16 m), 0.13 m at 5 m.
assert close(math.degrees(omega * dt), 1.5) and close(lat20, 0.5237, 1e-4) and close(lat5, 0.1309, 1e-4)
assert close(lat20 / 0.16, 3.27, 1e-2)
checks += 1
slope = lat20 / 20
# Check 4: lateral error against range is a line of slope tan(omega dt) ~ 0.026 m per metre; dividing
# by omega = 0.524 rad/s recovers dt ~ 0.05 s; the opposite turn gives the opposite slope.
assert close(slope, 0.02619, 1e-5) and close(omega, 0.5236, 1e-4) and close(slope / omega, 0.05, 1e-4)
assert close(20 * math.tan(-omega * dt) / 20, -slope)
assert close(10.0 * dt, 0.5)                    # straight at 10 m/s: 0.5 m at every range
checks += 1
T_sweep = 0.100                                 # 10 Hz spinning sensor (constructed)
# Check 5: a sweep placed with one pose is misplaced by up to omega T = 3 deg; a static wall at 20 m
# shows a tear of about 1.05 m where the sweep starts and ends.
assert close(math.degrees(omega * T_sweep), 3.0)
assert close(20 * math.tan(omega * T_sweep), 1.048, 1e-3) and close(2 * 20 * math.sin(omega * T_sweep / 2), 1.047, 1e-3)
checks += 1

# --- Figure: exact ray casting of the constructed scan ----------------------------------
NC, NR, CS, X0, Y0 = 13, 9, 30.0, 75.0, 70.0     # grid in figure units; y grows downwards
SX, SY = X0 + 6.5 * CS, Y0 + 8.5 * CS            # sensor at the centre of cell (6, 8)
PAL = (285.0, 160.0, 345.0, 190.0)               # pallet rectangle x0, y0, x1, y1 (cells (7,3), (8,3))
ANGLES = list(range(-36, 37, 6))                 # degrees from straight ahead, 13 rays


def ray_hit(deg):
    """First intersection with the pallet (slab method) or with the wall y = Y0."""
    th = math.radians(deg)
    dx, dy = math.sin(th), -math.cos(th)
    tmin, tmax = 0.0, math.inf
    for o, d, lo, hi in ((SX, dx, PAL[0], PAL[2]), (SY, dy, PAL[1], PAL[3])):
        if abs(d) < 1e-15:
            if not lo <= o <= hi:
                tmin, tmax = math.inf, -math.inf
        else:
            t1, t2 = (lo - o) / d, (hi - o) / d
            tmin, tmax = max(tmin, min(t1, t2)), min(tmax, max(t1, t2))
    if tmin <= tmax and tmin > 0:
        return tmin, dx, dy
    return (Y0 - SY) / dy, dx, dy


def cell(x, y):
    return (math.floor((x - X0) / CS), math.floor((y - Y0) / CS))


def traverse(t_end, dx, dy):
    """Amanatides-Woo traversal of the cells crossed before the end point."""
    c, r = cell(SX, SY)
    end_c, end_r = cell(SX + dx * (t_end + 1e-6), SY + dy * (t_end + 1e-6)) if False else cell(
        SX + dx * t_end + 1e-6 * dx, SY + dy * t_end + 1e-6 * dy)
    step_c, step_r = (1 if dx > 0 else -1), (1 if dy > 0 else -1)
    nx = X0 + (c + (1 if dx > 0 else 0)) * CS
    ny = Y0 + (r + (1 if dy > 0 else 0)) * CS
    t_max_x = (nx - SX) / dx if abs(dx) > 1e-15 else math.inf
    t_max_y = (ny - SY) / dy if abs(dy) > 1e-15 else math.inf
    t_dx = CS / abs(dx) if abs(dx) > 1e-15 else math.inf
    t_dy = CS / abs(dy) if abs(dy) > 1e-15 else math.inf
    crossed = []
    while True:
        crossed.append((c, r))
        if min(t_max_x, t_max_y) >= t_end - 1e-9:
            break
        if t_max_x < t_max_y:
            c += step_c
            t_max_x += t_dx
        else:
            r += step_r
            t_max_y += t_dy
    return crossed


free, occ, ends = set(), set(), []
for deg in ANGLES:
    t_end, dx, dy = ray_hit(deg)
    hx, hy = SX + dx * t_end, SY + dy * t_end
    crossed = traverse(t_end, dx, dy)
    if hy <= Y0 + 1e-9:                          # wall return: the end cell is the last cell inside
        end_cell = crossed[-1]
    else:                                         # pallet return: the cell just beyond the face
        end_cell = cell(hx + 1e-6 * dx, hy + 1e-6 * dy)
    occ.add(end_cell)
    free.update(cc for cc in crossed if cc != end_cell)
    ends.append((hx, hy))
free -= occ                                       # one update per scan, occupied preferred
state = {}
for r in range(NR):
    for c in range(NC):
        state[(c, r)] = "occ" if (c, r) in occ else ("free" if (c, r) in free else "unk")

svg_path = pathlib.Path("vault/99-Ressources/cv-bev-occupancy-implicit.svg")
doc = xml.dom.minidom.parse(str(svg_path))
fills = {"#b91c1c": "occ", "#15803d": "free", "url(#bv-hatch)": "unk"}
drawn = {}
for rect in doc.getElementsByTagName("rect"):
    rid = rect.getAttribute("id")
    if rid.startswith("bv-c"):
        c, r = (int(v) for v in rid[4:].split("r"))
        assert close(float(rect.getAttribute("x")), X0 + c * CS) and close(float(rect.getAttribute("y")), Y0 + r * CS)
        drawn[(c, r)] = fills[rect.getAttribute("fill")]
# Check 6: all 117 cells are drawn and each drawn state matches the exact ray casting.
assert len(drawn) == NC * NR and drawn == state
checks += 1
# Check 7: what the figure claims: the cells behind the pallet and the pallet's far cells are unknown,
# the two near pallet cells hold returns, the corners beside the field of view are unknown, and
# 13 rays leave 2 pallet returns plus 9 wall cells with returns.
assert state[(7, 3)] == state[(8, 3)] == "occ"
assert all(state[cc] == "unk" for cc in ((7, 0), (8, 0), (9, 0), (7, 1), (8, 1), (9, 1), (7, 2), (8, 2)))
assert all(state[cc] == "unk" for cc in ((0, 8), (1, 8), (2, 8), (0, 7), (12, 8), (12, 7)))
assert sum(1 for cc in occ if cc[1] == 0) == 9 and len(occ) == 11
checks += 1
# Check 8: the ray end points drawn in the figure match the exact intersections to 0.06 units.
lines = [ln for ln in doc.getElementsByTagName("line") if ln.parentNode.getAttribute("id") == "bv-rays"]
assert len(lines) == len(ANGLES)
for ln, (hx, hy) in zip(lines, ends):
    assert close(float(ln.getAttribute("x1")), SX) and close(float(ln.getAttribute("y1")), SY)
    assert abs(float(ln.getAttribute("x2")) - hx) <= 0.06 and abs(float(ln.getAttribute("y2")) - hy) <= 0.06
checks += 1

print(f"64-nuages-bev-occupation (CV-BEV-003, CV-BEV-004, figure): {checks} checks passed")
