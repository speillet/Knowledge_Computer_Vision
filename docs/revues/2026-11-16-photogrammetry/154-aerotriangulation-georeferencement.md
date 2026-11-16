# Creation — Aerotriangulation and georeferencing: ground control, GNSS/IMU and accuracy — 2026-11-16

## Overview

Mode: creation of a new reference note and five new cards for domain d15 (not a
`revue-cartes` pass; its card format, verification standard and report conventions are
reused). Reference `CV-AEROTRIANGULATION`, revision 1, `statut: redige`, tracks B and E,
depth `approfondissement`, prerequisites CV-BA, CV-MULTICALIB, CV-SFM and CV-GEODESIE.

Five cards, CV-AEROTRIANGULATION-001 to -005, in five families: evaluation, reasoning,
diagnosis, design and comparison. Answer lengths: 485, 439, 437, 451 and 453 lexical words
(minimum 437, median 451, maximum 485), counted by the inventory script; the count flags short
answers and does not measure their quality. Self-review: Agent Claude Code. No independent
scientific validation.

Files created:

- `vault/150-photogrammetrie/references/154-aerotriangulation-georeferencement.md` (573 lines,
  wrapped at about 95 characters);
- `vault/150-photogrammetrie/154-aerotriangulation-georeferencement.md`;
- `docs/revues/2026-11-16-photogrammetry/checks/154-aerotriangulation-georeferencement.py`;
- this report.

## Cards

| Card | Accuracy: central claims, verdict and exact passage | Relevance | Gradability: criteria and lexical words | Family |
| --- | --- | --- | --- | --- |
| CV-AEROTRIANGULATION-001 | RMSE per axis, radial $\mathrm{RMSE}_H$, survey component added in Edition 2, mean error below 25% of target, blunder at three times the target, 30-checkpoint minimum and reduced-checkpoint statement: confirmed in ASPRS Ed. 2 V2 (2024) §7.2, §7.12.1–§7.12.4, §7.13–§7.14, §7.16.1. Fitted residuals biased low and redundancy numbers summing to $n_z-n_x$: confirmed in Triggs et al. §10.1 and §10.4. Check-point z-error standard deviation seven times that of control points: confirmed in James and Robson 2014, Discussion (citing Javernick et al. 2014, not read). Checkpoint values, the redundancy case ($r=0.1$, ratio 10) and the 28% sampling uncertainty: project constructions, recomputed | Evaluation: separates fitted control residuals from independent accuracy, and RMSE compliance from bias; a frequent acceptance error in production | 3 criteria (ASPRS numbers with survey term; why control residuals are uninformative; non-compliance from mean error and checkpoint count); 485 words | Evaluation |
| CV-AEROTRIANGULATION-002 | Extrapolation and lack of redundancy in direct georeferencing: Heipke et al. 2001 §1 and §4. Boresight error growing with altitude: ASPRS Add. III §K. Misalignment differences of about $1.5\cdot10^{-3}$° giving about 5 cm at 2,000 m: Cramer et al. 2000 §3.4.1 (recomputed 0.052 m). Unresolved mid-exposure pulse visible as horizontal shift after adjusting for flight direction: ASPRS Add. V §A.4.2. Principal point x versus timing and focal length versus GNSS Z equivalences: Heipke et al. 2001 §4. Budget values, sign analysis and pitch-boresight-versus-latency separation: project derivations, recomputed | Reasoning: turns a calibration report into ground errors and predicts their signatures; distinct from CV-MULTICALIB-003 (camera–LiDAR contracts) and from the generic delay-versus-translation argument, which it links | 3 criteria (four magnitudes and combination; scaling and sign flips; constant offsets needing ground control); 439 words | Reasoning |
| CV-AEROTRIANGULATION-003 | Correlation of radial distortion and surface form in parallel-axis networks, convergence to a wrong radial term under noise, dome of about 0.2 m over about 100 m with 2° angle variation and no control, no significant gain from extra lines at another heading, reduction by one to two orders of magnitude with oblique images (20° banked turns, 30° tiltable camera), K1-bracketing reprocessing, partial persistence with control depending on weights: confirmed in James and Robson 2014, Results (idealized parallel geometries; sensitivity to variability; practical flight plans; optimized processing), Discussion and Conclusions, Fig. 5. Dome-shaped errors with GCPs only on a flat moorland: Przybilla et al. 2020 §3.2.1. Radial fit ($15.6-3.9\cdot10^{-4}r^2$, $R^2=0.98$) and stereo-pair closed form: project constructions, recomputed in exact fractions | Diagnosis: reads a spatial error signature, names the mechanism and chooses a discriminating test before a remedy | 3 criteria (pattern; cause; confirmation and remedy); 437 words | Diagnosis |
| CV-AEROTRIANGULATION-004 | GCPs at twice the product accuracy, checkpoints at least twice as accurate, AT at half the product RMSE, 3D perimeter plus interior height control for a conventional block, control at or beyond the boundary, no empirical absolute rule for UAS GCP numbers, 30 checkpoints up to 1,000 km², vertical checkpoints on open flat ground: confirmed in ASPRS §7.9–§7.10, §7.13–§7.14, Table C.1, Add. III §F.4, Add. V §A.5.9, §A.7.1. RTK-only height errors up to 30 GSD, one central GCP reducing systematic height deviations to about 15–30 mm, RTK plus four corner GCPs within the GSD, four corner GCPs alone 15–30 GSD in height, badly distributed GCPs increasing XY errors, ellipsoidal RTK heights: confirmed in Przybilla et al. 2020 abstract, §2.1, §2.2.2, §4 (Table 3). Budget $\sqrt{5^2-2.5^2}=4.33$ cm: project derivation, recomputed | Design: a complete control and checkpoint plan with a quantified survey budget and the RTK change | 3 criteria (accuracy budget; layout without and with RTK; checkpoint plan); 451 words | Design |
| CV-AEROTRIANGULATION-005 | Indirect orientation absorbing systematic errors into physically wrong EO (EO changing 10 cm to 10 m): Cramer et al. 2000 §2.1, Table 2. Cali10 RMS 4.2/5.3/9.0, 16.6/18.6/23.2 and 5.5/7.3/6.0 cm and the need for at least one GCP for the vertical offset: Cramer and Stallmann 2001 §4.2–§4.4, Table 1. Direct georeferencing 2–3 times less accurate, y-parallax, no redundancy: Heipke et al. 2001 §4–§5. Direct georeferencing not best practice for highly accurate products: ASPRS Add. III §G. UAS IMUs navigation-grade: ASPRS Add. V §A.4.4. Horizontal combinations 6.8, 24.9 and 9.1 cm: recomputed | Comparison: one coherent objective, the trade-off between control, redundancy and system calibration that decides how a block is oriented | 3 criteria (one per route, each with datum, error handling, control and relative accuracy) plus a choice rule; 453 words | Comparison |

## Reference content and verified claims

The note asserts, on these sources:

- Definitions of indirect, direct and integrated orientation, interpolation versus
  extrapolation, strips needing GCPs for the roll about the flight axis, the Cartesian-frame
  requirement, the OEEPE phase I accuracies, the principal-point–timing and focal-length–GNSS-Z
  equivalences, and the recommendation to recalibrate before and after blocks [Heipke et al.
  2001, §1, §4, §5].
- The correlation of self-calibration with EO, the $c$–$Z_0$ 100% correlation and the 9 m
  example, lever arms and misalignment, interpolation to exposure times and the combined
  adjustment results [Cramer et al. 2000, §2.1–§2.2, §3.4–§3.5, Tables 1–6].
- The direct georeferencing equation with boresight, the navigation-to-photogrammetric angle
  conversion, offset and drift terms, the 20 µm / 20 cm relation, the Cali10 table and the
  conclusion that constant shifts and vertical offsets are undetectable without ground
  information [Cramer and Stallmann 2001, §2.2–§2.4, §4.2–§4.4, Table 1].
- Doming, its mechanism and mitigations [James and Robson 2014].
- RTK drone results, the DJI lever-arm convention, the 40 cm antenna offset, the $c$–Z
  correlation and the camera residual patterns [Przybilla et al. 2020].
- ASPRS statistics, control and checkpoint requirements, AT acceptance criteria and the
  photogrammetry and UAS addenda [ASPRS 2024].
- Fitted-residual bias and redundancy numbers [Triggs et al. 2000, §10.1, §10.4].
- Tool contracts for COLMAP 4.2.1 and MicMac (documentation only).

Disagreements and oddities found in the sources:

- **ASPRS §7.10, horizontal GCP criterion for projects with elevation products.** The copy read
  prints $\mathrm{RMSE}_{H(GCP)}\le\tfrac12\mathrm{RMSE}_{V(MAP)}$, whereas Addendum III §I says
  that GCPs must meet the same criteria as the AT ($\mathrm{RMSE}_{H}\le\tfrac12\mathrm{RMSE}_{H(MAP)}$),
  and Table B.2 is consistent with the latter. The note and card 004 only state "at most half
  the product RMSE", which holds under both readings when the horizontal and vertical targets
  are equal (5 cm in card 004). Probably a typo in the standard; not resolved.
- **ASPRS Addendum V §A.4 versus §A.4.1.** PPK "requires minimal or no GCPs" while §A.4.1
  "highly recommend[s]" surveyed GCPs; the note reports both.
- **James and Robson 2014, Conclusions** attribute the practical flight plans to Figure 4,
  whereas they are shown in Figure 5; the cards cite by section.
- **James and Robson 2014, Methods**: $K_1=10^{-5}$ mm$^{-2}$ is said to give about 5.5 px of
  distortion in an image corner; with the stated 4000 × 3000 sensor of 5 µm pixels
  (half-diagonal 12.5 mm), $K_1r^3$ gives about 3.9 px. Unresolved (possibly a different
  distortion convention); the value is not used in the note.
- **Attitude standard deviations** for integrated adjustment differ between Cramer et al. 2000
  (0.001°) and Cramer and Stallmann 2001 (0.003°); they come from different data sets and both
  are reported as such.

Consistency with existing references: no contradiction found with CV-BA (fitted residuals,
gauge, overfitting of free parameters), CV-MULTICALIB (delay versus translation, which the
note links rather than repeats; it does not cover aerial boresight, lever-arm or ground-error
budgets, which this note adds) or CV-CAPTEURS (mid-exposure stamping). The sibling CV-SFM cites
the same COLMAP 4.2.1 `model_aligner` lines (faq.rst L410–L448) with the same reading.

## Constructed examples

All recomputed by `checks/154-aerotriangulation-georeferencement.py` (15 checks, stdlib, exact
fractions where practical):

- A: checkpoint statistics, product accuracy with survey error, mean-error and checkpoint-count
  tests (card 001).
- B: redundancy of a control coordinate ($r=0.1$, ratio 10) and of a similarity on four 3D GCPs
  ($\sqrt{5/12}=0.65$).
- C: direct-georeferencing budget, scaling with height, opposite-line discrepancies, heading
  term, drone contrast, and cross-checks of the cited 5 cm, 20 cm and 9 m values (card 002).
- D: stereo-pair doming in closed form checked against explicit projection and parallax
  triangulation in exact fractions; radial least-squares fit of the checkpoint pattern
  (card 003).
- E: control budget $\sqrt{5^2-2.5^2}=4.33$ cm and variants (card 004).
- F: sampling uncertainty of an RMSE from the $\chi_n$ distribution (13% for 30 checkpoints).
- G: horizontal combination of published RMS values (card 005).

## Proposals

Not registered in `docs/revues/propositions.md` (left to the coordinator and the learner):

1. Practice card: a synthetic chain test for importing GNSS/IMU exterior orientations (roll,
   pitch, yaw in a navigation frame to $\omega,\varphi,\kappa$ in a local frame, rotation order,
   lever-arm origin and sign). Sources: Cramer and Stallmann 2001 §2.3 (eq. 2), ASPRS Add. III
   §K, Przybilla et al. 2020 §2.1.
2. Understanding card: why a post-hoc similarity (COLMAP `model_aligner`, MicMac `GCPBascule`)
   cannot remove a block deformation while control inside the adjustment (`pose_prior_mapper`,
   `Campari`) can reduce it. Sources: James and Robson 2014 (3D Surface Models from Photographs,
   Discussion); COLMAP 4.2.1 faq.rst; MicMac documentation at a647a96.

## Sources

Scientific sources (PDF text extracted with pypdf and read at the cited passages):

- Cramer, Stallmann and Haala 2000, IAPRS XXXIII-B3, pp. 198–205, from isprs.org: all sections
  and Tables 1–6.
- Cramer and Stallmann 2001, OEEPE workshop paper, from ifpwww.ifp.uni-stuttgart.de: §1–§6 and
  Table 1.
- Heipke, Jacobsen and Wegmann 2001, Photogrammetric Week 01, pp. 195–204, from
  phowo.ifp.uni-stuttgart.de: all sections and Tables 1–3.
- James and Robson 2014, ESPL 39, 1413–1420, open access, from UCL Discovery: all sections and
  figure captions.
- Przybilla, Bäumker, Luhmann, Hastedt and Eilers 2020, ISPRS Archives XLIII-B1-2020, 485–492,
  from isprs-archives.copernicus.org: all sections and Tables 1–4.
- Triggs, McLauchlan, Hartley and Fitzgibbon 2000, from HAL: §10.1 and §10.4.
- Wegmann, Heipke and Jacobsen 2002, ISPRS Archives XXXV-B1 (Direct sensor orientation based on
  GPS network solutions): abstract and introduction read; not cited.

Implementation sources and standards:

- ASPRS Positional Accuracy Standards for Digital Geospatial Data, Edition 2, Version 2 (2024),
  doi:10.14358/ASPRS.PAS.2024, read in the copy hosted by CNIG (cnig.gouv.fr): Summary of
  Changes, §5–§7.16, App. B.1, C.1–C.7, Addenda III and V.
- COLMAP 4.2.1 (tag commit bd1fcf654d2dd8fefa1466999c190a246f83f4b9), `doc/faq.rst` from GitHub
  raw: L162–L189, L410–L448.
- MicMac documentation repository at commit a647a96b177c2ea047917a22b59aa133464fbc6a,
  `DocMicMac/Generalites/QuickStartSimplified-Tools.tex` from GitHub raw: L1534–L1653,
  L1697–L1722, L1850–L1928. Context7 was not available.

Failed access and claims not established:

- ASPRS official links (publicdocuments.asprs.org, Edition 2 Versions 1 and 2) redirected to a
  Microsoft sign-in page. The 2023 Version 1 text was therefore not read; the note cites the
  2024 Version 2 and does not state what changed between the two versions.
- James et al. 2019, Guidelines on the use of structure-from-motion photogrammetry in
  geomorphic research (ESPL 44): Loughborough repository (HTTP 202, empty body), figshare and
  CORE (HTTP 403), Wiley (HTTP 403), University of Melbourne (HTML page) and Lancaster eprints
  (connection timeout). Not cited.
- Heipke, Jacobsen and Wegmann 2002, analysis of the OEEPE results (OEEPE Official Publication
  No. 43): no open copy located; the phase I paper of 2001 was used, and phase II results are
  cited only through Cramer and Stallmann 2001.
- HAL first returned a bot-check page for Triggs et al.; a second request succeeded. CORE
  returned HTTP 403 for James and Robson 2014; the UCL Discovery copy was read.
- Javernick et al. 2014 was not read; its result is cited only as reported by James and
  Robson 2014.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 -I docs/revues/2026-11-16-photogrammetry/checks/154-aerotriangulation-georeferencement.py` | 15 checks passed |
| `python3 scripts/check_vault.py` | 11 errors for this subject, all "missing local link" to the sibling references `151-colinearite-autocalibration.md` and `153-systemes-reference.md`, not yet written; no other error for these files |
| `python3 scripts/learning_path.py` | Stops with `FileNotFoundError` on the sibling card file `152-sfm-incrementale-globale.md`, still in progress; to rerun once the siblings land |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/150-photogrammetrie/154-aerotriangulation-georeferencement.md` | 5 cards, no anomaly; 485, 439, 437, 451, 453 lexical words |
| `grep -n ' $'` on the four files | No trailing whitespace |

No photogrammetric processing was run and no tool (COLMAP, MicMac) was executed; the tool
contracts rest on documentation at fixed versions. The stereo-pair doming derivation assumes the
normal case, correct orientations and x-parallax only; real self-calibrating blocks behave as
James and Robson simulate, not as this closed form. Obsidian and AnkiDroid rendering of the
cards and of the Mermaid diagram were not verified. Export status: to republish with
`paquet-anki`. The learning path, sections, indexes, catalogue, progress log and proposal
register are left to the coordinator. Possible overlap to check when CV-COLINEARITE lands: its
self-calibration content may also treat the correlation of radial distortion with surface
shape; this subject keeps it as an aerial diagnosis (card 003).

## Coordinator review

The coordinator recomputed the five cards' numbers. One correction was applied to card
002, worked example C and check 7: the question gives a 0.003° boresight error in roll
*and* in pitch, two horizontal components of 0.105 m (across and along track), but the
budget counted one. The root-sum-square is 0.21 m, not 0.18 m; pitch and timing alone give
0.175 m along track. The other values (checkpoint RMSE with survey error, the 5.5 cm mean
bias, the radial fit $15.6-3.9\cdot10^{-4}r^2$ with $R^2=0.98$, the 4.33 cm fit limit) were
confirmed independently.
