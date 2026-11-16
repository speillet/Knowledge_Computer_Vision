"""Recompute the constructed examples of CV-GEODESIE (153-systemes-reference).

Stdlib only. Run with:
python3 -I docs/revues/2026-11-16-photogrammetry/checks/153-systemes-reference.py

Formulas re-implemented (no geodetic library and no photogrammetric software is executed here):
- IOGP Geomatics Guidance Note 7-2 (September 2019): ellipsoid parameters (section 1.1),
  geographic/geocentric conversion and its non-iterative reverse (4.1.1), geocentric/topocentric
  conversion (4.1.2), Lambert Conic Conformal 2SP (3.1.1.1), time-dependent Helmert in the
  position-vector and coordinate-frame conventions (4.2.5), H = h - zeta (4.11.1).
- Scale factor of the ellipsoidal LCC, k = rho n / (a m) (Snyder 1987, p. 108, eqs. 14-16, 15-6 to
  15-10); spherical Transverse Mercator k = k0 / sqrt(1 - B^2), x = R k0 artanh B (Snyder 1987,
  p. 58, eqs. 8-2 to 8-5).
- ITRS/ETRS89 relationship, EUREF Technical Note 1 (Altamimi and Collilieux, release 2024-03-04):
  eq. (1) general 14-parameter transformation, eqs. (2)-(3), Tables 1 and 4, Appendix B examples.
Parameter values: GRS80 and WGS84 ellipsoids, Lambert-93 conversion (EPSG 18085) and the
ITRF2020 -> ETRF2000 transformation (EPSG 10586) as stored in PROJ 9.9.0 data/sql (EPSG v13.102).
Floats are used for the geodetic conversions, with the tolerances stated in each check. Every input
not marked as a cited example is constructed. The RAF20 value range quoted in the reference
(42.07 to 56.43 m) was read once from fr_ign_RAF20.tif (PROJ-data 1.25.0) with tifffile outside this
script; it is not recomputed here.
"""

import math
from fractions import Fraction as F

checks = 0
D2R = math.pi / 180.0
MAS = D2R / 3600.0 / 1000.0          # milliarc-second in radians


def ellipsoid(a, inv_f):
    f = 1.0 / inv_f
    e2 = f * (2.0 - f)
    return {"a": a, "f": f, "e2": e2, "b": a * (1.0 - f)}


GRS80 = ellipsoid(6378137.0, 298.257222101)       # EPSG 7019 (PROJ 9.9.0 ellipsoid.sql L23)
WGS84 = ellipsoid(6378137.0, 298.257223563)       # EPSG 7030 (ellipsoid.sql L32)
WGS84_IOGP = ellipsoid(6378137.0, 298.2572236)    # rounded value printed in IOGP 7-2 examples


def nu(e, phi):
    """Prime-vertical radius of curvature (IOGP 1.1)."""
    return e["a"] / math.sqrt(1.0 - e["e2"] * math.sin(phi) ** 2)


def rho(e, phi):
    """Meridian radius of curvature (IOGP 1.1)."""
    return e["a"] * (1.0 - e["e2"]) / (1.0 - e["e2"] * math.sin(phi) ** 2) ** 1.5


def geodetic_to_ecef(e, lat, lon, h):
    p, l = lat * D2R, lon * D2R
    n = nu(e, p)
    return ((n + h) * math.cos(p) * math.cos(l),
            (n + h) * math.cos(p) * math.sin(l),
            ((1.0 - e["e2"]) * n + h) * math.sin(p))


def ecef_to_geodetic(e, X, Y, Z):
    """Non-iterative reverse of IOGP 4.1.1 (Bowring form)."""
    eps = e["e2"] / (1.0 - e["e2"])
    p = math.hypot(X, Y)
    q = math.atan2(Z * e["a"], p * e["b"])
    phi = math.atan2(Z + eps * e["b"] * math.sin(q) ** 3, p - e["e2"] * e["a"] * math.cos(q) ** 3)
    lam = math.atan2(Y, X)
    return phi / D2R, lam / D2R, p / math.cos(phi) - nu(e, phi)


def enu_matrix(lat0, lon0):
    p, l = lat0 * D2R, lon0 * D2R
    return ((-math.sin(l), math.cos(l), 0.0),
            (-math.sin(p) * math.cos(l), -math.sin(p) * math.sin(l), math.cos(p)),
            (math.cos(p) * math.cos(l), math.cos(p) * math.sin(l), math.sin(p)))


def ecef_to_enu(e, P, O):
    """IOGP 4.1.2: rotate the ECEF difference into East, North, Up at the origin O."""
    lat0, lon0, _ = ecef_to_geodetic(e, *O)
    R = enu_matrix(lat0, lon0)
    d = [P[i] - O[i] for i in range(3)]
    return tuple(sum(R[r][c] * d[c] for c in range(3)) for r in range(3))


def dms(d, m, s):
    return d + m / 60.0 + s / 3600.0


def close(x, y, tol):
    return abs(x - y) <= tol


# --- Ellipsoids ------------------------------------------------------------------------------
# Check 1: GRS80 and WGS84 share a; their semi-minor axes differ by about 0.105 mm.
assert close((WGS84["b"] - GRS80["b"]) * 1000.0, 0.1048, 5e-4)
assert close(GRS80["e2"], 0.00669438002290, 1e-14) and close(WGS84["e2"], 0.00669437999014, 1e-14)
checks += 1

# --- Cited examples reproduced (validation of the implementation) ----------------------------
# Check 2: IOGP 7-2 section 4.1.1 reverse example: 53 deg 48'33.820"N, 2 deg 07'46.380"E, h = 73.0 m.
lat, lon, h = ecef_to_geodetic(WGS84_IOGP, 3771793.968, 140253.342, 5124304.349)
assert close((lat - 53 - 48 / 60) * 3600, 33.820, 5e-4) and close((lon - 2 - 7 / 60) * 3600, 46.380, 5e-4)
assert close(h, 73.0, 5e-4)
checks += 1

# Check 3: PROJ 9.9.0 cart.rst example (GRS80 default): 17.7562015132 E, 45.3935192042 N,
# 133.12 m -> 4272922.1553, 1368283.0597, 4518261.3501 m; the round trip closes below 1 micrometre.
X = geodetic_to_ecef(GRS80, 45.3935192042, 17.7562015132, 133.12)
assert all(close(a, b, 1e-4) for a, b in zip(X, (4272922.1553, 1368283.0597, 4518261.3501)))
back = ecef_to_geodetic(GRS80, *X)
assert close(back[0], 45.3935192042, 1e-11) and close(back[1], 17.7562015132, 1e-11) and close(back[2], 133.12, 1e-6)
checks += 1

# Check 4: IOGP 4.1.2 example (WGS 84) and PROJ topocentric.rst example (GRS80 default):
# U = -189013.869, V = -128642.040, W = -4220.171 m, to the millimetre in both cases.
O_iogp = (3652755.3058, 319574.6799, 5201547.3536)
U, V, Wv = ecef_to_enu(WGS84_IOGP, (3771793.968, 140253.342, 5124304.349), O_iogp)
assert close(U, -189013.869, 1e-3) and close(V, -128642.040, 1e-3) and close(Wv, -4220.171, 1e-3)
P = geodetic_to_ecef(GRS80, dms(53, 48, 33.82), dms(2, 7, 46.38), 73.0)
O_proj = geodetic_to_ecef(GRS80, 55.0, 5.0, 200.0)
U2, V2, W2 = ecef_to_enu(GRS80, P, O_proj)
assert close(U2, -189013.869, 1e-3) and close(V2, -128642.040, 1e-3) and close(W2, -4220.171, 1e-3)
checks += 1

# Check 5: the W of that example is mostly Earth curvature: Delta h - d^2 / (2R) with
# d = 228.6 km and R = sqrt(rho nu) = 6385.4 km at the origin gives -4220.30 m, 0.13 m from
# the exact -4220.171 m.
d = math.hypot(U, V)
R55 = math.sqrt(rho(GRS80, 55 * D2R) * nu(GRS80, 55 * D2R))
w_approx = (73.0 - 200.0) - d * d / (2 * R55)
assert close(d, 228637.30, 0.01) and close(R55, 6385435.7, 0.1) and close(w_approx, -4220.30, 0.01)
assert abs(w_approx - Wv) < 0.2
checks += 1

# --- Worked example A (card 004): geodetic -> ECEF -> ENU -----------------------------------
# Constructed: block origin 48.000 N, 2.000 E, h0 = 150 m; checkpoint 48.010 N, 2.010 E, h = 160 m.
O = geodetic_to_ecef(GRS80, 48.0, 2.0, 150.0)
Pa = geodetic_to_ecef(GRS80, 48.01, 2.01, 160.0)
# Check 6: radii and ECEF coordinates.
assert close(nu(GRS80, 48 * D2R), 6389959.99, 0.01) and close(rho(GRS80, 48 * D2R), 6370736.21, 0.01)
assert all(close(a, b, 1e-3) for a, b in zip(O, (4273213.461, 149223.902, 4716987.802)))
assert all(close(a, b, 1e-3) for a, b in zip(Pa, (4272368.155, 149940.966, 4717739.189)))
checks += 1

# Check 7: ENU = (746.128, 1111.981, 9.859) m; Up is 0.141 m below the 10 m height difference,
# the drop d^2/(2R) over d = 1339.1 m with R = 6380.3 km, to 0.1 mm.
E_a, N_a, U_a = ecef_to_enu(GRS80, Pa, O)
assert close(E_a, 746.128, 1e-3) and close(N_a, 1111.981, 1e-3) and close(U_a, 9.859, 1e-3)
Rm48 = math.sqrt(rho(GRS80, 48 * D2R) * nu(GRS80, 48 * D2R))
drop = (E_a ** 2 + N_a ** 2) / (2 * Rm48)
assert close(Rm48, 6380340.9, 0.1) and close(drop, 0.1405, 1e-4) and close(10.0 - drop, U_a, 1e-4)
# Mental estimates of card 004: 0.01 deg of latitude ~ rho x 0.01 deg = 1.112 km; 0.01 deg of
# longitude ~ (nu + h) x 0.01 deg x cos 48 = 746.3 m, or 111.3 km x cos 48 / 100 = 744.7 m.
assert close(rho(GRS80, 48.005 * D2R) * 0.01 * D2R, 1111.9, 0.1)
assert close((nu(GRS80, 48 * D2R) + 155) * 0.01 * D2R * math.cos(48 * D2R), 746.3, 0.1)
assert close(111.3 * math.cos(48 * D2R) * 10, 744.7, 0.1)
checks += 1

# Check 8: the ECEF -> ENU matrix is a proper rotation (orthonormal, determinant +1).
Rm = enu_matrix(48.0, 2.0)
for i in range(3):
    for j in range(3):
        dot = sum(Rm[i][k] * Rm[j][k] for k in range(3))
        assert close(dot, 1.0 if i == j else 0.0, 1e-15)
det = (Rm[0][0] * (Rm[1][1] * Rm[2][2] - Rm[1][2] * Rm[2][1])
       - Rm[0][1] * (Rm[1][0] * Rm[2][2] - Rm[1][2] * Rm[2][0])
       + Rm[0][2] * (Rm[1][0] * Rm[2][1] - Rm[1][1] * Rm[2][0]))
assert close(det, 1.0, 1e-15)
checks += 1

# --- Worked example B (card 001): ellipsoidal height, altitude and the grid value ------------
# Constructed: RAF20 value zeta = 49.71 m at the site (inside the 42.07-56.43 m range of the grid),
# GCP altitude H = 195.61 m NGF-IGN69, flying height 120 m above the ground.
zeta, H_gcp, agl = F("49.71"), F("195.61"), F(120)
h_gcp = H_gcp + zeta                                  # IOGP 4.11.1: H = h - zeta
# Check 9: h = 245.32 m; mixing H with ellipsoidal camera heights inflates the apparent flying
# height to 169.71 m, a ratio of 1.414 (a 41 % focal change if self-calibration absorbs it).
assert h_gcp == F("245.32") and F("42.07") < zeta < F("56.43")
assert H_gcp - zeta == F("145.90")                    # the sign error quoted on the card
ratio = (agl + zeta) / agl
assert agl + zeta == F("169.71") and round(float(ratio), 3) == 1.414
checks += 1


# --- Lambert Conic Conformal (2SP), IOGP 3.1.1.1 ---------------------------------------------
def lcc_2sp(e, lat_f, lon_f, lat_1, lat_2, e_f, n_f):
    ec = math.sqrt(e["e2"])

    def m(p):
        return math.cos(p) / math.sqrt(1.0 - e["e2"] * math.sin(p) ** 2)

    def t(p):
        return math.tan(math.pi / 4 - p / 2) / ((1 - ec * math.sin(p)) / (1 + ec * math.sin(p))) ** (ec / 2)

    p1, p2, pf = lat_1 * D2R, lat_2 * D2R, lat_f * D2R
    n = (math.log(m(p1)) - math.log(m(p2))) / (math.log(t(p1)) - math.log(t(p2)))
    Fc = m(p1) / (n * t(p1) ** n)
    r_f = e["a"] * Fc * t(pf) ** n

    def forward(lat, lon):
        p = lat * D2R
        r = e["a"] * Fc * t(p) ** n
        theta = n * (lon - lon_f) * D2R
        k = n * r / (e["a"] * m(p))                     # Snyder eq. 14-16
        return e_f + r * math.sin(theta), n_f + r_f - r * math.cos(theta), k, theta / D2R

    return forward, n


# Check 10: IOGP 3.1.1.1 example (NAD27 / Texas South Central, Clarke 1866):
# E = 2963503.91 ftUS, N = 254759.80 ftUS, n = 0.48991263.
FTUS = 1200.0 / 3937.0
texas, n_tx = lcc_2sp(ellipsoid(6378206.4, 294.9786982), dms(27, 50, 0), -99.0,
                      dms(28, 23, 0), dms(30, 17, 0), 2000000.0 * FTUS, 0.0)
E_tx, N_tx, _, _ = texas(dms(28, 30, 0), -96.0)
assert close(E_tx / FTUS, 2963503.91, 0.01) and close(N_tx / FTUS, 254759.80, 0.01) and close(n_tx, 0.48991263, 1e-8)
checks += 1

# Lambert-93 (EPSG 18085): false origin 46 deg 30' N, 3 deg E; standard parallels 49 and 44 N;
# false easting 700000 m, false northing 6600000 m; GRS80.
l93, n93 = lcc_2sp(GRS80, 46.5, 3.0, 49.0, 44.0, 700000.0, 6600000.0)

# --- Worked example C (card 002): latitude/longitude swap ------------------------------------
# Check 11: Paris (48.8566 N, 2.3522 E) projects to (652469.02, 6862035.26); the swapped pair,
# read as 2.3522 N, 48.8566 E, projects to (6960803.48, 3114983.26), thousands of km away.
# (Same values as pyproj 3.8.0 / PROJ 9.8.1, executed once outside this script.)
E_ok, N_ok, k_paris, gam_paris = l93(48.8566, 2.3522)
E_sw, N_sw, _, _ = l93(2.3522, 48.8566)
assert close(E_ok, 652469.02, 0.01) and close(N_ok, 6862035.26, 0.01)
assert close(E_sw, 6960803.48, 0.01) and close(N_sw, 3114983.26, 0.01)
assert math.hypot(E_sw - E_ok, N_sw - N_ok) > 7.0e6
checks += 1


def fit_similarity(src, dst, reflect=False):
    """Least-squares 2-D similarity dst ~ a * z + b (complex form); reflect uses conj(z)."""
    zs = [complex(x, y).conjugate() if reflect else complex(x, y) for x, y in src]
    zd = [complex(x, y) for x, y in dst]
    ms, md = sum(zs) / len(zs), sum(zd) / len(zd)
    a = sum((d_ - md) * (s - ms).conjugate() for s, d_ in zip(zs, zd)) / sum(abs(s - ms) ** 2 for s in zs)
    res = [abs(a * (s - ms) + md - d_) for s, d_ in zip(zs, zd)]
    return math.sqrt(sum(r * r for r in res) / len(res))


# Check 12: four GCPs on a ~1 km square around Paris. The swap maps the block through a matrix with
# negative determinant (a mirror) and anisotropic scale, so the best proper similarity leaves
# residuals of 1151 m RMS; even a mirrored similarity leaves 233 m, because the two axes are also
# scaled differently (about 1/cos(48.86 deg) = 1.52 against 1.00).
gcps = [(48.8566 + dy, 2.3522 + dx) for dy in (-0.0045, 0.0045) for dx in (-0.0068, 0.0068)]
good = [l93(la, lo)[:2] for la, lo in gcps]
swapped = [l93(lo, la)[:2] for la, lo in gcps]
rms_proper = fit_similarity(good, swapped)
rms_mirror = fit_similarity(good, swapped, reflect=True)
assert close(rms_proper, 1151.0, 1.0) and close(rms_mirror, 232.6, 1.0)
# Local Jacobian of the swap, finite differences in metres: det < 0 and axis stretch ~1.5.
eps = 1e-4
e0 = l93(2.3522, 48.8566)[:2]
dE = l93(2.3522 + eps, 48.8566)[:2]          # true eastward step (longitude) becomes a latitude step
dN = l93(2.3522, 48.8566 + eps)[:2]          # true northward step becomes a longitude step
tE = l93(48.8566, 2.3522 + eps)[:2]
tN = l93(48.8566 + eps, 2.3522)[:2]
len_true_E, len_true_N = math.dist(tE, l93(48.8566, 2.3522)[:2]), math.dist(tN, l93(48.8566, 2.3522)[:2])
cross = (dE[0] - e0[0]) * (dN[1] - e0[1]) - (dE[1] - e0[1]) * (dN[0] - e0[0])
stretch = (math.dist(dE, e0) / len_true_E) / (math.dist(dN, e0) / len_true_N)
assert cross < 0 and close(stretch, 1.0 / math.cos(48.8566 * D2R), 0.03)
checks += 1

# --- Worked example D (card 003): curvature and projection scale ------------------------------
# Check 13: curvature drop d^2/(2R), R = 6380.3 km (mean radius at 48 N): 0.078, 0.313, 1.96,
# 7.84 m at 1, 2, 5, 10 km.
drops = [x * x / (2 * Rm48) for x in (1000.0, 2000.0, 5000.0, 10000.0)]
assert [round(v, 3) for v in drops] == [0.078, 0.313, 1.959, 7.837]
checks += 1

# Check 14: Lambert-93 point scale factor: 0.999051 at 46.5 N (minimum near 46.52 N, -949 ppm,
# -95 cm per km); 0.999893 in Paris; 1.000598 in Marseille; 1.002244 in Dunkerque; 1.002940 in
# Bonifacio; exactly 1 on the standard parallels.
assert close(l93(46.5, 3.0)[2], 0.999051, 1e-6)
kmin, latmin = min((l93(44 + i / 1000, 3.0)[2], 44 + i / 1000) for i in range(5001))
assert close(kmin, 0.999051, 1e-6) and close(latmin, 46.52, 0.01)
assert close(k_paris, 0.999893, 1e-6) and close(l93(43.2965, 5.3698)[2], 1.000598, 1e-6)
assert close(l93(51.0344, 2.3768)[2], 1.002244, 1e-6) and close(l93(41.3871, 9.1594)[2], 1.002940, 1e-6)
assert close(l93(44.0, 1.0)[2], 1.0, 1e-12) and close(l93(49.0, 5.0)[2], 1.0, 1e-12)
checks += 1

# Check 15: meridian convergence gamma = n (lambda - 3 deg), n = 0.725608: -0.47 deg in Paris,
# -5.43 deg in Brest, +3.45 deg in Strasbourg.
assert close(n93, 0.725608, 1e-6) and close(gam_paris, -0.470, 1e-3)
assert close(l93(48.3904, -4.4861)[3], -5.432, 1e-3) and close(l93(48.5734, 7.7521)[3], 3.448, 1e-3)
checks += 1

# Check 16: consequences at k = 0.999051 for a calibrated camera with f = 4000 px in a block
# adjusted with Lambert-93 planimetry and true heights: a free focal length absorbs f/k, +3.80 px;
# with f fixed, the radial misfit at r = 2000 px is 1.90 px. Height reduction at h = 1000 m:
# (R + h)/R - 1 = 157 ppm.
k_c = l93(46.5, 3.0)[2]
assert close(4000.0 / k_c - 4000.0, 3.80, 0.005) and close(2000.0 * (1.0 / k_c - 1.0), 1.90, 0.005)
assert close(1000.0 / Rm48 * 1e6, 156.7, 0.1)
# Camera heights shifted by (1 - k) per km of flying height: 0.95 m; local-vertical tilt d/R at
# 2 km: 0.31 mrad.
assert close((1.0 - k_c) * 1000.0, 0.949, 1e-3) and close(2000.0 / Rm48 * 1000, 0.313, 1e-3)
checks += 1

# Check 17: UTM (spherical TM, k0 = 0.9996, R = 6371 km): scale 1 about 180 km from the central
# meridian; 1.00097 at the zone edge on the equator (3 deg, 333.6 km), Snyder's "1 part in 1,000".
R_s, k0 = 6371000.0, 0.9996
x_true = R_s * k0 * math.acosh(1.0 / k0)
B_edge = math.cos(0.0) * math.sin(3 * D2R)
k_edge = k0 / math.sqrt(1 - B_edge ** 2)
assert close(x_true / 1000.0, 180.1, 0.1) and close(k_edge, 1.00097, 1e-5)
checks += 1

# Check 18: nadir frame image, f = 100 mm, flying height 3000 m, ground point 2 km from nadir:
# curvature drop 0.314 m, image radius 66.7 mm, radial displacement r^3 Hf / (2 R f^2) = 7.0 um.
f_m, Hf, Dg = 0.100, 3000.0, 2000.0
r_img = f_m * Dg / Hf
dr = r_img ** 3 * Hf / (2 * R_s * f_m ** 2)
assert close(Dg * Dg / (2 * R_s), 0.314, 1e-3) and close(r_img * 1000, 66.67, 0.01) and close(dr * 1e6, 6.98, 0.01)
assert close(dr, r_img * (Dg * Dg / (2 * R_s)) / Hf, 1e-12)
checks += 1


# --- Time-dependent Helmert (EUREF TN1 eq. 1; IOGP 4.2.5) --------------------------------------
def helmert(X, T_mm, D_ppb, R_mas, convention="position_vector"):
    s = 1.0 if convention == "position_vector" else -1.0
    rx, ry, rz = (s * r * MAS for r in R_mas)
    D = D_ppb * 1e-9
    x, y, z = X
    return (x + T_mm[0] / 1000 + D * x - rz * y + ry * z,
            y + T_mm[1] / 1000 + D * y + rz * x - rx * z,
            z + T_mm[2] / 1000 + D * z - ry * x + rx * y)


def at_epoch(p0, rate, t, t0):
    return [p + r * (t - t0) for p, r in zip(p0, rate)]


def itrf2020_to_etrf2000(X, t):
    """EPSG 10586 = EUREF TN1 Table 4 (ITRF2020 row), parameters at 2015.0 and rates."""
    T = at_epoch((53.8, 51.8, -82.2), (0.1, 0.0, -1.7), t, 2015.0)
    D = 2.25 + 0.11 * (t - 2015.0)
    R = at_epoch((2.106, 12.740, -20.592), (0.081, 0.490, -0.792), t, 2015.0)
    return helmert(X, T, D, R)


def itrf2020_to_etrf2020(X, t):
    """EUREF TN1 eq. 2 with Table 1: T = 0, rotation = rates x (t - 1989.0)."""
    return helmert(X, (0.0, 0.0, 0.0), 0.0, [r * (t - 1989.0) for r in (0.086, 0.519, -0.753)])


# Check 19: EUREF TN1 Appendix B (same station at 2010.0 and 2020.0): ITRF2020 -> ETRF2000 and
# ITRF2020 -> ETRF2020 reproduce the published coordinates within 0.1 mm.
cases = [
    (2010.0, (4027893.6750, 307045.9069, 4919475.1721), (4027894.0053, 307045.5939, 4919474.9083),
     (4027893.9585, 307045.5550, 4919474.9619)),
    (2020.0, (4027893.5389, 307046.0755, 4919475.2745), (4027894.0033, 307045.5889, 4919474.9047),
     (4027893.9574, 307045.5561, 4919474.9643)),
]
for t, Xi, X2000, X2020 in cases:
    assert all(close(a, b, 1e-4) for a, b in zip(itrf2020_to_etrf2000(Xi, t), X2000))
    assert all(close(a, b, 1e-4) for a, b in zip(itrf2020_to_etrf2020(Xi, t), X2020))
checks += 1

# Check 20: IOGP 4.2.5 coordinate-frame example (EPSG 6276, ITRF2008 -> GDA94 at 2013.90) is
# reproduced to the millimetre with the coordinate-frame sign convention.
T = at_epoch((-84.68, -19.42, 32.01), (1.42, 1.34, 0.90), 2013.90, 1994.0)
Rr = at_epoch((-0.4254, 2.2578, 2.4015), (1.5461, 1.1820, 1.1551), 2013.90, 1994.0)
D = (0.00971 + 0.000109 * (2013.90 - 1994.0)) * 1000.0                   # ppm -> ppb
gda = helmert((-3789470.710, 4841770.404, -1690893.952), T, D, Rr, convention="coordinate_frame")
assert all(close(a, b, 1e-3) for a, b in zip(gda, (-3789470.004, 4841770.686, -1690895.108)))
checks += 1

# --- Worked example E (card 005): epoch and frame mismatch -----------------------------------
# Constructed point: the block origin of example A (48.0 N, 2.0 E, h = 150 m), PPP control in
# ITRF2020 at epoch 2026.87 (16 November 2026), national frame RGF93 v2b = ETRF2000.
t_c = 2026.87
Xe = itrf2020_to_etrf2000(O, t_c)
dE_, dN_, dU_ = ecef_to_enu(GRS80, Xe, O)              # ETRF2000 minus ITRF2020, in the local frame
# Check 21: ETRF2000 - ITRF2020 = (-0.657 E, -0.680 N, -0.017 U) m: ITRF2020 coordinates lie
# 0.945 m to the north-east (azimuth 44 deg) of the RGF93 v2b ones; at 2019.0 the gap was 0.752 m.
assert close(dE_, -0.657, 1e-3) and close(dN_, -0.680, 1e-3) and close(dU_, -0.017, 1e-3)
assert close(math.hypot(dE_, dN_), 0.945, 1e-3) and close(math.atan2(-dE_, -dN_) / D2R, 44.0, 0.5)
dE19, dN19, _ = ecef_to_enu(GRS80, itrf2020_to_etrf2000(O, 2019.0), O)
assert close(math.hypot(dE19, dN19), 0.752, 1e-3)
checks += 1

# Check 22: plate velocity at the point in ITRF2020 (Eurasia rotation of ETRF2020, v = -R_dot x X):
# 1.80 cm/yr east, 1.59 cm/yr north, 2.40 cm/yr horizontal. Velocity x (t - 1989.0) = 0.91 m;
# the wrong elapsed time (t - 2019.0) gives 0.19 m.
w = [-r * MAS for r in (0.086, 0.519, -0.753)]
x, y, z = O
v = (w[1] * z - w[2] * y, w[2] * x - w[0] * z, w[0] * y - w[1] * x)
vE, vN, vU = ecef_to_enu(GRS80, tuple(O[i] + v[i] for i in range(3)), O)
speed = math.hypot(vE, vN)
assert close(vE, 0.0180, 1e-4) and close(vN, 0.0159, 1e-4) and abs(vU) < 1e-4 and close(speed, 0.0240, 1e-4)
assert close(speed * (t_c - 1989.0), 0.91, 0.005) and close(speed * (t_c - 2019.0), 0.19, 0.005)
# The TN1 velocity identity v_ITRF - v_ETRF = -R_dot x X holds for the Appendix B station:
xb, yb, zb = cases[0][1]
vb = (w[1] * zb - w[2] * yb, w[2] * xb - w[0] * zb, w[0] * yb - w[1] * xb)
assert all(close(a, b, 1e-4) for a, b in zip(vb, (-0.01361 + 0.00011, 0.01686 - 0.00011, 0.01024 - 0.00024)))
checks += 1

# --- Supporting numbers of the reference ------------------------------------------------------
# Check 23: CC46 (EPSG 18105: false origin 46 N, 3 E, standard parallels 45.25 and 46.75 N): the
# scale error is -8.5 cm/km at 46 N, the low end of the EPSG remark "between -9 and +7 cm/km".
cc46, _ = lcc_2sp(GRS80, 46.0, 3.0, 45.25, 46.75, 1700000.0, 5200000.0)
k46 = cc46(46.0, 3.0)[2]
assert close((k46 - 1.0) * 1e5, -8.54, 0.01) and close(cc46(45.25, 3.0)[2], 1.0, 1e-12)
checks += 1


# Check 24: float32 spacing. ECEF coordinates near 4.27e6 m are representable only every 0.5 m in
# IEEE 754 single precision; ENU coordinates between 8192 and 16384 m every 0.98 mm.
def f32_spacing(value):
    import struct
    bits = struct.unpack("<I", struct.pack("<f", value))[0]
    lo = struct.unpack("<f", struct.pack("<I", bits))[0]
    return struct.unpack("<f", struct.pack("<I", bits + 1))[0] - lo


assert f32_spacing(O[0]) == 0.5 and close(f32_spacing(10000.0) * 1000, 0.977, 1e-3)
checks += 1

# Check 25: unit sizes at the Earth's surface (R = 6371 km): 1 mas -> 3.09 cm, 1 ppb -> 6.4 mm.
# The z rotation of ITRF2020 -> ETRF2000 at 2026.87 is -29.99 mas; at 48 N it alone moves a point
# by 0.62 m, most of the 0.945 m of check 21.
assert close(MAS * R_s * 100, 3.09, 0.005) and close(1e-9 * R_s * 1000, 6.37, 0.005)
rz_t = -20.592 - 0.792 * (t_c - 2015.0)
assert close(rz_t, -29.99, 0.01) and close(abs(rz_t) * MAS * R_s * math.cos(48 * D2R), 0.62, 0.01)
checks += 1

print(f"153-systemes-reference (CV-GEODESIE): {checks} checks passed")
