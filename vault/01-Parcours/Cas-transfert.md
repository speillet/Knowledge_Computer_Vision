# Transfer case reserved

Twelve constructed cases, distinct from the corrected numerical examples. Do not read responses before attempting to transfer. A case seen under review is no longer an unprecedented case: record this exposure and prepare another scenario to measure the transfer. No results from the learner are filled in advance.

Common Correction: Adequate task/outputs, assumptions and conventions, reasoned choice, discriminating verification, conclusion limits. All applicable criteria must be met; justify non-applicability.

## Matching — choix

A poorly textured metal piece must be repositioned between two views with reflections, measured calculation budget and some possible coordinate frames. Which pipeline to compare before holding a learned matcher?

<details><summary>Reference answer and criteria</summary>

Stabilize light/coordinate frames and set precision/transformations. Compare a classic baseline, markers if possible and matching learned on the same pairs, resolution and geometric verification. Measure coverage, errors, and full cost, including failures. A model does not restore missing visual information. Success: Useful observations, compatible model, fair comparison and explicit rejection strategy.

</details>

## Matching — diagnostic

Matches are good on the left but biased on the right since a crop change in a single branch. How to isolate the defect?

<details><summary>Reference answer and criteria</summary>

Trace coordinate frames/resize/padding for each image and test known points. Restore coordinates and then examine residuals spatial and physical model. Compare before/after pretreatment to matcher unchanged. Do not conclude a descriptor defect since the match score alone.

</details>

Reference and sources: [matching appris](../40-features-matching/references/44-superpoint-lightglue-loftr.md).

## Calibration/geometry –  choice

An already calibrated camera must be located in relation to a known, non-flat 3D part. Which unknown and which solver to choose?

<details><summary>Reference answer and criteria</summary>

The pose object→camera is unknown; build matches 3D – 2D then choose a suitable robust PnP and check variant, with units, chirality and reserved validation. The homography of a plan does not describe the whole room. Compare useful precision and ambiguities; no precision is deduced from the number of points alone.

</details>

## Calibration/geometry –  diagnosis

A metric camera works but all translations of pose change by a factor after replacing the calibration target file. What to check?

<details><summary>Reference answer and criteria</summary>

Inspect square size, unit, and order of 3D points, without confusing intrinsic pixel and metric translations. Replay an independent pose and reference dimension; distinguish between change of unity and physical change. A small residual pixel can persist despite a false scale.

</details>

Reference and sources: [PnP/geometry](../50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md).

## Tracking — choix

Track identical-looking parcels seen by mobile camera with short detection losses. What assumptions to compare before a generic ReID?

<details><summary>Reference answer and criteria</summary>

Set cadence/IDs, measure detector and ego-motion, compare movement and second low-score association to an evaluated appearance in this field. Predict losses, uncertainty and life cycle; identical packages may not be distinguishable by appearance. Measure association and cost with same detections/sequences, not AP only.

</details>

## Tracking — diagnostic

The IDs fragment after changing rate, without visible modification of the detector. Which newspapers discriminate between time, association and expiration?

<details><summary>Reference answer and criteria</summary>

Keep timestamps, calls even without detections, predictions, dating, associations and ages. Check unit speed and lifetimes expressed in frames; compare a controlled cadence disturbance. A blind increase in max_age does not demonstrate cause or actual continuity.

</details>

Reference and sources: [association](../110-tracking-association/references/112-deepsort-bytetrack.md).

## Detection –  choice

A small defect detector must process large images under memory budget. What is the comparison between global resize and tile build?

<details><summary>Reference answer and criteria</summary>

Set critical size and tolerance; compare effective resolution, tiles with overlap and restitution of coordinates. Measure missed defects, duplicates/matches and full cost at fixed thresholds. Separate model quality from post-processing defects; no advantage is universal.

</details>

## Detection –  diagnosis

Predictions are good in crops, but some final boxes are staggered and disappear near fittings. Which investigation to conduct?

<details><summary>Reference answer and criteria</summary>

Trace crop/padding/resize to the global image, view proposals before NMS and tile duplicates, check valid area mask. Test an image with a known object passing through a fitting. Do not assign the error directly to the backbone; then measure the entire protocol.

</details>

Reference and sources: [Detection](../80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md).

## Classical segmentation –  choice

Cells of varying sizes touch under inhomogeneous illumination. Which classic baseline and what measure to test before a network?

<details><summary>Reference answer and criteria</summary>

Compare local lighting/shrinkage correction, markers and separation, with instance annotations. Examine size variations and contact; global Otsu does not necessarily follow semantics. Measure mergers/separations and limits; a network can be justified if the classical model remains insufficient.

</details>

## Classical Segmentation – Diagnosis

The foreground mask covers all cells but watershed produces too many fragments on their textured surfaces. How to isolate the problem?

<details><summary>Reference answer and criteria</summary>

View topography and germs, compare on copy with manual markers, check maxima parasites and morphological scale. Differentiate bad mask and oversegmentation of germs; validate by instances and sizes, without concluding from the only IoU foreground.

</details>

Reference and sources: [watershed](../90-segmentation/references/91-otsu-distance-watershed.md).

## registration 3D –  choice

Two partially overlapping scans of an unknown object have a large initial offset. What order of processing and what proof of pose foresee?

<details><summary>Reference answer and criteria</summary>

Check units/coordinate frames, reduce if useful, estimate features and global initialization then refine locally with adapted ICP variant. Measure overlap, residuals and pose reference; test symmetries and independent zones. The low RMSE alone does not guarantee the right minimum.

</details>

## Recalage 3D — diagnostic

A large flat plate gives very low point-to-plane residuals while its tangential position varies between tests. Is it necessarily a bug?

<details><summary>Reference answer and criteria</summary>

Test constrained directions: A plan provides little information about certain slips/rotations. Add geometry, distinctive points or other sensor as needed; examine packaging and reference. Changing only the number of iterations does not create the missing information.

</details>

Reference and sources: [recalage global/ICP](../60-vision-3d/references/62-recalage-global-icp.md).

[Home](../00-Accueil.md) · [Journal of Attempts](Suivi-pilote.md).
