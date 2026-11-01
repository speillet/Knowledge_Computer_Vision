# Flashcards — Line-scan imaging, remote sensing and medical volumes

reference note: [[20-acquisition-images/references/23-imageries-specialisees|Complete reference]]. Source: Agent. Status: written, experimental export.

TARGET DECK: CV::Pilote::20-acquisition-images

## CV-IMAGERIES-001

Objective: propagate units of a volume. Family: practice. Provenance: agent.

START
CV-Pilote
ID: CV-IMAGERIES-001
Question: Why should HD95 not be calculated blindly in voxel-index units for anisotropic MRI?
Reponse: **Expected answer**: The axes can have different physical spacings; convert the distances in the announced coordinate frame and unit.

**Further explanation**: Keep orientation, resampling and protocol of empty masks. A difference in a voxel does not have the same length along the axis.

**Analytical example**: with a spacing of 0,5 mm, 0,5 mm and 3 mm, a displacement of an index is 0,5 mm on the first two axes, but 3 mm on the third. For orthogonal axes, a difference of indices $\Delta i$ is converted into distance by $\sqrt{\sum_k(s_k\Delta i_k)^2}$, where $s_k$ is the spacing of the axis. The orientation and position conventions then determine the common coordinate frame.

**Consequences for the evaluation**: A surface distance calculation must use a consistent physical geometry for both masks. A forgotten axis permutation or resampling can change the result without changing segmentation. Check a known distance and announce the unit in the report. The percentile chosen and the treatment of empty masks belong to the protocol; no isolated value constitutes here a clinical conclusion.

**Complete Geometry**: A physical position is written $p=o+A i$, with index $i$, physical origin $o$ and columns of $A$ describing directions and spacings. The distance between indices follows $\|A\Delta i\|_2$; the formula with only spacings assumes orthogonal axes. DICOM distinguishes the nominal cutting thickness from the distance between centers: systematically using the thickness as spacing can be wrong. For a stack, check the positions and orientations of the cuts, regularity and order before making a single affine. The calculation of HD95 then requires a precise definition of the surfaces, directed distances and percentiles, with explicit policy if one of the surfaces is empty.

**Blocking errors**: Compare values in voxels and millimeters as if they were identical.
Source: [[20-acquisition-images/references/23-imageries-specialisees|Full reference]] ; [DICOM PS3.3, C.7.6.2.1.1, orientation/position and spacing (accessed on 2026-10-18)](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html).
Tags: cv::pilote cv::d02 famille::pratique cv_id::CV-IMAGERIES-001 provenance::agent pole::E
END

## CV-IMAGERIES-002

Objective: check is a line-scan acquisition. Family: diagnosis. Provenance: agent.

START
CV-Pilote
ID: CV-IMAGERIES-002
Question: A part appears stretched in a line-scan image when conveyor speed changes. What should be tested?
Reponse: **Expected answer**: The synchronization between lines and displacement, the encoder and the scale reconstructed in the direction of movement.

**Further explanation**: Test a known dimension at several speeds; distinguish this defect from optical magnification and detection.

**Mechanism and units**: a line-scan camera stacks lines acquired during the move. If the speed is $v$ in mm/s and the line frequency $f_l$ in line/s, the ideal advance per line is $v/f_l$ in mm/line. The scale in this direction therefore depends on the movement, while the other axis is mainly related to the optics and the sensor.

**Constructed example**: doubling the speed at constant line frequency doubles the advance between two lines; the number of lines representing a given length decreases. The aspect displayed also depends on the scale assigned to the reconstructed image. Examine trigger, encoder, line loss, and metadata before interpreting a length measurement. A known calibration target observed at multiple speeds helps isolate this fault from a segmentation error, but does not validate the entire chain metrology alone.

**Sizing Built**: for a desired longitudinal resolution of 0,1 mm/line and a speed of 500 mm/s, it is necessary $f_l=v/s=5000$ lines/s in the slip-free model. A long piece of 20 mm then occupies about 200 lines. If an encoder imposes a line per displacement of 0,1 mm, the frequency must follow the speed variations within the range allowed by the sensor. A maximum speed exceeded or a lost impulse breaks this contract. It is also necessary to limit the displacement during the exposure of a line: correct spatial triggering and low blur are two distinct constraints. The above calculations are analytical sizing, without conveyor testing.

**Blocking errors**: Retract without checking the spatial contract of the image.
Source: [[20-acquisition-images/references/23-imageries-specialisees|Full reference]] ; [Basler, GigE Line Scan Use Cases, Use Case 1 b (v136, 2026-10-01)](https://docs.baslerweb.com/line-scan-gige-use-cases).
Tags: cv::pilote cv::d02 famille::diagnostic cv_id::CV-IMAGERIES-002 provenance::agent pole::E
END

## CV-IMAGERIES-003

Objective: Avoid a geographical flight. Family: evaluation. Provenance: agent.

START
CV-Pilote
ID: CV-IMAGERIES-003
Question: Why can randomly splitting neighboring tiles between training and test overestimate generalization in remote sensing?
Reponse: **Expected answer**: They share scene, texture and context; the test can look like training beyond the intended future scenario.

**Further explanation**: Separate regions/dates/sites according to usage, check recoveries and keep an independent evaluation.

**Why splits can fool**: Separate tiles can contain the same buildings, the same background or part of a common image. Even without exact recovery, a site shares acquisition, season and materials. The model can therefore succeed by recognizing an environment already encountered, while the product must work in another region.

**Proposed Protocol**: first define the generalization sought: new positions of the same site, new date or new territory. Group the data according to this unit before the tile, check the geographical footprints and reserve a test that represents this use. Compare results by site and season rather than just the overall average. A more difficult geographic split is not automatically more representative: it must correspond to the announced need. The risk described is methodological reasoning, not a measure of leakage established on all remote sensing sets.

**Define the unit of the test**: Ten thousand tiles from ten scenes do not represent ten thousand independent contexts. Build a table linking each tile to the scene, site, date, and footprint; assign groups to scores before any increase or extraction of patches. The normalization statistics learned and the choice of thresholds must follow the same separation. A geographical margin can help remove recoveries, without guaranteeing the independence of all acquisition factors. To compare two methods, also aggregate their deviations by representative group of the deployment: a result dominated by a very cut site can tell a story other than the average sites. This is a proposed protocol, not an audit of SpaceNet.

**Blocking errors**: Assimilate file separation and statistical independence.
Source: [[20-acquisition-images/references/23-imageries-specialisees|Full reference]]; [SpaceNet7, The Problem and The Data (accessed 2026-10-18)](https://www.spacenet.ai/sn7-challenge/); risk of leakage deduced by the project.
Tags: cv::pilote cv::d02 famille::evaluation cv_id::CV-IMAGERIES-003 provenance::agent pole::E
END
