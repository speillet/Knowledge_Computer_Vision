# Review — Evaluating identities, trajectories and 3D localization — 2026-11-16

## Overview

Mode: `ajouter` for the accepted proposal P-CV-METRIQUES-TEMPS-01. One card added,
CV-METRIQUES-TEMPS-006; the five existing cards were not re-audited in this pass (see the
[2026-11-14 report](../2026-11-14-reference-depth/132-tracking-trajectoires.md)) and are
byte-for-byte unchanged.
Self-review: Agent Claude Code (revue-cartes).
Editorial status: redige. Reference revision 7 → 8.

## Added card

| Card | Accuracy | Relevance | Gradability | Consistency | Family |
| --- | --- | --- | --- | --- | --- |
| CV-METRIQUES-TEMPS-006 | The identity mapping is the minimum-cost one-to-one solution of a bipartite graph with one false-negative node per true trajectory and one false-positive node per computed trajectory; the cost of a pair counts the false-negative frames of the true trajectory and the false-positive frames of the computed one; IDTP, IDFN, IDFP and IDF1 follow: confirmed (Ristani et al. §3.3 eqs. 3–5, §3.4 eqs. 6–11). The mapping is "the most favorable to the tracker": confirmed (§3.4, property 2). One fragmentation and seven fragmentations both charged 33% of the trajectory: confirmed (§3.1, Fig. 1 caption). CLEAR MOT counts a mismatch once, where the mapping changes, treats intermediate segments as correct, and rejects a sequence-level best mapping because the swap time "drastically influences" its value: confirmed (Bernardin and Stiefelhagen §2.1.2, Fig. 2(c); procedure §2.1.3 step 2; MOTA eq. 2). TrackEval solves the same assignment on a padded cost matrix and computes IDF1 as IDTP/(IDTP + 0.5 IDFP + 0.5 IDFN): confirmed at 12c8791 (`identity.py` L52–L85, L134). IDTP 18 and 16, IDF1 0.90 and 0.80, MOTA 0.95, graph costs 12 and 8, the one-fragment formula, the one-frame relabel (MOTA 0.90, IDF1 0.95) and the blocking-error values (0.70, 1, 36/38): project constructions, recomputed by the check script | Reasoning: turns the qualitative detection/identity distinction of CV-METRIQUES-TEMPS-001 into a hand computation and trains why one switch has no fixed IDF1 cost, which is needed to read a tracker comparison. No other card computes identity counts: `grep -rn IDF1 vault` over card files finds only the Source line of CV-METRIQUES-TEMPS-001; the tracking cards (CV-SORT-006 diagnoses the causes of an ID change, CV-ASSOCIATION-004 controls a tracker comparison) do not compute a metric. No frame-rate (P-CV-METRIQUES-TEMPS-02) or evaluator-reconciliation (P-CV-METRIQUES-TEMPS-03) criterion | 3 expected criteria (global one-to-one mapping and the choice for A; counts and IDF1 for X and Y; cost set by the shorter piece, contrasted with one CLEAR mismatch and MOTA 0.95 for both); 608 lexical words, 202 in the expected answer | Scenario, notation and pedestrians of worked example A; worked example A extended with the same numbers; tags `cv::d13`, `pole::B pole::C pole::D` match the reference | Reasoning |

The question gives explicit per-frame labels and states the overlap assumption (each box
overlaps only its own pedestrian, above the threshold, with no missed or extra box), so
the per-frame correspondences are fixed and only the identity mapping is computed.

## Reference findings

Claims of the identity section checked again at the exact passages: the bipartite graph,
eqs. 3–11 and the one-to-one mapping versus CLEAR MOT's per-sequence many-to-many mapping
(Ristani et al. §3.3–§3.5): confirmed; "most favorable to the tracker" and "in the same
currency" (§3.4): confirmed; TrackEval `identity.py` lines cited in the note (L15, L40–L45,
L52–L85, L134): confirmed. One minor imprecision: the note described the edge cost as
"the frames where the two detections do not match". Eq. 4 sums the false-negative frames of
$\tau$ and the false-positive frames of $\gamma$, which include the frames where the other
trajectory is absent, and the graph also holds the false-negative and false-positive nodes
that make an unmatched identity cost all its frames. The fragment calculation depends on
exactly those frames, so the sentence was made precise.

Worked example A: its IDF1 and MOTA rows (0.50, 0.75, 0.857, 0.80; 0.90, 0.95, 0.75, 0.80)
were recomputed with the paper's graph and with a re-implementation of TrackEval's cost
matrix: confirmed. Its HOTA columns were not recomputed in this pass (2026-11-14 script).

Implementation note, not developed in the card: TrackEval counts, for each (gtID, prID),
every frame whose similarity reaches the threshold, without a per-frame one-to-one
matching (`identity.py` L55–L57); under the card's assumption this equals the paper's
count. Differences between evaluators belong to P-CV-METRIQUES-TEMPS-03.

No text in the reference called P-CV-METRIQUES-TEMPS-01 pending (search for "pending" and
"P-CV-METRIQUES" in the note and the card file). Outside the register and the scope
record, the proposal is named in the 2026-11-08 overview and the 2026-11-14 subject
report, dated records that are not rewritten. The register's wording, "an ID switch's effect
on IDF1", is followed through the scope record's objective: the card shows that the
effect belongs to the lengths of the pieces, not to the switch event.

## Applied corrections

- `vault/130-evaluation-fiabilite/132-tracking-trajectoires.md`: CV-METRIQUES-TEMPS-006
  appended after CV-METRIQUES-TEMPS-005; the preceding content is a byte-identical prefix
  of the new file.
- `vault/130-evaluation-fiabilite/references/132-tracking-trajectoires.md`, revision 7 → 8:
  identity-metrics edge cost stated with the false-negative and false-positive frames and
  nodes (Ristani et al. §3.3, eq. 4); worked example A extended with "Duration of a
  fragment" (IDF1 $1-\min(k-1,11-k)/20$ against one mismatch and MOTA 0.95, the one-frame
  relabel, the CLEAR MOT §2.1.2 and Ristani et al. §3.1 design statements); the CLEAR MOT
  and Ristani et al. source bullets extended with §2.1.2, Fig. 2(c), §3.1 and Fig. 1; the
  card listed under related flashcards; the constructed-example line names this pass's
  script; closing provenance line extended. Front matter unchanged except `revision`;
  `statut: redige` and `provenance: agent` kept.

For the correction log (to be entered by the coordinator): CV-METRIQUES-TEMPS revision 8,
2026-11-16; CV-METRIQUES-TEMPS-006 added (P-CV-METRIQUES-TEMPS-01, accepted 2026-11-09);
"an edge cost counting the frames where the two detections do not match" → the false-negative
and false-positive frames of the pair, including frames where one trajectory is absent,
with false-negative and false-positive nodes for unmatched identities (Ristani et al. §3.3,
eqs. 3–4); worked example A extended with the duration of a fragment. No card and no
other reference repeats the edge-cost wording (search for "do not match" and "edge cost"
over `vault/`). Agent Claude Code, self-review; export status: to republish with
`paquet-anki`.

## Proposals

P-CV-METRIQUES-TEMPS-01: accepted by the learner on 2026-11-09, completed as
CV-METRIQUES-TEMPS-006. P-CV-METRIQUES-TEMPS-02 (frame-rate dependence) and
P-CV-METRIQUES-TEMPS-03 (reconciling MOT evaluators) stay pending; the card does not
anticipate them. No new proposal.

## Sources

Scientific sources:

- Ristani et al. 2016, [arXiv 1609.01775v2](https://arxiv.org/abs/1609.01775) (latest
  version, 2016-09-19, per the abstract page), PDF text extracted with pypdf 5.1.0: §2
  (fragmentation, merge and MOTA in their notation), §3 introduction, §3.1 and the Fig. 1
  caption, §3.3 eqs. 3–5, §3.4 eqs. 6–11 and the three properties, §3.5 comparison with
  CLEAR MOT.
- Bernardin and Stiefelhagen 2008, [CLEAR MOT, EURASIP JIVP](https://doi.org/10.1155/2008/246309),
  publisher PDF from the KIT repository
  ([publikationen.bibliothek.kit.edu/1000026323/2020897](https://publikationen.bibliothek.kit.edu/1000026323/2020897)),
  extracted with pypdf 5.1.0: §2.1.2 and the Fig. 2 caption, §2.1.3 steps 1–5, §2.2
  eqs. 1–5 and Fig. 3.

Implementation sources (Context7 is unavailable in this session):

- TrackEval at commit 12c8791b303e0a0b50f753af204249e622d0281a, GitHub raw:
  `trackeval/metrics/identity.py` (135 lines, read in full); `trackeval/metrics/clear.py`
  L55–L125 and L170–L186, read to check that the one-frame relabel also gives two
  switches there (counted against the last matched ID, L62–L65, L93–L97).

Failed access: the Springer article and PDF URLs (link.springer.com, the DOI and
jivp-eurasipjournals routes) returned a JavaScript client challenge or a redirect to a
login service; they were not bypassed, and the KIT copy of the same article was used.
The HOTA paper was not reopened: the card makes no HOTA claim, and the HOTA columns of
example A rest on the 2026-11-14 verification.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 -I docs/revues/2026-11-09-four-proposals/checks/132-tracking-trajectoires.py` | 8 checks passed |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 298 cards (shared tree, other agents' cards included) |
| `python3 scripts/learning_path.py` | OK: 60 references, 298 cards, minimum 260 lexical words, 0 errors |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/130-evaluation-fiabilite/132-tracking-trajectoires.md` | 6 cards, no anomaly; CV-METRIQUES-TEMPS-006 608 lexical words; next free ID 007 |
| `git diff --check -- vault/130-evaluation-fiabilite/` | No whitespace error |

The check script finds the identity mapping three ways by brute force over permutations,
with exact fractions: the paper's graph with its false-negative and false-positive nodes,
the maximum one-to-one sum of shared frames, and TrackEval's padded cost matrix
(`identity.py` L63–L85); CLEAR MOT mismatches follow §2.1.3. TrackEval itself was not
executed, and no tracker was run. The sequences are constructed, with perfect overlaps;
the formula $1-\min(a,b)/20$ holds for one fragment of A in this two-pedestrian clip
without detection errors. The card is longer than its siblings (608 against at most 399
lexical words) because it carries the computation, the graph costs that justify the
mapping and the CLEAR MOT design contrast. Agent self-review only; the Obsidian rendering
and the AnkiDroid rendering of the card are not verified. Export status: to republish
with `paquet-anki`. The proposal register, the progress log, the generated catalogue and
current-state counts are left to the coordinator.
