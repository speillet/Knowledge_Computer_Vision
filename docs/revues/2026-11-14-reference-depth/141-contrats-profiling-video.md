# Review — Data contracts, profiling and video pipelines — 2026-11-14

## Overview

5 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 7 to revision 8. Highest severity per card before correction:
0 blocking, 2 important, 3 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is the pipeline note of the systems topic. Precision and runtimes stay
in [CV-QUANT](../../../vault/140-ingenierie-systemes/references/142-quantification-runtimes.md),
edge hardware and reproducibility in
[CV-DEPLOIEMENT](../../../vault/140-ingenierie-systemes/references/143-edge-reproductibilite.md),
and capture timing in
[CV-CAPTEURS](../../../vault/20-acquisition-images/references/22-capteurs-horodatage.md);
this note links to them. The deepened body adds the vision-specific half of the data
contract that revision 7 did not mention: YCbCr matrix and range, letterbox and
pixel-centre conventions, capture-timestamp semantics.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-PIPELINE-001 | Throughput does not bound age or deadline: confirmed (definition of age, Yates and Kaul §I, which also separates timeliness from throughput and delay). "the deadline by decision", "SPF", "bitrate", "expectation", "exits", "charging policy", "useful time", "abandonment" obscured the meaning | Comparison of three timing quantities; senior design decision | 2 criteria; 277 → 283 lexical words | Source cited unversioned TensorRT `latest` | Minor | Expected answer and explanation language fixed; source versioned; Yates and Kaul added |
| CV-PIPELINE-002 | Unbounded growth for λ > μ without drop, buffer only delays saturation: confirmed by the fluid arithmetic (recomputed) and GStreamer queue semantics (blocking, `leaky`). "tail" for *queue* in the blocking error collides with *tail latency*, another concept of the same note; "abandonment", "places", "Its ability alters" | Reasoning on queue dynamics | 2 criteria; 352 → 356 lexical words | Garbled link text in the source line | Important | Language fixed in explanation, blocking error and source |
| CV-PIPELINE-003 | Engine time excludes decoding, pre/postprocessing, transfers and queues: confirmed with TensorRT 11.4.1 (pre/postprocessing outside the measured path; H2D/D2H excluded by default since 11.0; trtexec enqueues one inference ahead). "An asynchronous operation can also only be started when the stopwatch stops" inverted the meaning (launched but not completed) | Practice: defining a benchmark's scope | 2 criteria; 357 → 452 lexical words | Version-dependent default undated in the card | Minor | Language fixed; added a short paragraph on trtexec's "Host Latency" naming and default scope (missing condition for this objective); sources versioned |
| CV-PIPELINE-004 | Per-stage p99s do not add: confirmed by constructed counterexamples in both directions (recomputed); fan-in amplification confirmed (Dean and Barroso). Expected answer said "choosing material" for *hardware*; "Rafals", "seniority", "floors", "file", "loophole", "compressing the only network" | Design: verifiable sizing under a tail budget | 3 criteria; 319 → 345 lexical words | — | Minor | Expected answer language fixed; one sentence on p99 sample size added to the system criteria; sources versioned |
| CV-PIPELINE-005 | Low utilization does not locate the bottleneck: confirmed (TensorRT 11.4.1: throughput below the reciprocal of GPU Compute Time signals host overhead or transfers; Enqueue Time above GPU Compute Time signals an enqueue-bound workload). "drop" for *bottleneck* ("Locate a drop by substitution", "If the drop moves") collides with frame drops; "floor", "low-busy", "file size" | Diagnosis by trace | 3 criteria; 356 → 440 lexical words | — | Important | Language fixed; launch-bound cause added (missing condition); source versioned |

Expected-answer changes (meaning-restoring language fixes, no change of criteria):

- CV-PIPELINE-001: "No: the throughput does not guarantee the age of the observation
  or the deadline by decision." → "No: throughput guarantees neither the age of the
  observation nor the per-decision deadline."
- CV-PIPELINE-004: "Set freshness, drops and quality; profile each stage and then the
  full stream at 240 images/s; test batching/concurrency/queues and load/thermal
  scenarios before choosing material or optimization." → "Set freshness, drop and
  quality requirements; profile each stage and then the full load of 240 images/s;
  test batching, concurrency, queues and load and thermal scenarios before choosing
  hardware or an optimization."

Protected-field defects reported, not edited (objective lines are invariants):

- CV-PIPELINE-001 objective "separate latency flow and freshness" would read
  "separate latency, throughput and freshness".
- CV-PIPELINE-002 objective "reasoning on a video file" is a mistranslation of
  *file vidéo* (video queue); proposed wording "reason about a video queue under
  overload".

## Reference findings

Claims of revision 7 checked against their passages:

- "A queue with arrival rate λ above the sustainable service μ grows without limit in
  a model without dropping": confirmed (fluid arithmetic, recomputed).
- "The sum of per-stage p99s is not a general statistical identity": confirmed; the
  note now gives counterexamples where the sum overestimates (80 against 50 ms) and
  underestimates (30 against 120 ms), and the comonotonic case where quantiles add.
- "trtexec commands and defaults evolve": confirmed and made specific. TensorRT 11.4.1
  states that `--noDataTransfers` is a no-op since 11.0 because transfers are excluded
  by default, and `--includeDataTransfers` restores them.
- "Hardware decoding and colour conversion can still be bottlenecks": kept and
  refined; NVDEC "runs completely independent of compute/graphics engine" (Video
  Codec SDK 13.0), so decoding does not use CUDA cores, while GPU colour conversion
  does.
- No scientific error was found. The body was shallow (one to three sentences per
  section) and mistranslated: "A line" (*file*, queue), "abandonment" (drop),
  "Low-busy GPU", "tail" (queue), "Question of work", "Reference Response",
  "Rafals and equity", "seniority", "floors" (stages), "drop" (bottleneck),
  "charging policy", "material results".

New claims verified for revision 8 (main ones):

- BT.601-7 §§2.5.1–2.5.3 and BT.709-6 items 3.2–3.4 and 4.6: luma coefficients,
  colour-difference divisors 1.402/1.772 and 1.5748/1.8556, 8-bit limited range
  (219 and 224 scaling, offsets 16 and 128, black 16, peak 235, chroma 16–240).
- OpenCV 4.13.0: 4:2:0 conversions use BT.601 limited range only (colors.markdown
  L53–L78; color_yuv.simd.hpp L1018–L1041); `resize` maps bilinear source indices
  with the half-pixel convention (L4101) and nearest neighbour with
  $\lfloor ds\rfloor$ (L1133); `INTER_NEAREST_EXACT` uses centres (L1271).
- FFmpeg n7.1 `scale`: matrix and range options; when unspecified they depend on the
  pixel format.
- V4L2 (kernel 6.12): timestamp field, monotonic flag, EOF and SOE sources,
  `sequence` counting dropped frames, USB caveat.
- GStreamer `queue`: blocking when full, `leaky` values, defaults 200 buffers,
  10,485,760 bytes and 1 s, level properties and signals.
- TensorRT 11.4.1 "Performance Benchmarking": metric definitions, trtexec scheduling,
  transfer default, wrapper costs excluded, CUDA events, Nsight Systems and NVTX,
  power and thermal throttling, input values and power, shared-memory platforms.
- PyTorch 2.11 CUDA semantics: asynchronous execution and timing.
- ROS 2 Jazzy QoS: policy definitions, defaults, sensor-data profile, reliability
  compatibility.
- Yates and Kaul (arXiv 1608.08622v2): age definition, FCFS versus lossy LCFS (§I),
  M/M/1 FCFS average age eq. (8) with $\rho^*\approx0.53$ (§II-A).
- Dean and Barroso (CACM 2013): 63% of requests above one second for a fan-out to 100
  servers with a one-second p99; power and thermal throttling as variability causes.

## Reference depth

Body word counts (front matter excluded, H1 included, up to "## Guided reasoning and
proposed checks"; whitespace tokens): 363 → 5,043. Of these, about 3,770 are prose,
1,010 table cells and 250 pseudocode and Mermaid. The length comes from covering
three contracts (data, timing, measurement) that each need their own mechanism; the
precision, edge and capture-timing mechanisms are linked to their notes.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Task and deadline; inputs with V4L2 timestamp and sequence semantics; outputs; eight-stage representation table (shape, type, range, contract, silent error); upstream and downstream expectations; throughput, latency and age separated |
| Intuition | Shallow | Developed | Chain of servers and queues; constructed 240 against 200 frames/s illustration; Mermaid data-flow diagram |
| Prerequisites | Shallow (one link) | Developed | Links to CV-CAPTEURS, CV-ACQUISITION, CV-DETECTEURS, CV-NMS, CV-SOT, CV-SORT, CV-QUANT, CV-DEPLOIEMENT |
| Assumptions | Shallow | Developed | Rate stationarity, single clock, timestamp instant, loss observability, colour metadata, degenerate cases (unbounded backlog, blocking moves loss upstream, batch timeout) |
| Procedure | Shallow | Developed | Contract and instrumentation pseudocode; five steps with their purpose |
| Mathematics | Shallow | Developed | Latency decomposition and age sawtooth (example A); serial versus pipelined stages and batching wait (B); fluid queue, leaky-queue waits $C/\lambda$ and $C/\mu$ (C); Little's law cross-check; FCFS age eq. (8); quantile non-additivity (D), fan-in and sample size; YCbCr equations and mismatch example (E); letterbox forward and inverse maps (F); pixel-centre conventions; data volumes (G) |
| Parameters | Shallow (list) | Developed | Nine-row table with GStreamer, NVDEC, ROS 2 and trtexec settings; four-step tuning approach |
| Properties | Shallow | Developed | Bottleneck, additivity, age, loss against age, colour invariants, geometry, zero-copy locality, decoder independence |
| Cost and implementation | Shallow | Developed | Cost drivers with variables; versioned contracts for OpenCV, FFmpeg, GStreamer, NVDEC, TensorRT, PyTorch, ROS 2 and V4L2; instrumentation sketch; execution status |
| Evaluation | Shallow | Developed | Per-stream metrics; open-loop replay protocol and the closed-loop trap; baseline; camera-phase variation with hypothesis; measurement limits |
| Failure modes and diagnosis | Shallow (three sentences) | Developed | Ten-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices (every frame, newest frame, stride, device decoding, batching, GStreamer); industrial uses labelled as project reasoning; sources split into scientific and implementation sources |

Constructed examples are recomputed by
[`checks/141-contrats-profiling-video.py`](checks/141-contrats-profiling-video.py)
(24 check groups): queue backlog (400 frames, 2 s), deterministic leaky-queue
simulation (drop fraction 1/6; waits 39.4 and 47.7 ms against fluid 41.7 and 50 ms),
Little's law (0.2 s), age sawtooth (66.7, 83.3 and 116.7 ms; 50 mm lag), FCFS age
($\rho^*\approx0.53$, 3.48 and 10.2 service times), quantile counterexamples (50
against 80 ms; 120 against 30 ms; comonotonic 30 ms), fan-in (7.7%, 63%), sample
size (18 values), stage throughput (52.6 and 100 frames/s), batching wait (29.2 ms),
data volumes and queue defaults in frames, colour divisors and OpenCV constants,
BT.709 red and green decoded with BT.601, grey invariance, range contrast (0.859),
letterbox maps and padding share, nearest versus bilinear offset.

## Applied corrections

- [Reference](../../../vault/140-ingenierie-systemes/references/141-contrats-profiling-video.md),
  revision 7 → 8: body rewritten and deepened as above; appendix language fixed
  identically to the cards ("Question of work" → "Working question", "Reference
  Response" → "Reference answer", "tail" → "queue", "Critical Path and Asynchronous"
  → "Critical path and asynchrony", "Rafals and equity" → "Bursts and fairness",
  "Locate a drop by substitution" → "Locate a bottleneck by substitution",
  "seniority" → "frame age", "floors" → "stages", "capture→exit" →
  "capture-to-output", "useful time" → "deadline", "abandonment" → "drop",
  "lastest" → "`latest`"); the "Reference answer" of the CV-PIPELINE-001 case
  follows the corrected expected answer; sources split into scientific and
  implementation sources; closing provenance line replaced. Front matter unchanged
  except `revision`; H1, per-card headings and `## Sources and flashcards` kept.
- [Cards](../../../vault/140-ingenierie-systemes/141-contrats-profiling-video.md):
  expected answers of CV-PIPELINE-001 and CV-PIPELINE-004 as quoted above. Language
  fixes in further explanations and blocking errors of all five cards: "bitrate" →
  "throughput", "expectation" → "wait", "exits" → "outputs", "charging policy" →
  "load-shedding policy", "Validate the product at the average SPF only" →
  "Validating the product on average FPS alone", "increasing the tail" → "enlarging
  the queue", "Its ability alters" → "Its size only changes", "Perimeter of
  measurement" → "Measurement scope", "entries" → "inputs", "An asynchronous
  operation can also only be started when the stopwatch stops" → "An asynchronous
  operation may also have only been launched, not completed, when the stopwatch
  stops", "Compare asynchronous GPU durations to contract-free user latency" →
  "Comparing asynchronous GPU durations with a user-facing latency whose measurement
  contract is undefined", "Provide an explicit overload" → "Plan an explicit overload
  policy", "the actual loophole" → "the actual bottleneck", "Change one floor" →
  "Change one stage", "low-busy GPU" → "underutilized GPU", "Criteria for correction
  of the case" → "Grading criteria for the case". Additions: CV-PIPELINE-003
  "Version-specific scope in TensorRT 11.4.1"; CV-PIPELINE-004 one sentence on p99
  sample size; CV-PIPELINE-005 "Launch-bound case". Source lines now cite TensorRT
  11.4.1 sections, Yates and Kaul (001), PyTorch 2.11 (003) and Dean and Barroso
  (004). Questions, IDs, objectives, families, tags and target deck unchanged.

No other vault file repeats a claim corrected here (`rg` over `vault/` for
"letterbox", "BT.709", "NV12", "p99", "percentile" and "Little").

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited
by this subject run; the register is a shared file). The register held no
CV-PIPELINE proposal, and earlier reports for this subject proposed none.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-PIPELINE-01 | CV-PIPELINE | After a camera or decoder change, saturated colours shift but greys are unchanged: name the cause (YCbCr matrix BT.601 against BT.709, or limited against full range) and the discriminating test (colour bars, black level) | No card tests the colour part of the data contract; the error is silent in timing measurements | Diagnosis; Mathematics example E, Failure modes | 1 card, 3 criteria | [BT.709-6 items 3.2–3.4, 4.6](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.709-6-201506-I!!PDF-E.pdf); [OpenCV 4.13.0 colors.markdown L53–L78](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/doc/colors.markdown#L53-L78) |
| P-CV-PIPELINE-02 | CV-PIPELINE | Map a detector box back through a letterbox ($r$, padding, inverse) for a 1920×1080 source and a 640×640 input, and state the symptom of a forgotten padding term | No card in the vault tests the geometric preprocessing contract between detector output and source pixels | Reasoning; Mathematics example F | 1 card, 3 criteria (scale, padding, inverse) | Constructed derivation; [OpenCV 4.13.0 resize.cpp L4101](https://github.com/opencv/opencv/blob/4.13.0/modules/imgproc/src/resize.cpp#L4096-L4103) for the pixel-centre convention |

## Sources

Scientific sources, opened at the passages listed:

- ITU-R BT.601-7 PDF (text extracted with `pdftotext`): §§2.5.1–2.5.3.
- ITU-R BT.709-6 PDF (text extracted with `pdftotext`): Part 2, items 3.2–3.5, 4.6, 4.7.
- Yates and Kaul, [arXiv 1608.08622v2](https://arxiv.org/abs/1608.08622) PDF: §I
  (age definition, FCFS and lossy LCFS paragraph), §II-A (eq. 8, $\rho^*\approx0.53$),
  §II-B opening.
- Dean and Barroso, The Tail at Scale, [author-hosted PDF](https://www.barroso.org/publications/TheTailAtScale.pdf):
  "Why Variability Exists?" and "Component-Level Variability Amplified By Scale".

Implementation sources:

- OpenCV 4.13.0 (raw GitHub files): `modules/imgproc/doc/colors.markdown` L53–L78,
  `modules/imgproc/src/color_yuv.simd.hpp` L1000–L1060,
  `modules/imgproc/src/resize.cpp` L1122–L1135, L1267–L1282, L3480–L3492, L4085–L4135,
  `modules/imgproc/include/opencv2/imgproc.hpp` (NV12 enum entries L650–L665).
- FFmpeg n7.1 `doc/filters.texi` L20984 (`scale` section), L21075–L21139.
- [GStreamer `queue`](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html):
  element description, `max-size-*`, `leaky`, `current-level-*`, `min-threshold-*`,
  signals.
- [NVIDIA Video Codec SDK 13.0 NVDEC guide](https://docs.nvidia.com/video-technologies/video-codec-sdk/13.0/nvdec-video-decoder-api-prog-guide/index.html):
  output formats, post-processing, decode surfaces, engine independence (page shows no
  SDK version beyond the URL).
- [TensorRT 11.4.1 Performance Benchmarking](https://docs.nvidia.com/deeplearning/tensorrt/11.4.1/performance/benchmarking.html)
  (downloaded and converted to text): sections listed in the note.
- [PyTorch 2.11 CUDA semantics](https://docs.pytorch.org/docs/2.11/notes/cuda.html):
  "Asynchronous execution", "CUDA streams".
- ROS 2 Jazzy QoS, source file `source/Concepts/Intermediate/About-Quality-of-Service-Settings.rst`
  on the `jazzy` branch of `ros2/ros2_documentation`: policies, profiles,
  compatibility tables.
- [Linux kernel 6.12 V4L2 buffers](https://www.kernel.org/doc/html/v6.12/userspace-api/media/v4l/buffer.html):
  `timestamp`, `sequence` and its note, buffer flags.

Failed accesses and limits:

- The rendered ROS 2 page (docs.ros.org) returned an anti-bot page; its source file
  on GitHub was read instead.
- cacm.acm.org returned HTTP 403 for The Tail at Scale; the author-hosted PDF was
  read instead.
- Little 1961 (Operations Research 9(3)) is paywalled: **not verifiable** in this
  pass. The note states Little's law with that qualification and uses it only as an
  instrumentation cross-check; the check script recomputes the arithmetic.
- Kaul, Yates and Gruteser, INFOCOM 2012 (the original single-source age paper) was
  not accessed; eq. (8) is cited from its restatement in Yates and Kaul §II-A.
- Context7 was not available in this session (scope record); versioned official
  documentation and source code replaced it.
- The GStreamer page is unversioned; claims tied to it are dated 2026-11-14.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 263 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/141-contrats-profiling-video.py` | 24 check groups passed |
| `git diff --check -- vault/140-ingenierie-systemes/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/140-ingenierie-systemes/141-contrats-profiling-video.md` | 5 cards, 283 to 452 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card `## CV-…`, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` lines identical (41 lines); reference front matter identical except `revision: 7` → `8`; H1 and per-card headings unchanged; `$$` and code fences balanced |

No pipeline, decoder, profiler or ROS 2 code was executed; the controlled variation
and the tuning approach are protocols, not results. The Mermaid diagram and tables
were not rendered in Obsidian, and AnkiDroid rendering of the corrected cards is
unverified. This is agent self-review, without independent scientific validation or
measurement of learner proficiency. Export status: **to republish with
`paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-PIPELINE revision 8, CV-PIPELINE-001 to CV-PIPELINE-005, corrections listed above,
Agent Claude Code self-review, to republish with `paquet-anki`) and the proposal
register (P-CV-PIPELINE-01, P-CV-PIPELINE-02).
