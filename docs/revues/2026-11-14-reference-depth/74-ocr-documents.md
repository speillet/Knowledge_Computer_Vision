# Review — OCR and document understanding — 2026-11-14

## Overview

3 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 7 to revision 8. Highest severity per card before correction:
0 blocking, 0 important, 3 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is a comparison note at *reperage* depth (priority V2, career track E). It
now traces the stages of a reading system (detection, recognition, reading order,
extraction) and the families that implement them (DBNet, CRNN with CTC, TrOCR,
LayoutLM, Donut), with the mechanisms needed to choose, evaluate and diagnose. Metric
families across applications stay in
[CV-METRIQUES-APPLIQUEES](../../../vault/130-evaluation-fiabilite/references/134-metriques-applications.md);
box matching stays in [CV-IOU-AP](../../../vault/130-evaluation-fiabilite/references/131-iou-ap-coco.md).

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-OCR-001 | CER as edit distance over reference length: confirmed (OCR-D, Text Evaluation, CER). 0.05% for one substitution in 2,000 characters: recomputed. Expected answer "measures the editing of characters", "order of reading", "accuracy of amounts": ambiguous wording. "standardization" for *normalization*, "predicted normalization" for *predefined*, French decimal comma "0,05%", unintelligible blocking error "Confounds near global text and correctly structured invoice" | Comparison: separates transcription quality from extraction quality | 2 expected criteria; 360 → 367 lexical words | ID, question, tags and heading unchanged; wording aligned with the reference appendix | Minor | Meaning-restoring fix of the expected answer; language fixes; blocking error made gradable |
| CV-OCR-002 | CER above 100% with many insertions, clipping and max-length mitigations biased, normalized CER bounded: confirmed (OCR-D, CER). Explanation said per-page averaging "weights the pages as well" for *equally*; blocking error "Rotate arbitrarily to 1" for *clipping to 1* | Reasoning: interprets a metric under its convention | 1 expected criterion; 359 → 360 lexical words | ID, question, tags and heading unchanged | Minor | Light language fix of the expected answer ("Inserts" → "insertions"); meaning-restoring fixes in the explanation and blocking error |
| CV-OCR-003 | Interleaved columns point to layout and reading order: confirmed (OCR-D, Layout Evaluation: two columns detected as one interleave lines and "all downstream processes to measure text accuracy will be defeated"). "fake" for *wrong*, "arrays" for *tables*, "sorting by height" for *by vertical position*, "a new recognition language does not correct this contract" | Diagnosis: localizes a failure by oracle substitution | 1 expected criterion; 263 → 268 lexical words | ID, question, tags and heading unchanged | Minor | Language fixes in explanation and blocking error; expected answer unchanged |

Expected-answer changes:

- CV-OCR-001 (meaning-restoring language fix): "CER measures the editing of characters
  according to a protocol; order of reading, association of fields and accuracy of
  amounts are other outputs." → "CER counts character edit operations under a stated
  protocol; reading order, field association and the correctness of amounts are other
  outputs."
- CV-OCR-002 (language fix): "Yes: Inserts can exceed the number of reference characters
  in (S+D+I)/N." → "Yes: in (S+D+I)/N, insertions can outnumber the N reference
  characters."

## Reference findings

Claims of revision 7 checked against their passages:

- Classic CER $(S+D+I)/N$, values above 1 with many insertions, OCR-D's normalized
  variant $(S+D+I)/(S+D+I+C)$ used in its benchmarks: confirmed (OCR-D, CER).
- CRNN/CTC as a sequential approach, TrOCR as a Transformer approach, LayoutLM combining
  text and layout, Donut without a separate OCR engine: confirmed (CRNN §2; TrOCR
  Introduction; LayoutLM §2.2; Donut abstract and §2.2). "TrOCR a transformative
  approach" was a mistranslation of *Transformer-based*.
- No scientific error found in revision 7. The body was shallow and contained
  mistranslations: "Entries" for inputs, "cutting" for segmentation, "a false critical
  amount", "fluid generation", "Question of work", "Reference Response", "material
  results", "standardization".

New claims verified for revision 8 (main ones):

- CTC: paths, map $\mathcal B$ with its published examples, conditional independence,
  eq. 3 (§3.1); best-path and prefix-search decoding, best path "not guaranteed to find
  the most probable labelling" (§3.2); forward recursion on $l'$ of length $2|l|+1$ with
  the skip rule, eqs. 5–8 (§4.1). The minimum-frame condition $T\ge|l|+r$ is derived from
  that recursion (project derivation, recomputed by brute force).
- CRNN: column feature sequence and height normalization (§2.1); eqs. 1–2, lexicon-free
  and lexicon-based transcription with BK-tree and $\delta$ (§2.3); $100\times32$ training
  input, 25 frames, test height 32 and width at least 100, 0.16 s and 0.53 s per sample on
  a Xeon/K40 workstation, $\delta=3$ (§3.2); 8.3 M parameters, 33 MB (§3.3).
- DBNet: eqs. 1–2 with $k=50$; label shrink eq. 6 with $r=0.4$; inference on the
  probability map, threshold 0.2, unclip eq. 10 with $r'=1.5$; speed with batch 1 on a
  1080 Ti; DB-ResNet-18 (736) at 62 frames/s on MSRA-TD500.
- TrOCR: $384\times384$ input and $16\times16$ patches; beam search, beam 10; model sizes
  62 M, 334 M and 558 M; IAM case-sensitive CER 3.42 and 2.89; 36-character filter for
  scene text; SROIE word-level F1; Table 5 speeds.
- LayoutLM: 2-D position embeddings (§2.2); coordinates scaled to 0–1,000 (§3.4);
  Tesseract OCR (§3.3); FUNSD F1 0.7866 and 0.7927 (§3.6).
- Donut: OCR error propagation (abstract); Swin encoder, BART decoder, JSON conversion
  (§2.2); pseudo-OCR pre-training, SynthDoG (§2.3); field-level F1 and TED accuracy
  (§3.1); $2560\times1920$, max length 1,536, P40 GPU (§3.2); CORD 0.7 s per image at
  $1280\times960$ with 91.1 accuracy (§3.3); resolution study (§3.4).
- OCR-D: grapheme clusters in NFC, white space counted, text concatenated in reading
  order; Levenshtein example; CER, normalized CER, granularity; WER with the normalized
  denominator and TR29 word boundaries; bag-of-words error; layout and reading-order
  evaluation; IoU; Unicode normalization; Flexible Character Accuracy.

Disagreements between the paper and the implementation, recorded in the note (FR-036):

| Aspect | DBNet paper | OpenCV 4.13.0 `TextDetectionModel_DB` |
| --- | --- | --- |
| Binarization threshold | 0.2 (Label generation, inference paragraph) | `binaryThreshold` 0.3 (`model.cpp` L1332; header L1895) |
| Unclip ratio | $r'=1.5$ (eq. 10) | `unclipRatio` 2.0 (`model.cpp` L1334; header L1897), same formula `area * unclipRatio / length` (L1500–L1508) |
| Instance score filter | Not described | `polygonThreshold` 0.5 (L1333, L1424) |

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 332 → 4,152. The note
compares five families across four pipeline stages and their evaluation protocols,
which justifies exceeding 3,000 words; mechanism detail is limited to what a choice or
a diagnosis needs.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Stage table with inputs, outputs, frames and types; units (dpi, points, CRNN height 32, TrOCR $384\times384$, LayoutLM 0–1,000, Donut $2560\times1920$); OCR-D character definition; pipeline role and downstream contract |
| Intuition | Shallow | Developed | One mechanism per family; constructed two-column invoice illustration; Mermaid diagram of the pipeline and the OCR-free path |
| Prerequisites | Shallow (conventions only) | Developed | Links to CV-ACQUISITION, CV-MORPHO, CV-HOMOGRAPHIE, CV-IOU-AP, CV-REPRESENTATIONS, CV-VLM, CV-METRIQUES-APPLIQUEES |
| Assumptions | Shallow | Developed | Legibility, linear text, alphabet coverage, CTC frame condition, conditional independence, defined reading order; degenerate cases |
| Procedure | Shallow | Developed | Pipeline pseudocode with the purpose of each step; four-family comparison table with reported sizes and speeds |
| Mathematics | Shallow (CER only) | Developed | CTC probability, forward recursion and decoding; DB binarization, shrink and unclip; classic and normalized CER, WER convention, alignment recursion; TED accuracy; worked examples A–D |
| Parameters | Shallow (list) | Developed | Ten-row table with paper values and OpenCV defaults; four-step tuning approach |
| Properties | Absent | Developed | Alignment-free training, invariances, uncalibrated scores, language priors, inherited OCR errors, order dependence of CER |
| Cost and implementation | Shallow (one sentence) | Developed | Cost drivers; reported speeds with hardware; OpenCV 4.13 `TextRecognitionModel` and `TextDetectionModel_DB` contracts; PyTorch 2.9 `CTCLoss` contract; execution status |
| Evaluation | Shallow | Developed | Metric table per output; published results with setting; proposed 300 → 150 dpi variation with oracle-box control; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Nine-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices among CTC, autoregressive, OCR-plus-layout, OCR-free, rules and VLMs; industrial uses labelled as project reasoning; sources split into scientific and implementation sources |

Constructed examples are recomputed by
[`checks/74-ocr-documents.py`](checks/74-ocr-documents.py) (19 assertions): CTC map on the
published examples; minimum frames (6 for "hello" and "1000"), confirmed by brute force;
5 alignments of "ab" in 3 frames and forward recursion equal to the brute-force sum
(0.261); best path returning "" while "a" has probability 0.64; CRNN 4 px per frame and
the "1000" frame budget; classic versus normalized CER (2.0 versus 2/3; 0.05%);
Levenshtein distance of OCR-D's example (3); "1000" → "100" as one deletion; print-size
arithmetic (41.7 px, 20.8 px, 12.5 px and scale factors); DB shrink and unclip on
$40\times40$, $120\times40$ and $400\times40$ boxes with $r'=1.5$ and 2.0.

## Applied corrections

- [Reference](../../../vault/70-reconnaissance-representations/references/74-ocr-documents.md),
  revision 7 → 8: body rewritten and deepened as above; appendices aligned with the card
  fixes ("Question of work" → "Working question", "Reference Response" → "Reference
  answer", "Example of Business Difference" → "Example of a business-relevant
  difference", "Keep normalization rules … in the assessment" → "Fix the normalization
  rules … in the evaluation", "A document of 2 000 characters … 0,05%" → "A
  2,000-character document … 0.05%", "predicted normalization" → "predefined
  normalization", "edges" → "boundary conditions", "weights the pages as well" →
  "weights every page equally", "arrays" → "tables", "sorting by height" → "sort by
  vertical position", "intertwine" → "interleave", "distance from Levenshtein" →
  "Levenshtein distance", "built order model" → "order model constructed by the
  project", "material results" → "hardware results"); sources split into scientific and
  implementation sources; closing provenance line replaced. Front matter unchanged except
  `revision`; H1 and the six `### CV-…` headings kept.
- [Cards](../../../vault/70-reconnaissance-representations/74-ocr-documents.md): expected
  answers of CV-OCR-001 and CV-OCR-002 changed as quoted above. Further explanations:
  identical fixes to the appendix, plus "Evaluate each of the deliverables useful to the
  product with reference and standardization rules" → "Evaluate each output the product
  uses, with its own reference and normalization rules"; "case N=0 … a simple proportion
  of false characters" → "the N=0 case … simply the proportion of wrong characters"; "an
  editing convention that has ten insertions" → "an edit alignment with ten insertions";
  "a new recognition language does not correct this contract" → "changing the
  recognizer's language does not fix a layout or ordering contract"; "fake" → "wrong".
  Blocking errors: "Confounds near global text and correctly structured invoice" →
  "Confusing an almost correct global text with a correctly structured invoice"; "Rotate
  arbitrarily to 1 without announcing another protocol" → "Arbitrarily clipping the CER
  to 1 without announcing another protocol"; gerund form for CV-OCR-003. Source lines:
  "Viewed on" → "consulted on". Questions, IDs, objectives, families, tags and target deck
  unchanged.

No other vault card repeats a corrected claim (`rg` over `vault/` for CER, WER, CTC,
TrOCR, CRNN, Donut, LayoutLM and DBNet: only CV-METRIQUES-APPLIQUEES names CER/WER as a
metric family, without a contradicting definition).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run). The 2026-10-20 proposal "Aggregate CER per medium mic/macro" was never
registered; its content now lives in the CV-OCR-002 explanation (2026-11-08) and is not
proposed again.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-OCR-01 | CV-OCR | Explain why a CTC recognizer reads "1000" as "100" on narrow print and compute whether a crop width and frame stride can emit a given string | No card trains the recognition mechanism; the algorithm and understanding families are absent | Reasoning; Mathematics, worked example A | 1 card, 3 criteria (blank between repeats; $T\ge\lvert l\rvert+r$; frames from width and stride) | [Graves et al. 2006, §3.1 and §4.1](https://www.cs.toronto.edu/~graves/icml_2006.pdf); [CRNN §3.2](https://arxiv.org/abs/1507.05717) |
| P-CV-OCR-02 | CV-OCR | Choose a recognition family for serial numbers on parts, handwritten forms and invoices that need box evidence, and name one discriminating test for each | No card trains the decision this comparison note exists for | Design; Alternatives and applications | 1 card, 3–4 criteria | [CRNN §2.3.3](https://arxiv.org/abs/1507.05717); [TrOCR Tables 4–5](https://arxiv.org/abs/2109.10282); [Donut §3.3–§3.4](https://arxiv.org/abs/2111.15664) |

No defective question was found.

## Sources

Scientific sources, opened at the passages listed (PDF text extracted with `pdftotext`):

- Graves et al., [CTC, ICML 2006](https://www.cs.toronto.edu/~graves/icml_2006.pdf): §3.1, §3.2, §4.1.
- Shi, Bai and Yao, [CRNN, arXiv 1507.05717](https://arxiv.org/abs/1507.05717): §2.1, §2.3.1–§2.3.3, §3.2, §3.3.
- Liao et al., [DBNet, arXiv 1911.08947](https://arxiv.org/abs/1911.08947): Methodology (Binarization, Differentiable binarization, Label generation and inference paragraph), experiments (implementation details and speed).
- Li et al., [TrOCR, arXiv 2109.10282](https://arxiv.org/abs/2109.10282): Introduction, Model Architecture, Model Initialization, Settings, Evaluation Metrics, Tables 1, 4 and 5.
- Xu et al., [LayoutLM, arXiv 1912.13318v5](https://arxiv.org/abs/1912.13318): §2.2, §3.3, §3.4, §3.6.
- Kim et al., [Donut, arXiv 2111.15664v5](https://arxiv.org/abs/2111.15664): abstract, §2.2, §2.3, §2.4, §3.1, §3.2, §3.3, §3.4.
- [OCR-D Quality Assurance specification](https://ocr-d.de/en/spec/ocrd_eval.html) (HTML, text extracted locally): Text Evaluation (Characters, Levenshtein Distance, CER, CER Granularity, WER, Bag of Words), Layout Evaluation, Reading Order, IoU, Unicode Normalization, Flexible Character Accuracy, Reading Order Evaluation.

Implementation sources (read, not executed):

- [OpenCV 4.13.0 `modules/dnn/include/opencv2/dnn/dnn.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/dnn/include/opencv2/dnn/dnn.hpp): L1676–L1760, L1778–L1782, L1890–L1932.
- [OpenCV 4.13.0 `modules/dnn/src/model.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/dnn/src/model.cpp): L700–L757, L840–L880, L1326–L1335, L1398–L1470, L1500–L1508.
- [PyTorch 2.9 `torch.nn.CTCLoss`](https://docs.pytorch.org/docs/2.9/generated/torch.nn.CTCLoss.html).

Failed accesses and limits:

- ICDAR robust-reading protocols (detection IoU threshold, end-to-end matching) were not
  opened; the note relies on OCR-D's region IoU and links CV-IOU-AP for matching instead
  of stating an ICDAR threshold.
- Clausner et al. 2013 (reading-order evaluation) was not opened; the note uses OCR-D's
  description of it.
- Context7 was not available in this session (see the scope record); versioned OpenCV
  code and PyTorch documentation replaced it. docs.opencv.org was not used (HTTP 403 in
  this session per the pilot).
- The TrOCR inference hardware for Table 5 was not found in the passages read; the note
  says so.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | ECHEC caused only by `80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md` (another agent's in-progress file); no error in the files of this subject |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 268 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/74-ocr-documents.py` | 19 checks passed |
| `git diff --check -- vault/70-reconnaissance-representations/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/70-reconnaissance-representations/74-ocr-documents.md` | 3 cards, 268 to 367 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card protected lines identical; reference front matter identical except `revision: 7` → `8`; H1 and per-card headings unchanged; `$$` balanced; table column counts consistent; local links resolve |

No OCR model, detector or benchmark was executed; the proposed baseline and variation
are protocols, not results. The Mermaid diagram and tables were not rendered in Obsidian,
and AnkiDroid rendering of the corrected cards is unverified. This is agent self-review,
without independent scientific validation or measurement of learner proficiency.
Export status: **to republish with `paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator:
the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-OCR revision 8,
CV-OCR-001 to -003, corrections listed above, Agent Claude Code self-review, to republish
with `paquet-anki`) and the proposal register (P-CV-OCR-01, P-CV-OCR-02).
