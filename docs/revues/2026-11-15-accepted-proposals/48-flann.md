# Review — FLANN — approximate nearest-neighbor search and distance conventions — 2026-11-15

## Overview

Mode: `ajouter` for the accepted proposal P-CV-FLANN-01. One card added, CV-FLANN-005;
the four existing cards were not re-audited in this pass (see the
[2026-11-14 report](../2026-11-14-reference-depth/48-flann.md)).
Self-review: Agent Claude Code (revue-cartes).
Editorial status: redige. Reference revision 7 → 8.

## Added card

| Card | Accuracy | Relevance | Gradability | Consistency | Family |
| --- | --- | --- | --- | --- | --- |
| CV-FLANN-005 | One-shot `knnMatch(query, train, k)` clones an empty matcher, adds `train` and matches through the clone: matchers.cpp L589–L598, `clone(true)` L1389–L1405. The clone builds an index because it has none: L659 then L1160–L1176. The overload is `const` and the train set "is not added to the train descriptors collection stored in the class object": features2d.hpp L1072–L1092. The stored-collection overload calls `train()` itself: matchers.cpp L647–L661. `add` raises a count (L1113–L1148) and `train()` rebuilds when the count exceeds the merged set, copying all descriptors into one matrix and building a new index (L1164–L1174, L423–L470). `match` and `radiusMatch` take the same path: L579–L609. `imgIdx` and `trainIdx`: L1407–L1429. Timings 1.02, 1.01, 612, 13 s: recomputed. Second-matcher swap and exhaustive buffer: project design, labelled as such | Practice: a frequent implementation trap that cancels the amortization CV-FLANN-001 computes, and an update policy that decides latency spikes in a live map | 3 expected criteria; 445 lexical words | Aligned with worked example A and the OpenCV contract of the reference; CV-FLANN-001 mentions the trap in one sentence of its explanation, while this card makes the restructuring and the rebuild policy the recall objective | Practice |

The question gives the per-call time and its insensitivity to `checks`, which point to
the build without naming it, and asks for the cost of an update policy. It does not
name `clone`, `train()`, the two-argument overload or the full rebuild.

## Reference findings

- The assumptions said that "OpenCV's matcher retrains when descriptors are added
  [matchers.cpp L1160–L1176]". This is imprecise: any `add` makes the next `train()` or
  match rebuild the whole index from all stored descriptors, after copying them into one
  matrix, with no incremental insertion (L423–L470, L1113–L1176). The bullet now says so.
- No error was found in worked example A or in the existing contract bullets. The
  contract gained the `const` one-shot overloads and their documentation, the shared
  clone path of `match`, `knnMatch` and `radiusMatch`, the implicit `train()` of the
  stored-collection overloads, the rebuild condition and the `imgIdx`/`trainIdx`
  bookkeeping. The failure table gained the `checks`-insensitivity symptom and a row on
  latency spikes after map updates.

## Applied corrections

- `vault/40-features-matching/48-flann.md`: CV-FLANN-005 appended.
- `vault/40-features-matching/references/48-flann.md`, revision 7 → 8: "Static
  database" assumption made precise; worked example A points to the card; three
  contract bullets (index reuse, indices, timing check); "FLANN slower than brute force"
  row extended and a "Latency spikes after map updates" row added; the matchers.cpp and
  features2d.hpp source entries extended; the card listed under related flashcards; the
  "no code executed" sentence qualified; closing provenance line extended.

## Proposals

P-CV-FLANN-01: accepted by the learner on 2026-11-15, completed as CV-FLANN-005.

## Sources

Implementation sources, read at tag 4.13.0 on GitHub raw (docs.opencv.org returns
HTTP 403 from this environment and was not retried; Context7 is unavailable in this
session):

- `modules/features2d/src/matchers.cpp` L423–L475 (`DescriptorCollection::set`),
  L540–L680 (`add`, `clear`, `train`, one-shot and stored-collection matching),
  L1095–L1180 (`FlannBasedMatcher` constructor, `add`, `clear`, `train`), L1385–L1445
  (`clone`, `convertToDMatches`, `knnMatchImpl`);
- `modules/features2d/include/opencv2/features2d.hpp` L1018–L1145 (`add`, `train`,
  matching overloads and their documentation), L1290–L1345 (`FlannBasedMatcher`).

`matchers.cpp` at tag 4.11.0 was also downloaded: it is identical to 4.13.0.

No scientific source carries this card: the behavior belongs to OpenCV's matcher, not to
FLANN's algorithms (Muja and Lowe), which the reference already cites for the cost model.

## Checks and limitations

`python3 -I checks/48-flann.py` passes its 4 checks: the 1.02 s and 1.01 s per call and
the 1% effect of halving the search, 612 s against 13 s for one minute at 10 frames per
second (factor 47), the once-a-minute rebuild with its 1.02 s spike, and the return to
the one-shot cost when appending on every frame. The build and search times are project
assumptions.

Timing check, executed with the OpenCV 4.11.0 Python package installed in this
environment, on one machine, one run each: 100,000 random float32 descriptors of
dimension 128 as the map, 1,000 as the frame, `KDTreeIndexParams(trees=4)`,
`checks=32`. One-shot calls took 0.55–0.57 s; `add` and `train()` 0.64 s; stored-index
calls 0.019–0.032 s; a one-shot call after `train()` still 0.57 s; the first
stored-index call after adding 10 rows 0.575 s, the next 0.019 s; the added batch came
back with `imgIdx` 1; without an explicit `train()`, the first stored-index call took
0.58 s and the second 0.023 s. These runs confirm the code paths and both Python
overloads; they are not a FLANN benchmark, and the card keeps constructed figures. The
script stays in the session scratchpad and is not part of the repository.

`python3 scripts/check_vault.py`: OK (142 Markdown documents, 60 references, 292 cards at
the last run, including concurrent additions by other agents). `python3 scripts/learning_path.py`: OK,
0 errors. Inventory of the card file: 5 cards, no anomaly. `git diff --check` on the
subject's files: clean. Front matter unchanged except `revision`; H1 and existing
per-card headings unchanged.

Agent self-review, without independent scientific validation. Obsidian and AnkiDroid
rendering of the card are not verified. Export status: **to republish with
`paquet-anki`**. Shared files left to the coordinator: the proposal register
(P-CV-FLANN-01), the correction log of `vault/01-Parcours/Suivi-pilote.md` (CV-FLANN
revision 8: "Static database" precision), and the generated catalogue and card counts.
