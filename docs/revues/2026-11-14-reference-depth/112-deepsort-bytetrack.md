# Review — DeepSORT, ByteTrack and multi-object association — 2026-11-14

## Overview

4 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 6 to revision 7. Highest severity per card before correction:
0 blocking, 1 important, 3 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The note is the comparison of association methods built on SORT. It now covers
DeepSORT, ByteTrack's BYTE and OC-SORT with their equations, code defaults and protocols;
the SORT baseline stays in
[CV-SORT](../../../vault/110-tracking-association/references/111-sort.md).

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ASSOCIATION-001 | Appearance, gating and cascade added to SORT's motion: confirmed (DeepSORT §2.2 eqs. 1–6, §2.3). Expected answer ended "according to its design" (vague); "waterfall" for cascade in the appendix-mirrored paragraph | Comparison: what each cue contributes | 3 expected criteria; 346 → 349 lexical words | Aligned with CV-FUSION's 9.4877 gate | Minor | Expected answer made explicit (language fix); language fixes; Source line cites §§2.2–2.3 and `tracker.py` |
| CV-ASSOCIATION-002 | High scores first, low scores only for remaining tracks, unmatched low boxes deleted "since we view them as background": confirmed (ByteTrack §3). Expected answer "the weak not associated are rejected according to the pipeline" imprecise | Algorithm: evidence to continue versus to start a track | 2 expected criteria; 377 → 400 lexical words | Code adds a new-track margin of 0.1 above $\tau$ (L154, L266) | Minor | Sourced precision of the expected answer; one sentence added on the code's new-track margin; language fixes |
| CV-ASSOCIATION-003 | Embedding domain and separability, crop quality, physical ambiguity: confirmed as a diagnosis consistent with DeepSORT §2.4 (pedestrian ReID training data) and §2.2 (threshold tuned on separate data). Expected answer "the field of embeddings" mistranslated *domaine* (training domain), hiding the key criterion | Diagnosis: transfer versus true indistinguishability | 2 expected criteria; 343 → 342 lexical words | "Survey built", "Test of Separability", "threshold ReID" | Important | Meaning-restoring fix of the expected answer; language fixes; Source line cites §2.2 and §2.4 |
| CV-ASSOCIATION-004 | Fix detections to compare associations: confirmed practice in DeepSORT §3 ("re-run SORT on the same detections") and ByteTrack §4.2; SORT Table 1 shows the detector effect. "Plan factoriel minimal" left in French | Evaluation: isolating the association | 2 expected criteria; 347 → 349 lexical words | Aligned with CV-SORT evaluation | Minor | Language fixes; Source line cites SORT §3.1 and ByteTrack §4.2 |

Expected-answer changes:

- CV-ASSOCIATION-001 (language fix): "Appearance/ReID and gating/cascade strategies, in
  addition to movement, according to its design." → "Appearance (ReID) descriptors, a
  motion gate and a matching cascade, in addition to SORT's motion prediction."
- CV-ASSOCIATION-002 (sourced precision, ByteTrack §3): "No: it first exploits high scores,
  then tries to recover weak observations for the remaining tracks; the weak not associated
  are rejected according to the pipeline." → "No: it first associates high-score boxes, then
  tries to recover low-score observations for the remaining tracks; unmatched low-score boxes
  are discarded as background."
- CV-ASSOCIATION-003 (meaning-restoring): "Discrimination and the field of embeddings, as well
  as the quality of the crops and physical ambiguities of the parts." → "The discriminative
  power and training domain of the embeddings, as well as crop quality and the physical
  ambiguity of the parts."

Explanation added (CV-ASSOCIATION-002): "In the official code a new track also needs a score
at least 0.1 above the high-score threshold" (byte_tracker.py L154, L266).

Protected fields not edited: `Objective:` lines of CV-ASSOCIATION-002 ("understand the use of
low scores ByteTrack" → proposed "Understand ByteTrack's use of low-score detections"),
CV-ASSOCIATION-003 ("check the transfer ReID" → proposed "Check ReID transfer") and
CV-ASSOCIATION-004 ("separate detector and association", lowercase). No question is
defective.

## Reference findings

Claims of revision 6 checked: DeepSORT combines motion, Mahalanobis gating, appearance and a
cascade (confirmed, §2.2–2.3); ByteTrack associates high then low scores and does not start
tracks from unmatched low boxes (confirmed, §3); cosine distance $1-a^Tb$ for unit vectors
(confirmed, eq. 3); mixing thresholds of different distances is not a probabilistic fusion
(consistent with eq. 5 and the use of $\lambda=0$). The AB3DMOT sentence was not re-read and is
kept as a qualified pointer. No scientific error; the body was one to three sentences per
section, with mistranslations ("gating Mahalanobis", "low discriminants", "affectation",
"waterfall", "Plan factoriel minimal", "built protocols").

New claims verified for revision 7: DeepSORT 8-D state, tentative period, $A_{\max}$ (§2.1);
eqs. 1–6, $t^{(1)}=9.4877$, gallery of 100, $\lambda=0$ with camera motion (§2.2); cascade
motivation and final IoU stage (§2.3); descriptor training data, 128-D, 2,800,864 parameters,
30 ms for 32 boxes on a GTX 1050 mobile (§2.4); MOT16 protocol and Table 2 (§3). ByteTrack:
motivation (§1), Algorithm 1 and stages, IoU only for the second association, lost tracks
not output, 30-frame buffer (§3); datasets, metrics, $\tau=0.6$, IoU 0.2 rejection (§4.1);
similarity ablation and BYTE versus SORT and DeepSORT (§4.2). OC-SORT: abstract, ORU (§4.1,
eqs. 6–7), OCM (§4.2, eq. 8), OCR.

Disagreements between papers and official code (FR-036):

| Aspect | Paper | Official code |
| --- | --- | --- |
| DeepSORT cost | $\lambda d^{(1)}+(1-\lambda)d^{(2)}$ (eq. 5) | Appearance distance with Mahalanobis gate only, i.e. $\lambda=0$ (`tracker.py` L95–L103) |
| DeepSORT gallery | Last 100 descriptors (§2.2) | `nn_budget=None`, no limit (`deep_sort_app.py` L250–L251) |
| DeepSORT detection threshold | 0.3 on MOT16 (§3) | `min_confidence=0.8`, NMS overlap 1.0 (L236–L245) |
| ByteTrack low boxes | All boxes below $\tau$ (Algorithm 1) | Only $0.1<\text{score}<\tau$; a score equal to $\tau$ is in neither set (`byte_tracker.py` L177–L181) |
| ByteTrack first-stage rejection | IoU < 0.2 (§4.1) | Cost $1-\mathrm{IoU}\cdot\text{score}$ against `match_thresh=0.9` (`matching.py` L173–L181; `tools/track.py` L107) |
| ByteTrack track creation | Unmatched high-score boxes (§3) | Score at least $\tau+0.1$ (L154, L266) |
| ByteTrack second association | Remaining tracks $T_{remain}$ (§3) | Only tracks currently in the tracked state; lost tracks need a high-score box (L230–L232) |
| ByteTrack lost buffer | 30 frames (§3, §4.1) | `int(frame_rate/30*track_buffer)` frames (L155–L156) |

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 322 → 3,166.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Three-method contract table (extra input, state, cue, life cycle); descriptor and score contracts; frame-rate handling; output of lost tracks; pipeline role |
| Intuition | Shallow | Developed | One mechanism per method in plain terms; Mermaid flow of the official ByteTrack tracker with its thresholds |
| Prerequisites | Shallow (one link) | Developed | CV-FUSION, CV-BIOMETRIE and CV-NMS links |
| Assumptions | Shallow | Developed | Appearance discriminability, linear motion, informative low scores, unreliable Re-ID on low boxes; observability limits |
| Procedure | Shallow | Developed | DeepSORT pseudocode, BYTE stages, OC-SORT additions; purpose of each step |
| Mathematics | Shallow (one formula) | Developed | DeepSORT eqs. 1–6 with units and gate, height-scaled noise, BYTE costs in paper and code, OC-SORT eq. 8; worked examples A (cascade) and B (ByteTrack routing) |
| Parameters | Shallow (list) | Developed | Eleven-row table with paper value, code default and interactions; tuning approach |
| Properties | Shallow | Developed | Appearance versus identity, gating limits, measured trade-offs, detector dependence, domain dependence of cue choice |
| Cost and implementation | Shallow | Developed | Descriptor cost with hardware, distance cost with variables, OC-SORT speed; implementation contracts at pinned commits; execution status |
| Evaluation | Shallow | Developed | DeepSORT MOT16 and ByteTrack MOT17 evidence with protocol and side effects; proposed baseline and second-association variation with confound; measurement limits |
| Failure modes and diagnosis | Shallow (two sentences) | Developed | Seven-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices among SORT, DeepSORT, BYTE, OC-SORT and 3D tracking; industrial uses labelled as project reasoning; sources split |

Constructed examples are recomputed by
[`checks/112-deepsort-bytetrack.py`](checks/112-deepsort-bytetrack.py) (10 assertions):
$\chi^2$ quantiles 9.4877 (4 dof) and 5.9915 (2 dof), cosine threshold 0.2 as 36.9°,
Mahalanobis distance of a recent versus a stale track ($S$ 73.7 versus 794 px$^2$; $d^2$ 5.43
versus 0.50), height scaling of the noise, ByteTrack score routing and fused costs, the
frame-rate-scaled buffer, the relative changes of the published results and the cascade
versus global assignment choice.

## Applied corrections

- [Reference](../../../vault/110-tracking-association/references/112-deepsort-bytetrack.md),
  revision 6 → 7: body rewritten and deepened; appendix language fixed ("Question of work",
  "Reference Response", "Reasoning for Association", "Example of limit … low discriminants …
  affectation", "Example of a confusing factor" → "confounding factor", "waterfall" →
  "cascade", "unitary embeddings" → "unit-norm embeddings", "Two uses of score", "filter
  upstream of the detector" → "filter between the detector and the tracker", "Test of
  Separability", "Plan factoriel minimal" → "Minimal factorial design", "built protocols").
  Sources split; closing provenance line replaced. Front matter unchanged except `revision`;
  H1 and per-card headings kept.
- [Cards](../../../vault/110-tracking-association/112-deepsort-bytetrack.md): expected answers
  of 001–003 corrected as quoted above; explanation of 002 extended; shared paragraphs aligned
  word for word with the appendices; other fixes include "Why keep some boxes weak" → "Why keep
  some low-score boxes", "Product Compromise" → "Product trade-off", "a real hidden box" → "a
  real occluded box", "Survey built" → "Constructed investigation", "Assimilate the second
  association to a massive creation of weak tracks" → "Equating the second association with
  mass creation of tracks from low-score boxes", "Assign any final gain to the tracker without
  check upstream" → "Attributing any final gain to the tracker without controlling the
  upstream stages". Source lines cite exact sections and code lines. IDs, questions,
  objectives, families, tags and target deck unchanged.

Other subjects: CV-FUSION (`13-kalman-ekf-eskf`) cites the same 9.4877 gate, consistent; no
other card repeats a corrected claim.

## Proposals

To register as `pending` in the [proposal register](../propositions.md):

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-ASSOCIATION-01 | CV-ASSOCIATION | Explain why DeepSORT's matching cascade lets recently seen tracks choose first, from the effect of covariance growth on the Mahalanobis distance | The cascade is named in CV-ASSOCIATION-001 but its mechanism is untested; registers the unregistered 2026-10-20 idea "Explain the priority of the DeepSORT waterfall" | Algorithm; worked example A | 1 card, 3 criteria (covariance grows while unseen; $d^2$ shrinks; cascade by age) | [Wojke et al. 2017, §2.3 and Listing 1](https://arxiv.org/abs/1703.07402) |
| P-CV-ASSOCIATION-02 | CV-ASSOCIATION | Choose among SORT, DeepSORT, BYTE and OC-SORT for a stated scene (similar-looking objects, frequent partial occlusion, non-linear motion, compute budget) and name the discriminating test | The "design" family is absent for association; the conditional choices of the note are untested | Design; Alternatives | 1 card, 3–4 criteria | [ByteTrack §4.2](https://arxiv.org/abs/2110.06864); [OC-SORT §4](https://arxiv.org/abs/2203.14360); [DeepSORT §2.2](https://arxiv.org/abs/1703.07402) |

## Sources

Scientific sources, opened at the passages listed (arXiv PDFs, text extracted with
`pdftotext`):

- DeepSORT, [arXiv 1703.07402v1](https://arxiv.org/abs/1703.07402): abstract, §2.1, §2.2 (eqs. 1–6, Listing 1), §2.3, §2.4 (Table 1), §3 (Table 2).
- ByteTrack, [arXiv 2110.06864v3](https://arxiv.org/abs/2110.06864): §1, §3 (Algorithm 1), §4.1, §4.2.
- OC-SORT, [arXiv 2203.14360v3](https://arxiv.org/abs/2203.14360): abstract, §4.1, §4.2, OCR paragraph.
- SORT, [arXiv 1602.00763v2](https://arxiv.org/abs/1602.00763): §3.1, Table 1 (read for CV-SORT).

Implementation sources:

- [nwojke/deep_sort at f08cf1d](https://github.com/nwojke/deep_sort/tree/f08cf1dc470eeb1cd2add1cbf077d95ac6c48aab): `tracker.py`, `linear_assignment.py`, `kalman_filter.py`, `track.py`, `nn_matching.py`, `deep_sort_app.py`.
- [ifzhang/ByteTrack at d1bf019](https://github.com/ifzhang/ByteTrack/tree/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99): `yolox/tracker/byte_tracker.py`, `yolox/tracker/matching.py`, `tools/track.py`.

Not opened: AB3DMOT (kept as a qualified pointer), the OC-SORT code, the Ristani et al. IDF1
paper (IDF1 quoted from HOTA §4.2 in CV-SORT). No access failure. Context7 was not available.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, minimum 260 lexical words, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/112-deepsort-bytetrack.py` | 10 checks passed |
| `git diff --check` on the vault files of CV-SORT and CV-ASSOCIATION | No whitespace error |
| `inventaire_cartes.py vault/110-tracking-association/` | No anomaly; CV-ASSOCIATION 349, 400, 342 and 349 words |
| Protected-field comparison with the pre-edit copy | Card `## CV-…`, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` lines identical; front matter identical except `revision: 6` → `7`; H1 and per-card headings unchanged; `$$` and fences balanced |

No tracker was run; examples re-implement rules of the pinned code in plain Python. The
proposed variation is a protocol. Rendering in Obsidian and AnkiDroid is unverified. Agent
self-review only. Export status: **to republish with `paquet-anki`**.

Shared files not edited, entries needed: `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-ASSOCIATION revision 7, CV-ASSOCIATION-001 to 004, corrections above, to republish with
`paquet-anki`) and the proposal register (P-CV-ASSOCIATION-01, P-CV-ASSOCIATION-02).
