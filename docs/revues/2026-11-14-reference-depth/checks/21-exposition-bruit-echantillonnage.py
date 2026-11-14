"""Recompute the constructed examples of CV-ACQUISITION (reference 21-exposition-bruit-echantillonnage).

Stdlib only. Run with:
    python3 docs/revues/2026-11-14-reference-depth/checks/21-exposition-bruit-echantillonnage.py
Model equations come from EMVA 1288 Linear 4.0 (eqs. 4, 5, 15, 18, 21, 25), the sRGB
transfer function (W3C ICC interpretation, A.8 and B.1) and Parmar et al. 2022, Sec. 6.1
(filter taps). Every scenario value (speeds, electrons, noise, gain, PRNU) is constructed.
"""

import math

checks = 0


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


def snr(mu_e, sigma_d, k_gain):
    """EMVA eq. 21 written with mu_e = eta * mu_p; sigma_q^2 = 1/12 DN^2."""
    return mu_e / math.sqrt(sigma_d ** 2 + (1 / 12) / k_gain ** 2 + mu_e)


# --- Example A: blur, photons and gain -------------------------------------
V_IMG = 800.0          # image speed, px/s
SIGMA_D = 5.0          # read noise, e-
K = 0.5                # system gain, DN/e-
DARK = 100.0           # dark offset, DN
BITS = 12

# Check 1: blur = v * t_exp: 4 px at 5 ms and 1 px at 1.25 ms (card CV-ACQUISITION-001).
assert close(V_IMG * 0.005, 4.0) and close(V_IMG * 0.00125, 1.0)
checks += 1

base = snr(400, SIGMA_D, K)
short = snr(100, SIGMA_D, K)
short_gain = snr(100, SIGMA_D, 4 * K)
# Check 2: SNR of 19.4 at 400 e-, 8.93 at 100 e-, and only 8.94 after a x4 gain.
assert close(base, 19.395, 1e-3) and close(short, 8.932, 1e-3) and close(short_gain, 8.944, 1e-3)
checks += 1
# Check 3: the x4 gain restores the mean signal (200 DN above dark) but not the SNR.
assert close(100 * 4 * K, 400 * K) and short_gain < base / 2
checks += 1
# Check 4: electrons reaching the top code drop from 7,990 to 1,997.5 when K goes from 0.5 to 2.
top = 2 ** BITS - 1
assert close((top - DARK) / K, 7990.0) and close((top - DARK) / (4 * K), 1997.5)
checks += 1

# Check 5: EMVA eq. 4, 400 e- in 1.25 ms with 3.45 um pixels, 525 nm, eta = 0.6 needs ~1.7 uW/cm^2.
area_um2 = 3.45 ** 2
mu_p = 400 / 0.6
irradiance = mu_p / (50.34 * area_um2 * 1.25 * 0.525)
assert close(irradiance, 1.695, 1e-3)
checks += 1

# Check 6: EMVA eq. 25 without quantization: SNR = 10 needs 50 * (1 + sqrt(2)) = 120.7 e-.
target = 10.0
mu_e_needed = target ** 2 / 2 * (1 + math.sqrt(1 + 4 * SIGMA_D ** 2 / target ** 2))
assert close(mu_e_needed, 120.71, 1e-2) and close(mu_e_needed / math.sqrt(SIGMA_D ** 2 + mu_e_needed), 10.0, 1e-9)
checks += 1

# Check 7: quantization noise referred to electrons is sqrt(1/12)/K = 0.577 e- for K = 0.5.
assert close(math.sqrt(1 / 12) / K, 0.577, 1e-3)
checks += 1


# --- Example B: photon transfer and fixed patterns -------------------------
def temporal_var(signal_dn):
    """EMVA eq. 15: sigma_y^2 = K^2 sigma_d^2 + sigma_q^2 + K (mu_y - mu_dark)."""
    return K ** 2 * SIGMA_D ** 2 + 1 / 12 + K * signal_dn


v200, v1000 = temporal_var(200), temporal_var(1000)
# Check 8: predicted temporal variances of 106.3 and 506.3 DN^2.
assert close(v200, 106.333, 1e-3) and close(v1000, 506.333, 1e-3)
checks += 1
slope = (v1000 - v200) / 800
offset = v200 - slope * 200
# Check 9: the slope returns K = 0.5 and the offset returns sigma_d^2 = 25 e-^2.
assert close(slope, 0.5, 1e-12) and close((offset - 1 / 12) / slope ** 2, 25.0, 1e-9)
checks += 1
PRNU = 0.01
w200, w1000 = v200 + (PRNU * 200) ** 2, v1000 + (PRNU * 1000) ** 2
# Check 10: a single-image variance with 1% PRNU reads a slope of 0.62, a 24% error on K.
assert close((w1000 - w200) / 800, 0.62, 1e-9) and close((w1000 - w200) / 800 / K - 1, 0.24, 1e-9)
checks += 1
# Check 11: EMVA eq. 19, relative uncertainty sqrt(2/NM) is about 0.14% for one megapixel.
assert close(math.sqrt(2 / 1e6), 0.00141, 1e-5)
checks += 1
# Check 12: PRNU deviation p*mu_e equals shot noise sqrt(mu_e) at mu_e = 1/p^2.
assert close(1 / 0.01 ** 2, 10000.0) and close(1 / 0.005 ** 2, 40000.0)
for p in (0.01, 0.005):
    mu = 1 / p ** 2
    assert close(p * mu, math.sqrt(mu), 1e-9)
checks += 1


# --- Example C: aliasing and the prefilter ---------------------------------
def alias(freq):
    """Apparent frequency on a unit-spaced grid, in cycles per sample."""
    return abs(freq - round(freq))


# Check 13: 0.4 cyc/px decimated by 2 becomes 0.8 cyc per output px, which aliases to 0.2.
assert close(0.4 * 2, 0.8) and close(alias(0.8), 0.2)
checks += 1


def gain(taps, freq):
    """Magnitude of the frequency response of a symmetric FIR filter."""
    centre = (len(taps) - 1) / 2
    re = sum(t * math.cos(2 * math.pi * freq * (i - centre)) for i, t in enumerate(taps))
    im = sum(t * math.sin(2 * math.pi * freq * (i - centre)) for i, t in enumerate(taps))
    return math.hypot(re, im)


box2 = [0.5, 0.5]
bilinear_adaptive = [1 / 8, 3 / 8, 3 / 8, 1 / 8]   # Parmar et al. Sec. 6.1, r = 2
binomial = [1 / 16, 4 / 16, 6 / 16, 4 / 16, 1 / 16]  # pyrDown kernel, one axis
# Check 14: responses at 0.4 cyc/px (aliased part): 0.309, 0.030 and 0.009.
assert close(gain(box2, 0.4), 0.309, 1e-3)
assert close(gain(bilinear_adaptive, 0.4), 0.0295, 1e-4)
assert close(gain(binomial, 0.4), 0.0091, 1e-4)
checks += 1
# Check 15: responses at the new limit 0.25 cyc/px: 0.707, 0.354 and 0.250.
assert close(gain(box2, 0.25), 0.7071, 1e-4)
assert close(gain(bilinear_adaptive, 0.25), 0.3536, 1e-4)
assert close(gain(binomial, 0.25), 0.25, 1e-9)
checks += 1
# Check 16: responses at 0.1 cyc/px (kept detail): 0.951, 0.860 and 0.818.
assert close(gain(box2, 0.1), 0.951, 1e-3)
assert close(gain(bilinear_adaptive, 0.1), 0.860, 1e-3)
assert close(gain(binomial, 0.1), 0.818, 1e-3)
checks += 1

# --- Other constructed statements -------------------------------------------
# Check 17: a 4 px box blur has a zero response at 1/4 cyc/px and its odd harmonics,
# so a pattern of period 4 px is erased along the motion.
box4 = [0.25] * 4
for harmonic in (0.25, 0.5, 0.75):
    assert gain(box4, harmonic) < 1e-12
checks += 1


def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def linear_to_srgb(x):
    return 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055


# Check 18: encoded 0.5 is 0.214 in linear light; linear 0.5 encodes to 0.735.
assert close(srgb_to_linear(0.5), 0.2140, 1e-4)
assert close(linear_to_srgb(0.5), 0.7354, 1e-4)
checks += 1
# Check 19: the two branches of the sRGB curve meet at the thresholds (round trip within 1e-6).
for c in (0.0, 0.02, 0.04045, 0.1, 0.5, 1.0):
    assert close(linear_to_srgb(srgb_to_linear(c)), c, 1e-6)
checks += 1

# Check 20: raw data rate of a 5 MP, 12-bit, 100 frames/s stream is 6 Gbit/s (4 Gbit/s at 8 bits).
assert close(5e6 * 12 * 100 / 1e9, 6.0) and close(5e6 * 8 * 100 / 1e9, 4.0)
checks += 1

# Check 21: card CV-ACQUISITION-002 values: sigma_d = 5 e-, 100 e- -> 8.9, 200 e- -> 13.3,
# 25 e- -> 3.54, 50 e- -> 5.77 (quantization neglected).
def snr_noq(n):
    return n / math.sqrt(n + SIGMA_D ** 2)


assert close(snr_noq(100), 8.944, 1e-3) and close(snr_noq(200), 13.333, 1e-3)
assert close(snr_noq(25), 3.536, 1e-3) and close(snr_noq(50), 5.774, 1e-3)
assert close(snr_noq(50) / snr_noq(25), 1.633, 1e-3)
checks += 1

print(f"21-exposition-bruit-echantillonnage: {checks} checks passed")
