# Review — Biometric recognition, ArcFace and PAD — 2026-11-14

## Overview

2 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 7 to revision 8. Highest severity per card before correction:
0 blocking, 0 important, 2 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is a comparison note at *reperage* depth (priority V2, career track E). It
now separates 1:1 verification, 1:N identification and presentation attack detection
by their outputs and error definitions, develops ArcFace as the reference embedding
mechanism, and treats operating points and the amount of evidence they require. Metric
families across applications stay in
[CV-METRIQUES-APPLIQUEES](../../../vault/130-evaluation-fiabilite/references/134-metriques-applications.md).

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-BIOMETRIE-001 | Identity similarity does not establish presentation validity: consistent with NISTIR 8491 §1.1 (presentation attacks with the intent of impersonation preserve identity; PAD evaluated as a separate task). ArcFace normalized logits and target $\cos(\theta_y+m)$: confirmed (ArcFace §III-A, eqs. 2–3). Language: "Difference of Targets", "What the Margin Learns", "materiality of a photographic presentation or on screen", "At the inference", "the decision PAD" | Comparison: separates two outputs that a system must evaluate separately | 1 expected criterion with its justification; 341 → 338 lexical words | ID, question, tags and heading unchanged; wording aligned with the reference appendix | Minor | Language fixes in the explanation; expected answer unchanged |
| CV-BIOMETRIE-002 | EER is one point of the tradeoff; NIST ranks at FNMR at FMR $=10^{-6}$: confirmed (NIST FRTE 1:1). Zero-error bound $1-0.05^{1/n}\approx3/n$: confirmed by Mansfield and Wayman §3.4 (Rule of 3, with the dependence caveat) and recomputed (0.002991 for $n=1{,}000$). Language: "non-matte comparisons" for *nonmated*, "probability of false correspondence", "unilateral upper limit", French decimal commas "0,05" and "0,003", "1 000", "setting data", "wrongly rejected identities" for mated comparisons, blocking error "Assimilate EER and performance to any threshold" | Evaluation: chooses and justifies an operating point | 2 expected criteria; 358 → 355 lexical words | ID, question, tags and heading unchanged | Minor | Language and notation fixes in explanation and blocking error; expected answer unchanged |

No expected answer was changed.

## Reference findings

Claims of revision 7 checked against their passages:

- "FMR/FNMR describe comparison errors below a threshold": imprecise. FMR is the
  proportion of impostor comparisons *at or above* the threshold and FNMR the proportion
  of mated comparisons below it (NIST FRTE 1:1 page). Corrected in the body (task table and
  equations); no card repeats the wording.
- "FAR/FRR system also depend on procedure and acquisition failures": confirmed
  (Mansfield and Wayman, §2.4.2.1 para. 41 and §5.2 para. 156).
- EER as a balance point of a protocol, not a low-FMR result: consistent with NIST's
  reporting at FNMR at FMR $=10^{-6}$.
- NISTIR 8491 source: title, authors (Ngan, Grother, Hom), date (September 2023) and DOI
  confirmed on the NIST publication page; the report itself was opened.
- No other scientific error. Mistranslations obscured meaning: "Entries", "conditioned
  to the threshold", "Encode, search, and maintain the gallery", "Question of work",
  "Reference Response", "built cases", "material results".

New claims verified for revision 8 (main ones):

- ArcFace: eqs. 1–4, 512-D embedding, normalized weights and features, geodesic margin,
  combined margin with SphereFace and CosFace as special cases, Figs. 3–5 (§III-A); target
  angles from about $90^\circ$ to $30^\circ$ during training (§III-A, Fig. 4a); $112\times112$
  five-point crops, $s=64$, $m=0.5$, templates as feature centres, 8.9 and 15.4 ms per face,
  training data (§IV-A); pose and age gaps increase positive-pair angles (Fig. 10), LFW and
  YTF saturation, IJB-B and IJB-C protocol sizes and metrics (§IV-D).
- Mansfield and Wayman 2002: FAR, FRR, FMR, FNMR, non-self, decision versus matching errors
  (§2.4); Rule of 3 and Rule of 30 with the "over-optimistic" dependence caveat (§3.4);
  FAR and FRR formulas with FTA, PR and BER (§5.2).
- NIST FRTE 1:1: FNMR and FMR definitions; VISABORDER ranking at FMR $=10^{-6}$; demographic
  FMR summary with a threshold for overall FMR 0.0003.
- NIST FRTE 1:N: FNIR and FPIR definitions; FPIR $=0.003$ operating point; investigation
  mode with 50 candidates and FNIR as rank-1 miss.
- NISTIR 8491: definition of a presentation attack, impersonation and evasion (§1.1);
  APCER, BPCER, failure-to-process policy (§3.1–§3.3); APCER at BPCER $=0.01$ and BPCER at
  APCER $=0.01$ (§3.4); 82 algorithms, 45 developers, about 20,000 attacks and 21,000 bona
  fide presentations, 9 attack categories, framed versus zoomed print and replay attacks,
  sum-rule fusion (executive summary, §5.4).

Implementation contract (FR-036): OpenCV 4.13.0 `FaceRecognizerSF` aligns with a
five-point similarity transform to $112\times112$, normalizes features and returns a
cosine similarity or an $\ell_2$ distance; the official sample's thresholds 0.363 and 1.128
are the same decision for unit vectors (recomputed: 1.1287) and belong to one model.

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 298 → 3,560. The length
covers three tasks with different error definitions plus the evidence needed for low
error rates; embedding mechanics beyond ArcFace's loss are linked to CV-REPRESENTATIONS.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Task table with inputs, outputs and sourced error definitions; comparison versus transaction rates; ArcFace data contract (five-point alignment, $112\times112$, 512-D, cosine); pipeline role |
| Intuition | Shallow | Developed | Angular embedding, threshold as product, 1:N multiplication, PAD as another question; constructed door-access illustration tied to NISTIR 8491; Mermaid decision flow |
| Prerequisites | Shallow (conventions only) | Developed | Links to CV-REPRESENTATIONS, CV-CLIP, CV-DETECTEURS, CV-NMS, CV-ACQUISITION, CV-FLANN, CV-FIABILITE, CV-METRIQUES-APPLIQUEES |
| Assumptions | Shallow | Developed | Alignment, training domain, relative separability, independence of trials, open-ended attacks; observability (twins, $3/n$ floor, failures to acquire, non-faces) |
| Procedure | Shallow | Developed | Enrol, verify and identify pseudocode with purposes; three-task comparison table |
| Mathematics | Shallow (no equation) | Developed | ArcFace loss and margin condition; cosine–$\ell_2$ equivalence; FMR and FNMR formulas; FAR and FRR with FTA; Rule of 3 and Rule of 30; 1:1 to 1:N approximation; worked examples A–E |
| Parameters | Shallow (list) | Developed | Eight-row table; four-step tuning approach on person-grouped data |
| Properties | Shallow | Developed | Invariances, training-loss geometry versus test guarantees, calibration, demographic differentials, PAD coverage, no compliance |
| Cost and implementation | Shallow (one sentence) | Developed | Extraction time with its limits, gallery storage and search (example F), OpenCV 4.13 `FaceRecognizerSF` contract and sample thresholds; execution status |
| Evaluation | Shallow | Developed | Protocol table (FRTE 1:1, FRTE 1:N, FATE PAD, IJB-B/C, LFW/YTF); NIST PAD scale; proposed pose variation at fixed threshold with landmark confound; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Eight-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices between 1:1, thresholded 1:N, investigation mode, PAD and second factors; applications labelled as project reasoning; sources split into scientific and implementation sources |

Constructed examples are recomputed by
[`checks/75-embeddings-biometrie.py`](checks/75-embeddings-biometrie.py) (14 assertions):
margin in degrees (28.65°) and logits 55.43 versus 33.30 at $30^\circ$; the margin decision
condition; cosine 0.363 ↔ $\ell_2$ 1.1287; Rule-of-3 counts (29,956 and 2,995,731) and the
1,000-comparison bound (0.002991); IJB-C expected false matches (156.4, 15.6, 0.16); Rule
of 30 at $10^{-6}$ (30 M); 2,449 people giving 2,997,576 pairs; FPIR 0.632 for $N=10^6$ and
$f=10^{-6}$, and $f\approx3.0045\times10^{-9}$ for FPIR 0.003; FAR $9.7\times10^{-5}$ and FRR
0.0494; 2,048-byte templates, 2.048 GB and 512 M multiply-accumulates for $10^6$ templates;
accepted-error composition $1.03\times10^{-6}$ versus 1.0% under prevalence 0.99 and 0.01.

## Applied corrections

- [Reference](../../../vault/70-reconnaissance-representations/references/75-embeddings-biometrie.md),
  revision 7 → 8: body rewritten and deepened as above, including the corrected FMR and
  FNMR definitions; appendices aligned with the card fixes ("Question of work" → "Working
  question", "Reference Response" → "Reference answer", "built cases" → "constructed
  cases", "point of exploitation" → "operating point", "material results" → "hardware
  results", "presentation of the evaluation check and errors" → "presentation of the
  evaluation and its error rates", "binomial bound and system reasoning constructed" →
  "… constructed by the project"); sources split into scientific and implementation
  sources, with the NISTIR 8491 DOI; closing provenance line replaced. Front matter
  unchanged except `revision`; H1 and the four `### CV-…` headings kept.
- [Cards](../../../vault/70-reconnaissance-representations/75-embeddings-biometrie.md):
  CV-BIOMETRIE-001: "Difference of Targets" → "Different targets"; "What the Margin Learns"
  → "What the margin learns"; "It does not provide a label on the materiality of a
  photographic presentation or on screen. At the inference, … the decision PAD" → "It
  provides no label on whether the presentation is physically a photograph or a screen.
  At inference, … the PAD decision". CV-BIOMETRIE-002: "wrongly accepted comparisons and
  wrongly rejected identities" → "wrongly accepted nonmated comparisons and wrongly
  rejected mated comparisons"; "a very low rate of false correspondence" → "a very low
  false-match rate"; "set the threshold on setting data, then measure the rate of false
  non-matches at the level of FMR targeted" → "set the threshold on tuning data, then
  measure the false non-match rate at the target FMR"; "non-matte comparisons with
  probability of false correspondence" → "nonmated comparisons with false-match
  probability"; "The unilateral upper limit of 95% is then $1-0,05^{1/n}$" → "The one-sided
  95% upper bound is then $1-0.05^{1/n}$"; "Zero error on 1 000 comparisons thus remains
  compatible with a rate of around 0,003" → "Zero errors on 1,000 comparisons thus remain
  compatible with a rate of about 0.003"; blocking error "Assimilate EER and performance to
  any threshold" → "Equating the EER with performance at any threshold". Source lines:
  "constructed" → "constructed by the project", "consulted the" → "consulted on".
  Questions, IDs, objectives, families, tags and target deck unchanged.

No other vault card repeats a corrected claim (`rg` over `vault/` for FMR, FNMR, ArcFace,
APCER and presentation attack: CV-METRIQUES-APPLIQUEES distinguishes FMR/FNMR, FAR/FRR and
PAD consistently with this note).

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited by
this subject run). P-CV-BIOMETRIE-01 takes up the 2026-10-20 proposal "Set a rating 1:N
with open gallery", which was never registered, with the NIST definitions now verified.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-BIOMETRIE-01 | CV-BIOMETRIE | Explain why a 1:N search over a large open gallery needs a much stricter threshold than 1:1 verification, using FPIR and FNIR and an order-of-magnitude estimate | No card trains identification; FPIR/FNIR are untested | Reasoning or evaluation; Mathematics, worked example D | 1 card, 3 criteria (FPIR definition; growth with $N$; threshold set at deployed $N$) | [NIST FRTE 1:N](https://pages.nist.gov/frvt/html/frvt1N.html) |
| P-CV-BIOMETRIE-02 | CV-BIOMETRIE | Diagnose a deployed system whose transaction-level false rejection rate far exceeds the matcher's FNMR at the same threshold | Matcher versus decision errors (FTA, attempts) are untested | Diagnosis; Mathematics, worked example E | 1 card, 3 criteria (FAR/FRR versus FMR/FNMR; FTA term; per-transaction logging) | [Mansfield and Wayman 2002, §2.4.2.1 and §5.2](https://www.face-rec.org/databases/Mansfield02.pdf) |

No defective question was found.

## Sources

Scientific sources, opened at the passages listed:

- Deng et al., [ArcFace, arXiv HTML v4](https://arxiv.org/html/1801.07698v4) (text extracted locally): §III-A, §IV-A, §IV-D (Tables IV–IX captions and text, Fig. 10).
- Mansfield and Wayman, [Best Practices in Testing and Reporting Performance of Biometric Devices v2.01](https://www.face-rec.org/databases/Mansfield02.pdf) (PDF, `pdftotext`): §2.4 paras. 32–41, §3.4 paras. 84–86 and footnotes 4–6, §5.2 paras. 155–156.
- [NIST FRTE 1:1 Verification](https://pages.nist.gov/frvt/html/frvt11.html) (HTML): table introductions defining FNMR and FMR; demographic FMR summary.
- [NIST FRTE 1:N Identification](https://pages.nist.gov/frvt/html/frvt1N.html) (HTML): identification and investigation table introductions.
- Ngan, Grother and Hom, [NISTIR 8491](https://doi.org/10.6028/NIST.IR.8491) (publication page via WebFetch; PDF from nvlpubs.nist.gov with `pdftotext`): executive summary, §1.1, §3.1–§3.4, §5.4.

Implementation sources (read, not executed):

- [OpenCV 4.13.0 `objdetect/face.hpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/objdetect/include/opencv2/objdetect/face.hpp): L122–L160.
- [OpenCV 4.13.0 `objdetect/src/face_recognize.cpp`](https://github.com/opencv/opencv/blob/4.13.0/modules/objdetect/src/face_recognize.cpp): L42–L76.
- [OpenCV 4.13.0 `samples/dnn/face_detect.py`](https://github.com/opencv/opencv/blob/4.13.0/samples/dnn/face_detect.py): L108–L128.

Failed accesses and limits:

- ISO/IEC 19795-1 (performance testing) and ISO/IEC 30107-3 (PAD testing) are paywalled and
  were not read: **not verifiable** here. Definitions rely on Mansfield and Wayman 2002 (on
  which the ISO work drew) and on NISTIR 8491, which states that it adopts ISO/IEC 30107-3
  terminology.
- CosFace and SphereFace papers were not opened; the note describes them only through
  ArcFace's eq. 4 and §III-A.
- The hardware behind ArcFace's 8.9 and 15.4 ms per face is not stated in the passage read;
  the note says so.
- Context7 was not available in this session (see the scope record); versioned OpenCV code
  replaced it.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards (after moving a citation that began a line and was parsed as a link definition) |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 260 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/75-embeddings-biometrie.py` | 14 checks passed |
| `git diff --check -- vault/70-reconnaissance-representations/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/70-reconnaissance-representations/75-embeddings-biometrie.md` | 2 cards, 338 and 355 words, no anomaly |
| Protected-field comparison with the pre-edit copy | Card protected lines identical; reference front matter identical except `revision: 7` → `8`; H1 and per-card headings unchanged; `$$` balanced; table column counts consistent; local links resolve |

No face model, PAD algorithm or benchmark was executed; the proposed baseline and
variation are protocols, not results. The Mermaid diagram and tables were not rendered in
Obsidian, and AnkiDroid rendering of the corrected cards is unverified. This is agent
self-review, without independent scientific validation or measurement of learner
proficiency; it establishes no regulatory compliance. Export status: **to republish with
`paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the coordinator:
the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14, CV-BIOMETRIE
revision 8, CV-BIOMETRIE-001 and -002, language corrections listed above, Agent Claude
Code self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-BIOMETRIE-01, P-CV-BIOMETRIE-02).
