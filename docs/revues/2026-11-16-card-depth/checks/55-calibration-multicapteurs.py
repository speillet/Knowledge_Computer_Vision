"""Recompute the constructed numbers added to CV-MULTICALIB-002 and to reference
55-calibration-multicapteurs (2026-11-16).

Stdlib only. Run with: python3 -I docs/revues/2026-11-16-card-depth/checks/55-calibration-multicapteurs.py
Rotation equation R_A R_X = R_X R_B and axis relation n_A = R_X n_B: Horaud and Dornaika
1995, Sec. 3, eq. 18. Translation equation (R_A - I) t_X = R_X t_B - t_A: reference,
"Observability".
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

def mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]

def T(A):
    return [[A[j][i] for j in range(3)] for i in range(3)]

def sub_eye(A):
    return [[A[i][j] - (1.0 if i == j else 0.0) for j in range(3)] for i in range(3)]

def close(A, B, tol=1e-12):
    return all(abs(A[i][j] - B[i][j]) < tol for i in range(3) for j in range(3))

def sym_eigvals(S, sweeps=60):
    """Jacobi eigenvalues of a symmetric 3 x 3 matrix."""
    A = [row[:] for row in S]
    for _ in range(sweeps):
        for p, q in ((0, 1), (0, 2), (1, 2)):
            if abs(A[p][q]) < 1e-15:
                continue
            th = 0.5 * math.atan2(2 * A[p][q], A[q][q] - A[p][p])
            c, s = math.cos(th), math.sin(th)
            for k in range(3):
                akp, akq = A[k][p], A[k][q]
                A[k][p], A[k][q] = c * akp - s * akq, s * akp + c * akq
            for k in range(3):
                apk, aqk = A[p][k], A[q][k]
                A[p][k], A[q][k] = c * apk - s * aqk, s * apk + c * aqk
    return sorted((A[i][i] for i in range(3)), reverse=True)

def stacked_singular_values(rotations):
    M = [[0.0] * 3 for _ in range(3)]
    for R in rotations:
        D = sub_eye(R)
        DtD = mul(T(D), D)
        M = [[M[i][j] + DtD[i][j] for j in range(3)] for i in range(3)]
    return [math.sqrt(max(e, 0.0)) for e in sym_eigvals(M)]

# 20 motions of 30 degrees about z: singular values 2.31, 2.31, 0 whatever the count.
for n in (3, 20, 200):
    sv = stacked_singular_values([rot((0, 0, 1), 30)] * n)
    assert abs(sv[0] - math.sqrt(n) * 2 * math.sin(math.radians(15))) < 1e-9 and sv[2] < 1e-9
sv20 = stacked_singular_values([rot((0, 0, 1), 30)] * 20)
assert [round(v, 2) for v in sv20] == [2.31, 2.31, 0.0]; checks += 1

# Same count, two motions replaced by 30 degree motions about x: 2.31, 2.20, 0.73.
sv_mix = stacked_singular_values([rot((0, 0, 1), 30)] * 18 + [rot((1, 0, 0), 30)] * 2)
assert [round(v, 2) for v in sv_mix] == [2.31, 2.20, 0.73]; checks += 1

# Rotation ambiguity: with parallel axes n_A, R_X' = Rot(n_A, phi) R_X satisfies every
# rotation equation R_A R_X' = R_X' R_B (project deduction from Horaud and Dornaika eq. 18).
R_X = rot((0.3, -0.5, 0.8), 40)
nA = (0.0, 0.0, 1.0)
for theta in (25, 40, 70):
    R_A = rot(nA, theta)
    R_B = mul(T(R_X), mul(R_A, R_X))          # consistent camera motion
    R_Xp = mul(rot(nA, 17), R_X)
    assert close(mul(R_A, R_Xp), mul(R_Xp, R_B), 1e-12)
checks += 1

# Translation: (R_A - I) n_A = 0, so t_X + lambda n_A satisfies the same equations.
for theta in (25, 40, 70):
    D = sub_eye(rot(nA, theta))
    v = [sum(D[i][k] * nA[k] for k in range(3)) for i in range(3)]
    assert max(abs(x) for x in v) < 1e-12
checks += 1

print(f"55-calibration-multicapteurs (CV-MULTICALIB-002): {checks} checks passed")
