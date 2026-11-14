# Review — PTQ, QAT, INT8/FP8 and runtimes — 2026-11-14

## Overview

5 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 6 to revision 7. Highest severity per card before correction:
0 blocking, 1 important, 4 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the method note on quantization and inference runtimes. Pipeline
timing stays in
[CV-PIPELINE](../../../vault/140-ingenierie-systemes/references/141-contrats-profiling-video.md)
and Amdahl's bound, pruning, distillation and edge deployment in
[CV-DEPLOIEMENT](../../../vault/140-ingenierie-systemes/references/143-edge-reproductibilite.md).
OpenVINO and LiteRT remain inventory items APP-117 and APP-118 and are only named.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-QUANT-001 | PTQ after training, QAT simulates quantization during training: confirmed (Jacob et al. §3, "Backpropagation still happens as usual" with simulated quantization in the forward pass; TensorRT 11.4.1 Quantization Workflows). "Substitution gradient" is the straight-through estimator (Nagel et al. §4.1; Krishnamoorthi §2.4). Expected answer said "quantification model" and "adapts learning"; "digital effects", "digital contract", "floating baseline", "reserved data", "equipment" | Comparison of two workflows; senior decision | 2 criteria; 353 → 353 lexical words | Sources unversioned (TensorRT `latest`) | Minor | Expected answer and explanation language fixed; sources versioned; Nagel §4.1 added |
| CV-QUANT-002 | Unrepresentative calibration causes clipping or coarse resolution: confirmed (Nagel et al. §2.2 rounding error in $[-s/2,s/2]$, clipping beyond the grid; §3.1 range setting). Expected answer said "digital saturation" and "sensitive errors" (*erreurs sensibles*: significant errors); "Digital Compromise", "setting the test indefinitely" | Reasoning on range against resolution | 2 criteria; 382 → 368 lexical words | ONNX operator link pointed to an anchor no longer on the current page (now opset 28) | Minor | Expected answer and explanation language fixed; ONNX link versioned (v1.16.0); Nagel §§2.2, 3.1 added |
| CV-QUANT-003 | Export does not guarantee runtime support: confirmed and made concrete (TensorRT 11.4.1 rejects `QLinearConv`, `QLinearMatMul`, `ConvInteger`, `MatMulInteger` at import; symmetric scheme only; ONNX Runtime GPU S8S8 only; EP assignment by `GetCapability()`). Expected answer listed "accuracy" for *numerical precision*, which turns a support criterion into a task-quality one; "Versioner", "commissioning", "control inputs", "deletion" | Practice: checking a runtime's support | 2 criteria; 275 → 367 lexical words | — | Important | Expected answer language fixed; "Format dialects" paragraph added (missing condition); sources versioned |
| CV-QUANT-004 | Missing INT8 gain has engine, conversion and pipeline causes: confirmed (TensorRT 11.4.1: unfused Q/DQ can lower performance, older devices may lack kernels; ONNX Runtime FAQ: quantize/dequantize overhead, worse performance on old devices). Amdahl figures 1.11 and 1.0 recomputed. "neck" (bottleneck), "off-grid optimization" (outside the network), "outdoor stage", "quantified" | Diagnosis | 3 criteria; 366 → 457 lexical words | — | Minor | Language fixed; "Fusion and kernel conditions" paragraph added; sources versioned |
| CV-QUANT-005 | Memory reduction must be judged with quality and system cost: confirmed (factor 4 for 8-bit weights, Krishnamoorthi abstract; activations and workspaces unaffected by weight-only quantization). Expected answer said "latency/flow/memory" (*débit*: throughput), "reserved data", "set operating point"; French decimal commas "0,501", "0,499", "0,5" | Evaluation of quality and cost together | 3 criteria; 276 → 281 lexical words | — | Minor | Expected answer and explanation language fixed; decimal commas fixed; sources versioned |

Expected-answer changes (meaning-restoring language fixes, no change of criteria):

- CV-QUANT-001: "PTQ comes after training; QAT adapts learning to a quantification
  model." → "PTQ is applied after training; QAT adapts training to a model of
  quantization."
- CV-QUANT-002: "Inadequate digital saturation or resolution for real-world
  activations, with sensitive errors on some outputs." → "Saturation or resolution
  unsuited to real activations, with significant errors on some outputs."
- CV-QUANT-003: "Supported operators, shapes, kernels, accuracy and hardware differ;
  conversions/fallbacks and preprocessing must be validated." → "Supported operators,
  shapes, kernels, numerical precisions and hardware differ; conversions, fallbacks
  and preprocessing must be validated."
- CV-QUANT-005: "Quality on reserved data and critical cases, plus full system
  latency/flow/memory at the set operating point." → "Quality on held-out data and
  critical cases, plus full-system latency, throughput and memory at the fixed
  operating point."

Protected-field defect reported, not edited: the CV-QUANT-004 objective "diagnose an
absence of gain INT8" would read "diagnose a missing INT8 gain".

## Reference findings

Claims of revision 6 checked against their passages:

- Affine scheme $q=\mathrm{clip}(\mathrm{round}(x/s)+z)$, $\hat x=s(q-z)$: confirmed
  (Jacob et al. eq. 1; Nagel et al. eqs. 4–7; ONNX opset 21 formula).
- "The rounding rule depends on the contract": confirmed and made specific; ONNX
  `QuantizeLinear` and TensorRT 11.4.1 round ties to even, TensorRT clips $x/s$
  before rounding.
- "INT8 and FP8 have different representations": confirmed (Micikevicius et al.
  Table 1; TensorRT FP8 scheme).
- "A serialized engine is not universally portable" and "a file format is not a
  guarantee of acceleration": confirmed (TensorRT import restrictions, kernel
  availability; ONNX Runtime FAQ).
- No scientific error was found. The body was shallow and mistranslated:
  "whole affine quantification" (*entière*: integer), "terminals" (*bornes*: bounds),
  "motor" (engine), "Mixed accuracy" (mixed precision), "Question of work",
  "Reference Response", "material results".

New claims verified for revision 7 (main ones):

- Jacob et al.: eq. 1 and exact zero (§2.1), eqs. 4–5 and $M=2^{-n}M_0$ with
  $M_0\in[0.5,1)$ (§2.2), int32 bias (§2.4), simulated quantization and eq. 12 (§3),
  weight ranges in $[-127,127]$, EMA activation ranges, delayed activation
  quantization of 50 thousand to 2 million steps (§3.1), BN folding (§3.2), MobileNet
  SSD on COCO, Table 4.4 (mAP 22.1 against 21.7; 778/687, 370/272, 270/146,
  121/61 ms on Snapdragon 835 cores), Appendix B.
- Nagel et al.: eqs. 4–8, rounding against clipping (§2.2), eq. 13 and the common
  symmetric-weights/asymmetric-activations choice (§2.4.1), per-channel weights and
  impractical per-channel activations (§2.4.2), min-max against MSE with Table 1
  (§3.1), PTQ pipeline and 500–1,000-image calibration footnote (§3.5), debugging
  flow (§3.7), straight-through estimator (§4.1).
- Krishnamoorthi: abstract items 1–4 and 7, STE with clamp indicator (§2.4), Tables 2
  and 3 (MobileNet-v1 per-layer 0.001 against per-channel 0.703, float 0.709) and the
  batch-normalization explanation (§3.1).
- Micikevicius et al.: Table 1 (E4M3 bias 7, max 448, no infinities; E5M2 max
  57,344), §2 scaling factors, §4.2 and Table 5 (PTQ comparison on language models).
- ONNX v1.16.0 `QuantizeLinear`/`DequantizeLinear` opset 21.
- TensorRT 11.4.1: symmetric scheme and data types; workflows, explicit
  quantization, granularities, rounding, dynamic quantization; INT8/FP8/INT4/NVFP4
  formulas; ONNX support, unsupported QOperator operators, Q/DQ placement
  recommendations; tactic non-determinism with floating clocks (benchmarking page).
- ONNX Runtime quantization page: QOperator and QDQ, static and dynamic, calibration
  methods, S8S8 default, GPU S8S8, `VPMADDUBSW` saturation and `reduce_range`,
  debugging functions, FAQ; Execution Providers page: `GetCapability()` and priority.
- PyTorch 2.11 quantization page: migration to `torchao`, planned removal of
  `torch.ao.quantization`.

## Reference depth

Body word counts (front matter excluded, H1 included, up to "## Guided reasoning and
proposed checks"; whitespace tokens): 328 → 4,069. Of these, about 3,150 are prose,
720 table cells and 190 pseudocode and Mermaid.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Task with a detector example; inputs (calibration and held-out sets, runtime and version); outputs (Q/DQ graph or engine, per-tensor parameters, report); data contract at the quantizer boundary; pipeline role |
| Intuition | Shallow | Developed | Ruler analogy for scale, PTQ, QAT and FP8; fusion against fallback; constructed specular-highlight illustration; Mermaid workflow |
| Prerequisites | Shallow (one link) | Developed | Links to CV-PIPELINE, CV-DETECTEURS, CV-NMS, CV-IOU-AP, CV-FIABILITE, CV-ACQUISITION, CV-DEPLOIEMENT |
| Assumptions | Absent | Developed | Representative calibration, exact zero, BN folding and range spread, runtime support, degenerate cases |
| Procedure | Shallow | Developed | Eight-step pseudocode with the purpose of each step, tied to Nagel et al. §§3.5, 3.7 and TensorRT placement rules |
| Mathematics | Shallow (one formula) | Developed | Affine and symmetric schemes, rounding conventions, error terms and RMS; examples A (range against resolution), B (granularity), C (FP8 against INT8), D (requantization multiplier), E (16-bit saturation), F (decision sensitivity); integer-only arithmetic; published speedups; memory |
| Parameters | Shallow (list) | Developed | Ten-row table with source options and interactions; four-step tuning approach |
| Properties | Shallow | Developed | Error bound inside the range, exact zero, non-bitwise portability, STE as a biased approximation, granularity and BN, FP8 against INT8, conditional speed |
| Cost and implementation | Shallow | Developed | Cost drivers; versioned contracts for ONNX opset 21, TensorRT 11.4.1, ONNX Runtime, PyTorch 2.11; execution status |
| Evaluation | Shallow | Developed | Tensor, task and system metrics; same-runtime FP16 baseline; calibration-set variation with hypothesis; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Ten-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (FP16, INT8 PTQ, QAT, FP8, INT4 weight-only, structural alternatives); industrial uses labelled as project reasoning; sources split |

Constructed examples are recomputed by
[`checks/142-quantification-runtimes.py`](checks/142-quantification-runtimes.py)
(15 check groups): steps 0.235 and 0.0235 with maximal errors 0.118 and 0.0118, RMS
$s/\sqrt{12}$ (0.068, 0.0068), 23.5% relative error and the clipped outlier;
per-tensor codes $-3..3$ and the per-channel scale; E4M3 and E5M2 maxima, 6.25%
relative bound, 0.01 → 0 in INT8 and 0.010045 in FP8; $M=2^{-9}\times0.512$; 16-bit
saturation (64,770 against 32,130); Table 4.4 ratios (1.13×, 1.36×, 1.85×, 1.98×;
−1.8% relative mAP); weight and activation memory; score step 0.0125 and flip band
±0.00625; box step 2.51 px and IoU 0.62; int8 product bound $<2^{14}$; Amdahl 1.11
and 1.0 (2026-11-08 appendix, re-verified).

## Applied corrections

- [Reference](../../../vault/140-ingenierie-systemes/references/142-quantification-runtimes.md),
  revision 6 → 7: body rewritten and deepened as above; appendix language fixed
  identically to the cards ("Question of work" → "Working question", "Reference
  Response" → "Reference answer", "constant in pieces" → "piecewise constant",
  "substitution gradient" → "straight-through estimator", "schema" → "scheme",
  "digital" → "numerical", "control inputs" → "reference inputs", "deletion" → "NMS
  suppression", "quantified" → "quantized", "outdoor stage" → "stage outside the
  engine", "0,501/0,499/0,5" → "0.501/0.499/0.5", "Different memories" → "Different
  memory terms"); the "Reference answer" of the CV-QUANT-001 and CV-QUANT-005 cases
  follows the corrected expected answers; the documentary link now targets ONNX
  v1.16.0; sources split into scientific and implementation sources; closing
  provenance line replaced. Front matter unchanged except `revision`; H1, per-card
  headings and `## Sources and flashcards` kept.
- [Cards](../../../vault/140-ingenierie-systemes/142-quantification-runtimes.md):
  expected answers of CV-QUANT-001, 002, 003 and 005 as quoted above. Language fixes
  in further explanations and blocking errors of all five cards, including
  "Assimilate the word INT8 to a single learning method" → "Equating the word INT8
  with a single training method", "Suppose that some arbitrary images give a
  universal calibration" → "Assuming that a few arbitrary images give a universal
  calibration", "Assimilate exchange format and universal optimized execution" →
  "Equating an exchange format with universally optimized execution", "Conclude that
  quantification is always useless" → "Concluding that quantization is always
  useless", "Report only the number of bits or weight of the file" → "Reporting only
  the bit width or the file size", "Criteria for correction of the case" → "Grading
  criteria for the case". Additions: CV-QUANT-003 "Format dialects"; CV-QUANT-004
  "Fusion and kernel conditions". Source lines now cite TensorRT 11.4.1 pages, ONNX
  v1.16.0, Nagel et al. (001, 002) and Krishnamoorthi (005). Questions, IDs,
  objectives, families, tags and target deck unchanged.

No other vault file repeats a claim corrected here (`rg` over `vault/` for
"quantification", "INT8" and "QAT").

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited
by this subject run). The register held no CV-QUANT proposal, and earlier reports for
this subject proposed none.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-QUANT-01 | CV-QUANT | After BN folding, predict whether per-tensor or per-channel INT8 weights preserve a MobileNet-type backbone, and explain why from the spread of per-channel ranges | Granularity is only mentioned inside CV-QUANT-002's explanation; no card trains the mechanism behind the best-documented PTQ failure | Reasoning; Mathematics example B | 1 card, 3 criteria (range spread from BN, codes left to small channels, per-channel scale factors out of the accumulator) | [Krishnamoorthi §3.1, Table 3](https://arxiv.org/abs/1806.08342); [Nagel et al. §2.4.2](https://arxiv.org/html/2106.08295) |
| P-CV-QUANT-02 | CV-QUANT | For a quantized detector, decide which outputs to keep in higher precision by computing the score flip band near the threshold and the IoU loss of a small box under a coarse coordinate scale | No card connects quantization error to detection decisions (thresholds, NMS, IoU at 0.75) | Design; Mathematics example F | 1 card, 3 criteria | Constructed calculation; [TensorRT 11.4.1 Q/DQ placement recommendations](https://docs.nvidia.com/deeplearning/tensorrt/11.4.1/inference-library/quantized-types-explicit-quantization.html) |

## Sources

Scientific sources, opened at the passages listed:

- Jacob et al., [arXiv HTML 1712.05877v1](https://arxiv.org/html/1712.05877v1): §1
  contributions, §2.1, §2.2, §2.4, §3, §3.1, §3.2, §4.2.1 opening, §4.2.2 and Table 4.4,
  Appendix B.
- Krishnamoorthi, [arXiv 1806.08342v1](https://arxiv.org/abs/1806.08342) PDF (text
  extracted with `pdftotext`): abstract, contents, §2.4, §3.1 (Tables 2 and 3 and
  observations).
- Nagel et al., [arXiv HTML 2106.08295](https://arxiv.org/html/2106.08295): §2.2,
  §2.2.1, §2.2.2, §2.2.3, §2.4.1, §2.4.2, §3.1 (Table 1), §3.5, §3.7, §4 opening,
  §4.1.
- Micikevicius et al., [arXiv 2209.05433v2](https://arxiv.org/abs/2209.05433) PDF:
  §2, Table 1, §3.1, §4.2.

Implementation sources:

- ONNX v1.16.0 `docs/Operators.md`, `QuantizeLinear` and `DequantizeLinear`
  (opset 21), read from the raw GitHub file. The current onnx.ai page documents
  opset 28 (new types such as float4e2m1, int2 and the `precision` attribute); the
  revision-6 link anchor `#quantizelinear-21` no longer points to version 21 there.
- TensorRT 11.4.1 pages (downloaded and converted to text): "Working with Quantized
  Types", "Quantization Workflows", "Quantization Schemes", "Explicit Quantization",
  and the "Performance Benchmarking" clock-locking paragraph.
- [ONNX Runtime quantization](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html)
  (unversioned; read 2026-11-14): overview, representation formats, pre-processing,
  dynamic and static quantization, debugging, method and data-type selection, GPU,
  FAQ. [Execution Providers](https://onnxruntime.ai/docs/execution-providers/):
  `GetCapability()` and priority (the page does not state CPU fallback explicitly
  beyond its example).
- [PyTorch 2.11 quantization](https://docs.pytorch.org/docs/2.11/quantization.html):
  migration note.
- [felixcloutier.com PMADDUBSW](https://www.felixcloutier.com/x86/pmaddubsw):
  unofficial extract of the Intel SDM (the page says so); used only for the
  pairwise-sum and saturation semantics behind ONNX Runtime's warning.

Failed accesses and limits:

- Context7 was not available in this session (scope record); versioned official
  documentation replaced it. ONNX Runtime's page is not versioned, so its claims are
  dated 2026-11-14.
- OpenVINO and LiteRT documentation was not opened; the note names them without
  claims.
- No claim relies on unverified FP8 results for vision models; the consulted FP8 PTQ
  comparison concerns language models only, and the note says so.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | At this subject's run: ECHEC caused only by another subject's in-progress file (`70-reconnaissance-representations/references/75-embeddings-biometrie.md`, a display-math line read as a link), no message concerning `140-ingenierie-systemes`; rerun after the third subject: OK, 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/142-quantification-runtimes.py` | 15 check groups passed |
| `git diff --check -- vault/140-ingenierie-systemes/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/140-ingenierie-systemes/142-quantification-runtimes.md` | 5 cards, 281 to 457 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card `## CV-…`, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` lines identical (41 lines); reference front matter identical except `revision: 6` → `7`; H1 and per-card headings unchanged; `$$` and code fences balanced |

No model was quantized, no engine built and no benchmark run; the controlled variation
and the tuning approach are protocols, not results. The Mermaid diagram and tables were
not rendered in Obsidian, and AnkiDroid rendering of the corrected cards is
unverified. This is agent self-review, without independent scientific validation or
measurement of learner proficiency. Export status: **to republish with
`paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-QUANT revision 7, CV-QUANT-001 to CV-QUANT-005, corrections listed above, Agent
Claude Code self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-QUANT-01, P-CV-QUANT-02).
