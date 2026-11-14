# Flashcards — Line-scan imaging, remote sensing and medical volumes

reference note: [[20-acquisition-images/references/23-imageries-specialisees|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::20-acquisition-images

## CV-IMAGERIES-001

Objective: propagate units of a volume. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-IMAGERIES-001
Question: Why should HD95 not be calculated blindly in voxel-index units for anisotropic MRI?
Reponse: **Expected answer**: The axes can have different physical spacings; convert distances into physical units in the stated coordinate frame.

**Further explanation**: Keep track of orientation, resampling and the empty-mask protocol. A one-voxel difference does not have the same length along every axis.

**Analytical example**: with a spacing of 0.5 mm, 0.5 mm and 3 mm, a displacement of one index is 0.5 mm along the first two axes, but 3 mm along the third. For orthogonal axes, an index difference $\Delta i$ is converted into a distance by $\sqrt{\sum_k(s_k\Delta i_k)^2}$, where $s_k$ is the spacing of axis $k$. The orientation and position conventions then determine the common coordinate frame.

**Consequences for the evaluation**: A surface distance calculation must use a consistent physical geometry for both masks. A forgotten axis permutation or resampling can change the result without changing the segmentation. Check a known distance and state the unit in the report. The chosen percentile and the treatment of empty masks belong to the protocol; no isolated value here is a clinical conclusion.

**Complete geometry**: A physical position is written $p=o+A i$, with index $i$, physical origin $o$ and columns of $A$ describing directions and spacings. The distance between indices follows $\|A\Delta i\|_2$; the formula with spacings only assumes orthogonal axes. DICOM distinguishes the nominal slice thickness from the centre-to-centre spacing: systematically using the thickness as spacing can be wrong. For a stack, check the positions and orientations of the slices, their regularity and order before building a single affine. Computing HD95 then requires a precise definition of the surfaces, directed distances and percentiles, with an explicit policy if one of the surfaces is empty.

**A voxel step is not a fixed distance**: Constructed case: spacing is $(0.5,0.5,3)$ mm. One voxel along the third axis is six times farther than one voxel along the first; a displacement $(1,0,1)$ has physical length $\sqrt{0.5^2+3^2}\approx3.04$ mm. Applying HD95 to index coordinates would distort this geometry. Surface extraction and resampling can also change the sampled surface, so record both physical coordinates and the exact distance/percentile convention.

**Blocking errors**: Comparing values in voxels and in millimeters as if they were identical.
Source: [[20-acquisition-images/references/23-imageries-specialisees|Full reference]] ; [DICOM PS3.3 2026d, Table C.7-10 and C.7.6.2.1.1, position, orientation, Pixel Spacing and Spacing Between Slices](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html) ; [MONAI 1.6.1, `compute_hausdorff_distance`, spacing defaults to unity](https://github.com/Project-MONAI/MONAI/blob/1.6.1/monai/metrics/hausdorff_distance.py#L150-L183). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d02 famille::pratique cv_id::CV-IMAGERIES-001 provenance::agent pole::E
END

## CV-IMAGERIES-002

Objective: Check a line-scan acquisition. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-IMAGERIES-002
Question: A part appears stretched in a line-scan image when conveyor speed changes. What should be tested?
Reponse: **Expected answer**: The synchronization between lines and displacement, the encoder and the scale reconstructed in the direction of movement.

**Further explanation**: Test a known dimension at several speeds; distinguish this defect from optical magnification and detection.

**Mechanism and units**: a line-scan camera stacks lines acquired during the motion. If the speed is $v$ in mm/s and the line frequency $f_l$ in line/s, the ideal advance per line is $v/f_l$ in mm/line. The scale in this direction therefore depends on the movement, while the other axis is mainly related to the optics and the sensor.

**Constructed example**: doubling the speed at constant line frequency doubles the advance between two lines; the number of lines representing a given length decreases. The aspect displayed also depends on the scale assigned to the reconstructed image. Examine trigger, encoder, line loss, and metadata before interpreting a length measurement. A known calibration target observed at multiple speeds helps isolate this fault from a segmentation error, but does not by itself validate the whole metrology chain.

**Constructed sizing**: for a desired longitudinal resolution $s=0.1$ mm/line and a speed of 500 mm/s, the slip-free model requires $f_l=v/s=5000$ lines/s. A 20 mm long part then occupies about 200 lines. If an encoder triggers one line per 0.1 mm of displacement, the line rate must follow speed variations within the range the sensor allows. Exceeding the maximum line rate or losing a pulse breaks this contract. The displacement during the exposure of one line must also be limited: correct spatial triggering and low blur are two distinct constraints. These calculations are analytical sizing, without conveyor testing.

**Speed changes alter geometry at fixed line rate**: At a fixed 5000 lines/s, increasing speed from 500 to 750 mm/s changes longitudinal sampling from 0.10 to 0.15 mm/line. A 30 mm part then occupies 200 rather than 300 lines. Reusing the original pixel-to-millimeter calibration produces a 20 mm estimate. Encoder triggering can preserve displacement per line within its supported range; dropped pulses or conveyor slip still require an independent geometric check.

**Blocking errors**: Retraining without checking the spatial contract of the image.
Source: [[20-acquisition-images/references/23-imageries-specialisees|Full reference]] ; [Basler, GigE Line Scan Use Cases, Use Cases 1a and 1b (v138, 2026-11-12)](https://docs.baslerweb.com/line-scan-gige-use-cases). Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d02 famille::diagnostic cv_id::CV-IMAGERIES-002 provenance::agent pole::E
END

## CV-IMAGERIES-003

Objective: Avoid geographic leakage. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-IMAGERIES-003
Question: Why can randomly splitting neighboring tiles between training and test overestimate generalization in remote sensing?
Reponse: **Expected answer**: They share scene, texture and context; the test can look like training beyond the intended future scenario.

**Further explanation**: Separate regions, dates or sites according to the intended use, check footprint overlaps and keep an independent evaluation.

**Why splits can fool**: Separate tiles can contain the same buildings, the same background or part of a common image. Even without exact overlap, a site shares acquisition, season and materials. The model can therefore succeed by recognizing an environment already encountered, while the product must work in another region.

**Proposed protocol**: first define the generalization sought: new positions on the same site, a new date or a new territory. Group the data by this unit before tiling, check the geographic footprints and hold out a test set that represents this use. Compare results by site and season rather than only the overall average. A harder geographic split is not automatically more representative: it must correspond to the stated need. The risk described is methodological reasoning, not a measured leakage on every remote sensing dataset.

**Define the unit of the test**: Ten thousand tiles from ten scenes do not represent ten thousand independent contexts. Build a table linking each tile to its scene, site, date and footprint; assign groups to folds before any augmentation or patch extraction. Learned normalization statistics and threshold choices must follow the same separation. A geographic margin can help remove overlaps, without guaranteeing independence from every acquisition factor. To compare two methods, also aggregate their differences by groups representative of the deployment: a result dominated by one heavily tiled site can tell a different story from the average site. This is a proposed protocol, not an audit of SpaceNet.

**A deployment question determines the split**: A geographic holdout tests transfer to new places; a later-date holdout at known places tests temporal transfer. Neither substitutes automatically for the other. A proposed protocol states the deployment question first, then groups samples by footprint, acquisition and site before preprocessing or model selection. Where multiple tiles share the same source imagery, confidence intervals should respect that grouping rather than treating every tile as an independent replication.

**Blocking errors**: Equating separate files with statistical independence.
Source: [[20-acquisition-images/references/23-imageries-specialisees|Full reference]]; [Roberts et al. 2017, abstract and Box 1, block cross-validation for spatially structured data](https://doi.org/10.1111/ecog.02881); [SpaceNet7, The Problem and The Data (accessed 2026-10-18)](https://www.spacenet.ai/sn7-challenge/); tile-leakage scenario deduced by the project. Added reasoning: project deduction; consulted passages are recorded in the canonical reference.
Tags: cv::pilote cv::d02 famille::evaluation cv_id::CV-IMAGERIES-003 provenance::agent pole::E
END
