# Review –  Kalman, EKF, UKF and ESKF for merger –  2026-10-23

## Overview

Four flashcards audited, plus their reference note. No false statements, but three important ones:

- a UKF source never read since the first review;
- a standardized innovation core without the $\chi^2$ law, which its own source gives;
- a flashcard "diagnosis" without symptoms.

Corrections are applied: reference note in revision 3, IDs and objectives unchanged. The three proposed enrichments were accepted and drafted in revision 4: the subject goes from 4 to 6 flashcards, and CV-FUSION-004 is enriched.

Self-review: Agent Claude Code (`revue-cartes`). Editorial status `redige`.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FUSION-001 | UKF not verifiable so far, then confirmed (Julier and Uhlmann 1997, §3); "ESKF uses an imprecise EKF": Solà applies the prediction and the Jacobian of a EKF to the error | Utile | Net Core | Source marked "to check" from 2026-10-18 | Important | Source read; formulation specified; medium grade/covariance |
| CV-FUSION-002 | Confirmed, but the law of $\chi^2$ and threshold were omitted; "without unity when consistent" imprecise | Strong: the basis of the gating | Nose too vague to “interpret” | Absent link with the DeepSORT gating (CV-ASSOCIATION) | Important | $\chi^2_m$, quantile, feeding DeepSORT, on/under-trust |
| CV-FUSION-003 | Confirmed (Solà, eq. 285 – 288) | Forte | Front in "why not... not" that directs; no symptoms for a flashcard diagnosis | Agreement reference note | Important | Symptom, discriminant test, $G\approx I$ |
| CV-FUSION-004 | Confirmed (Solà, §5.4, Annex E) | Utile | A camera slows down | Agreement reference note | Minor | Proposed enrichment rather than correction |

## Corrections applied

- `vault/10-mathematiques-estimation/references/13-kalman-ekf-eskf.md`, revision 3:
  - UKF and its precision order;
  - ESKF described according to Solà equations;
  - $\chi^2$ and quantiles recalculated;
  - threshold of DeepSORT;
  - $G$ and practice $G=I$;
  - Sources specified by equation.
- `vault/10-mathematiques-estimation/13-kalman-ekf-eskf.md`: CV-FUSION-001, 002 and 003 fixed; link arXiv PDF replaced by summary page in 004.
- Journal: Three lines.

`grep` on the former reference Julier and Uhlmann 2004: no other active occurrence in the vault.

## Enrichments accepted and applied

All accepted on 2026-10-23:

- **CV-FUSION-005**, why the ESKF;
- **CV-FUSION-006**, form of Joseph;
- **CV-FUSION-004**, enriched. Reasoning of the project: at 200 Hz, the propagation step IMU does not depend on the camera rate. The flashcard therefore targets the real traps: fixed-step propagation, lost IMU samples and dated image upon receipt.

Unified notation on $R$; Solà note $V$ the measurement covariance. The total goes from 240 to 242 flashcards; current state counters are updated.

Table of proposals as submitted:

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| CV-FUSION-005: why an error-state formulation for orientation IMU: minimal error, always close to origin, small, slow | The "why" of the ESKF is not questioned anywhere, while it structures all the VIO filters | reasoning | 1 flashcard; core to 3 or 4 points | Solà, §5.1 |
| CV-FUSION-006: covariance that loses symmetry or defines positivity; unstable $(I-KH)P$ form, symmetric or Joseph form | Frequent implementation bug, no flashcard | diagnosis | 1 flashcard; core at 3 points | Solà, §6.1, note 26 |
| CV-FUSION-004: effect of the actual $\Delta t$ on each covariance term; acquisition timestamp and not reception timestamp; late measurements | flashcard fair but generic | practice, enrichment of the flashcard | No new reminders | Solà, §5.4.2, eq. 262 – 265, and Annex E, eq. 440: exponential, quadratic, linear |
| reference note: update shapes from $P$, dependence on $\Delta t$, advantages of ESKF | Topics Cost and Thin Settings | reference note | without flashcard | The same sources |

## Sources

- [Solà, Quaternion kinetics for the error-state Kalman filter](https://arxiv.org/abs/1711.02508), PDF v1 read in full text:
  - §5.1, four advantages;
  - §5.2 ;
  - §5.4.2, eq. 262 – 265;
  - §6.1, eq. 272 – 278 and note 26 on the form of Joseph;
  - §6.3, eq. 284 – 288, and "G = I18" in most implementations;
  - Annex E, Eq. 438 – 442.
- [Gamse, Nobakht-Ersi and Sharifi 2014, Sensors 14(10)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4239867/): §2.2.2, eq. 5 – 10; §3.4.2, $m=3$, $\alpha=0{,}05$, threshold 7,815.
- [Julier and Uhlmann 1997, SPIE 3068](https://doi.org/10.1117/12.280797), §3, eq. 12 – 14. DOI verified by redirection to SPIE; text read on a course copy hosted by Berkeley.
- [Wojke, Bewley and Paulus 2017, DeepSORT](https://arxiv.org/abs/1703.07402), §2.2: threshold 9,4877.
- Quantiles of the $\chi^2$ recalculated with SciPy 1.13.1.
- Julier and Uhlmann 2004, Proceedings of the IEEE. He is no longer quoted.

## Checks and limitations

`check_vault.py` OK (240 flashcards) after corrections, then 242 flashcards after additions, 34 tests passed, catalog regenerated and then updated. The inventory compared to the initial state shows only the added IDs. Context7 is not available in this session. Not verified: export Anki, rendering Obsidian and AnkiDroid, mastering, independent validation.
