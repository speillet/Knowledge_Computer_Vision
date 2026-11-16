"""Recompute the constructed examples of CV-COLINEARITE (reference 151-colinearite-autocalibration).

Stdlib only. Run with:
python3 -I docs/revues/2026-11-16-photogrammetry/checks/151-colinearite-autocalibration.py

Conventions (those of the reference note):
- OpenCV 4.13 camera: X_c = R_cv X_w + t, x right, y down, z forward; pixel model
  u = f_x x'' + c_x with x'' the distorted normalized coordinate (calib3d.hpp L225-L262).
- Photogrammetric image frame: x right, y up, z backwards (towards the viewer), principal
  distance c > 0, image coordinates in mm relative to the principal point. R_ph maps
  image-frame vectors to object space (its columns are the image axes in object space), so
  p = R_ph^T (X - X0) and the ideal image point is x_u = -c p_x / p_z, y_u = -c p_y / p_z
  (form of Hastedt and Luhmann 2015, eq. 1, with Delta x' added to the projection).
- Angles: R_ph = Rx(omega) Ry(phi) Rz(kappa) with counter-clockwise (active) elementary
  rotations; the MicMac OriExport matrix appends diag(1, -1, -1) (DocMicMac section 14.3.6).
- Additional parameters in the distortion direction (ideal -> observed), in mm:
  dx = x_u (A1 r^2 + A2 r^4) + B1 (r^2 + 2 x_u^2) + 2 B2 x_u y_u,
  dy = y_u (A1 r^2 + A2 r^4) + B2 (r^2 + 2 y_u^2) + 2 B1 x_u y_u.
Every constructed number of the note and the cards is asserted below. No photogrammetric
software is executed; section D is a constructed first-order covariance study (numerical
Jacobian, normal equations, Schur elimination of the object points, minimal datum).
"""

from fractions import Fraction as F
from math import asin, atan2, cos, radians, sin, sqrt

checks = 0


def check(cond, label):
    global checks
    assert cond, label
    checks += 1


# ---------------------------------------------------------------- small linear algebra
def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
            for i in range(len(a))]


def transpose(a):
    return [list(r) for r in zip(*a)]


def matvec(a, v):
    return [sum(a[i][k] * v[k] for k in range(len(v))) for i in range(len(a))]


def inverse(m):
    """Gauss-Jordan with partial pivoting; returns (inverse, smallest |pivot|)."""
    n = len(m)
    a = [list(r) + [1.0 if i == j else 0.0 for j in range(n)] for i, r in enumerate(m)]
    piv_min = float("inf")
    for col in range(n):
        p = max(range(col, n), key=lambda r: abs(a[r][col]))
        a[col], a[p] = a[p], a[col]
        piv = a[col][col]
        piv_min = min(piv_min, abs(piv))
        if piv == 0:
            return None, 0.0
        a[col] = [x / piv for x in a[col]]
        for r in range(n):
            if r != col and a[r][col] != 0:
                f = a[r][col]
                a[r] = [x - f * y for x, y in zip(a[r], a[col])]
    return [r[n:] for r in a], piv_min


def rx(w):
    return [[1, 0, 0], [0, cos(w), -sin(w)], [0, sin(w), cos(w)]]


def ry(p):
    return [[cos(p), 0, sin(p)], [0, 1, 0], [-sin(p), 0, cos(p)]]


def rz(k):
    return [[cos(k), -sin(k), 0], [sin(k), cos(k), 0], [0, 0, 1]]


def r_opk(w, p, k):
    return matmul(matmul(rx(w), ry(p)), rz(k))


def opk_from_r(r):
    """Inverse of r_opk for |phi| < 90 deg: R[0][2] = sin(phi)."""
    return atan2(-r[1][2], r[2][2]), asin(r[0][2]), atan2(-r[0][1], r[0][0])


D = [[1, 0, 0], [0, -1, 0], [0, 0, -1]]   # OpenCV camera axes <-> photogrammetric image axes

# =============================================================== A. OpenCV -> photogrammetry
# Constructed camera: 6000 x 4000 px, pixel pitch 4.0 um (24 x 16 mm format).
W, H = 6000, 4000
PIX = F(4, 1000)                                  # mm per pixel
FX = FY = F(6000)
CX, CY = F(30105, 10), F(19855, 10)               # 3010.5, 1985.5 px
K1, K2, P1, P2 = F(-6, 100), F(2, 100), F(4, 10000), F(-3, 10000)

c_mm = FX * PIX
check(c_mm == 24, "A1: c = 6000 px x 0.004 mm = 24.000 mm")

centre_u, centre_v = F(W - 1, 2), F(H - 1, 2)     # OpenCV init (calibration.cpp L80-L81)
x0 = (CX - centre_u) * PIX
y0 = -(CY - centre_v) * PIX
check((x0, y0) == (F(44, 1000), F(56, 1000)), "A2: x'0 = +0.044 mm, y'0 = +0.056 mm")
x0_half = (CX - F(W, 2)) * PIX                    # Hastedt and Luhmann Table 1: 0.5 x size
y0_half = (-CY + F(H, 2)) * PIX
check((x0_half, y0_half) == (F(42, 1000), F(58, 1000)) and x0 - x0_half == F(2, 1000),
      "A3: the w/2 convention moves the principal point by half a pixel (2 um)")

A1, A2 = K1 / c_mm ** 2, K2 / c_mm ** 4
B1, B2 = P2 / c_mm, -P1 / c_mm                    # project derivation, checked numerically in A10
check(A1 == F(-6, 100) / 576 and round(float(A1), 8) == -1.0417e-4,
      "A4: A1 = k1 / c^2 = -0.06 / 576 = -1.04e-4 mm^-2")
check(round(float(A2), 11) == 6.028e-8 and round(float(B1), 9) == -1.25e-5
      and round(float(B2), 9) == -1.6667e-5, "A5: A2 = k2/c^4, B1 = p2/c, B2 = -p1/c")

# Nadir pose: OpenCV R = diag(1, -1, -1), centre C = (500, 300, 120) m.
R_cv_nadir = [[1, 0, 0], [0, -1, 0], [0, 0, -1]]
C_nadir = [500, 300, 120]
t_nadir = [-v for v in matvec(R_cv_nadir, C_nadir)]
check(t_nadir == [-500, 300, 120], "A6: t = -R C = (-500, 300, 120) m")
check([-v for v in matvec(transpose(R_cv_nadir), t_nadir)] == C_nadir,
      "A7: projection centre C = -R^T t = (500, 300, 120) m")
check(matmul(transpose(R_cv_nadir), D) == [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
      "A8: nadir camera: R_ph = R_cv^T diag(1,-1,-1) = I, omega = phi = kappa = 0")
check(opk_from_r([[1.0, 0, 0], [0, -1.0, 0], [0, 0, -1.0]])[0] in (radians(180), -radians(180)),
      "A8b: reading omega directly off R_cv gives 180 deg")


def project_opencv(Xw, R_cv, t, fx, fy, cx, cy, k1, k2, p1, p2):
    xc = [a + b for a, b in zip(matvec(R_cv, Xw), t)]
    xn, yn = xc[0] / xc[2], xc[1] / xc[2]
    r2 = xn * xn + yn * yn
    rad = 1 + k1 * r2 + k2 * r2 * r2
    xd = xn * rad + 2 * p1 * xn * yn + p2 * (r2 + 2 * xn * xn)
    yd = yn * rad + p1 * (r2 + 2 * yn * yn) + 2 * p2 * xn * yn
    return fx * xd + cx, fy * yd + cy


def project_photo(Xo, R_ph, C, c, x0_, y0_, a1, a2, b1, b2):
    p = matvec(transpose(R_ph), [a - b for a, b in zip(Xo, C)])
    xu, yu = -c * p[0] / p[2], -c * p[1] / p[2]
    r2 = xu * xu + yu * yu
    dx = xu * (a1 * r2 + a2 * r2 * r2) + b1 * (r2 + 2 * xu * xu) + 2 * b2 * xu * yu
    dy = yu * (a1 * r2 + a2 * r2 * r2) + b2 * (r2 + 2 * yu * yu) + 2 * b1 * xu * yu
    return x0_ + xu + dx, y0_ + yu + dy


# Tilted pose (omega, phi, kappa) = (2, -3, 30) deg, same centre, object points in metres.
om, ph, ka = radians(2), radians(-3), radians(30)
R_ph = r_opk(om, ph, ka)
R_cv = matmul(D, transpose(R_ph))                  # inverse relation of A8
t_cv = [-v for v in matvec(R_cv, C_nadir)]
check(all(abs(a - b) < 1e-12 for a, b in zip(opk_from_r(matmul(transpose(R_cv), D)),
                                             (om, ph, ka))),
      "A9: omega, phi, kappa recovered from R_ph = R_cv^T D")
fl = {k: float(v) for k, v in dict(fx=FX, fy=FY, cx=CX, cy=CY, k1=K1, k2=K2, p1=P1, p2=P2).items()}
max_err = 0.0
for Xw in ([520.0, 310.0, 5.0], [470.0, 285.0, 0.0], [540.0, 330.0, 12.0], [505.0, 255.0, 2.0]):
    u, v = project_opencv(Xw, R_cv, t_cv, **fl)
    xm, ym = project_photo(Xw, R_ph, C_nadir, float(c_mm), float(x0), float(y0),
                           float(A1), float(A2), float(B1), float(B2))
    u2 = float(centre_u) + xm / float(PIX)         # mm -> OpenCV pixels, y axis flipped
    v2 = float(centre_v) - ym / float(PIX)
    max_err = max(max_err, abs(u - u2), abs(v - v2))
check(max_err < 1e-8, "A10: OpenCV and converted photogrammetric models give the same pixels")

# Metashape 2.2 (Appendix D): u = w/2 + cx + x' f + x' B1 + y' B2, top-left pixel centre (0.5, 0.5),
# x' = x(...) + (P1 (r^2 + 2x^2) + 2 P2 x y): its P1 multiplies OpenCV's p2 term.
cx_ms, cy_ms = CX - centre_u, CY - centre_v
check((cx_ms, cy_ms) == (11, -14), "A11: Metashape cx, cy = +11, -14 px from the centre")


def project_metashape(Xw, R_cv_, t, f, cx, cy, k1, k2, P1m, P2m):
    xc = [a + b for a, b in zip(matvec(R_cv_, Xw), t)]
    x, y = xc[0] / xc[2], xc[1] / xc[2]
    r2 = x * x + y * y
    rad = 1 + k1 * r2 + k2 * r2 * r2
    xd = x * rad + (P1m * (r2 + 2 * x * x) + 2 * P2m * x * y)
    yd = y * rad + (P2m * (r2 + 2 * y * y) + 2 * P1m * x * y)
    return W * 0.5 + cx + xd * f, H * 0.5 + cy + yd * f


u, v = project_opencv([520.0, 310.0, 5.0], R_cv, t_cv, **fl)
um, vm = project_metashape([520.0, 310.0, 5.0], R_cv, t_cv, 6000.0, float(cx_ms), float(cy_ms),
                           fl["k1"], fl["k2"], fl["p2"], fl["p1"])
check(abs((um - 0.5) - u) < 1e-8 and abs((vm - 0.5) - v) < 1e-8,
      "A12: Metashape P1 = OpenCV p2, P2 = OpenCV p1; u_Metashape = u_OpenCV + 0.5")

# Direction: a correction model (measured -> ideal) has, to first order, the opposite sign.
r = F(12)
dist = A1 * r ** 3
check(dist == F(-18, 100) and dist / PIX == -45, "A13: A1 r^3 = -0.180 mm = -45 px at r = 12 mm")
check(2 * dist == F(-36, 100), "A14: a coefficient used in the wrong direction leaves -0.360 mm")

# MicMac OriExport example (DocMicMac 14.3.6, p. 256-257): R = Rx Ry Rz diag(1,-1,-1).
Rm = matmul(r_opk(radians(-5.819826), radians(-7.058795), radians(-12.262634)), D)
L = [[0.969777798578237427, -0.210783330505758815, 0.122887790140630643],
     [-0.199121821850641506, -0.974794184828703614, -0.100631989382226852],
     [0.141001849092942777, 0.0731210284736428379, -0.987305319416100224]]
check(max(abs(Rm[i][j] - L[i][j]) for i in range(3) for j in range(3)) < 1e-7,
      "A15: MicMac omega-phi-kappa example reproduced to 1e-7")
RmT = transpose(Rm)
check(max(abs(RmT[i][j] - L[i][j]) for i in range(3) for j in range(3)) > 0.1,
      "A16: the transposed (opposite-direction) reading of the same angles differs by > 0.1")

# =============================================================== B. c versus depth scale
c0, Hd, dX = F(24), F(2000), F(500)
k = F(101, 100)
check(c0 * dX / Hd == 6 and (k * c0) * dX / (k * Hd) == 6,
      "B1: (24 mm, 2000 mm) and (24.24 mm, 2020 mm) both give x = 6.000 mm")
Zr = F(400)
check(c0 * dX / (Hd - Zr) == F(15, 2), "B2: a point 400 mm in front of the wall images at 7.5 mm")
check((k * c0) * dX / (k * Hd - k * Zr) == F(15, 2),
      "B3: free relief stretched to 404 mm: same 7.5 mm")
dxk = (k * c0) * dX / (k * Hd - Zr) - F(15, 2)
check(round(float(dxk) * 1000, 1) == -18.5 and round(float(dxk / PIX), 2) == -4.63,
      "B4: relief known to be 400 mm: -18.5 um = -4.63 px at 4 um")

# Exact invariance for any parallel-axis network with rolls and varied distances, free points:
# (c, Z0_i, Z_j) -> (k c, k Z0_i, k Z_j), X and Y unchanged. Rational rotations about the common
# axis (Pythagorean triples) keep the test exact.
rolls = [((1, 0), 1), ((3, 4), 5), ((0, 1), 1), ((-5, 12), 13)]
cams = [(F(-300), F(50), F(1800)), (F(200), F(-100), F(2100)), (F(600), F(400), F(1500)),
        (F(0), F(0), F(2600))]
pts = [(F(100), F(200), F(0)), (F(-250), F(80), F(300)), (F(400), F(-150), F(-120)),
       (F(30), F(30), F(650))]


def img_parallel(c, cam, roll, P, kz=F(1)):
    (cr, sr), n = roll
    cr, sr = F(cr, n), F(sr, n)
    dx, dy, dz = P[0] - cam[0], P[1] - cam[1], kz * P[2] - kz * cam[2]
    px, py = cr * dx + sr * dy, -sr * dx + cr * dy
    return -c * px / dz, -c * py / dz


check(all(img_parallel(c0, cm, rl, P) == img_parallel(k * c0, cm, rl, P, kz=k)
          for cm, rl in zip(cams, rolls) for P in pts),
      "B5: parallel axes with rolls and varied distances: every image point is unchanged")

# B6: with camera heights observed (GNSS) up to a common offset b, c -> k c needs, for a flat
# object (Z = 0), b' = (k - 1) H_i + k b: one height admits it, two heights do not.
b_old = F(0)
b_new = {Hi: (k - 1) * Hi + k * b_old for Hi in (F(1800), F(2200))}
check(b_new[F(1800)] != b_new[F(2200)] and b_new[F(2200)] - b_new[F(1800)] == 4,
      "B6: observed heights 1800 and 2200 mm need offsets differing by 4 mm: c separable")

# ============================================ C. decentring as a shifted distortion centre
A1c, e, xr = -1e-4, 0.05, 15.0
exact = A1c * ((xr - e) ** 3 - xr ** 3)           # radial about x = e minus radial about 0
first_order = -A1c * e * (xr * xr + 2 * xr * xr)   # B1 (r^2 + 2 x^2) with B1 = -A1 e
check(abs(-A1c * e - 5e-6) < 1e-18, "C1: B1 = -A1 e = 5.0e-6 mm^-1")
check(round(exact * 1000, 3) == 3.364 and round(first_order * 1000, 3) == 3.375,
      "C2: 3.364 um exact versus 3.375 um to first order at x = 15 mm")

# ============================================ D. network study: precision and correlations
# Constructed. Flat array of 13 x 9 targets (100 mm spacing, Z = 0), camera c = 24 mm,
# 36 x 24 mm format, image sigma 0.6 um (0.1 px at 6 um). Unknowns: c, xp, yp, A1, A2, B1, B2,
# six exterior parameters per image (X0, Y0, Z0, local rotation increment) and, in the free
# network, the target coordinates. Datum: exterior orientation of image 0 and X0 of image 1
# held fixed (seven parameters).
TRUE_IO = [24.0, 0.05, -0.03, -1e-4, 3e-7, 1e-5, -8e-6]
STEPS_IO = [1e-4, 1e-4, 1e-4, 1e-9, 1e-12, 1e-8, 1e-8]
STEPS_EO = [1e-3, 1e-3, 1e-3, 1e-7, 1e-7, 1e-7]
TARGET = [(100.0 * i, 100.0 * j, 0.0) for i in range(13) for j in range(9)]
CENTRE = (600.0, 400.0, 0.0)
SIGMA = 0.0006                                   # mm
N_IO = 7


def unit(v):
    n = sqrt(sum(a * a for a in v))
    return [a / n for a in v]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def look_at(X0, roll_deg):
    z = unit([a - b for a, b in zip(X0, CENTRE)])           # image z points back to the camera
    x = unit(cross([0.0, 1.0, 0.0], z))
    y = cross(z, x)
    rr = radians(roll_deg)
    xr_ = [cos(rr) * a + sin(rr) * b for a, b in zip(x, y)]
    yr_ = [-sin(rr) * a + cos(rr) * b for a, b in zip(x, y)]
    return [[xr_[i], yr_[i], z[i]] for i in range(3)]        # columns = image axes


def observe(io, R0, eo, P):
    c, xp, yp, a1, a2, b1, b2 = io
    Rk = matmul(R0, r_opk(eo[3], eo[4], eo[5]))
    p = matvec(transpose(Rk), [P[i] - eo[i] for i in range(3)])
    xu, yu = -c * p[0] / p[2], -c * p[1] / p[2]
    r2 = xu * xu + yu * yu
    dx = xu * (a1 * r2 + a2 * r2 * r2) + b1 * (r2 + 2 * xu * xu) + 2 * b2 * xu * yu
    dy = yu * (a1 * r2 + a2 * r2 * r2) + b2 * (r2 + 2 * yu * yu) + 2 * b1 * xu * yu
    return xp + xu + dx, yp + yu + dy


def rows_for(stations, P, free):
    """Jacobian rows (camera part, point part) of the observations of target P."""
    nc = N_IO + 6 * len(stations)
    out = []
    for s, (X0, R0) in enumerate(stations):
        eo = list(X0) + [0.0, 0.0, 0.0]
        xu, yu = observe([TRUE_IO[0], 0, 0, 0, 0, 0, 0], R0, eo, P)
        if not (abs(xu) <= 17.0 and abs(yu) <= 11.0):
            continue
        gc = [[0.0] * nc, [0.0] * nc]
        gp = [[0.0] * 3, [0.0] * 3]
        for j in range(N_IO):
            hi, lo = list(TRUE_IO), list(TRUE_IO)
            hi[j] += STEPS_IO[j]
            lo[j] -= STEPS_IO[j]
            (a, b), (cc, d) = observe(hi, R0, eo, P), observe(lo, R0, eo, P)
            gc[0][j], gc[1][j] = (a - cc) / (2 * STEPS_IO[j]), (b - d) / (2 * STEPS_IO[j])
        for j in range(6):
            hi, lo = list(eo), list(eo)
            hi[j] += STEPS_EO[j]
            lo[j] -= STEPS_EO[j]
            (a, b), (cc, d) = observe(TRUE_IO, R0, hi, P), observe(TRUE_IO, R0, lo, P)
            col = N_IO + 6 * s + j
            gc[0][col], gc[1][col] = (a - cc) / (2 * STEPS_EO[j]), (b - d) / (2 * STEPS_EO[j])
        if free:
            for j in range(3):
                hi, lo = list(P), list(P)
                hi[j] += 1e-3
                lo[j] -= 1e-3
                (a, b), (cc, d) = observe(TRUE_IO, R0, eo, hi), observe(TRUE_IO, R0, eo, lo)
                gp[0][j], gp[1][j] = (a - cc) / 2e-3, (b - d) / 2e-3
        out.append((s, gc, gp))
    return out


def analyse(stations, free=True, datum=(0, 1)):
    """Reduced normal matrix of IO and EO after eliminating the points; minimal datum."""
    nc = N_IO + 6 * len(stations)
    S = [[0.0] * nc for _ in range(nc)]
    counts = [0] * len(stations)
    for P in TARGET:
        Npp = [[0.0] * 3 for _ in range(3)]
        Ncp = [[0.0] * 3 for _ in range(nc)]
        for s, gc, gp in rows_for(stations, P, free):
            counts[s] += 1
            for rr_ in range(2):
                nz = [i for i in range(nc) if gc[rr_][i] != 0.0]
                for i in nz:
                    for kk in nz:
                        S[i][kk] += gc[rr_][i] * gc[rr_][kk]
                    for kk in range(3):
                        Ncp[i][kk] += gc[rr_][i] * gp[rr_][kk]
                for i in range(3):
                    for kk in range(3):
                        Npp[i][kk] += gp[rr_][i] * gp[rr_][kk]
        if free:
            Ninv, _ = inverse(Npp)
            T = matmul(Ncp, Ninv)
            for i in range(nc):
                if any(Ncp[i]):
                    for kk in range(nc):
                        S[i][kk] -= sum(T[i][m] * Ncp[kk][m] for m in range(3))
    if free:
        a, b = datum
        drop = set(range(N_IO + 6 * a, N_IO + 6 * a + 6)) | {N_IO + 6 * b}
    else:
        drop = set()
    keep = [i for i in range(nc) if i not in drop]
    Sr = [[S[i][kk] for kk in keep] for i in keep]
    sc = [1 / sqrt(Sr[i][i]) for i in range(len(Sr))]
    Ss = [[Sr[i][kk] * sc[i] * sc[kk] for kk in range(len(Sr))] for i in range(len(Sr))]
    Q, piv = inverse(Ss)
    return dict(keep=keep, Q=Q, sc=sc, piv=piv, counts=counts)


def stat(res, name):
    keep, Q, sc = res["keep"], res["Q"], res["sc"]
    pos = {p: i for i, p in enumerate(keep)}

    def corr(a, b):
        return Q[pos[a]][pos[b]] / sqrt(Q[pos[a]][pos[a]] * Q[pos[b]][pos[b]])

    eo = [p for p in keep if p >= N_IO]
    i = {"c": 0, "xp": 1}[name]
    return dict(sigma_um=1000 * SIGMA * sc[pos[i]] * sqrt(Q[pos[i]][pos[i]]),
                max_eo=max(abs(corr(i, p)) for p in eo),
                r_b1=corr(1, 5))


def cone(tilt_deg, roll_cycle):
    tilt, dist = radians(tilt_deg), 1300.0
    out = []
    for i in range(8):
        a = radians(45.0 * i)
        X0 = (CENTRE[0] + dist * sin(tilt) * cos(a), CENTRE[1] + dist * sin(tilt) * sin(a),
              dist * cos(tilt))
        out.append((X0, look_at(X0, 90.0 * (i % 4) if roll_cycle else 0.0)))
    return out


# D1: parallel axes (nadir), heights alternating 1300 and 1400 mm, with and without rolls.
I3 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
par_pos = [(CENTRE[0] + 150 * cos(radians(45 * i)), CENTRE[1] + 100 * sin(radians(45 * i)),
            1300.0 + 100.0 * (i % 2)) for i in range(8)]
for rolled in (False, True):
    st = [(X0, matmul(I3, rz(radians(90.0 * (i % 4)))) if rolled else I3)
          for i, X0 in enumerate(par_pos)]
    res = analyse(st)
    check(min(res["counts"]) >= 60 and res["piv"] < 1e-9,
          f"D1: parallel network (rolls={rolled}): singular after a minimal datum")

# D2-D4: eight stations on a cone, 1300 mm from the centre, without and with 0/90/180/270 rolls.
study = {}
for tilt in (5.0, 15.0, 35.0):
    for rolled in (False, True):
        res = analyse(cone(tilt, rolled))
        check(min(res["counts"]) >= 40 and res["piv"] > 1e-6,
              f"D2: cone {tilt} deg (rolls={rolled}): >= 40 targets per image, invertible")
        study[(tilt, rolled)] = (stat(res, "c"), stat(res, "xp"))

c5, c15, c35 = (study[(t, False)][0]["sigma_um"] for t in (5.0, 15.0, 35.0))
check((round(c5, 1), round(c15, 2), round(c35, 2)) == (17.8, 2.69, 0.84),
      "D3: sigma(c) = 17.8, 2.69, 0.84 um at 5, 15, 35 deg convergence")
c15r = study[(15.0, True)][0]["sigma_um"]
check(round(c15r, 2) == 2.80 and c15r > c15, "D4: rolls do not reduce sigma(c) (2.80 um at 15 deg)")
xp_a, xp_b = study[(15.0, False)][1], study[(15.0, True)][1]
check((round(xp_a["sigma_um"], 1), round(xp_a["max_eo"], 3), round(xp_a["r_b1"], 2))
      == (15.2, 0.997, -0.05), "D5: no rolls: sigma(xp) 15.2 um, max |r(xp,EO)| 0.997, r(xp,B1) -0.05")
check((round(xp_b["sigma_um"], 2), round(xp_b["max_eo"], 2), round(xp_b["r_b1"], 2))
      == (1.0, 0.79, 0.82), "D6: rolls: sigma(xp) 1.00 um, max |r(xp,EO)| 0.79, r(xp,B1) +0.82")
check(round(xp_a["sigma_um"] / xp_b["sigma_um"]) == 15, "D7: rolls divide sigma(xp) by about 15")
xp35a, xp35b = study[(35.0, False)][1], study[(35.0, True)][1]
check((round(xp35a["sigma_um"], 1), round(xp35b["sigma_um"], 1), round(xp35b["r_b1"], 2))
      == (4.4, 1.0, 0.93), "D8: 35 deg: sigma(xp) 4.4 -> 1.0 um, r(xp,B1) +0.93 with rolls")

# D9: IO precision does not depend on which minimal datum is chosen (gauge invariance).
alt = stat(analyse(cone(15.0, True), datum=(3, 6)), "xp")
check(abs(alt["sigma_um"] - xp_b["sigma_um"]) < 1e-6 * xp_b["sigma_um"],
      "D9: same sigma(xp) with another minimal datum")

# D10: with the target coordinates held fixed (known target), rolls change sigma(xp) little.
kn_a = stat(analyse(cone(15.0, False), free=False), "xp")
kn_b = stat(analyse(cone(15.0, True), free=False), "xp")
check((round(kn_a["sigma_um"], 2), round(kn_b["sigma_um"], 2)) == (1.08, 0.99),
      "D10: known target: sigma(xp) 1.08 -> 0.99 um")

# =============================================== E. precision versus accuracy (card 005)
s_xyz = F(10, 1000)                                 # mm per coordinate
rel_prec = 2000 / (sqrt(3) * float(s_xyz))
check(round(rel_prec, -3) == 115000, "E1: 2 m / (sqrt(3) x 0.010 mm) = 1:115,000")
lme_theory = sqrt(18) * float(s_xyz)
check(round(lme_theory, 3) == 0.042, "E2: theoretical LME = sqrt(18) x 0.010 = 0.042 mm")
check(round(sqrt(2) * float(s_xyz), 3) == 0.014, "E3: sigma of a length ~ sqrt(2) x 0.010 = 0.014 mm")
Ls = [F(1500), F(1200), F(800), F(500)]
errs = [F(105, 1000), F(86, 1000), F(54, 1000), F(36, 1000)]
n = len(Ls)
mL, me = sum(Ls) / n, sum(errs) / n
slope = sum((a - mL) * (b - me) for a, b in zip(Ls, errs)) / sum((a - mL) ** 2 for a in Ls)
icpt = me - slope * mL
check(round(float(slope) * 1e6, 1) == 70.5 and round(float(icpt) * 1000, 2) == -0.27,
      "E4: least-squares slope 70.5 ppm, intercept -0.27 um")
check(max(errs) == F(105, 1000) and round(float(max(errs)) / lme_theory, 1) == 2.5,
      "E5: LME_max 0.105 mm is 2.5 times the precision-based expectation")
check(round(1 / (float(slope)), -2) == 14200, "E6: 70 ppm is a scale error of about 1:14,200")
resid = [float(b - (icpt + slope * a)) * 1000 for a, b in zip(Ls, errs)]
check(round(max(abs(x) for x in resid), 1) == 2.1, "E7: after the scale trend, residuals stay within 2.1 um")
# Cited values, Hastedt et al. 2018: eq. 2 and Table 5-6 (free network, set III, 28 m).
check((round(sqrt(18) * 5), round(sqrt(18) * 8)) == (21, 34), "E8: sqrt(18) x 5 and 8 um = 21, 34 um")
check(round(28000 / 0.0744, -3) == 376000, "E9: 28 m / 74.4 um = 1:376,000")
check(round(28000 / 2.27, -2) == 12300 and round(2.27 / 0.0744) == 31,
      "E10: LME 2.27 mm = 1:12,300, about 31 times the RMS precision")

# ======================================================= F. design numbers (card 004)
s_req = 0.05 / sqrt(18)
check(round(s_req, 4) == 0.0118, "F1: LME 0.05 mm needs s_XYZ <= 0.0118 mm")
check(12 * 2 * 4 == 96, "F2: 12 stations x 2 heights x 4 rolls = 96 images")
check(round(sqrt(8 / 4), 2) == 1.41, "F3: from 4 to 8 rays per point, precision gains sqrt(2)")
scale = F(2000) / F(24)
check(round(float(scale), 1) == 83.3 and F(36) * scale == 3000 and F(24) * scale == 2000,
      "F4: 24 mm at 2000 mm: scale 1:83.3, footprint 3000 x 2000 mm")

print("network study (constructed): sigma in um, max |r| with exterior parameters, r(xp,B1)")
for (tilt, rolled), (sc_, sx_) in sorted(study.items()):
    print(f"  cone {tilt:4.1f} deg rolls={str(rolled):5}: sigma(c) {sc_['sigma_um']:6.2f}"
          f"  max|r(c,EO)| {sc_['max_eo']:.3f}  sigma(xp) {sx_['sigma_um']:6.2f}"
          f"  max|r(xp,EO)| {sx_['max_eo']:.3f}  r(xp,B1) {sx_['r_b1']:+.2f}")
print(f"151-colinearite-autocalibration (CV-COLINEARITE): {checks} checks passed")
