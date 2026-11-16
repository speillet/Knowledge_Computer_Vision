# Creation — Reference systems for photogrammetry: datums, projections and heights — 2026-11-16

## Overview

New subject CV-GEODESIE (domain d15, tracks B and E, depth `usage-operationnel`,
prerequisite CV-SE3): one reference note and 5 cards, CV-GEODESIE-001 to
CV-GEODESIE-005, in five families: understanding, practice, reasoning, algorithm and
diagnosis. Answer lengths from the inventory: 443, 423, 445, 422 and 429 lexical words
(minimum 422, median 429, maximum 445). The note has 521 lines and 25 recomputation
checks. Self-review: Agent Claude Code. Editorial status: redige, reference revision 1.

Files created:

- `vault/150-photogrammetrie/references/153-systemes-reference.md`
- `vault/150-photogrammetrie/153-systemes-reference.md`
- `docs/revues/2026-11-16-photogrammetry/checks/153-systemes-reference.py`
- `docs/revues/2026-11-16-photogrammetry/153-systemes-reference.md` (this report)

## Cards

| Card | Accuracy: central claims, verdict and exact passage | Relevance | Gradability: criteria and lexical words | Family |
| --- | --- | --- | --- | --- |
| CV-GEODESIE-001 | $H=h-\zeta$ for geoid-separation and height-correction models alike: confirmed, IOGP 7-2 §4.11.1 (pp. 157–158). RAF20 converts RGF93 v2b ellipsoidal heights to NGF-IGN69, accuracy 0.01 m: confirmed, EPSG 9876 (`grid_transformation.sql` L1180) and IGN 2026 pp. 13 and 21. RAF18b adapts QGF16 to 10,658 levelled GNSS points, centimetric at one sigma: confirmed, IGN 2021b pp. 5 and 7. WGS 84 ellipsoid to mean sea level from −100 to +80 m: confirmed, IOGP 7-2 §4.1.1 note. Exif `GPSAltitude` is sea-level referenced: confirmed, Exif 2.32 §4.6.6. COLMAP treats the EXIF altitude as an ellipsoidal height: confirmed in code, `image_reader.cc` L302–L308 and `gps.cc` L118–L141; the bias it causes is a project deduction. GDAL assumes ellipsoidal heights on geographic and projected CRSs: confirmed, `osr_api_tut.rst` L389–L395. `vgridshift` default multiplier −1: confirmed, `vgridshift.rst` L118–L132, and by execution (43.79 m at Paris). 245.32 m, 169.71 m, ratio 1.414, 145.90 m: constructed, recomputed | Mechanism and consequence: two height types, the grid that links them, and where a 50 m bias goes in a self-calibrating adjustment. Distinct from CV-AEROTRIANGULATION-004, whose answer names height-system mixing only as a blocking error of a control plan | 3 criteria (conversion and meaning; absorption of the bias with its size; prevention rule); 443 words | understanding |
| CV-GEODESIE-002 | GeoJSON positions are longitude, latitude: confirmed, RFC 7946 §3.1.1. EPSG:4326 lists latitude first: confirmed, `axis.sql` L265–L266 and the WKT in `faq.rst` L142–L170. PROJ follows the authority order since version 6: confirmed, `faq.rst` L113–L119. GDAL since 3.0, `OAMS_TRADITIONAL_GIS_ORDER`, default authority-compliant: confirmed, `osr_api_tut.rst` L193–L228. Rasters use the traditional order: confirmed, RFC 73 L366–L369. `always_xy=False` by default: confirmed, `transformer.py` L671 and L698–L701. Output values: executed with pyproj 3.8.0 / PROJ 9.8.1 and recomputed with the stdlib LCC. Mirror, stretch 1.5, 1,151 m and 233 m RMS: constructed, recomputed | Practice with a diagnostic angle: a frequent, costly integration error and the guard that catches it; the size of the error identifies its class | 3 criteria (cause from the two conventions; two confirming symptoms; fix and guard); 423 words | practice |
| CV-GEODESIE-003 | Collinearity needs a Cartesian system that most mapping systems are not; local tangential system significantly better for one OEEPE data set, no difference for the other; recommendation: confirmed, Heipke et al. 2001 §1 and §4. LCC scale factor $k=rn/(am)$: confirmed, Snyder 1987 p. 108; "too small between the standard parallels": p. 105; convergence definition: p. 21. Lambert-93 parameters: confirmed, `conversion.sql` L4881. MicMac needs a Euclidean frame and builds a local tangent system: confirmed, `QuickStartSimplified-Tools-2.tex` L524–L528. Curvature drops, $k=0.999051$, focal absorption 3.8 px, misfit 1.9 px, 0.31 mrad, 157 ppm, 7 µm, −5.4° at Brest: project derivations, recomputed; $k$ and convergence cross-checked by executing pyproj `get_factors` | Reasoning about the object space of an adjustment, with orders of magnitude a senior must estimate without software | 3 criteria (two quantified non-Euclidean effects; how they surface; what to do instead); 445 words | reasoning |
| CV-GEODESIE-004 | Geodetic to ECEF formulas, closed-form reverse: confirmed, IOGP 7-2 §4.1.1 (p. 95). ENU matrix, its inverse, Up along the ellipsoid normal: confirmed, §4.1.2 (pp. 96–99). PROJ `cart` axes and `topocentric` (EPSG 9836, 9837): confirmed, `cart.rst` L21–L25, `topocentric.rst` L21–L51. COLMAP uses the same matrix: confirmed, `gps.cc` L191–L217. IOGP's worked values U, V, W: reproduced to 1 mm. Checkpoint ENU (746.13, 1,111.98, 9.86) m: constructed, recomputed and reproduced by an executed PROJ pipeline. Float32 spacing 0.5 m: recomputed | Core algorithm for any GNSS-aided reconstruction; validation habit against authority examples | 3 criteria (ECEF formulas; ENU rotation with its properties; estimated result and the curvature explanation); 422 words | algorithm |
| CV-GEODESIE-005 | ETRS89 coincides with the ITRS at 1989.0, fixed to stable Eurasia, relation $X^E=X^I+T+\dot{\mathcal R}X^I(t-1989.0)$: confirmed, EUREF TN1 §2, eqs. 2–3. ITRF2020 → ETRF2000 parameters: confirmed, TN1 Table 4 and EPSG 10586 (`helmert_transformation.sql` L2785), with identical values. RGF93 v2b = ETRF2000 at 2019.0 and the near-1 m gap in 2026: confirmed, IGN 2026 pp. 5–6. Null WGS 84 shift at the 1 m level: confirmed, EPSG 9792 (L2598). WGS 84 (G2296) aligned to ITRF2020 in NGA products since 7 January 2024: confirmed, IGSMAIL-8444. 0.945 m at azimuth 44°, 1.7 cm vertical, 2.40 cm/yr, 0.91 m and 0.19 m, 0.62 m from the $z$ rotation: constructed, recomputed after reproducing TN1 Appendix B within 0.1 mm | Diagnosis by the signature and size of a residual; a trap (elapsed time from 1989.0, not 2019.0) that national-frame users meet | 3 criteria (size and direction with the right elapsed time; discriminating check; fix and metadata rule); 429 words | diagnosis |

## Reference content and verified claims

The note asserts, on the following passages:

- **Vocabulary**: CRS = coordinate system + datum; conversions are error free,
  transformations are empirical; point motion within a CRS [IOGP 7-2, §2.1, p. 8].
- **Ellipsoids**: GRS80 and WGS 84 parameters [EPSG v13.102 via PROJ 9.9.0,
  `ellipsoid.sql` L23, L32]; their semi-minor axes differ by 0.105 mm (recomputed).
- **Conversions**: geodetic/ECEF and ECEF/ENU formulas and their examples [IOGP 7-2,
  §4.1.1–§4.1.3]; ECEF axes [PROJ `cart.rst` L21–L25]; the two kinds of topocentric
  height axis [IOGP 7-2, §4.1.2]; 2D-to-3D artificial heights [§4.1.4].
- **Frames and epochs**: ITRF2020 dynamic with frame reference epoch 2015.0
  [`geodetic_datum.sql` L357]; ETRS89 definition, eqs. 1–3, Table 1 translations and
  rates, Table 4 [EUREF TN1]; RGF93 realizations and epochs [IGN 2026, p. 6;
  `geodetic_datum.sql` L341, L343, L735]; v2b changes of millimetres and under a
  centimetre [IGN 2021a]; versions indistinguishable above 5 cm but grids tied to a
  realization [IGN 2026, pp. 7 and 13]; WGS 84 ensemble of eight realizations, 2 m
  [`geodetic_datum.sql` L1403, `geodetic_datum_ensemble_member.sql` L65–L72]; ETRS89
  ensemble 0.1 m [L1401]; G2296 aligned to ITRF2020 [NGA 2024; EPSG 10608 at
  `helmert_transformation.sql` L2793].
- **Projections**: LCC 2SP formulas [IOGP 7-2, §3.1.1.1], scale factor and its
  behaviour [Snyder 1987, pp. 105 and 108], convergence [p. 21], UTM [pp. 57–58; PROJ
  `utm.rst` L35–L57], Lambert-93 and CC46 parameters [`conversion.sql` L4881, L4901].
- **Heights**: $H=h-\zeta$, geoid versus height-correction models, kinds of
  gravity-related height [IOGP 7-2, §4.11.1–§4.11.2]; RAF20 and its predecessors
  [EPSG `grid_transformation.sql` L1172–L1182; PROJ-data 1.25.0 README]; RAF18b
  construction [IGN 2021b].
- **Helmert**: conventions, small-angle limit, time dependence [IOGP 7-2, §4.2.1 and
  §4.2.5; PROJ `helmert.rst` L80–L170].
- **Libraries**: PROJ axis order, ballpark operations, operation ranking, `vgridshift`;
  GDAL axis mapping and height assumption; pyproj options; COLMAP GPS handling; MicMac
  local tangent system (passages listed in the note).
- **Published comparison**: local tangential system versus UTM in the OEEPE test
  [Heipke et al. 2001, §4].

Disagreements and corrections between sources:

- The brief named "Altamimi et al. 2023, ITRF2020, J. Geophys. Res.". EUREF TN1's
  reference list gives the ITRF2020 paper in *Journal of Geodesy*
  (doi 10.1007/s00190-023-01738-w); the ITRF2014 paper was in J. Geophys. Res. The paper
  itself could not be opened (see failed access), so the note cites ITRF2020 only through
  TN1 and EPSG.
- IGN quotes "~2.6 cm/an" for the ITRS–ETRS89 drift [IGN 2026, p. 5]. At 48°N, 2°E the
  ETRF2020 rotation gives 2.40 cm/yr and the ITRF2020–ETRF2000 gap grows by 2.46 cm/yr
  between 2019.0 and 2026.87 (recomputed). Both lead to "nearly 1 m" in 2026 (0.945 m
  computed); the IGN figure is a rounded national value and the note quotes both.
- IOGP 7-2 §4.2.5, coordinate-frame example: the computation line for $r_Z'$ prints a
  rate of 1.5551 msec/yr while the parameter list gives 1.1551; the printed result,
  25.3880 msec, corresponds to 1.1551. The check script uses 1.1551 and reproduces the
  target coordinates to 1 mm.
- PROJ 9.9.0 `helmert.rst` contains typographical errors ("$R_z$ = radians(ry)",
  "rotation rate of the y-axis" for `drz`); they do not change the documented
  conventions and are not quoted.
- EPSG naming changed: v13.102 (PROJ 9.9.0) calls the French frames "ETRS89-FRA [RGF93
  v1/v2/v2b]", while the EPSG v12.029 database bundled with the executed pyproj wheel
  still prints "RGF93 v2b to WGS 84 (1)". The note uses the v13.102 names and EPSG codes,
  which did not change.
- The brief listed "orthometric H". IOGP notes that several kinds of gravity-related
  height exist and IGN's QGF16 is a quasi-geoid; the note uses "gravity-related height"
  for NGF-IGN69 and does not assert its height type, which was not verified.

Existing references: no error found in the references read (CV-SE3, CV-IMAGERIES,
CV-CAPTEURS, CV-VIO). CV-IMAGERIES' "one degree of longitude spans $111.2\cos\varphi$
km" is labelled as a spherical approximation and remains correct as such.

## Constructed examples

All recomputed by `checks/153-systemes-reference.py` (25 checks, stdlib, floats with
stated tolerances and `Fraction` for the height arithmetic). Before the constructed
cases, the script reproduces IOGP 7-2 §4.1.1, §4.1.2 and §3.1.1.1 examples, PROJ's
`cart` and `topocentric` documentation examples, EUREF TN1 Appendix B (within 0.1 mm)
and IOGP's time-dependent coordinate-frame example (to 1 mm).

- **A** (card 004): GRS80, origin 48°N 2°E 150 m, checkpoint 48.01°N 2.01°E 160 m →
  ENU (746.128, 1111.981, 9.859) m; drop 0.1405 m for $d=1339.1$ m, $R=6380.3$ km.
- **B** (card 001): $\zeta=49.71$ m, $H=195.61$ m → $h=245.32$ m; apparent flying height
  169.71 m for 120 m, ratio 1.414; sign error gives 145.90 m.
- **C** (card 002): Paris (652,469.02, 6,862,035.26) versus swapped (6,960,803.48,
  3,114,983.26); 1 km square of four GCPs: 1,151 m RMS after the best similarity, 233 m
  after the best mirrored similarity; Jacobian determinant negative, stretch 1.51.
- **D** (card 003): curvature 0.078, 0.313, 1.96, 7.84 m at 1, 2, 5, 10 km; Lambert-93
  $k$ 0.999051 (minimum near 46.52°N), 0.999893 Paris, 1.000598 Marseille, 1.002244
  Dunkerque, 1.002940 Bonifacio; $n=0.725608$; convergence −0.47°, −5.43°, +3.45°;
  focal absorption 3.80 px, radial misfit 1.90 px, 0.95 m per km of flying height,
  0.31 mrad, 157 ppm; frame-camera radial displacement 7.0 µm; UTM true scale 180.1 km,
  1.00097 at the zone edge; CC46 −8.5 cm/km at 46°N.
- **E** (card 005): ITRF2020 at 2026.87 → ETRF2000 at 48°N 2°E: (−0.657, −0.680, −0.017) m
  in ENU, 0.945 m at azimuth 44°; 0.752 m at 2019.0; velocity 1.80 E, 1.59 N,
  2.40 cm/yr; 0.91 m since 1989.0 against 0.19 m since 2019.0; $z$ rotation −29.99 mas,
  0.62 m.
- Supporting: float32 spacing 0.5 m at ECEF magnitudes and 0.98 mm at 10 km; 1 mas =
  3.09 cm and 1 ppb = 6.4 mm at the Earth's radius.

The RAF20 range 42.07–56.43 m and the values at Paris, Brest and Chamonix come from
`fr_ign_RAF20.tif` (PROJ-data 1.25.0, git blob 589a569d9f2fbbb9c1ff43eb8711c1c3e11e1b0f,
identical to the CDN copy), read with tifffile and interpolated by an executed PROJ
`vgridshift`; they are not recomputed by the stdlib script.

## Proposals

Not registered in `docs/revues/propositions.md` (left to the coordinator):

1. **Comparison card**: a global geoid model (EGM2008, EPSG 3858) versus a national
   height-correction grid (RAF20) for a drone survey: which reproduces the national
   datum, at what accuracy, and when each is acceptable. Source: IOGP 7-2 §4.11.1, EPSG
   records, IGN 2021b.
2. **Design card**: tie a VIO or SLAM world frame to geodetic coordinates with GNSS: ENU
   origin, gravity versus ellipsoid normal, the 4-DOF alignment of CV-VIO and the epoch
   of the GNSS fixes. Sources to verify: IOGP 7-2 §4.1.2 and the VIO references.

## Sources

Scientific and agency sources (read at the cited passages):

- IOGP Publication 373-7-2, Guidance Note 7 part 2, revised September 2019 (PDF from
  iogp.org): pp. 5–8, 17–20, 95–112, 157–159.
- Snyder 1987, USGS Professional Paper 1395 (pubs.usgs.gov PDF): pp. 21, 57–58, 105–108.
- Altamimi and Collilieux, EUREF Technical Note 1, release 2024-03-04 (IGN mirror
  etrs89.ign.fr): all pages, including Tables 1–4 and Appendices A–B.
- IGN, Virly, GEOPOS 26 March 2026 (cnig.gouv.fr): pp. 1–21.
- IGN/DOT/SGM, "Mise à jour du repère de référence en France", January 2021 (ign.fr).
- IGN, GEOPOS 25 March 2021, QGF16 and RAF18b (cnig.gouv.fr): pp. 1–10.
- NGA Office of Geomatics, IGSMAIL-8444, 8 March 2024 (lists.igs.org).
- Heipke, Jacobsen and Wegmann 2001, Photogrammetric Week 01, pp. 195–204
  (phowo.ifp.uni-stuttgart.de): §1–§5.

Implementation sources and standards:

- PROJ 9.9.0 (tag): documentation sources `cart.rst`, `topocentric.rst`,
  `axisswap.rst`, `helmert.rst`, `vgridshift.rst`, `lcc.rst`, `utm.rst`, `faq.rst`,
  `glossary.rst`, `operations_computation.rst`; EPSG database SQL (EPSG v13.102,
  2026-08-27): `metadata`, `ellipsoid`, `axis`, `coordinate_system`, `unit_of_measure`,
  `geodetic_datum`, `geodetic_datum_ensemble_member`, `geodetic_crs`, `projected_crs`,
  `conversion`, `vertical_crs`, `compound_crs`, `grid_transformation`,
  `helmert_transformation`, `grid_alternatives`, `proj_db_table_defs`.
- PROJ-data 1.25.0 (tag): `fr_ign/fr_ign_README.txt`, `fr_ign/fr_ign_RAF20.tif`.
- GDAL v3.13.3 (tag): `doc/source/tutorials/osr_api_tut.rst`,
  `doc/source/development/rfc/rfc73_proj6_wkt2_srsbarn.rst`.
- pyproj 3.8.0 (tag): `pyproj/transformer.py`.
- COLMAP 4.2.1 (tag): `src/colmap/geometry/gps.h`, `gps.cc`,
  `src/colmap/sensor/bitmap.cc`, `src/colmap/controllers/image_reader.cc`,
  `src/colmap/geometry/pose_prior.h`.
- MicMac Documentation repository at commit a647a96b177c2ea047917a22b59aa133464fbc6a:
  `DocMicMac/Generalites/QuickStartSimplified-Tools-2.tex`, `DocRef/GeoLocalisation.tex`,
  `DocRef/ConvTool.tex`.
- CIPA DC-X008-2019 (Exif 2.32, English translation): §4.6.6.
- RFC 7946 (rfc-editor.org text): §3.1.1, §4.
- Executed: pyproj 3.8.0 wheel bundling PROJ 9.8.1 and EPSG v12.029 (2025-10-02),
  installed with `uv` in a scratch environment and run with `python -I`; outputs quoted
  in the note and cards.

Failed access (not cited for unread passages):

- earth-info.nga.mil timed out: NGA.STND.0036 (WGS 84 definition) and the "WGS 84
  (G2296)" paper; WGS 84 facts rest on EPSG records and IGSMAIL-8444.
- Moritz 2000, GRS80 (geodesy.geology.ohio-state.edu) unreachable; GRS80 values rest on
  EPSG.
- Altamimi et al. 2023, ITRF2020, Journal of Geodesy (Springer "client challenge"), and
  the ITRF2020 plate motion model, Geophysical Research Letters (Wiley HTTP 403): plate
  rotation rests on EUREF TN1 Table 1.
- IGN technical notes NT/G 71 and NT/G 80 at guessed geodesie.ign.fr URLs: HTTP 404;
  Lambert formulas rest on IOGP 7-2 and Snyder.
- The euref.eu copy of TN1 (HTTP 404); the IGN mirror was read instead.
- CIPA Exif 3.0 (DC-008-2023) is behind a download form; Exif 2.32 was read.
- EGM2008 (Pavlis et al. 2012) was not consulted; EGM2008 is cited only through EPSG
  records.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 -I docs/revues/2026-11-16-photogrammetry/checks/153-systemes-reference.py` | 25 checks passed |
| `python3 scripts/check_vault.py` | OK: 150 Markdown documents, 64 references, 318 cards (shared tree, sibling subjects included) |
| `python3 scripts/learning_path.py` | OK: 64 references, 318 cards, 0 errors |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/150-photogrammetrie/153-systemes-reference.md` | 5 cards, no anomaly; 443, 423, 445, 422, 429 lexical words |
| `grep -n ' $'` on the four files | No trailing whitespace |

No photogrammetric processing was run. pyproj was executed only to cross-check
conventions and numbers; it bundles an older EPSG dataset (v12.029) than the PROJ 9.9.0
sources read (v13.102). The magnitudes of example D are derivations under stated
assumptions; how a given adjustment program distributes them depends on its weights and
on corrections it may apply internally, and the proposed comparison is not executed. The
deflection of the vertical and the type of NGF-IGN69 heights are not quantified or
asserted. The note links CV-SATELLITE and CV-ORTHO by name only, because those batch-2
files do not exist yet. Agent self-review only, without independent validation;
Obsidian and AnkiDroid rendering are not verified. Export: to republish with
`paquet-anki`. The learning path, sections, indexes, catalogue, progress log and
proposal register are left to the coordinator.
