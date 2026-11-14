"""Recompute the constructed examples of CV-IMAGERIES (reference 23-imageries-specialisees).

Stdlib only. Run with:
    python3 docs/revues/2026-11-14-reference-depth/checks/23-imageries-specialisees.py
Conventions: DICOM PS3.3 2026d eq. C.7.6.2.1-1 (Pixel Spacing = row spacing, column spacing;
LPS+ axes), NIfTI-1 RAS+ axes (nifti1.h v3.0.1), GDAL geotransform with (0,0) at the top-left
corner (raster data model, GDAL 3.13.3). All numerical scenarios are constructed.
"""

import math

checks = 0


def close(a, b, tol=1e-3):
    return abs(a - b) <= tol


# --- Example A: conventions that move a result --------------------------------
spacing = (0.5, 0.5, 3.0)  # mm


def physical_length(delta, sp):
    return math.sqrt(sum((s * d) ** 2 for s, d in zip(sp, delta)))


# Check 1: an index step (1, 0, 1) is sqrt(0.5^2 + 3^2) = 3.04 mm (card CV-IMAGERIES-001 appendix).
assert close(physical_length((1, 0, 1), spacing), 3.0414, 1e-4)
checks += 1
# Check 2: two voxels along the slice axis are 6 mm; two in-plane are 1 mm (equal in index units).
assert close(physical_length((0, 0, 2), spacing), 6.0) and close(physical_length((2, 0, 0), spacing), 1.0)
checks += 1


def dicom_point(S, row_cos, col_cos, pixel_spacing, i, j):
    """Eq. C.7.6.2.1-1: P = S + X*di*i + Y*dj*j, with Pixel Spacing = (row spacing, column spacing).
    i is the column index (uses the column spacing), j the row index (uses the row spacing)."""
    row_spacing, col_spacing = pixel_spacing
    return tuple(s + x * col_spacing * i + y * row_spacing * j for s, x, y in zip(S, row_cos, col_cos))


S = (0.0, 0.0, 0.0)
X = (1.0, 0.0, 0.0)  # row direction cosine
Y = (0.0, 1.0, 0.0)  # column direction cosine
good = dicom_point(S, X, Y, (0.5, 0.8), 10, 20)
swapped = dicom_point(S, X, Y, (0.8, 0.5), 10, 20)
# Check 3: Pixel Spacing 0.5\0.8 puts pixel (i=10, j=20) at S + (8, 10, 0) mm; swapping gives (5, 16, 0),
# an error of sqrt(3^2 + 6^2) = 6.7 mm.
assert good == (8.0, 10.0, 0.0) and swapped == (5.0, 16.0, 0.0)
assert close(math.dist(good, swapped), 6.708, 1e-3)
checks += 1


def lps_to_ras(p):
    return (-p[0], -p[1], p[2])


# Check 4: DICOM LPS (10, 20, 30) is RAS (-10, -20, 30); the conversion is its own inverse.
assert lps_to_ras((10.0, 20.0, 30.0)) == (-10.0, -20.0, 30.0)
assert lps_to_ras(lps_to_ras((1.0, 2.0, 3.0))) == (1.0, 2.0, 3.0)
checks += 1

GT = (500000.0, 10.0, 0.0, 4200000.0, 0.0, -10.0)


def gdal_xy(gt, px, ln):
    return gt[0] + px * gt[1] + ln * gt[2], gt[3] + px * gt[4] + ln * gt[5]


centre = gdal_xy(GT, 0.5, 0.5)
corner = gdal_xy(GT, 0.0, 0.0)
# Check 5: the centre of the top-left pixel is (500005, 4199995); treating index 0 as a centre
# shifts every prediction by 5 m per axis, 7.07 m diagonally.
assert centre == (500005.0, 4199995.0)
assert close(math.dist(centre, corner), 7.071, 1e-3)
checks += 1

R_EARTH_KM = 6371.0
deg_lat_km = math.pi * R_EARTH_KM / 180
# Check 6: spherical Earth, one degree of latitude is about 111.2 km; of longitude at 45 deg, 78.6 km;
# a 0.0001 deg cell at 45N is about 11.1 m by 7.9 m.
assert close(deg_lat_km, 111.19, 1e-2) and close(deg_lat_km * math.cos(math.radians(45)), 78.63, 1e-2)
assert close(1e-4 * deg_lat_km * 1000, 11.12, 1e-2) and close(1e-4 * deg_lat_km * math.cos(math.radians(45)) * 1000, 7.86, 1e-2)
checks += 1

# --- Example B: line-scan scale and exposure ----------------------------------
F_LINE = 5000.0  # lines/s
# Check 7: 500 mm/s -> 0.1 mm/line and 200 lines for a 20 mm part (card CV-IMAGERIES-002).
assert close(500 / F_LINE, 0.1) and close(20 / (500 / F_LINE), 200)
checks += 1
# Check 8: 750 mm/s -> 0.15 mm/line; a 30 mm part spans 200 lines instead of 300; the old
# calibration (0.1 mm/line) reports 20 mm.
s_fast = 750 / F_LINE
lines = 30 / s_fast
assert close(s_fast, 0.15) and close(lines, 200) and close(30 / 0.1, 300) and close(lines * 0.1, 20.0)
checks += 1
# Check 9: one line per 0.1 mm at 750 mm/s needs 7500 lines/s.
assert close(750 / 0.1, 7500)
checks += 1
# Check 10: line period at 5000 lines/s is 200 us; 100 us exposure at 500 mm/s blurs 0.05 mm (half a line).
assert close(1 / F_LINE, 200e-6, 1e-12) and close(500 * 100e-6, 0.05) and close(500 * 100e-6 / 0.1, 0.5)
checks += 1

# --- Cost ----------------------------------------------------------------------
vol_bytes = 512 * 512 * 300 * 4
# Check 11: a 512x512x300 float32 volume is 315 MB; resampling 3 mm to 0.5 mm (x6 slices) gives 1.9 GB.
assert close(vol_bytes / 1e6, 314.57, 1e-2) and close(vol_bytes * 6 / 1e9, 1.887, 1e-3)
checks += 1

print(f"23-imageries-specialisees: {checks} checks passed")
