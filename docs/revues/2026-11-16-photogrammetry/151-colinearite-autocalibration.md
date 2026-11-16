# Creation — Collinearity, orientations and photogrammetric self-calibration — 2026-11-16

## Overview

Creation of the reference note CV-COLINEARITE (revision 1, `statut: redige`, tracks B and E,
depth `approfondissement`, prerequisites CV-ZHANG and CV-BA) and of five new cards,
CV-COLINEARITE-001 to CV-COLINEARITE-005, for the photogrammetry domain (`d15`, batch 1).
Five families: practice, reasoning, diagnosis, design, evaluation. Answers have 431 to 455
lexical words according to the inventory (detail below). Constructed numbers are recomputed by
`checks/151-colinearite-autocalibration.py` (55 checks).
Self-review: Agent Claude Code.

## Cards

| Card | Accuracy: central claims, verdict and exact passage | Relevance | Gradability: criteria and lexical words | Family |
| --- | --- | --- | --- | --- |
| CV-COLINEARITE-001 | $c=f_x\cdot$pitch, principal point in mm with the $y$ flip, $A_1=k_1/c^2$: confirmed in Hastedt and Luhmann 2015, §2.2 Table 1 (which uses $0.5\times$ image size as the centre). $R,t$ map world to camera, intrinsics in pixels, distortion acts on normalized coordinates: confirmed, OpenCV 4.13.0 calib3d.hpp L64–L86, L225–L262. Initial principal point $((w-1)/2,(h-1)/2)$: confirmed, calibration.cpp L80–L81. Image vector $(x-x_p+dx,\,y-y_p+dy,\,-c)$: confirmed, Fraser 2006 eq. 1. Projection centre, $R_{ph}=R^\top D$, $\omega=\varphi=\kappa=0$ for the nadir case, decentring scaling $1/c$ and the reprojection agreement: project derivations, recomputed (A1–A14). Metashape $P_1$/OpenCV $p_2$ naming and $c_x$ offset: confirmed in Metashape 2.2, App. D p. 243 | Practice: the interface conversion that breaks mixed CV/photogrammetry pipelines (units, axes, angle convention, distortion direction). Distinct from CV-SE3-002 (camera centre only) and CV-SE3-006 (OpenCV–OpenGL axes) by interior orientation and the $\omega,\varphi,\kappa$ convention | 3 criteria (IO values and centre convention; EO values and axis flip; $A_1$ and direction); 443 words | Practice |
| CV-COLINEARITE-002 | Exact invariance of all image points under $(c,Z_0,Z)\to k(c,Z_0,Z)$ with parallel axes, rolls and varied distances: project derivation, verified exactly with fractions (B1–B5); separability when heights are observed with a common offset (B6). Convergence, rolls and "maximum possible imaging scale variation": Remondino and Fraser 2006, §5. 30–45° cone: Triggs et al. 2000, §11. Tilted images improve heights in a simulated block: Hastedt and Luhmann 2015, §4. $\sigma(c)$ values: constructed covariance analysis (D3–D4) | Reasoning: why a free parameter is unobservable and which acquisition breaks it. Distinct from CV-SVD (single-view $(f,Z)$ coupling) and CV-ZHANG-003/006 (known planar target). Related to CV-AEROTRIANGULATION-003 (doming, radial distortion with nadir blocks), whose mechanism differs | 3 criteria (computation and null direction; why distances, rolls and the lateral bar fail, effect on depths; acquisition fix); 455 words | Reasoning |
| CV-COLINEARITE-003 | Decentring "invariably strongly projectively coupled" with the principal point, growing with focal length, reduced by 3D arrays and convergence: confirmed, Remondino and Fraser 2006, §4.2. Orthogonal rolls "must be present to break the projective coupling between IO and EO": confirmed, §5. Planar network without rolls "essentially singular", any plausible principal point with RMSE 0.57–0.63 µm, $P_1,P_2$ making no difference: confirmed, §6.2. Dropping decentring changes the principal point: confirmed, Hastedt and Luhmann 2015, §3.3. OpenCV standard deviations only: calib3d.hpp L1640–L1643, calibration.cpp L562–L571. Network numbers: constructed (D5–D7, D10); decentring equivalence $B_1=-A_1e$: project derivation (C1–C2) | Diagnosis: reading a covariance correctly and choosing the acquisition, a senior calibration task. Distinct from CV-ZHANG-006 (frontal views, known target) and CV-BA-004 (over-free model) | 3 criteria (A defective and why; B's residual correlation expected and why; checks before transfer); 434 words | Diagnosis |
| CV-COLINEARITE-004 | Network rules (convergence, orthogonal rolls, distributed points, $\sqrt n$ gain levelling off near 8 rays): Remondino and Fraser 2006, §5. At least four images per point, covariance as design aid: Triggs et al. 2000, §11. VDI/VDE 2634 practice (160 images, 12 positions, three levels, four rolls, 58 lengths on seven bars): Reznicek et al. 2016, §1–§2.2. 144 images, three scale bars along the main axes, longest test length two-thirds of the diagonal, $LME_{theoretic}=\sqrt{18}\,s$: Hastedt et al. 2018, §3.1–§3.3, eq. 2. Coded targets: Fraser 2006, §3.4, §4. Requirement $s\le0.0118$ mm, 96 images, scale 1:83: constructed (F1–F4) | Design: turning a tolerance into a network, scale and acceptance plan. Distinct from CV-ZHANG-007 (fixed camera, known target, plane inspection) and from CV-AEROTRIANGULATION-004 (aerial control plan) | 3 criteria (geometry; scale and independent lengths; acceptance with the precision requirement); 443 words | Design |
| CV-COLINEARITE-005 | Accuracy, trueness and precision definitions: confirmed, JCGM 200:2012, 2.13–2.15. Relative accuracy up to 100% lower than relative precision: confirmed, Hastedt et al. 2018, §1 (citing Peggs et al. 2009). $\sqrt{18}$ rule with 21 and 34 µm: §3.3, eq. 2. 74.4 µm RMS and −2.27 mm at 28 m, distances too short: §4.3, Tables 5–6 (free network, set III). 40 µm against 4 µm: Reznicek et al. 2016, §2.4, §3.1. Object RMSE as main quality indicator: Remondino and Fraser 2006, §6.1. Terminology warning: Triggs et al. 2000, §10, footnote 20. Card numbers (0.042 mm, 70.5 ppm, 1:14,200): constructed (E1–E7) | Evaluation: separating internal precision from accuracy and identifying a scale error. Shares the principle "independent checks, not internal residuals" with CV-AEROTRIANGULATION-001 (aerial checkpoints against control residuals) but trains the covariance-based expectation, the $\sqrt{18}$ rule and the length-proportional signature; the coordinator should confirm the two objectives stay distinct | 3 criteria (quantified comparison and scale signature; what precision measures; what to report); 431 words | Evaluation |

The front of each card gives every number the answer needs and does not name the mechanism.
The objective of CV-COLINEARITE-001 was narrowed from the suggested "convert $K[R|t]$" to
include the angle convention and the distortion direction, because the centre $-R^\top t$ alone
is already tested by CV-SE3-002. CV-COLINEARITE-003 was turned from "very high correlation
between principal point and decentring" into a comparison of two networks: the constructed
covariance analysis showed that this correlation stays high, or rises, in a network with rolls
(0.82 at 15°, 0.93 at 35°), so a high value is not by itself the defect.

## Reference content and verified claims

- **Collinearity forms.** Fraser's form with $-c$ in the image vector, $R$ from object to image
  and $dx$ on the measured side (Fraser 2006, eqs. 1 and 4, read on the rendered page);
  Hastedt and Luhmann's form with the columns of $R$ in the numerators and $\Delta x'$ added to
  the projection (2015, eq. 1, rendered page). The note states that the same symbol denotes
  inverse matrices in the two sources.
- **IO, APs and their couplings**: Remondino and Fraser 2006, §1, §2, §4.1, §4.2, §5, §6.1–§6.3,
  §7, read in full. MicMac models (RadialBasic, RadialExtended, Fraser, FraserBasic, distortion
  centre, World → Camera direction, inverse coefficients, eq. 15.13): DocMicMac at commit
  501444e, §3.4.3.2, §14.2, §14.3.6, §15.1, §15.2. Metashape model, half-pixel origin, angle
  conventions and correlation report: Metashape 2.2 manual. OpenCV model, iterative inverse,
  standard deviations, `calibrateCameraRO`: OpenCV 4.13.0 sources.
- **Angle convention.** MicMac's exported $R=R_{\omega|X}R_{\varphi|Y}R_{\kappa|Z}\operatorname{diag}(1,-1,-1)$
  and its numerical example (L1–L3) are reproduced to $10^{-7}$ (A15); the transposed reading
  differs by more than 0.1 (A16).
- **Close-range practice and evaluation**: Reznicek et al. 2016, §1–§3.1, §3.6; Hastedt et al.
  2018, §1, §3.1–§3.3, §4.3; Hastedt et al. 2021, §1, §2.3, §3; Triggs et al. 2000, §10, §11;
  VIM 2.13–2.15.

Disagreements and points left open:

1. **Decentring conversion.** Hastedt and Luhmann's Table 1 maps $B_1=P_2/c^2$ and
   $B_2=-P_1/c^2$ with unit 1/mm². With their eq. 5 read in Brown's form,
   $\Delta x'_{\tan}=B_1(r'^2+2x'^2)+2B_2x'y'$, dimensional analysis gives 1/mm and the divisor
   $c$; the check script confirms $B_1=p_2/c$, $B_2=-p_1/c$ by reprojecting through both models
   (A10, agreement to $10^{-8}$ px). The pairing and the signs of the table agree. Eq. 5 as
   printed also shows a cross term $2B_2x'^2y'^2$, presumably a typesetting error. The note
   uses the derived form and points to this report.
2. **Sign of $c$.** Fraser enters $-c$ as the third image coordinate; Hastedt and Luhmann's
   Table 1 gives $c=-f_x\cdot$pixel size for their software (Ax.Ori), whose simulation tables
   list $C_k\approx-14.52$ mm. With a negative $c$, their eq. 1 as printed would mirror the
   image unless their axes or $R$ differ; the text does not resolve this. The note treats the
   sign as a software convention to check.
3. **Image centre.** Hastedt and Luhmann's Table 1 uses $0.5\times$ size for "PhotoScan /
   OpenCV". This matches Metashape's half-pixel origin (App. D), but OpenCV initializes the
   principal point at $(w-1)/2$; the two conventions differ by half a pixel (2 µm in the
   card's example). The note presents both.
4. **Coefficient names.** Metashape 2.2's $P_1$ multiplies $(r^2+2x^2)$ in $x$, the term that
   OpenCV 4.13 calls $p_2$ (A12).
5. **Labels in sources.** Remondino and Fraser caption their comparison table "Table 1" but
   cite it as "Table 2". In DocMicMac §14.2, subsection 14.2.1 ("Internal orientation")
   describes angles and 14.2.2 ("External orientation") describes calibrations in mm; the
   note cites §14.2 as a whole.
6. **Two flying heights.** CV-AEROTRIANGULATION cites Heipke et al. 2001: $c$ and a GNSS
   height shift can be separated only with two flying heights. This does not contradict the
   statement here that varied distances do not separate $c$ in a free network: with observed
   camera heights the ambiguity is $c$ against a constant offset, which two heights break
   (B6); with free camera positions it is a depth stretch, which they do not (B5). The note
   now states both cases.

No existing reference was found to be wrong. CV-BA's citation of Triggs et al. §11 matches
the passage read here, and CV-SVD's single-view $(f,Z)$ example is consistent with worked
example B. No existing file was edited.

## Constructed examples

All are recomputed by `checks/151-colinearite-autocalibration.py` (stdlib, fractions where
practical; about 7 s).

- **A** (A1–A16): conversion of a 6000 × 4000 px OpenCV camera ($c=24.000$ mm, $x'_0=+0.044$,
  $y'_0=+0.056$ mm, $A_1=-1.04\cdot10^{-4}$ mm$^{-2}$, $B_1,B_2$), nadir and tilted poses,
  identical reprojection through OpenCV, photogrammetric and Metashape models, direction error
  (−0.180 mm against −0.360 mm at $r=12$ mm), MicMac angle example.
- **B** (B1–B6): exact $c$–depth invariance (6.000 mm; 7.5 mm with free relief; −18.5 µm with
  known relief), exact invariance over parallel cameras with rolls and distances, separability
  with observed heights.
- **C** (C1–C2): offset distortion centre as decentring, 3.364 µm exact against 3.375 µm.
- **D** (D1–D10): first-order covariance analysis of a constructed free network (117 targets
  on a flat array, eight stations, numerical Jacobian, Schur elimination of points, minimal
  datum). Parallel networks are singular; $\sigma(c)$ = 17.8, 2.69, 0.84 µm at 5°, 15°, 35°
  without rolls and 18.8, 2.80, 0.89 µm with rolls; at 15°, $\sigma(x_p)$ = 15.2 µm without rolls
  and 1.00 µm with rolls; with the target coordinates fixed, 1.08 against 0.99 µm. D9 checks
  that $\sigma(x_p)$ does not depend on the chosen minimal datum. No images were generated or
  adjusted; the values depend on the constructed geometry and are not general results.
- **E** (E1–E10): precision against check lengths (0.042 mm expected, 0.105 mm observed, 70.5
  ppm trend) and the cited values of Hastedt et al. 2018.
- **F** (F1–F4): design numbers.

## Proposals

Not registered in `docs/revues/propositions.md`; for the coordinator and the learner.

1. **Comparison**: compare a distortion-direction model and a correction-direction model of
   the same lens, and the error of an approximate inverse at the image edge (OpenCV's iterative
   `undistortPoints`, five iterations by default; MicMac's inverse coefficients with one more
   degree). Sources: calib3d.hpp L4003, L4026; DocMicMac §15.2.3.
2. **Understanding**: explain why the interior-orientation covariance is invariant to the
   minimal datum while object-point covariances depend on it, and what that means for
   reporting precision (inner constraints against control). Sources: Remondino and Fraser
   2006, §4.1; Triggs et al. 2000, §9; Hastedt et al. 2018, §4.3; check D9.

## Sources

Scientific sources (PDF text extracted with pypdf; equations and tables checked on rendered
page images where the extraction was garbled):

- Remondino and Fraser 2006, IAPRS XXXVI-5, pp. 266–272, ISPRS PDF `REMO_616.pdf`: full text.
- Fraser 2006, Evolution of network orientation procedures, IAPRS XXXVI-5, pp. 114–120, ISPRS
  PDF `FRAS_611.pdf`: §1–§4, eqs. 1, 2, 4, 5 on rendered pages.
- Hastedt and Luhmann 2015, ISPRS Archives XL-1/W4, pp. 321–328: full text; eqs. 1–6 and
  Table 1 on rendered pages.
- Hastedt, Rofallski, Luhmann, Rosenbauer, Ochsner and Rieke-Zapp 2018, ISPRS Archives XLII-2,
  pp. 441–448: §1, §3.1–§3.3, §4.3, Tables 2–3, 5–6.
- Reznicek, Luhmann and Jepping 2016, ISPRS Archives XLI-B5, pp. 107–113: §1–§3.1, §3.6.
- Hastedt, Luhmann, Przybilla and Rofallski 2021, ISPRS Archives XLIII-B2-2021, pp. 17–24:
  §1, §2.1–§2.3, §3 (beginning).
- Triggs, McLauchlan, Hartley and Fitzgibbon 2000, HAL inria-00548290: §10 (introduction,
  footnote 20, §10.3), §11.

Implementation sources and standards:

- OpenCV 4.13.0 (GitHub raw at tag `4.13.0`): `modules/calib3d/include/opencv2/calib3d.hpp`
  L56–L330, L1640–L1660, L1744–L1800, L3990–L4031;
  `modules/calib3d/src/calibration.cpp` L75–L85, L555–L575.
- Agisoft Metashape Professional Edition 2.2 user manual (agisoft.com PDF, publication date
  2025): pp. 29, 36–37, 90, 98, Appendix D pp. 242–244. The 2.1 manual was downloaded but not
  used.
- MicMac documentation, `DocMicMac.pdf` in `micmacIGN/Documentation` at commit
  `501444edf00862939b400b1f7096cd6ea87c8e8a` (last commit touching the file, 2022-07-06):
  pp. 52, 247–249, 256–257, 259–264.
- JCGM 200:2012 (VIM), BIPM PDF: 2.13–2.15.

Failed access (not cited for unread passages):

- Brown 1971, Close-range camera calibration, and Brown 1966, Decentering distortion of
  lenses: ASPRS archive URLs returned HTTP 404; no open copy found. A retry with a browser
  user agent was refused by the permission system and not pursued.
- Fraser 1980 (PE&RS): ASPRS URL returned HTTP 404 to curl.
- Luhmann, Fraser and Maas 2016 (ISPRS J. 115): ScienceDirect returned HTTP 403; paywalled.
- Fraser 1997, Digital camera self-calibration (ISPRS J. 52): paywalled, not attempted.
- Fraser 2012 ASPRS conference paper: HTTP 406. Fraser 2013 (PE&RS 79(4)): no open copy found.
- NGA.SIG.0002 frame sensor model profile: not located. VDI/VDE 2634 Part 1 and ISO/TS 19130:
  paywalled, not read; VDI practice is cited through Reznicek et al. 2016 and Hastedt et al.
  2018.

Web search and fetch were used only to locate documents. Context7 was unavailable.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 -I docs/revues/2026-11-16-photogrammetry/checks/151-colinearite-autocalibration.py` | 55 checks passed |
| `python3 scripts/check_vault.py` | OK, no error for these files (150 Markdown documents, 64 references, 318 cards in the shared tree at the time of the run) |
| `python3 scripts/learning_path.py` | OK, 0 errors (64 references, 318 cards) |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/150-photogrammetrie/151-colinearite-autocalibration.md` | 5 cards, no anomaly |
| `grep -n ' $'` on the four files | No trailing whitespace |

No photogrammetric processing was run: the network study is a first-order covariance analysis
of a constructed geometry, and no software (OpenCV, Metashape, MicMac) was executed. The
Obsidian and AnkiDroid renderings, including the Mermaid diagram and the wide tables, were not
verified. Export status: to republish with `paquet-anki`. Agent self-review only, without
independent scientific validation; the learning-path stage, index, catalogue, progress log and
proposal register are left to the coordinator.
