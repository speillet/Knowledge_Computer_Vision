# Review — Data splits, annotations, score calibration and drift — 2026-11-14

## Overview

5 cards audited in `approfondir` mode; the canonical reference body was deepened from
revision 7 to revision 8. Highest severity per card before correction: 0 blocking,
2 important, 3 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is a problem note: does a measured score transfer to deployment, and can
scores be read as probabilities? Geometric camera calibration stays in
[CV-ZHANG](../../../vault/50-calibration-geometrie/references/52-calibration-zhang.md);
remote-sensing acquisition factors in
[CV-IMAGERIES](../../../vault/20-acquisition-images/references/23-imageries-specialisees.md).
The anchor `#cv-fiabilite-004` used by `Poles-metiers.md` targets the card heading,
which is unchanged.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FIABILITE-001 | Neighboring frames share scene, objects and conditions; the split must follow the deployment scenario: confirmed by Kapoor and Narayanan §2.4 (L1.4 duplicates, L3.2 non-independence). Roberts et al. could be checked at abstract level only | Practice: choose a split unit, a recurring senior decision | 1 criterion; 350 → 353 lexical words | "before the diversions and increases" (cropping and augmentation), "decor", "space zone" | Minor | Language fixes; Source line adds Kapoor and Narayanan and qualifies Roberts |
| CV-FIABILITE-002 | Geometric versus score calibration: confirmed (Guo et al. §2 eq. 1 for score calibration; Küppers et al. §3.1 eq. 1 for the detection event). The explanation named the calibration error "CDE" (ECE), called a principal point a "main dot", and wrote "accurancy" | Comparison: disambiguates one word with two technical meanings | 1 criterion; 271 → 278 | Source line contained a garbled label ("cover risk built") | Important | Terminology corrected; Source line cites Guo §2 and §4.2, Küppers §3.1; Zhang's report marked not re-read |
| CV-FIABILITE-003 | Selecting on the test set biases the final estimate: confirmed (Cawley and Talbot, abstract; WILDS §9.3) | Evaluation: protects the final evidence | 1 criterion; 384 → 377 | "perimeter" (scope), "many essays" (trials), "makes it impossible to interpret" (prevents interpreting) | Minor | Language fixes; Source line adds WILDS §9.3 |
| CV-FIABILITE-004 | Season, sensor, bands and label policy can be confounded: consistent with WILDS §3.3 and §4.3.1 (FMoW domains by year and region, worst-region metric). "check tapes" for bands; "per square" for each cell of the 2×2 plan; "Criteria for correction" for grading criteria | Diagnosis: separates shift causes in remote sensing (track E) | 3 criteria; 381 → 376 | Source line had no primary computer-vision source | Minor | Language fixes; Source line adds WILDS FMoW |
| CV-FIABILITE-005 | Displayed confidence is not calibration under shift: confirmed (Ovadia et al. §5). Missing condition: the risk guarantees of selective classification assume i.i.d. test samples (Geifman and El-Yaniv §2, eq. 2). "denies", "critical layers", "entry contract", "two strings" (acquisition chains) | Diagnosis: interprets confidence after a sensor change | 1 criterion; 278 → 295 | Source line cited only Ovadia's summary | Important | i.i.d. condition added to the explanation and the reference appendix; language fixes; Source line cites Ovadia §5 and Geifman §2 |

No expected answer was changed.

## Reference findings

Claims of revision 7 checked: "file separation does not guarantee data independence"
(Kapoor and Narayanan L3.2): confirmed; score calibration as agreement between scores and
frequencies under a protocol (Guo et al. eq. 1): confirmed; uncertainty should be assessed
under relevant change, not inferred from a softmax (Ovadia et al. §5): confirmed; an
adaptive test biases evaluation (Cawley and Talbot): confirmed. No scientific error was
found; the body held one to three sentences per section, with mistranslations ("Establish
whether a system is generalized", "Collect/review annotations have a cost", "lag" for
shift, "Editor: agent"). The 2026-10-30 appendix said "CDE"; corrected to ECE.

New claims verified for revision 8 (main ones): Guo et al. definitions, ECE and MCE with
$(\frac{m-1}{M},\frac{m}{M}]$ bins, reliability diagrams hide bin counts, temperature
scaling fitted on validation NLL leaves the class unchanged, results with 15 bins (§2,
§4.2, §5); Ovadia et al. take-home messages (§5); WILDS mixture model, domain
generalization versus subpopulation shift, FMoW and iWildCam settings, ID-versus-OOD
measurement (§5.1), Table 1 gaps and Table 2 baselines, §9.3–§9.4; Kapoor and Narayanan
leakage taxonomy (§2.4); Geifman and El-Yaniv coverage, selective risk and i.i.d.
assumption (§2); Küppers et al. detection calibration event, precision surrogate, D-ECE
and boundary effect (§1, §3.1); scikit-learn 1.9.1 and SciPy 1.18.1 contracts.

## Reference depth

Body word counts (front matter excluded, H1 included, up to "## Guided reasoning and
proposed checks"; whitespace tokens): 319 → 3,652.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Inputs (acquisition metadata, label policy, scores), deployment scenario, outputs, pipeline role |
| Intuition | Shallow | Developed | Which distribution a split estimates; calibration as frequency of a defined event; constructed line-four illustration; Mermaid protocol flow |
| Prerequisites | Shallow (one link) | Developed | Links to CV-IOU-AP, CV-METRIQUES-TEMPS, CV-METRIQUES-APPLIQUEES, CV-ACQUISITION, CV-IMAGERIES, CV-REPRESENTATIONS, CV-EDGE, CV-ZHANG |
| Assumptions | Shallow | Developed | Leakage taxonomy; within-group dependence; domain mixture; label stability; relative calibration; observability without labels; degenerate cases |
| Procedure | Shallow | Developed | Nine-step pseudocode with the purpose of each step and its source |
| Mathematics | Shallow (no equation) | Developed | Perfect calibration, ECE, MCE, detection calibration, temperature scaling; coverage and selective risk; WILDS mixture; variance inflation derivation; worked examples A (effective sample size), B (ECE binning, event, temperature), C (selection optimism) |
| Parameters | Shallow (list) | Developed | Nine-row table (split unit, folds, stratification, temporal gap, bins, event, calibrator, resampling, monitoring) and a four-step approach |
| Properties | Shallow | Developed | Limits of grouped splits; temperature scaling preserves ranking; calibration under shift (empirical); WILDS gaps; ECE as a binned estimate |
| Cost and implementation | Shallow | Developed | Cost drivers; scikit-learn 1.9.1 split and calibration contracts; SciPy 1.18.1 bootstrap contract and a grouped recipe; execution status |
| Evaluation | Shallow | Developed | Baseline by sequence versus random-frame variation; calibration and shift checks with WILDS ID/OOD guidance |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Eight-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (split axes, nested CV, leave-one-domain-out, calibrators, ensembles, selective prediction); industrial uses labelled as project reasoning; scientific and implementation sources split |

Constructed examples are recomputed by
[`checks/133-donnees-generalisation.py`](checks/133-donnees-generalisation.py)
(10 checks): standard error 0.003 and half-width 0.0059 for 10,000 independent frames;
inflation 60.7, effective size 164.7 and half-width 0.0458 for $\rho=0.3$; effective size
913 for $\rho=0.05$; the variance identity; ECE 0 with 1–2 bins and 0.20 with 5 or 15
bins; ECE 0 versus 0.2 for IoU events 0.5 and 0.75; temperature scaling 0.659 → 0.502 with
the same class; expected maxima 1.8675 (20 draws) and 1.1630 (5 draws) and the
corresponding optimism 0.0177 and 0.0110.

## Applied corrections

- [Reference](../../../vault/130-evaluation-fiabilite/references/133-donnees-generalisation.md),
  revision 7 → 8: body rewritten and deepened as above; appendices corrected identically to
  the cards ("Question of work" → "Working question", "Reference Response" → "Reference
  answer", "decor" → "background", "clues" → "cues", "before the diversions and increases"
  → "before cropping, tiling and augmentation", "Data Dependency Graph" → "Data dependency
  graph", "CDE" → "ECE", "Test became development" → "Test turned into development data",
  "many essays" → "many trials", "check tapes" → "Check bands", "per square" → "per cell",
  "Risk and Coverage" → "Risk and coverage", "denies" → "rejects", "critical layers" →
  "critical strata", "entry contract" → "input contract", "two strings" → "two
  acquisition chains", plus the selective-classification i.i.d. condition); one line that
  Markdown would have parsed as a link definition was reflowed; sources split into
  scientific and implementation sources; closing provenance line replaced. Front matter
  unchanged except `revision`; H1 and the eight `### …CV-FIABILITE-…` headings kept.
- [Cards](../../../vault/130-evaluation-fiabilite/133-donnees-generalisation.md): further
  explanations and blocking errors corrected for language in all five cards;
  CV-FIABILITE-002 terminology ("ECE", "principal point", "accuracy");
  CV-FIABILITE-005 i.i.d. condition added. Source lines now cite exact sections, add
  WILDS, Kapoor and Narayanan, Geifman and El-Yaniv and Küppers et al. where they support
  the card, and qualify Roberts et al. and Zhang's report as not re-read. Expected answers,
  questions, IDs, objectives, families, tags and target deck unchanged.

No other vault file repeats a corrected claim (`rg` for ECE, CDE, temperature scaling,
GroupKFold, leakage). The CV-IMAGERIES card and reference (another subject) cite Roberts
et al. "abstract and Box 1"; this pass could not read Box 1 to confirm or contradict it.

## Proposals

To register as `pending` (the register is a shared file, not edited here):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-FIABILITE-01 | CV-FIABILITE | From sequence length and intra-sequence correlation, compute the effective sample size of a frame-level accuracy and decide whether a two-point difference between two detectors is meaningful | No card trains the uncertainty of scores computed on dependent frames, although every video evaluation needs it | Reasoning; Mathematics, worked example A | 1 card, 3 criteria (inflation $1+(m-1)\rho$; effective size; resample sequences, not frames) | Project derivation; [SciPy 1.18.1 `bootstrap`](https://github.com/scipy/scipy/blob/v1.18.1/scipy/stats/_resampling.py) for the resampling contract |
| P-CV-FIABILITE-02 | CV-FIABILITE | Design an evaluation that separates the effect of a domain shift from differences in test difficulty (OOD test, ID setting evaluated on the test distribution, worst-domain metric) | The design family is absent; no card trains measuring a shift gap correctly | Design; Evaluation | 1 card, 3–4 criteria | [WILDS §5.1–§5.2 and Table 1](https://arxiv.org/abs/2012.07421) |

No defective question was found.

## Sources

Scientific sources, opened at the passages listed:

- Guo et al., [arXiv HTML v2](https://arxiv.org/html/1706.04599v2): §2 (eqs. 1–6),
  §4.2 (eq. 9), §5 ("Calibration Results", "Reliability diagrams").
- Ovadia et al., [arXiv 1906.02530v2](https://arxiv.org/abs/1906.02530) (PDF text):
  abstract, §1, §5.
- Koh et al., WILDS, [arXiv 2012.07421v3](https://arxiv.org/abs/2012.07421) (PDF text):
  §3, §4.3.1, §5.1–§5.4, Tables 1–2, §9.3–§9.4.
- Kapoor and Narayanan, [arXiv 2207.07048v1](https://arxiv.org/abs/2207.07048) (PDF
  text): §2.4.
- Cawley and Talbot, [JMLR 11](https://www.jmlr.org/papers/v11/cawley10a.html): abstract.
- Geifman and El-Yaniv, [arXiv 1705.08500v2](https://arxiv.org/abs/1705.08500) (PDF text):
  §2, eqs. 1–2.
- Küppers et al., [arXiv 2004.13546v1](https://arxiv.org/abs/2004.13546) (PDF text): §1,
  §3.1 eq. 1, D-ECE eq. 14.

Implementation sources:

- [scikit-learn 1.9.1 `model_selection/_split.py`](https://github.com/scikit-learn/scikit-learn/blob/1.9.1/sklearn/model_selection/_split.py)
  and [`calibration.py`](https://github.com/scikit-learn/scikit-learn/blob/1.9.1/sklearn/calibration.py):
  class docstrings at the cited lines; release list from the GitHub API.
- [SciPy 1.18.1 `stats/_resampling.py`](https://github.com/scipy/scipy/blob/v1.18.1/scipy/stats/_resampling.py):
  L300–L400.

Failed accesses and limits:

- Roberts et al. 2017 (Ecography): the Wiley pages returned HTTP 403 and WebFetch refused
  the domain; an author-hosted copy found by search was not read (the session's permission
  check blocked it, and the downloaded file was deleted). Only the abstract-level claims
  reported by the search engine are used, and the note labels them so: **not verifiable**
  in full.
- Zhang 1998 technical report (geometric calibration, card CV-FIABILITE-002) and the ML Test
  Score page: retained links, not re-read in this pass.
- Context7 was not available (scope record); versioned source code replaced it. No code was
  executed apart from the stdlib check script.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards (an intermediate run flagged one line starting with a bracketed citation and a colon; reflowed) |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 260 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/133-donnees-generalisation.py` | 10 checks passed |
| `git diff --check -- vault/130-evaluation-fiabilite/ docs/revues/2026-11-14-reference-depth/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/130-evaluation-fiabilite/133-donnees-generalisation.md` | 5 cards, 278–377 words, no anomaly |
| Protected-field comparison with the pre-edit copy | 41 protected card lines identical; front matter identical except `revision: 7` → `8`; H1 and 8 per-card headings unchanged; `$$` and fences balanced |

No model, split or calibration was run; the baseline and variation are protocols, not
results. The Mermaid diagram and tables were not rendered in Obsidian, and AnkiDroid
rendering is unverified. Agent self-review, without independent scientific validation or
measurement of learner proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator: the
correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-FIABILITE revision 8,
CV-FIABILITE-001 to 005, corrections listed above, Agent Claude Code self-review, to
republish with `paquet-anki`) and the proposal register (P-CV-FIABILITE-01,
P-CV-FIABILITE-02).
