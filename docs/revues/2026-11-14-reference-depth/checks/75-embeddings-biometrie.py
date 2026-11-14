"""Recompute the constructed examples of CV-BIOMETRIE (reference 75-embeddings-biometrie).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/75-embeddings-biometrie.py
Inputs come from ArcFace (arXiv 1801.07698v4, Sec. III-A eq. 3, Sec. IV-A: s = 64, m = 0.5,
512-D, about 30 degrees at the end of training; Sec. IV-D: IJB-C impostor count),
OpenCV 4.13.0 samples/dnn/face_detect.py (thresholds 0.363 and 1.128), Mansfield and
Wayman 2002 (Rule of 3, Rule of 30, FAR and FRR formulas) and NIST FRTE 1:N (FPIR 0.003).
Gallery sizes, error rates and the independence assumptions are constructed.
"""

import math


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


checks = 0

# --- Example A: ArcFace margin geometry -------------------------------------------
S, M = 64.0, 0.5                        # feature scale and additive angular margin (rad)
theta = math.radians(30.0)
# Check: m = 0.5 rad is 28.65 degrees.
assert close(math.degrees(M), 28.648, 1e-3); checks += 1
# Check: at theta_y = 30 deg the target logit drops from 64 cos 30 = 55.43 to 64 cos(58.65 deg) = 33.30.
assert close(S * math.cos(theta), 55.426, 1e-3) and close(S * math.cos(theta + M), 33.299, 1e-3); checks += 1
# Check: class y beats class j only if cos(theta_y + m) > cos(theta_j), i.e. theta_j > theta_y + m
# (both angles in [0, pi]); at theta_y = 30 deg a competitor must be farther than 58.65 deg.
for theta_j_deg in (58.0, 59.0):
    wins = math.cos(theta + M) > math.cos(math.radians(theta_j_deg))
    assert wins == (math.radians(theta_j_deg) > theta + M)
checks += 1

# --- Example B: cosine and L2 thresholds on unit vectors ---------------------------
def l2_from_cos(c):
    return math.sqrt(2 - 2 * c)          # |a - b|^2 = 2 - 2 cos for unit vectors


# Check: OpenCV's sample thresholds are the same decision: cos 0.363 <-> L2 1.1287 (sample uses 1.128).
assert close(l2_from_cos(0.363), 1.12872, 1e-5) and abs(l2_from_cos(0.363) - 1.128) < 1e-3; checks += 1

# --- Example C: how many comparisons a target FMR needs ----------------------------
def n_zero_errors(p, conf=0.95):
    """Smallest n such that zero errors in n i.i.d. trials bounds the rate below p (one-sided)."""
    return math.ceil(math.log(1 - conf) / math.log(1 - p))


# Check: Rule of 3: 29,956 comparisons for 1e-4 and 2,995,731 for 1e-6 (about 3/p).
assert n_zero_errors(1e-4) == 29_956 and n_zero_errors(1e-6) == 2_995_731; checks += 1
# Check: zero errors on 1,000 comparisons only bounds the rate below 0.002991 (about 3/1000).
assert close(1 - 0.05 ** (1 / 1000), 0.002991, 1e-6); checks += 1
IJBC_IMPOSTORS = 15_639_000               # "15,639K impostor matches" (ArcFace Sec. IV-D)
expected = {fmr: IJBC_IMPOSTORS * fmr for fmr in (1e-4, 1e-5, 1e-6, 1e-8)}
# Check: at FMR 1e-5 about 156 false matches support the threshold, at 1e-6 about 16, at 1e-8 about 0.16.
assert close(expected[1e-5], 156.39, 1e-2) and close(expected[1e-6], 15.639, 1e-3) and close(expected[1e-8], 0.15639, 1e-5); checks += 1
# Check: Rule of 30 at FMR 1e-6 needs 30 errors, i.e. 30 million nonmated comparisons.
assert close(30 / 1e-6, 3.0e7, 1e-6); checks += 1
k = 2449
# Check: one image from each of 2,449 people already gives 2,997,576 nonmated pairs (k(k-1)/2),
# but each person appears in 2,448 of them: the pairs are not independent.
assert k * (k - 1) // 2 == 2_997_576 and k - 1 == 2448; checks += 1

# --- Example D: from 1:1 FMR to 1:N FPIR (independence approximation) --------------
def fpir(fmr, n):
    return 1 - (1 - fmr) ** n


# Check: with a gallery of 1e6 and a per-comparison FMR of 1e-6, about 63 % of nonmated searches
# would return at least one candidate above threshold.
assert close(fpir(1e-6, 10 ** 6), 0.63212, 1e-5); checks += 1
f_needed = 1 - (1 - 0.003) ** (1 / 10 ** 6)
# Check: keeping FPIR at 0.003 (NIST FRTE 1:N operating point) needs a per-comparison rate of ~3.0e-9.
assert close(f_needed, 3.0045e-9, 1e-12) and close(fpir(f_needed, 10 ** 6), 0.003, 1e-9); checks += 1

# --- Example E: matcher errors versus decision errors -------------------------------
FMR, FNMR, FTA = 1e-4, 0.02, 0.03
FAR = FMR * (1 - FTA)                     # single attempt, no binning (PR = 1, BER = 0)
FRR = FTA + (1 - FTA) * FNMR
# Check: FAR 9.7e-5 and FRR 0.0494: acquisition failures dominate the rejections.
assert close(FAR, 9.7e-5, 1e-12) and close(FRR, 0.0494, 1e-12) and FTA > (1 - FTA) * FNMR; checks += 1

# --- Example F: gallery storage and exact search ---------------------------------------
D, BYTES, N = 512, 4, 10 ** 6
# Check: one 512-D float32 template is 2,048 bytes; a million templates take 2.048 GB and an
# exact search costs 512 million multiply-accumulates per probe.
assert D * BYTES == 2048 and close(D * BYTES * N / 1e9, 2.048, 1e-12) and D * N == 512_000_000; checks += 1

# --- Example G: accepted-attempt composition under prevalence ----------------------
def false_share(pi, fmr, fnmr):
    return (1 - pi) * fmr / (pi * (1 - fnmr) + (1 - pi) * fmr)


# Check: at FMR 1e-4 and FNMR 0.02, about 1.03e-6 of accepted attempts are false matches when 99 % of attempts
# are genuine, but about 1.0 % when only 1 % are genuine.
assert close(false_share(0.99, 1e-4, 0.02), 1.0306e-6, 1e-9) and close(false_share(0.01, 1e-4, 0.02), 0.0100, 1e-4); checks += 1

print(f"75-embeddings-biometrie: {checks} checks passed")
