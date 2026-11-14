# Review — Edge deployment, compression and monitoring — 2026-11-14

## Overview

4 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 8 to revision 9. Highest severity per card before correction:
0 blocking, 0 important, 4 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the deployment note of the systems topic. Precision and runtimes stay
in [CV-QUANT](../../../vault/140-ingenierie-systemes/references/142-quantification-runtimes.md),
timing and queues in
[CV-PIPELINE](../../../vault/140-ingenierie-systemes/references/141-contrats-profiling-video.md),
drift and evaluation splits in
[CV-FIABILITE](../../../vault/130-evaluation-fiabilite/references/133-donnees-generalisation.md).
Serving frameworks and over-the-air updates remain inventory items APP-128 and
APP-129 and are only named.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-DEPLOIEMENT-001 | $1/0.95\approx1.053$, bound $1/0.9$, cancellation at $c\ge0.05$: recomputed. Amdahl 1967 p. 483 states the sequential-fraction limit in words, not the closed form; the card already labelled the formula as a project derivation, which is correct. Expected answer used French decimal commas ("1/0,95 = 1,053×", with "=" for an approximation) and "depending on Amdahl model announced" | Reasoning: bounding a system gain before optimizing | 1 criterion; 277 → 273 lexical words | Decimal commas in explanation and source line | Minor | Expected answer and explanation language fixed; source line notes that the paper states the limit in words; TensorRT link versioned |
| CV-DEPLOIEMENT-002 | Zeros do not shorten dense kernels; the target must support the sparsity pattern: confirmed (TensorRT 11.4.1 Sparsity: 2:4 pattern on Ampere and later, FP16 or INT8, 22 of 53 eligible layers chose sparse tactics in the documented example; Li et al.: irregular sparsity does not reduce convolution cost without sparse libraries). "Hollow tactics" (*creuses*: sparse), "less regular clues" (*indices*: index metadata), "equipment", "schema" | Comparison of compression and acceleration | 2 criteria; 274 → 350 lexical words | Source pointed to TensorRT 8.6.1 only | Minor | Language fixed; "Hardware-supported pattern" paragraph added (missing condition: pattern, precision and tactic choice); sources updated to TensorRT 11.4.1 and Li et al. |
| CV-DEPLOIEMENT-003 | Weights alone do not reproduce a system: confirmed (Sculley et al. §2 CACE, §6 configuration debt; ML Test Score Infra 1, 6, 7 and Monitor 3; TensorRT 11.4.1 engine compatibility; PyTorch 2.11 reproducibility limits). Expected answer said "reference entry" (*entrée de référence*: reference input); "footprints" (hashes), "backtracking", "back-test on a test line", "Manifeste reproductible" left in French | Practice: versioning a complete system | 3 criteria; 335 → 438 lexical words | — | Minor | Expected answer language fixed; "Engine portability" paragraph added (plan tied to TensorRT version and compute capability; no hardware compatibility on JetPack); sources versioned |
| CV-DEPLOIEMENT-004 | Thermal, memory and queue signatures distinguish causes of a slow-down: confirmed (Jetson Linux r36.4: DVFS throttling at passive trip points, CPU-zone SW throttling at 99.0 °C, HW throttling at 103.0 °C, overcurrent counters, `tegrastats`). "sustainable diet" (*régime soutenable*: sustained regime), "Declare sufficient material" (hardware), "keep accurate", "abandoning", "Signatures temporelles" left in French | Diagnosis of a sustained-load failure | 3 criteria; 355 → 440 lexical words | — | Minor | Language fixed; "Platform counters" paragraph added; sources versioned |

Expected-answer changes (meaning-restoring language fixes, no change of criteria):

- CV-DEPLOIEMENT-001: "Approximately 1/0,95 = 1,053×, depending on Amdahl model
  announced." → "Approximately 1/0.95 ≈ 1.053×, under the stated Amdahl model."
- CV-DEPLOIEMENT-003: "Pre-processing/coordinate frames, architecture, taxonomy,
  post-processing/thresholds, runtime and relevant dependencies, as well as a
  reference entry." → "Preprocessing and coordinate frames, architecture, taxonomy,
  postprocessing and thresholds, runtime and relevant dependencies, as well as a
  reference input."

Protected-field defects reported, not edited: the CV-DEPLOIEMENT-004 objective "Test
the edge" translates *tester le régime edge* and would read "test sustained edge
operation"; the CV-DEPLOIEMENT-001 objective "Limiting a system gain" would read
"bound a system gain".

## Reference findings

Claims of revision 8 checked against their passages:

- "Amdahl's simplified law limits an overall gain to $1/((1-f)+f/s)$": confirmed as the
  usual formalization; the 1967 paper argues the limit in words (p. 483: sequential
  housekeeping, "the effort expended on achieving high parallel processing rates is
  wasted unless it is accompanied by achievements in sequential processing rates of
  very nearly the same magnitude"). The note now says so.
- "Accelerating a stage of 10% of the time by 2 yields only about 1,053×": correct
  value, French decimal comma fixed (1.053×).
- "Unstructured pruning only accelerates if kernels or hardware exploit its sparsity":
  confirmed (TensorRT 11.4.1 Sparsity; Li et al.).
- "A short run does not prove a stable thermal regime": confirmed in mechanism
  (Jetson r36.4 software clock throttling at trip points; TensorRT benchmarking on
  thermal and power throttling).
- No scientific error was found. The body was shallow and mistranslated ("update
  mastered", "Fault/Return Policy", "video file" for *file vidéo*, video queue,
  "Question of work", "Reference Response", "floor", "competing system", "material").

New claims verified for revision 9 (main ones):

- TensorRT 11.4.1 Engine Compatibility: version and compute capability recorded and
  checked at deserialization; version-compatible engines can be slower; hardware
  compatibility not supported on DriveOS or JetPack; platform-specific by default.
- TensorRT 11.4.1 Data Formats and Tensors, Sparsity: 2:4 rule, `kSPARSE_WEIGHTS`,
  FP16 or INT8, 53 eligible against 22 chosen layers, possible accuracy loss.
- Jetson Linux r36.4 Platform Power and Performance: power modes capping frequencies
  and online cores, the example `MODE_15W` entry (4 of 8 cores, 1.2 GHz CPU, 670 MHz
  GPU), software clock throttling, hardware throttling, thermal specification table
  (99.0, 103.0 and 104.5 °C for the CPU zone; 112.0, 116.0 and 117.5 °C for AGX Orin
  Industrial), `jetson_clocks`, `tegrastats`, overcurrent event counters.
- PyTorch 2.11 Reproducibility: limits across releases, commits, platforms and
  CPU/GPU; cuDNN benchmarking; deterministic algorithms.
- Sculley et al. 2015: CACE and its extension to settings (§2), undeclared consumers
  (§2), unstable data dependencies (§3), configuration debt (§6), fixed thresholds and
  monitoring (§7).
- Breck et al. (ML Test Score): Infra 1, 6, 7; Monitor 3, 4; alerting thresholds;
  image-data teams (§IV-D).
- Hinton et al.: softmax with temperature, weighted objectives, $T^2$ scaling (§2).
- Li et al.: filter pruning results and irregular sparsity (abstract).

## Reference depth

Body word counts (front matter excluded, H1 included, up to "## Guided reasoning and
proposed checks"; whitespace tokens): 327 → 3,628. Of these, about 2,770 are prose,
660 table cells and 200 pseudocode and Mermaid.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Task; bundle inputs (engine per device, preprocessing, class map, thresholds, versions, power mode); outputs (manifest, acceptance report, monitoring); engine portability constraint; role |
| Intuition | Shallow | Developed | CACE; device state as part of a performance figure; structured against unstructured compression; constructed class-map rollback illustration; Mermaid release state machine |
| Prerequisites | Shallow (two links) | Developed | Links to CV-PIPELINE, CV-QUANT, CV-FIABILITE, CV-DETECTEURS, CV-NMS, CV-IOU-AP, CV-CAPTEURS |
| Assumptions | Absent | Developed | Additive model, fixed operating conditions, local determinism, field observability, degenerate cases |
| Procedure | Shallow | Developed | Seven-step release pseudocode with the purpose of each step, tied to the ML Test Score |
| Mathematics | Shallow (one formula) | Developed | Amdahl bound with overhead and cancellation condition (example A, sequential against pipelined); convolution cost and pruning arithmetic, sparse storage (example B); distillation with temperature (example C); first-order thermal model with Jetson trip point (example D); soak sizing (example E) |
| Parameters | Shallow (list) | Developed | Nine-row table (power mode, clocks, soak duration, engine compatibility, pruning ratio, sparsity flag, distillation, canary, monitoring thresholds); tuning approach |
| Properties | Shallow | Developed | Limits of Amdahl's bound, pruning, distillation, reproducibility, label-free monitoring, thermal behaviour |
| Cost and implementation | Shallow | Developed | Cost drivers; versioned contracts for TensorRT 11.4.1 (compatibility, sparsity, benchmarking), Jetson Linux r36.4 and PyTorch 2.11; execution status |
| Evaluation | Shallow | Developed | Time-windowed metrics; same-device previous-bundle baseline; ambient-temperature variation with hypothesis; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Nine-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Edge, central or hybrid serving; compression choice; per-target against compatible engines; clock policy; industrial uses labelled as project reasoning; sources split |

Constructed examples are recomputed by
[`checks/143-edge-reproductibilite.py`](checks/143-edge-reproductibilite.py)
(11 check groups): Amdahl values (1.053, 1.111, cancellation at 0.05), 40 → 30 ms and
50 → 100 frames/s, convolution MACs (943.7 M → 530.8 M), sparse storage (2 and 0.4
bytes per weight), 22/53 sparse layers, softmax at $T=1$ and $T=4$, high-temperature
$1/T^2$ gradient scaling, thermal fractions (39%, 95%) and time to the 99 °C trip point
(23 min), soak sizing (864,000 frames, 864 MB against 14.4 MB).

## Applied corrections

- [Reference](../../../vault/140-ingenierie-systemes/references/143-edge-reproductibilite.md),
  revision 8 → 9: body rewritten and deepened as above; appendix language fixed
  identically to the cards ("Question of work" → "Working question", "Reference
  Response" → "Reference answer", decimal commas → points, "floor" → "stage",
  "competing system" → "system with contention", "Why Duration Matters" → "Why
  duration matters", "sustainable diet" → "sustained regime", "Boundary and additional
  cost" → "Bound and added cost", "standardized cost" → "normalized cost", "less
  regular clues" → "index metadata and less regular memory access", "Manifeste
  reproductible" → "Reproducible manifest", "footprints" → "hashes", "back-test on a
  test line" → "rollback rehearsal on a test bench", "Signatures temporelles" →
  "Temporal signatures", "keep accurate" → "record accuracy", "p. 1. 483" → "p. 483");
  the "Reference answer" of the CV-DEPLOIEMENT-001 case follows the corrected expected
  answer; sources split into scientific and implementation sources; closing provenance
  line replaced. Front matter unchanged except `revision`; H1, per-card headings and
  `## Sources and flashcards` kept.
- [Cards](../../../vault/140-ingenierie-systemes/143-edge-reproductibilite.md):
  expected answers of CV-DEPLOIEMENT-001 and CV-DEPLOIEMENT-003 as quoted above.
  Language fixes in further explanations and blocking errors of all four cards,
  including "Announce a pipeline twice as fast" → "Announcing a pipeline twice as
  fast", "Automatically deducts speed and energy from the zero weight ratio" →
  "Deducing speed and energy automatically from the fraction of zero weights",
  "Consider the weights as the only artifact of the model exploited" → "Treating the
  weights as the only artifact of the deployed model", "Declare sufficient material on
  an isolated cold test" → "Declaring the hardware sufficient from an isolated cold
  test". Additions: CV-DEPLOIEMENT-002 "Hardware-supported pattern"; CV-DEPLOIEMENT-003
  "Engine portability"; CV-DEPLOIEMENT-004 "Platform counters". Source lines now cite
  TensorRT 11.4.1 pages, Li et al., Sculley et al., the ML Test Score items, PyTorch
  2.11 and the Jetson r36.4 sections. Questions, IDs, objectives, families, tags and
  target deck unchanged.

No other vault file repeats a claim corrected here (`rg` over `vault/` for "Amdahl",
"pruning", "sparsity" and "1,053").

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited
by this subject run). The register held no CV-DEPLOIEMENT proposal, and earlier
reports for this subject proposed none.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-DEPLOIEMENT-01 | CV-DEPLOIEMENT | Without field labels, which signals can reveal that one camera's detector has regressed (input statistics, score and prediction distributions per camera, action rates, upstream producer health), and what can these signals not prove? | The note's title includes monitoring, but no card tests it; label-free monitoring detects change, not error | Evaluation; Properties and Failure modes | 1 card, 3 criteria | [Sculley et al. 2015, §7](https://papers.nips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf); [ML Test Score, Monitor 3 and 4, §IV-D](https://storage.googleapis.com/gweb-research2023-media/pubtools/4156.pdf) |

## Sources

Scientific sources, opened at the passages listed:

- Amdahl 1967, [CMU-hosted PDF](https://www.cs.cmu.edu/~18742/papers/Amdahl1967.pdf)
  (text extracted with `pdftotext`): pp. 483–484.
- Sculley et al. 2015, [NeurIPS PDF](https://papers.nips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf):
  abstract, §2 (entanglement, CACE, undeclared consumers), §3 (unstable data
  dependencies), §6, §7 (fixed thresholds, monitoring and testing).
- Breck et al., [ML Test Score PDF](https://storage.googleapis.com/gweb-research2023-media/pubtools/4156.pdf):
  Infra 1, Infra 6, Infra 7, Monitor 3, Monitor 4, Monitor 5 heading, alerting
  paragraph, §IV-D.
- Hinton et al., [arXiv 1503.02531v1](https://arxiv.org/abs/1503.02531) PDF: §1, §2.
- Li et al., [arXiv 1608.08710](https://arxiv.org/abs/1608.08710): abstract page only
  (the full paper was not opened).

Implementation sources:

- TensorRT 11.4.1 (downloaded and converted to text): Engine Compatibility; Data
  Formats and Tensors, Sparsity; Performance Benchmarking (clock locking, power and
  thermal throttling, timing cache).
- [Jetson Linux r36.4, Platform Power and Performance (Orin series)](https://docs.nvidia.com/jetson/archives/r36.4/DeveloperGuide/SD/PlatformPowerAndPerformance/JetsonOrinNanoSeriesJetsonOrinNxSeriesAndJetsonAgxOrinSeries.html)
  (downloaded and converted to text): sections listed in the note.
- [PyTorch 2.11, Reproducibility](https://docs.pytorch.org/docs/2.11/notes/randomness.html).

Failed accesses and limits:

- TensorRT 8.6.1 §6.10, cited by revision 8, was not re-read; the same behaviour was
  verified in TensorRT 11.4.1, and the old link is kept as a continuity source.
- Detection-specific distillation and NVIDIA's 2:4 accuracy-recovery recipe were not
  consulted; the note states that they are outside its sources.
- The first-order thermal model is a project approximation, not a property of a
  datasheet; the trip-point temperatures are the only device figures used.
- Context7 was not available in this session (scope record).

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 260 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/143-edge-reproductibilite.py` | 11 check groups passed |
| `git diff --check -- vault/140-ingenierie-systemes/ docs/revues/2026-11-14-reference-depth/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/140-ingenierie-systemes/143-edge-reproductibilite.md` | 4 cards, 273 to 440 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card `## CV-…`, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` lines identical (33 lines); reference front matter identical except `revision: 8` → `9`; H1 and per-card headings unchanged; `$$` and code fences balanced |

No device was configured, no engine built, no model pruned or distilled and no
temperature or power measured; the controlled variation and tuning approach are
protocols, not results. The Mermaid diagram and tables were not rendered in Obsidian,
and AnkiDroid rendering of the corrected cards is unverified. This is agent
self-review, without independent scientific validation or measurement of learner
proficiency. Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-DEPLOIEMENT revision 9, CV-DEPLOIEMENT-001 to CV-DEPLOIEMENT-004, corrections
listed above, Agent Claude Code self-review, to republish with `paquet-anki`) and the
proposal register (P-CV-DEPLOIEMENT-01).
