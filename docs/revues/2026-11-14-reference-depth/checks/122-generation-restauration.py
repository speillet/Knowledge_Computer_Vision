"""Recompute the constructed examples of CV-DIFFUSION (reference 122-generation-restauration).

Stdlib only. Run with: python3 docs/revues/2026-11-14-reference-depth/checks/122-generation-restauration.py
Inputs: DDPM linear schedule beta_1 = 1e-4 to beta_T = 0.02, T = 1000 (Ho et al. 2020, Sec. 4),
eq. 4 and its inversion; perception-distortion Example 1 of Blau and Michaeli (Y = X + N, X_hat = aY);
LDM downsampling factor f (Rombach et al., Sec. 3.1). Numbers below are constructed.
"""

import math

# --- Example A: DDPM linear schedule ------------------------------------------------
T = 1000
betas = [1e-4 + (0.02 - 1e-4) * (t - 1) / (T - 1) for t in range(1, T + 1)]
alpha_bar = []
prod = 1.0
for b in betas:
    prod *= 1 - b
    alpha_bar.append(prod)
snr = [a / (1 - a) for a in alpha_bar]
# Check 1: at t = T the signal weight sqrt(alpha_bar) is about 0.0064 (alpha_bar about 4.0e-5).
assert abs(alpha_bar[-1] - 4.04e-5) < 0.05e-5 and abs(math.sqrt(alpha_bar[-1]) - 0.00635) < 1e-4
t_equal = next(t for t, s in enumerate(snr, start=1) if s < 1)
# Check 2: signal and noise variances become equal (SNR = 1) at t = 260 of 1000.
assert t_equal == 260, t_equal

# Check 3: inverting eq. 4 with the true noise recovers x0 exactly (x0 = 0.3, eps = -1.2, t = 500).
x0, eps, ab = 0.3, -1.2, alpha_bar[499]
xt = math.sqrt(ab) * x0 + math.sqrt(1 - ab) * eps
assert abs((xt - math.sqrt(1 - ab) * eps) / math.sqrt(ab) - x0) < 1e-12
# Check 4: a noise-prediction error of 0.1 becomes an x0 error of 0.1*sqrt((1-ab)/ab): 0.34 at t = 500 (ab = 0.079).
assert abs(ab - 0.0786) < 1e-4 and abs(0.1 * math.sqrt((1 - ab) / ab) - 0.342) < 0.001


# --- Example B: perception-distortion in Blau and Michaeli's Example 1 -------------------
def mse(a, s2):            # E[(X - aY)^2] with X ~ N(0, 1), N ~ N(0, s2)
    return (1 - a) ** 2 + a * a * s2


def kl_to_prior(a, s2):    # KL(N(0, 1) || N(0, a^2 (1 + s2)))
    v = a * a * (1 + s2)
    return 0.5 * math.log(v) + 1 / (2 * v) - 0.5


s2 = 1.0
a_mmse = 1 / (1 + s2)
a_match = 1 / math.sqrt(1 + s2)
# Check 5: the MMSE estimator has MSE 0.5 but a distribution mismatch KL 0.153 (too smooth);
# matching the prior distribution (KL 0) costs MSE 0.586, about 17% more.
assert abs(mse(a_mmse, s2) - 0.5) < 1e-12 and abs(kl_to_prior(a_mmse, s2) - 0.1534) < 1e-4
assert abs(kl_to_prior(a_match, s2)) < 1e-12 and abs(mse(a_match, s2) - 0.5858) < 1e-4
assert abs(mse(a_match, s2) / mse(a_mmse, s2) - 1.1716) < 1e-4

# --- Example C: a detail invisible to the measurement (null space of H) -----------------
x = [10, 12, 30, 31, 12, 11]            # 1-D intensity profile, a crack around samples 2-3
delta = [1, -1, 1, -1, 1, -1]           # alternating detail at the finest scale


def downsample(v):                      # H: average adjacent pairs (2x downsampling)
    return [(v[2 * i] + v[2 * i + 1]) / 2 for i in range(len(v) // 2)]


# Check 6: H(x + delta) = H(x): the measurement cannot distinguish the two high-resolution profiles.
assert downsample([a + b for a, b in zip(x, delta)]) == downsample(x) == [11.0, 30.5, 11.5]

# --- Example D: latent grid size -----------------------------------------------------------
# Check 7: f = 8 on a 512 x 512 image gives a 64 x 64 latent: 64 times fewer spatial positions;
# a 6-pixel-wide crack spans less than one latent cell.
assert (512 // 8) ** 2 * 64 == 512 * 512 and 6 / 8 < 1

# --- Example E: PSNR on an 8-bit scale ----------------------------------------------------
# Check 8: MSE 25 (RMS error 5 grey levels) gives PSNR = 10 log10(255^2 / 25) = 34.15 dB.
assert abs(10 * math.log10(255 ** 2 / 25) - 34.15) < 0.01

print("122-generation-restauration: 8 checks passed (schedule, inversion, perception-distortion, null space, latent grid, PSNR)")
