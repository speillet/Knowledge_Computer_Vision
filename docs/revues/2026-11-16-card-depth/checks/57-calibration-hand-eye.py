"""Recompute the constructed numbers and the frame graph added to CV-HANDEYE-005 and
CV-HANDEYE-001 and to reference 57-calibration-hand-eye (2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/57-calibration-hand-eye.py
Convention: aTb maps coordinates in frame b to frame a (reference, "Convention").
Eye-in-hand: G_i X C_i = Y, A = G_j^-1 G_i, B = C_j C_i^-1 (OpenCV 4.13.0 calib3d.hpp
L2322-L2335, calibration_handeye.cpp L297-L304). Eye-to-hand: G_i^-1 X C_i = Y
(calib3d.hpp L2336-L2346).
"""
import math

checks = 0

def rot(axis, deg):
    x, y, z = axis
    n = math.sqrt(x * x + y * y + z * z); x, y, z = x / n, y / n, z / n
    t = math.radians(deg); c, s = math.cos(t), math.sin(t); C = 1 - c
    return [[c + x * x * C, x * y * C - z * s, x * z * C + y * s],
            [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
            [z * x * C - y * s, z * y * C + x * s, c + z * z * C]]

def H(R, t):
    return [R[0] + [t[0]], R[1] + [t[1]], R[2] + [t[2]], [0.0, 0.0, 0.0, 1.0]]

def mul(*Ms):
    out = Ms[0]
    for M in Ms[1:]:
        out = [[sum(out[i][k] * M[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
    return out

def inv(M):
    R = [[M[j][i] for j in range(3)] for i in range(3)]
    t = [-sum(R[i][k] * M[k][3] for k in range(3)) for i in range(3)]
    return H(R, t)

def apply(M, p):
    return [sum(M[i][k] * p[k] for k in range(3)) + M[i][3] for i in range(3)]

def close(A, B, tol=1e-9):
    return all(abs(A[i][j] - B[i][j]) < tol for i in range(4) for j in range(4))

# --- Eye-in-hand, the frame graph of the figure cv-handeye-loop.svg --------------------
X = H(rot((0.2, 1, 0.3), 25), [0.03, -0.05, 0.12])          # gTc, metres
Y = H(rot((1, -0.4, 0.2), 140), [0.6, 0.1, -0.2])           # bTt, fixed target
G = [H(rot((0.3, 0.5, 1), 30), [0.4, 0.0, 0.5]),
     H(rot((1, 0.2, -0.1), 70), [0.5, 0.2, 0.45]),
     H(rot((-0.4, 1, 0.5), 110), [0.3, -0.2, 0.6])]         # bTg_i
C = [mul(inv(X), inv(Gi), Y) for Gi in G]                   # c_iTt from G_i X C_i = Y
for i in range(3):
    assert close(mul(G[i], X, C[i]), Y)
for i in range(3):
    for j in range(3):
        if i == j:
            continue
        A = mul(inv(G[j]), G[i])                            # g_j T g_i
        B = mul(C[j], inv(C[i]))                            # c_j T c_i
        assert close(mul(A, X), mul(X, B))
        # A maps gripper-i coordinates of a point to gripper-j coordinates.
        p_b = [0.7, -0.3, 0.2]
        p_gi = apply(inv(G[i]), p_b); p_gj = apply(inv(G[j]), p_b)
        assert all(abs(a - b) < 1e-12 for a, b in zip(apply(A, p_gi), p_gj))
checks += 1

# --- Eye-to-hand: camera fixed in the base, target on the gripper ------------------------
Xe = H(rot((0.1, 1, -0.2), 160), [1.2, 0.3, 0.9])          # bTc, camera 1.5 m from the base
Ye = H(rot((1, 0, 0.3), 15), [0.0, 0.02, 0.10])            # gTt, target on the flange
Ce = [mul(inv(Xe), Gi, Ye) for Gi in G]                     # cTt_i from G_i Y = X C_i
for i in range(3):
    assert close(mul(inv(G[i]), Xe, Ce[i]), Ye)
for i in range(3):
    for j in range(3):
        if i == j:
            continue
        A_base = mul(G[j], inv(G[i]))                       # gripper motion in the base frame
        B = mul(Ce[j], inv(Ce[i]))
        assert close(mul(A_base, Xe), mul(Xe, B))
        # OpenCV's recipe: pass base->gripper in the gripper2base slots; its
        # inv(Hg[j]) * Hg[i] then equals G_j G_i^-1.
        Hg = [inv(Gk) for Gk in G]
        assert close(mul(inv(Hg[j]), Hg[i]), A_base)
        # The eye-in-hand form G_j^-1 G_i is a different matrix.
        assert not close(mul(inv(G[j]), G[i]), A_base, 1e-3)
checks += 1

# Inverting the eye-in-hand unknown does not give a constant camera->base transform:
# with a fixed camera, gTc_i = G_i^-1 Xe changes with the station.
assert not close(mul(inv(G[0]), Xe), mul(inv(G[1]), Xe), 1e-3); checks += 1

# --- Error signature in the task ----------------------------------------------------
# Translation error e = 2 mm along the camera x axis: X' = X E.
e = [0.002, 0.0, 0.0]
E = H(rot((0, 0, 1), 0), e)
# Eye-in-hand: two stations differing by a 90 degree roll about the tool z axis; the camera
# x axis is mapped by R_X into the tool frame, kept perpendicular to z here.
Xr = H(rot((0, 0, 1), 30), [0.0, 0.05, 0.10])
G1 = H(rot((0, 0, 1), 0), [0.5, 0.0, 0.4])
G2 = mul(G1, H(rot((0, 0, 1), 90), [0.0, 0.0, 0.0]))       # same flange position, wrist roll
P = [0.55, 0.08, 0.0]                                       # object fixed in the base
offsets = []
for Gk in (G1, G2):
    p_cam = apply(inv(mul(Gk, Xr)), P)
    est = apply(mul(Gk, Xr, E), p_cam)
    offsets.append([a - b for a, b in zip(est, P)])
assert all(abs(math.dist(o, (0, 0, 0)) - 0.002) < 1e-12 for o in offsets)
assert abs(math.dist(offsets[0], offsets[1]) - 0.002 * math.sqrt(2)) < 1e-12
assert round(1000 * math.dist(offsets[0], offsets[1]), 2) == 2.83
# Eye-to-hand: the detection maps through X alone, so the offset is the same at every station.
off_e = []
for Q in ([0.4, 0.1, 0.0], [0.6, -0.2, 0.05]):
    p_cam = apply(inv(Xe), Q)
    est = apply(mul(Xe, E), p_cam)
    off_e.append([a - b for a, b in zip(est, Q)])
assert math.dist(off_e[0], off_e[1]) < 1e-12 and abs(math.dist(off_e[0], (0, 0, 0)) - 0.002) < 1e-12
checks += 1

print(f"57-calibration-hand-eye (CV-HANDEYE-005, CV-HANDEYE-001 figure): {checks} checks passed")
