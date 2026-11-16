# Photogrammetry domain — scope — 2026-11-16

Request: the learner asked for "une partie importante sur la photogrammétrie".
Before this pass the vault covered photogrammetry only through bundle adjustment
(CV-BA) and scattered mentions: no reference treated SfM pipelines,
aerotriangulation, georeferencing, reference systems, dense matching,
orthoimagery or satellite sensor models. Asked to choose, the learner decided:

- **Structure:** a new domain 15, `150-photogrammetrie` (`d15`), with its own
  index, Anki subdeck and learning-path stage, linked to the existing geometry
  references.
- **Contexts:** all four — pipeline core, aerial and drone mapping, satellite,
  close-range and terrestrial.
- **Size:** eight subjects, about forty cards, delivered in two or three pull
  requests.

Mode: creation of new reference notes and cards (not a `revue-cartes` pass;
its card format, verification standard and report conventions are reused).
Starting point: `main` at `d53ea2f`, branch `docs/photogrammetry-domain-20261116`,
in a dedicated worktree because another session uses the main checkout.

## Subjects

| File | ID | Title | Contexts | Tracks | Priority / depth | Prerequisites | Batch |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 151-colinearite-autocalibration | CV-COLINEARITE | Collinearity, orientations and photogrammetric self-calibration | core, close-range | B, E | V1 / in-depth study | CV-ZHANG, CV-BA | 1 |
| 152-sfm-incrementale-globale | CV-SFM | Structure from Motion: incremental and global pipelines | core | B, C | V1 / in-depth study | CV-EPIPOLAIRE, CV-BA, CV-MATCHING | 1 |
| 153-systemes-reference | CV-GEODESIE | Reference systems for photogrammetry: datums, projections and heights | aerial, satellite | B, E | V1 / operational use | CV-SE3 | 1 |
| 154-aerotriangulation-georeferencement | CV-AEROTRIANGULATION | Aerotriangulation and georeferencing: ground control, GNSS/IMU and accuracy | aerial and drone | B, E | V1 / in-depth study | CV-BA, CV-MULTICALIB, CV-SFM, CV-GEODESIE | 1 |
| 155-mvs-correlation-dense | CV-MVS | Multi-view stereo and dense image matching | core, aerial, close-range | B, E | V1 / operational use | CV-STEREO, CV-SFM | 2 |
| 156-mns-orthorectification | CV-ORTHO | Surface models and orthorectification | aerial and drone | B, E | V1 / operational use | CV-MVS, CV-GEODESIE, CV-AEROTRIANGULATION | 2 |
| 157-satellite-pushbroom-rpc | CV-SATELLITE | Satellite photogrammetry: pushbroom geometry and RPC models | satellite | B, E | V1 / operational use | CV-COLINEARITE, CV-AEROTRIANGULATION, CV-IMAGERIES | 2 |
| 158-planification-precision | CV-PLANIFICATION | Photogrammetric acquisition design and expected accuracy | aerial, drone, close-range | B, E | V1 / operational use | CV-AEROTRIANGULATION, CV-MVS | 2 |

All eight join a new learning-path stage, `photogrammetrie`, placed after the
`geometrie` stage. Each subject receives five cards with distinct recall
objectives and at least four card families.

## Delivery criteria

- **Structure.** `d15` is added to `scripts/vault_sections.json`. The validator
  derives the allowed domains from that file instead of a hard-coded
  `d01`–`d14` range, with unit tests. The learning path gains the stage; the
  catalogue is regenerated, never edited by hand.
- **References.** Each note uses the front matter of the existing references
  (`statut: redige`, `provenance: agent`, `revision: 1`) and the section
  structure of the deepened references: problem and data contract, intuition,
  prerequisites and competencies, assumptions and degenerate cases, procedure,
  mathematics with conventions and units, parameters, properties and limits,
  cost and implementation, evaluation and controlled variation, failure modes
  and diagnosis, alternatives and applications, worked examples, sources and
  flashcards. Depth matters more than length; existing references are linked,
  not repeated.
- **Sources.** Every central claim is checked at the exact passage of a primary
  paper, a standard, an official geodetic or agency document, or code at a
  release tag or commit. Open-access versions are preferred; paywalled sources
  are named as such and not cited for unread passages. Memory does not
  establish confirmation. Context7 is unavailable; API claims rest on
  versioned code or documentation.
- **Numbers.** Every number is a constructed example or a cited value.
  Constructed numbers are recomputed by a stdlib script under `checks/`.
- **Cards.** Five per subject, in the card template, with new IDs from `001`,
  `Provenance: agent`, a standalone front that does not reveal the answer,
  three or so gradable criteria, at least 180 lexical words (about 250–450
  targeted, no padding), plausible blocking errors, and tags matching the
  reference's domain and tracks. No two cards in the domain share an
  objective, and none duplicates a card of another domain.
- **Invariants.** No existing card block, ID, Anki identity, expected answer or
  tag changes. Existing references may receive a link to the new domain only
  if their revision is incremented and the change is logged.
- **Records.** One report per subject and an overview in this directory; the
  additions logged in `vault/01-Parcours/Suivi-pilote.md`; current-state
  counts and "fourteen domains" statements updated outside dated evidence.
- **Checks.** Vault, catalogue, learning-path, unit-test, inventory comparison,
  anchor and recomputation checks pass; the full diff is reviewed. Agent
  self-review only: no independent scientific validation, photogrammetric
  processing run, Obsidian or AnkiDroid rendering is claimed.

## Organization

Batch 1 (core pipeline and georeferencing) and batch 2 (dense products,
satellite and acquisition design) are each written by four subagents from a
shared brief, on disjoint files. The coordinator edits the shared files
(sections, learning path, catalogue, counts, progress log, register), reviews
every card and recomputes its numbers before delivery.

## Baseline

Executed on `main` at `d53ea2f` before content edits: 142 vault Markdown
documents, 60 references, 298 cards; catalogue 19 documents, none stale;
learning path OK; 62 unit tests pass.
