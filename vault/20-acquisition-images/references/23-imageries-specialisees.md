---
id: CV-IMAGERIES
type: comparaison
domaine: d02
poles: [E]
priorite: V2
profondeur: reperage
statut: redige
provenance: agent
revision: 5
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d02]
---
# Line-scan imaging, remote sensing and medical volumes

## Problem, data and assumptions

Understand specialized procurement contracts before applying a 2D network. Input comparison: lines synchronized to motion, multispectral/SAR bands, volumes with physical spacing/orientation. The reference note introduces these families; it does not constitute a mastery of each modality.

## Prerequisites and competencies

**Required prerequisites**: [Conventions of vault](../../01-Parcours/Pre-requis.md). **Target competencies**: Explain the mechanism, compare under constraints, interpret a measurement and diagnose a failure. The level displayed is for this reference note; not all variants mentioned are detailed.

## Intuition and procedure

Line-scan reconstructs an image as it moves; a telecentric lens aims to limit certain magnification changes on its designed range. A georeferenced image carries a transformation to terrestrial coordinates. A medical volume has axes, spacing, and orientation; the order of the chart is not the coordinate frame patient.

## Mathematics, conventions and units

A voxel $(s_x,s_y,s_z)$ spacing in mm transforms a displacement of indices into physical length. Anisotropic pixels or voxels make distances in indices misleading. A geospatial or volume affine must retain axis, unity, and convention; a latitude/longitude coordinate is not a Euclidean distance in meters.

## Parameters and properties

Specify line-scan/encoder calibration, bands and normalization, ground resolution, no-data, axes and spacing. DICOM/NifTI are formats with metadata, not guarantees of consistent annotations or clinical utility.

## Cost and implementation

Large mosaics and volumes require tile with overlapping and restitution of coordinates. No real patient or geospatial files are loaded here; no clinical results are claimed.

## Evaluation and controlled variation

Proposed variation: resample an anisotropic volume or change the conveyor speed. Predict errors if transformation is not propagated; check a known length and tile fittings.

## Failure modes and diagnosis

Incoherent contour distances: check spacing and orientation. Artifacts with fittings: check padding, coating and fusion. Seasonal degradation: distinguish between acquisition and distribution of labels.

## Alternatives and applications

Choose a representation according to the task and units; good segmentation does not prove accurate georeferencing or metrology accuracy.

## Guided reasoning and proposed checks

These constructed cases develop physical geometry, line-scan and generalization unit. They are used to explain or test reasoning; their image, video or material results are not advertised as measured. The method properties remain attached to the sources below.

### Case linked to CV-IMAGERIES-001

**Question of work**: Why should HD95 not be calculated blindly in voxel-index units for anisotropic MRI?

**Reference Response**: The axes can have different physical spacings; convert the distances in the announced coordinate frame and unit.

**Analytical example**: with a spacing of 0,5 mm, 0,5 mm and 3 mm, a displacement of an index is 0,5 mm on the first two axes, but 3 mm on the third. For orthogonal axes, a difference of indices $\Delta i$ is converted into distance by $\sqrt{\sum_k(s_k\Delta i_k)^2}$, where $s_k$ is the spacing of the axis. The orientation and position conventions then determine the common coordinate frame.

**Consequences for the evaluation**: A surface distance calculation must use a consistent physical geometry for both masks. A forgotten axis permutation or resampling can change the result without changing segmentation. Check a known distance and announce the unit in the report. The percentile chosen and the treatment of empty masks belong to the protocol; no isolated value constitutes here a clinical conclusion.

### Case linked to CV-IMAGERIES-003

**Question of work**: Why can randomly splitting neighboring tiles between training and test overestimate generalization in remote sensing?

**Reference Response**: They share scene, texture and context; the test can look like training beyond the intended future scenario.

**Why splits can fool**: Separate tiles can contain the same buildings, the same background or part of a common image. Even without exact recovery, a site shares acquisition, season and materials. The model can therefore succeed by recognizing an environment already encountered, while the product must work in another region.

**Proposed Protocol**: first define the generalization sought: new positions of the same site, new date or new territory. Group the data according to this unit before the tile, check the geographical footprints and reserve a test that represents this use. Compare results by site and season rather than just the overall average. A more difficult geographic split is not automatically more representative: it must correspond to the announced need. The risk described is methodological reasoning, not a measure of leakage established on all remote sensing sets.

**Documentary reference for this pass**: [DICOM, Image Plane Module](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html), §C.7.6.2.1.1, position, orientation and pixel spacing. The other developments are in the [flashcards](../23-imageries-specialisees.md).

## Additional technical explanations — 2026-10-30

These explanations complement the mechanism associated with each question. Calculations are cases constructed under assumptions; protocols remain proposed until a test is recorded.

### CV-IMAGERIES-001

**Situation**: Why should HD95 not be calculated blindly in voxel-index units for anisotropic MRI?

**Complete Geometry**: A physical position is written $p=o+A i$, with index $i$, physical origin $o$ and columns of $A$ describing directions and spacings. The distance between indices follows $\|A\Delta i\|_2$; the formula with only spacings assumes orthogonal axes. DICOM distinguishes the nominal cutting thickness from the distance between centers: systematically using the thickness as spacing can be wrong. For a stack, check the positions and orientations of the cuts, regularity and order before making a single affine. The calculation of HD95 then requires a precise definition of the surfaces, directed distances and percentiles, with explicit policy if one of the surfaces is empty.

### CV-IMAGERIES-002

**Situation**: A part appears stretched in a line-scan image when conveyor speed changes. What should be tested?

**Sizing Built**: for a desired longitudinal resolution of 0,1 mm/line and a speed of 500 mm/s, it is necessary $f_l=v/s=5000$ lines/s in the slip-free model. A long piece of 20 mm then occupies about 200 lines. If an encoder imposes a line per displacement of 0,1 mm, the frequency must follow the speed variations within the range allowed by the sensor. A maximum speed exceeded or a lost impulse breaks this contract. It is also necessary to limit the displacement during the exposure of a line: correct spatial triggering and low blur are two distinct constraints. The above calculations are analytical sizing, without conveyor testing.

### CV-IMAGERIES-003

**Situation**: Why can randomly splitting neighboring tiles between training and test overestimate generalization in remote sensing?

**Define the unit of the test**: Ten thousand tiles from ten scenes do not represent ten thousand independent contexts. Build a table linking each tile to the scene, site, date, and footprint; assign groups to scores before any increase or extraction of patches. The normalization statistics learned and the choice of thresholds must follow the same separation. A geographical margin can help remove recoveries, without guaranteeing the independence of all acquisition factors. To compare two methods, also aggregate their deviations by representative group of the deployment: a result dominated by a very cut site can tell a story other than the average sites. This is a proposed protocol, not an audit of SpaceNet.

**Passages consulted for these developments**: [DICOM PS3.3 2026d](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html), C.7.6.2, position, orientation and spacings; [Basler, GigE Line Scan](https://docs.baslerweb.com/line-scan-gige-use-cases), Case 1 b, trigger encoder; [SpaceNet7](https://www.spacenet.ai/sn7-challenge/), The Problem and The Data; geographical separation deduced by the project.

## Sources and flashcards

- [Basler, GigE Line Scan Use Cases, Use Case 1 b (v136, 2026-10-01)](https://docs.baslerweb.com/line-scan-gige-use-cases).
- [Edmund Optics, The Advantages of Telecentricity](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/advantages-of-telecentricity/).

The leak between neighboring tiles is a risk deduced by the project, to be evaluated according to the generalization scenario; the description SpaceNet contextualizes the geographical series without alone proving this bias for any split.

- [NIfTI, standard and transformations](https://nifti.nimh.nih.gov/nifti-1/).
- [DICOM, standard courant](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html).
- [SpaceNet7, multi-temporal data](https://www.spacenet.ai/sn7-challenge/).
- [Related flashcards](../23-imageries-specialisees.md).

Editor: agent, 2026-10-18. Documentary confrontation of the central statements with the quoted passages; no image/video experience, material performance or independent validation announced. The cases constructed are reasonings of the project.
