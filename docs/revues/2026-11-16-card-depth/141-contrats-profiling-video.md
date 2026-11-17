# Review — Data contracts, profiling and video pipelines — 2026-11-16

## Overview

1 card audited and deepened in `approfondir` mode (CV-PIPELINE-001), and one figure
added to CV-PIPELINE-006. Highest severity per card before correction: 0 blocking,
0 important, 1 minor (CV-PIPELINE-001: answer among the shortest of the vault, no
worked number), 0 with no defect identified.
Self-review: Agent Claude Code (revue-cartes).
Editorial status: redige. Reference revision 9 → 10.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-PIPELINE-001 | Throughput guarantees neither age nor deadline: confirmed against the age definition $\Delta(t)=t-u(t)$ (Yates and Kaul §I) and the reference's constant-latency sawtooth. The existing paragraphs are correct. Missing: a worked number and the mechanism that keeps outputs old at full throughput | Comparison: separates throughput from latency and age before accepting a "real-time" claim | 1 expected criterion, unchanged; 283 → 585 lexical words (counter includes the image path and formula tokens) | Aligned with worked example A and "Queues and freshness" | Minor | Deepened: figure, sawtooth reading, warm-up backlog at $\lambda=\mu$, Little's law cross-check, bounded queue; one blocking error added; Source line extended |
| CV-PIPELINE-006 | Not re-audited (written and checked on 2026-11-15) | — | 522 lexical words | Figure drawn to scale from worked example F | — | Letterbox figure added with a two-sentence reading |

## Added figures

Both SVG files live in `vault/99-Ressources/`. They are self-contained: no script,
external font or embedded raster. Each has a light background, so it stays readable
in dark mode, plus a `<title>` and a `<desc>`. Both were rendered with
`rsvg-convert` at 380 px (phone width) and 1080 px, and inspected visually. The
inspection fixed one label crossed by an arrow and the spacing lost after
subscripts.

- `cv-pipeline-throughput-age.svg`: equal output spacing for two pipelines with
  latencies of 0.5 and 2.5 periods, and the age sawtooth from $L$ to $L+1/X$
  against a deadline. It is schematic: the periods are not to scale with any
  example.
- `cv-pipeline-letterbox.svg`: drawn to scale for worked example F. The input is
  drawn at 0.375 px per pixel and the source at 0.25 px per pixel. The model box
  $(320,290,416,350)$ maps back to $(960,450,1248,630)$, and to $y\in[870,1050]$
  without $p_y$. The check script recomputes the figure's coordinates.

## Applied corrections

- `vault/140-ingenierie-systemes/141-contrats-profiling-video.md`, card
  CV-PIPELINE-001:
  - a "Reading the diagram" paragraph with the figure, then a constructed
    warm-up backlog example;
  - the blocking error "Assuming that a backlog drains by itself once the engine
    reaches the camera's frame rate";
  - the Source line now gives the passages and labels the constructions.
- Same file, card CV-PIPELINE-006: letterbox figure and its reading.
- `vault/140-ingenierie-systemes/references/141-contrats-profiling-video.md`,
  revision 9 → 10: both figures with captions, and the $\lambda=\mu$ backlog case
  in "Queues and freshness"; closing provenance line extended.

Expected answers, questions, objectives, families, tags and IDs are unchanged.

## Sources

- Yates and Kaul, arXiv 1608.08622v2, §I. Read as PDF text: the definition
  $\Delta(t)=t-u(t)$ (lines 69–70 of the extraction), FCFS queueing new updates
  behind outdated ones, and the lossy LCFS discipline (lines 95–103).
- Little (1961) is cited for Little's law as in the reference. It is paywalled and
  was not re-read.
- The GStreamer `queue` page was fetched, but its text could not be extracted
  (rendered client-side). The `leaky=downstream` behaviour rests on the 2026-11-14
  reading recorded in the reference; the card names no GStreamer property.

Context7 is unavailable in this session.

## Checks and limitations

`python3 -I checks/141-contrats-profiling-video.py`: 8 checks pass. They cover the
sawtooth mean, the fluid backlog at $\lambda=\mu$, a FIFO simulation of 10 s, Little's
law, the bounded wait, and the letterbox numbers and figure coordinates. The
warm-up scenario is a constructed example, not a measurement. SVG rendering in
AnkiDroid's WebView and in Obsidian is not verified, only with `rsvg-convert`.
