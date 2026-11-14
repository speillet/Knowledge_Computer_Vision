# Review — Metrics for segmentation, inspection and applications — 2026-11-14

## Overview

4 cards audited in `approfondir` mode; the canonical reference body was deepened from
revision 6 to revision 7. Highest severity per card before correction: 0 blocking,
1 important, 3 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is a metric-selection and protocol note. Text-recognition rates stay in
[CV-OCR](../../../vault/70-reconnaissance-representations/references/74-ocr-documents.md),
biometric error rates in
[CV-BIOMETRIE](../../../vault/70-reconnaissance-representations/references/75-embeddings-biometrie.md),
physical units for anisotropic data in
[CV-IMAGERIES](../../../vault/20-acquisition-images/references/23-imageries-specialisees.md)
and anomaly-detection methods in
[CV-INSPECTION](../../../vault/70-reconnaissance-representations/references/73-patchcore-padim.md),
which points to this note for AUROC, PRO and their aggregation.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-METRIQUES-APPLIQUEES-001 | Dice measures overlap, HD95 a percentile boundary distance in physical units when spacing is applied: confirmed (Metrics Reloaded SemS recommendations and DG7.3; Reinke et al. Fig. 4a, Fig. 5c). The 2026-11-08 warning about pooled versus directed percentiles is confirmed by MONAI 1.6.1, which takes the maximum of the directed percentiles | Comparison: overlap versus boundary error | 1 criterion; 356 → 359 lexical words | "Covering … weighted", "unity", "borders"; the objective line reads "Distinguish between border and border" (French: *recouvrement et frontière*), a protected line | Minor | Language fixes; Source line cites exact passages and the MONAI lines; objective defect reported |
| CV-METRIQUES-APPLIQUEES-002 | Background or large defects dominate pixel aggregates; PRO weighs regions equally and its FPR range must be stated: confirmed (MVTec AD 2 §IV-B1 eq. 1, Fig. 4; limits 0.30 and 0.05). "Measure default recall" read *défaut* as "default" instead of defect; "release rate" for reject rate | Evaluation: region- and part-level inspection metrics | 1 criterion; 354 → 351 | "flaw", "piece", "balance sheet" | Important | Meaning-restoring fixes in the explanation; Source line cites §IV-B1 and §IV-B2 |
| CV-METRIQUES-APPLIQUEES-003 | Reprojection RMS does not establish repeatability, reproducibility or absence of bias: confirmed (NIST §2.4.1, §2.4.4.1, §2.4.4.2, §2.4.5: calibration "may not assure that the gauge reacts properly in its working environment") | Diagnosis: separates camera calibration from measurement qualification | 1 criterion; 352 → 355 | "assembly" (fixturing), "Protocol built", "millimeter warranty" | Minor | Language fixes; Source line labels NIST sections, §2.4.4.3 marked not re-read |
| CV-METRIQUES-APPLIQUEES-004 | Empty references or predictions need a declared convention: confirmed (Reinke et al. P2.3–P2.4, P3.2). Missing condition: libraries already encode one (MONAI 1.6.1: Dice NaN for an empty reference with `ignore_empty=True`, infinite Hausdorff distance for one empty mask, NaN for two, reductions over non-NaN values) | Practice: empty-case policy | 1 criterion; 356 → 405 | "indefinite", "digital trick" (numerical trick) | Minor | Library-default condition added; language fixes; Source line adds MONAI lines |

No expected answer was changed.

## Reference findings

Claims of revision 6 checked: Dice $=2TP/(2TP+FP+FN)$, HD95 needs surfaces, units and
direction conventions, PRO weights regions and AU-PRO needs an FPR range, metrology
separates bias, repeatability, reproducibility and stability: all confirmed (Reinke et al.;
Maier-Hein et al.; MVTec AD 2 §IV-B1; NIST §2.4.1). No scientific error was found; the body
was shallow and mistranslated ("unity", "Covering", "a RMS pixel camera is not a dimensional
uncertainty", "Editor: agent").

New claims verified for revision 7 (main ones): category errors and boundary-unaware overlap
(Reinke et al. Fig. 3, Fig. 4a), size and reference-outlier pitfalls (P2.2, P2.3), empty
outputs (P2.4), non-standard boundary extraction (P3.1), global-pixel aggregation (P3.2);
per-image aggregation, Dice as pixel $F_1$, overlap plus boundary recommendation, NSD for
imprecise annotations, clDice for tubular structures, invalid TN-based metrics in detection,
HD versus percentile HD (Metrics Reloaded); PRO equation, FPR limits, the 25,000× figure,
threshold rule, image score and saturation (MVTec AD 2 §I, §IV-B); Elkan's two-class
decision rule and "one degree of freedom" remark (§1.3); NIST definitions; MONAI 1.6.1
conventions.

Source disagreement recorded in the note (FR-036):

| Aspect | Convention A | Convention B |
| --- | --- | --- |
| HD95 | 95th percentile of the pooled distances of both directions | Maximum of the two directed 95th percentiles (MONAI 1.6.1, `hausdorff_distance.py` L224–L249); worked example C gives 0 px versus 10 px |
| Boundary extraction for NSD | Edge pixels (MONAI default) | Local surface elements (DeepMind `surface-distance`), as noted in MONAI's docstring |

## Reference depth

Body word counts (front matter excluded, H1 included, up to "## Guided reasoning and
proposed checks"; whitespace tokens): 325 → 3,667. CER, WER and biometric rates were linked
to their notes rather than restated.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Unit of assessment; inputs with shapes, spacing and anomaly-map scale; outputs per case, aggregate and special-case counts; pipeline roles |
| Intuition | Shallow | Developed | One question per metric; constructed aggregation illustration; Mermaid data flow of an inspection evaluation |
| Prerequisites | Shallow (two links) | Developed | Links to CV-INSPECTION, CV-IMAGERIES, CV-ZHANG, CV-OCR, CV-BIOMETRIE, CV-FIABILITE |
| Assumptions | Shallow | Developed | Problem category, reference quality, shared geometry, existence of true negatives, hierarchical data; empty-case policies of MONAI; observability limits |
| Procedure | Shallow | Developed | Seven-step pseudocode with the purpose of each step |
| Mathematics | Shallow (three formulas) | Developed | Dice, IoU and their relation; HD, HD95 conventions, NSD; PRO and AU-PRO with thresholds; cost-derived threshold; gauge-study definitions and propagation; worked examples A–E |
| Parameters | Shallow (list) | Developed | Eleven-row table and a three-step approach |
| Properties | Shallow | Developed | Overlap, HD, HD95, NSD, PRO, threshold-free areas, saturation, calibration versus working-environment bias |
| Cost and implementation | Shallow (two sentences) | Developed | Cost drivers; MONAI 1.6.1 contracts (Hausdorff, surface distance, Dice, NSD); execution status |
| Evaluation | Shallow | Developed | Metric-code validation with synthetic cases; baseline and FPR-limit variation with expected effect and limits |
| Failure modes and diagnosis | Shallow (one sentence) | Developed | Eight-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (Dice/NSD/HD95/HD, instance metrics, AU-PRO versus part-level rates, cost thresholds, gauge studies); industrial uses labelled as project reasoning; scientific and implementation sources split |

Constructed examples are recomputed by
[`checks/134-metriques-applications.py`](checks/134-metriques-applications.py) (11 checks):
per-image Dice 0.95 and 0, mean 0.475, pooled 0.9453, Dice–IoU identity, 99-empty-case mean
0.99; pixel TPR 0.899 versus PRO 0.45; 250,000 false-positive pixels and the 25,000 ratio;
HD95 of 10 px (max of directed) versus 0 px (pooled), 5 mm at 0.5 mm/px; cost threshold
$1/51=0.0196$ and its indifference identity; $L=10$ mm, $\sigma_L=0.0427$ mm, 88% scale share.

## Applied corrections

- [Reference](../../../vault/130-evaluation-fiabilite/references/134-metriques-applications.md),
  revision 6 → 7: body rewritten and deepened as above; appendices corrected identically to
  the cards ("Question of work" → "Working question", "Reference Response" → "Reference
  answer", "Example of Divergence" → "Example of divergence", "Covering and a surface
  distance weighted this gap" → "Overlap and a surface distance weigh this deviation",
  "unity" → "unit", "Link and difference of units" → "Relation and difference of units",
  "fault" → "defect", "Completing by decision by part" → "Adding part-level decisions",
  "plane geometry and a scale adapted" → "planar geometry and a suitable scale", "Choice of
  proposed protocol" → "Proposed protocol choice", "digital trick" → "numerical trick"); one line that
  Markdown would have parsed as a link definition was reflowed; sources split into
  scientific and implementation sources; closing provenance line replaced. Front matter
  unchanged except `revision`; H1 and the eight `### …CV-METRIQUES-APPLIQUEES-…` headings kept.
- [Cards](../../../vault/130-evaluation-fiabilite/134-metriques-applications.md): further
  explanations and blocking errors corrected for language in all four cards;
  CV-METRIQUES-APPLIQUEES-002 "default recall" → "defect recall", "release rate" → "reject
  rate"; CV-METRIQUES-APPLIQUEES-004 library-default condition added. Source lines cite the
  arXiv versions with sections, MONAI lines and NIST sections, and label project
  constructions. Expected answers, questions, IDs, objectives, families, tags and target deck
  unchanged.

No other vault file repeats a corrected claim (`rg` for HD95, AU-PRO, PRO, Dice). The
CV-IMAGERIES reference (another subject) quotes HD95 as "designed to deal with spatial
outliers" from Reinke et al. Fig. 5c; this pass found that wording in the Metrics Reloaded
Extended Data Fig. SN 2.23 caption and did not re-read Reinke Fig. 5c's full caption, so no
error is claimed.

## Proposals

To register as `pending` (the register is a shared file, not edited here):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-METRIQUES-APPLIQUEES-01 | CV-METRIQUES-APPLIQUEES | Derive a reject threshold from the costs of a shipped defect and a false reject, and state why it requires calibrated probabilities on the deployment population | No card trains cost-based operating points, although inspection acceptance depends on them | Reasoning; Mathematics, worked example D | 1 card, 3 criteria ($p^*=c_{FP}/(c_{FP}+c_{FN})$; only the ratio matters; calibration needed) | [Elkan 2001, §1.3](https://cseweb.ucsd.edu/~elkan/rescale.pdf) |
| P-CV-METRIQUES-APPLIQUEES-02 | CV-METRIQUES-APPLIQUEES | Design a gauge study for a vision length measurement (artifacts, repetitions, days, operators, configurations) that separates bias, repeatability and reproducibility | Card 003 diagnoses the misuse of reprojection RMS; no card trains the study design (design family absent) | Design; Mathematics (measurement uncertainty) | 1 card, 4 criteria | [NIST/SEMATECH e-Handbook §2.4.1–§2.4.5](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc4.htm) |

Protected-line defects (not edited; for the coordinator): the objective of
CV-METRIQUES-APPLIQUEES-001 reads "Distinguish between border and border"; proposed wording
"Distinguish overlap from boundary error" (French source: *distinguer recouvrement et
frontière*). The objective of CV-METRIQUES-APPLIQUEES-002 "Measure the small flaws" would read
better as "Measure small defects". No defective question was found.

## Sources

Scientific sources, opened at the passages listed:

- Reinke et al., [arXiv HTML v4](https://arxiv.org/html/2302.01790v4): P1–P3 sections,
  Fig. 3–5 captions, P3.1, P3.2, Suppl. Note 1.2.
- Maier-Hein et al., Metrics Reloaded, [arXiv HTML v8](https://arxiv.org/html/2206.01653v8):
  "Semantic segmentation (SemS)" and object-detection recommendations, Suppl. Note 2.7.6
  (DG7.3) and Extended Data Fig. SN 2.23 caption.
- Heckler-Kram et al., MVTec AD 2, [arXiv HTML v1](https://arxiv.org/abs/2503.21622v1): abstract,
  §I and Table I, §IV-B1 (eq. 1, Fig. 4 and 5 captions), §IV-B2.
- Elkan 2001, [PDF](https://cseweb.ucsd.edu/~elkan/rescale.pdf), §1.3: the section text was
  readable but the formula was garbled by PDF extraction; the threshold is re-derived in the
  note and labelled as a project derivation.
- NIST/SEMATECH e-Handbook: [§2.4](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc4.htm),
  §2.4.1, §2.4.4.1, §2.4.4.2, §2.4.5 (HTML pages fetched; §2.4.4.3 not re-read).

Implementation sources:

- [MONAI 1.6.1](https://github.com/Project-MONAI/MONAI/tree/1.6.1/monai/metrics) (release
  list from the GitHub API): `hausdorff_distance.py` (read in full), `utils.py` L300–L481,
  `meandice.py` L30–L131, `surface_dice.py` L30–L190.

Not executed: MONAI or any metric library; the check script uses only the standard library.
Context7 was not available (scope record). Not re-verified: the TorchMetrics default reported by
Reinke et al. (stated in the note as reported by them); Nikolov et al.'s NSD paper (definition
taken from MONAI's documented equation).

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards (an intermediate run flagged one line starting with a bracketed citation and a colon; reflowed) |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 260 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/134-metriques-applications.py` | 11 checks passed |
| `git diff --check -- vault/130-evaluation-fiabilite/ docs/revues/2026-11-14-reference-depth/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/130-evaluation-fiabilite/134-metriques-applications.md` | 4 cards, 351–405 words, no anomaly |
| Protected-field comparison with the pre-edit copy | 33 protected card lines identical; front matter identical except `revision: 6` → `7`; H1 and 8 per-card headings unchanged; `$$` and fences balanced |

No model, metric library or gauge study was run; the baseline and variation are protocols, not
results. The Mermaid diagram and tables were not rendered in Obsidian, and AnkiDroid rendering is
unverified. Agent self-review, without independent scientific validation or measurement of learner
proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator: the
correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-METRIQUES-APPLIQUEES
revision 7, CV-METRIQUES-APPLIQUEES-001 to 004, corrections listed above, Agent Claude Code
self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-METRIQUES-APPLIQUEES-01, P-CV-METRIQUES-APPLIQUEES-02).
