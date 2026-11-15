# Review — Data contracts, profiling and video pipelines — 2026-11-15

## Overview

Mode: `ajouter` for the accepted proposal P-CV-PIPELINE-02. One card added,
CV-PIPELINE-006; the five existing cards were not re-audited in this pass (see the
[2026-11-14 report](../2026-11-14-reference-depth/141-contrats-profiling-video.md)).
Self-review: Agent Claude Code (revue-cartes).
Editorial status: redige. Reference revision 8 → 9.

## Added card

| Card | Accuracy | Relevance | Gradability | Consistency | Family |
| --- | --- | --- | --- | --- | --- |
| CV-PIPELINE-006 | Pixel-centre convention of OpenCV's bilinear resize, source index $(d+0.5)s-0.5$: confirmed in resize.cpp L4101 (L4096–L4103). Applied factor computed from the integer sizes when an output size is given: resize.cpp L4216–L4221. Scale $1/3$, content $640\times360$, padding 140, box $(960,450,1248,630)$, forgotten-padding offset 420 px with the top 420 rows empty and coordinates above 660 px pushed below the frame, wrong-order offset 280 px, stretch-inverse values 489.4 and 590.6, index mapping 290 → 451: project derivations, recomputed by the check script | Reasoning: the geometric contract between detector output and source pixels, a silent production error. CV-DETECTEURS-004 uses the same letterbox as context for a small-object diagnosis and states the inverse in its explanation, but no card trains computing the map or recognizing the forgotten-padding signature | 3 expected criteria (scale; padding with its symptom; inverse with the box); 462 lexical words | Notation $r$, $p_x$, $p_y$ and the corner-origin continuous frame of worked example F; the card uses another box than example F so that it is not a copy of the worked example | Reasoning |

The question names the padding that the postprocessing omits, because predicting the
symptom is part of the objective; it does not state the offset, its direction or the
contrast with a scale error.

## Reference findings

Worked example F was correct (recomputed: $r=1/3$, $640\times360$ content, $p_y=140$,
$(100,200,300,400)\mapsto(300,180,900,780)$, 420 px offset). Two imprecisions:

- The forward and inverse maps were written with $r$, whereas the content size is
  rounded. The factor OpenCV actually applies depends on the call: with an output
  size it is the ratio of integer sizes, $\mathrm{round}(rW)/W$ (resize.cpp
  L4216–L4221); with `fx` and `fy` and no output size, the generic path samples with
  $r$ and only converts $rW$ to an integer for the output size (L4209–L4214, passed on
  at L4245). The maps now use the applied factors $s_x,s_y$, equal to $r$ in example F.
- "Implementations that split it differently disagree by one pixel" did not say which
  pixel. The disagreement is one input pixel, about $1/r$ source pixels; the note now
  gives a 277-row example ($1920\times1088$ source).

Absent and added for the card: the order of the inverse (padding removed before the
division; the reverse order leaves $p_y(1/r-1)$), and the signatures that separate a
forgotten padding term (constant offset on one axis, sizes intact, an empty band at
the top) from a wrong scale (an error that grows with position).

## Applied corrections

- `vault/140-ingenierie-systemes/141-contrats-profiling-video.md`: CV-PIPELINE-006
  appended.
- `vault/140-ingenierie-systemes/references/141-contrats-profiling-video.md`,
  revision 8 → 9: letterbox paragraph written with the applied factors and the order of
  the inverse; worked example F extended with the card's box, the symptom and the
  odd-split example; the OpenCV `resize` implementation contract and source entry
  extended (L4209–L4221, L4245); the card listed under related flashcards; closing
  provenance line extended.

For the correction log (to be entered by the coordinator): CV-PIPELINE revision 9;
letterbox maps written with $r$ although the applied factor is the rounded size ratio
when an output size is given (OpenCV 4.13.0 resize.cpp L4216–L4221) → written with
the applied factors; "disagree by one pixel" → one input pixel, about $1/r$ source
pixels. No existing card repeated either claim (case-insensitive search for
"letterbox", "disagree by one" and "split it differently" over `vault/`;
CV-DETECTEURS-004 and the CV-DETECTEURS reference use the exact case
$1920\times1080$, where the factors equal $r$).

## Proposals

P-CV-PIPELINE-02: accepted by the learner on 2026-11-15, completed as CV-PIPELINE-006.

## Sources

Implementation sources, read at tag 4.13.0 on GitHub raw (docs.opencv.org returns
HTTP 403 from this environment and was not retried; Context7 is unavailable in this
session):

- `modules/imgproc/src/resize.cpp` L3826–L3840 (`hal::resize` entry), L3965
  (`scale_x = 1/inv_scale_x`), L4060–L4140 (generic table setup, bilinear source index
  at L4101), L4195–L4260 (`cv::resize`: output size or `fx`, `fy`, call at L4245).

No scientific source carries this card: the letterbox maps are a project derivation,
and the convention belongs to the implementation.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 -I docs/revues/2026-11-15-accepted-proposals/checks/141-contrats-profiling-video.py` | 11 checks passed |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 292 cards (shared tree, other agents' cards included) |
| `python3 scripts/learning_path.py` | OK: 60 references, 292 cards, 0 errors |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/140-ingenierie-systemes/141-contrats-profiling-video.md` | 6 cards, no anomaly; CV-PIPELINE-006 462 lexical words |
| `git diff --check -- vault/140-ingenierie-systemes/` | No whitespace error |

The check script uses exact fractions and models coordinates only; no image was
resized and no OpenCV call was executed, so the index mapping is checked against the
formula at L4101, not against pixel output. HAL or OpenCL backends receive the same
factors (L4227, L3840) but their sampling was not read. Agent self-review only; the
Obsidian rendering and the AnkiDroid rendering of the card are not verified. Export
status: to republish with `paquet-anki`. The proposal register, the progress log and
the generated catalogue are left to the coordinator.
