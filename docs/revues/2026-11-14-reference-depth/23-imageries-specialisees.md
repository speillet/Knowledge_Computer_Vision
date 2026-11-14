# Review — Line-scan imaging, remote sensing and medical volumes — 2026-11-14

## Overview

3 cards audited in `approfondir` mode; the canonical reference body was deepened
from revision 7 to revision 8. Highest severity per card before correction:
0 blocking, 0 important, 3 minor, 0 with no defect identified.
Self-review: Agent Claude Code (`revue-cartes`).
Editorial status: redige.

The reference is a comparison note at orientation depth (`profondeur: reperage`,
priority V2, career track E). It compares the geometric contracts of three
families; exposure and sampling stay in
[CV-ACQUISITION](../../../vault/20-acquisition-images/references/21-exposition-bruit-echantillonnage.md)
and line timing in
[CV-CAPTEURS](../../../vault/20-acquisition-images/references/22-capteurs-horodatage.md).

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-IMAGERIES-001 | Physical distance $\|A\Delta i\|$, (0.5, 0.5, 3) mm example (3.04 mm): confirmed and recomputed; DICOM distinction between nominal Slice Thickness and centre-to-centre Spacing Between Slices: confirmed (PS3.3 2026d, Table C.7-10). "Announced coordinate frame" in the expected answer; "nominal cutting thickness", "cuts" (slices), French decimal commas | Practice: propagate physical units through a volume metric | 1 criterion; 380 → 384 lexical words | Consistent with reference worked example A and with CV-METRIQUES-APPLIQUEES | Minor | Meaning-restoring fix of the expected answer; language fixes; Source adds the MONAI 1.6.1 spacing default |
| CV-IMAGERIES-002 | $s=v/f_l$, 5000 lines/s, 200 and 300 lines, 20 mm misestimate: recomputed; encoder triggering for variable speed: confirmed (Basler Use Case 1b). Blocking error "Retract without checking…" mistranslated *Réentraîner* (retrain) and was unreadable; "Sizing Built", "a lost impulse" | Diagnosis: separate a geometric acquisition defect from a model error | 1 criterion; 376 → 370 lexical words | Consistent with reference worked example B | Minor | Language fixes, including the blocking error; Source updated to Basler v138, Use Cases 1a–1b |
| CV-IMAGERIES-003 | Neighbouring tiles share context and inflate scores: supported by Roberts et al. 2017 (random cross-validation underestimates predictive error for structured data; abstract, Box 1); the remote-sensing scenario remains a project deduction. "Check recoveries" (French *recouvrements* = overlaps), "assign groups to scores before any increase" (folds, augmentation), "a very cut site" (heavily tiled) obscured the protocol | Evaluation: choose the split unit from the deployment question | 1 criterion; 366 → 364 lexical words | Consistent with CV-FIABILITE | Minor | Language fixes; Source adds Roberts et al. |

Expected-answer change (meaning-restoring language fix): CV-IMAGERIES-001 "The axes
can have different physical spacings; convert the distances in the announced
coordinate frame and unit." → "The axes can have different physical spacings;
convert distances into physical units in the stated coordinate frame."

Defective protected fields (not edited; objective lines are invariants):

- CV-IMAGERIES-002 objective "check is a line-scan acquisition." Proposed: "Check
  the geometry of a line-scan acquisition."
- CV-IMAGERIES-003 objective "Avoid a geographical flight." (*fuite* = leakage).
  Proposed: "Avoid geographic leakage between training and test."

No defective question was found.

## Reference findings

Claims of revision 7 checked against their passages:

- "A voxel spacing transforms a displacement of indices into physical length;
  anisotropic voxels make index distances misleading": confirmed (DICOM eq.
  C.7.6.2.1-1; NIfTI methods 2–3).
- "A geospatial or volume affine must retain axis, unit and convention; a
  latitude/longitude coordinate is not a Euclidean distance in meters": confirmed as
  geometry; now illustrated with the corner convention of GDAL and a degree-to-metre
  example.
- "A telecentric lens aims to limit certain magnification changes on its designed
  range": the cited Edmund Optics page returned HTTP 403 (not verifiable); the note
  now cites Watanabe and Nayar for magnification invariance to defocus and marks the
  object-side range claim as not re-verified.
- "DICOM/NIfTI are formats with metadata, not guarantees of consistent annotations or
  clinical utility": kept as a project statement.
- No scientific error found. The body was shallow (329 words) and contained
  mistranslations: "specialized procurement contracts" (acquisition contracts),
  "coating" (overlap), "fittings" (tile seams), "the order of the chart is not the
  coordinate frame patient", "Question of work", "Reference Response", "Proposed
  Protocol", "Complete Geometry", "Sizing Built".

New claims verified for revision 8 (main ones):

- DICOM PS3.3 2026d, C.7.6.2: Pixel Spacing order (row spacing, then column
  spacing); Image Position = centre of the first voxel; direction cosines
  orthonormal; equation C.7.6.2.1-1 with zero-based integer indices and the
  edge-based sub-pixel form C.7.6.2.1-2; LPS axes; nominal Slice Thickness versus
  centre-to-centre Spacing Between Slices; Slice Location relative to an
  unspecified reference point.
- NIfTI-1 `nifti1.h` v3.0.1: voxel centres, RAS+ axes, storage order, ANALYZE 7.5
  left-handed convention, methods 1–3 and their intended use.
- GDAL 3.13.3: geotransform formula, corner origin, centre at (0.5, 0.5), north-up
  coefficients, GCPs as the other georeferencing method.
- SentiWiki: 13 bands at 10, 20 and 60 m; 290 km swath; 5-day constellation revisit.
- Roberts et al. 2017: underestimation of error by random cross-validation; blocks
  substantially larger than the residual autocorrelation range in their simulation
  (Box 1); minimum blocking distance and anisotropic blocks (p. 919); risk of induced
  extrapolation (abstract).
- Reinke et al.: HD95 designed for spatial outliers (Fig. 5c); empty reference or
  prediction gives undefined values (Extended Data Fig. 2b, SN 2.20); grid size
  changes metric values (SN 2.36).
- MONAI 1.6.1 `compute_hausdorff_distance`: unity spacing by default, spacing only for
  the Euclidean metric, `percentile=None` returns the maximum.
- Basler line-scan Use Cases 1a (fixed line rate for predictable speed) and 1b
  (shaft-encoder line trigger when "load changes and vibrations cause the transport
  speed to vary").

Convention disagreements recorded in the note (FR-036): GDAL counts pixel/line from
the pixel corner while DICOM and NIfTI integer indices address voxel centres
(DICOM's sub-pixel form uses the edge); DICOM patient axes are LPS+ while NIfTI uses
RAS+.

## Reference depth

Body word counts (front matter excluded, H1 included, up to
"## Guided reasoning and proposed checks"; whitespace tokens): 329 → 3,313. About
700 tokens are tables, the pseudocode and the Mermaid diagram. The length comes from
comparing three geometric contracts side by side at orientation depth; metric
details are linked to CV-METRIQUES-APPLIQUEES.

| Contract section | Before | After | What was added |
| --- | --- | --- | --- |
| Problem | Shallow | Developed | Common affine model $p=o+Ai$; comparison table of arrays, mappings, origin conventions, frames and failures; per-family contracts from Basler, SentiWiki, GDAL, DICOM and NIfTI; role of metadata through the pipeline |
| Intuition | Shallow | Developed | Array as key, metadata as meaning; one illustration per family; constructed HD95 ranking inversion; Mermaid diagram of metadata propagation |
| Prerequisites | Shallow (one link) | Developed | Links to CV-SE3, CV-ACQUISITION, CV-CAPTEURS, CV-FIABILITE, CV-SEGMENTATION, CV-METRIQUES-APPLIQUEES |
| Assumptions | Absent (merged) | Developed | Speed or encoder assumptions; affine versus GCP; orthonormal cosines and regular slices; independence for evaluation; observability and degenerate cases |
| Procedure | Shallow | Developed | Eight-step pseudocode from metadata reading to an end-to-end geometric check |
| Mathematics | Shallow | Developed | Line-scan sampling and exposure; DICOM equations and Pixel Spacing order; NIfTI methods and LPS/RAS; GDAL corner convention; degrees versus metres; Hausdorff and HD95; worked examples A (conventions) and B (line-scan) |
| Parameters | Shallow (list) | Developed | Eight-row table and a tuning order including block size |
| Properties | Absent | Developed | Affine validity, resampling, formats versus truth, telecentric optics, blocked-split extrapolation |
| Cost and implementation | Shallow | Developed | Volume memory and resampling cost; GDAL, NIfTI, DICOM, MONAI and Basler contracts; execution status |
| Evaluation | Shallow | Developed | Geometric checks first; proposed random versus city split with a confound; measurement limits |
| Failure modes and diagnosis | Shallow | Developed | Nine-row Symptom / Causes / Discriminating check / Remedy table |
| Alternatives and sources | Shallow | Developed | Conditional choices for line-scan triggering, grids, CRS and holdouts; industrial uses labelled as project reasoning; sources split into scientific sources and implementation sources and standards |

Constructed examples are recomputed by
[`checks/23-imageries-specialisees.py`](checks/23-imageries-specialisees.py)
(11 checks): 3.04 mm, 6 mm and 1 mm index steps; DICOM Pixel Spacing order (8, 10, 0)
versus (5, 16, 0) and 6.7 mm; LPS/RAS sign change; GDAL centre (500005, 4199995) and
7.07 m shift; degree lengths 111.2 and 78.6 km and an 11.1 m × 7.9 m cell; line-scan
0.1 and 0.15 mm/line, 200/300 lines, 20 mm estimate, 7,500 lines/s, 200 µs and
0.05 mm; 315 MB and 1.9 GB volumes.

## Applied corrections

- [Reference](../../../vault/20-acquisition-images/references/23-imageries-specialisees.md),
  revision 7 → 8: body rewritten and deepened as above; appendices given the same
  language fixes as the cards ("Question of work" → "Working question", "Reference
  Response" → "Reference answer", "Proposed Protocol" → "Proposed protocol",
  "Complete Geometry" → "Complete geometry", "Sizing Built" → "Constructed sizing",
  "Use Case 1 b" → "Use Case 1b", decimal commas); sources split into scientific and
  implementation sources; closing provenance line replaced. Front matter unchanged
  except `revision`; H1 and per-card headings unchanged.
- [Cards](../../../vault/20-acquisition-images/23-imageries-specialisees.md): one
  expected answer fixed as quoted above. Other language fixes: "Keep orientation,
  resampling and protocol of empty masks" → "Keep track of orientation, resampling
  and the empty-mask protocol"; "A difference in a voxel does not have the same length
  along the axis" → "A one-voxel difference does not have the same length along every
  axis"; "nominal cutting thickness from the distance between centers" → "nominal
  slice thickness from the centre-to-centre spacing"; "Retract without checking" →
  "Retraining without checking"; "A maximum speed exceeded or a lost impulse" →
  "Exceeding the maximum line rate or losing a pulse"; "does not validate the entire
  chain metrology alone" → "does not by itself validate the whole metrology chain";
  "check recoveries" → "check footprint overlaps"; "assign groups to scores before any
  increase or extraction of patches" → "assign groups to folds before any
  augmentation or patch extraction"; "a very cut site" → "one heavily tiled site";
  "Assimilate file separation and statistical independence" → "Equating separate
  files with statistical independence"; French decimal commas. Source lines given
  exact passages and versions. Questions, IDs, objectives, families, tags and target
  deck unchanged.

No other vault file repeats a claim corrected here (`rg` over `vault/` for `HD95`,
`Pixel Spacing`, `line-scan`, `recoveries`); CV-METRIQUES-APPLIQUEES states HD95 in
physical units consistently.

## Proposals

To register as `pending` in the [proposal register](../propositions.md) (not edited
by this subject run).

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- | --- | --- |
| P-CV-IMAGERIES-01 | CV-IMAGERIES | Map a DICOM pixel $(i,j)$ to patient coordinates from Image Position, Image Orientation and Pixel Spacing, then name the two convention traps (Pixel Spacing order; LPS+ versus NIfTI RAS+) | No card trains the index-to-patient mapping that every volume metric and overlay depends on | Practice; Mathematics, worked example A | 1 card, 3 criteria | [DICOM PS3.3 C.7.6.2.1.1](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html); [nifti1.h v3.0.1](https://github.com/NIFTI-Imaging/nifti_clib/blob/v3.0.1/niftilib/nifti1.h#L995-L1120) |

## Sources

Scientific sources, opened at the passages listed:

- Roberts et al. 2017, read in the copy at
  [biometrie.uni-freiburg.de](https://www.biometrie.uni-freiburg.de/mitarbeiter/dormann/roberts-et-al-2017-ecography.pdf)
  (published version, DOI 10.1111/ecog.02881; the Wiley page returned HTTP 403):
  abstract, Box 1, p. 919.
- Reinke et al., [arXiv HTML 2302.01790](https://arxiv.org/html/2302.01790): Fig. 5
  caption, Extended Data Fig. 2 caption, SN 2.20 and SN 2.36 captions.
- Watanabe and Nayar 1996, [abstract page](https://mlanthology.org/eccv/1996/watanabe1996eccv-telecentric).

Implementation sources and standards:

- [DICOM PS3.3 2026d, C.7.6.2](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html): Table C.7-10, C.7.6.2.1.1, C.7.6.2.1.2.
- [nifti1.h, nifti_clib v3.0.1](https://github.com/NIFTI-Imaging/nifti_clib/blob/v3.0.1/niftilib/nifti1.h): L995–L1120.
- [GDAL v3.13.3 `doc/source/user/raster_data_model.rst`](https://github.com/OSGeo/gdal/blob/v3.13.3/doc/source/user/raster_data_model.rst): L36–L55.
- [SentiWiki, S2 mission](https://sentiwiki.copernicus.eu/web/s2-mission): spatial and spectral resolution, swath, revisit.
- [MONAI 1.6.1 `monai/metrics/hausdorff_distance.py`](https://github.com/Project-MONAI/MONAI/blob/1.6.1/monai/metrics/hausdorff_distance.py): L150–L230.
- [Basler, GigE Line Scan Use Cases](https://docs.baslerweb.com/line-scan-gige-use-cases): version 138, Use Cases 1a and 1b (first 100,000 characters of the page).

Failed accesses and limits:

- Edmund Optics, The Advantages of Telecentricity: HTTP 403; not used for any claim.
- Watanabe and Nayar, IEEE PAMI 1997 PDF: HTTP 404 at the Columbia URL; only the
  ECCV 1996 abstract was read.
- Roberts et al. on the Wiley site: HTTP 403; the published version was read from the
  Freiburg copy.
- NIfTI documentation site: not retried (HTTP 403 on 2026-11-08); the header file at a
  tagged release replaced it.
- SpaceNet 7 page: retained from earlier passes, not re-read in this pass.
- Context7 was not available in this session.

## Checks and limitations

| Command | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 Markdown documents, 60 references, 282 cards |
| `python3 scripts/learning_path.py` | OK: 60 references, 282 cards, 0 errors |
| `python3 docs/revues/2026-11-14-reference-depth/checks/23-imageries-specialisees.py` | 11 checks passed |
| `git diff --check -- vault/20-acquisition-images/` | No whitespace error |
| `python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault/20-acquisition-images/23-imageries-specialisees.md` | 3 cards, 384, 370 and 364 words, no anomaly |
| Protected-field comparison with the pre-edit copy | No protected-field error: card headings, `Objective`, `START`, `CV-Pilote`, `ID`, `Question`, `Tags`, `END`, `TARGET DECK` unchanged; reference front matter identical except `revision: 7` → `8`; H1 and per-card headings unchanged |
| Local links and anchors under `vault/20-acquisition-images` | 0 errors |

No DICOM, NIfTI, GDAL, MONAI or line-scan code was executed; the proposed baseline
and variation are protocols, not results. The Mermaid diagram and tables were not
rendered in Obsidian, and AnkiDroid rendering of the corrected cards is unverified.
This is agent self-review, without independent scientific validation, clinical
validation or measurement of learner proficiency. Export status: **to republish with
`paquet-anki`**.

Shared files not edited by this subject run and needing an entry from the
coordinator: the correction log of `vault/01-Parcours/Suivi-pilote.md` (2026-11-14,
CV-IMAGERIES revision 8, CV-IMAGERIES-001 to -003, corrections listed above, Agent
Claude Code self-review, to republish with `paquet-anki`) and the proposal register
(P-CV-IMAGERIES-01).
