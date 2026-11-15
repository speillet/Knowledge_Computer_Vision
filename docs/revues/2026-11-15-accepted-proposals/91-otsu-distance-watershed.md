# Review — Otsu, distance transforms and watershed — 2026-11-15

## Overview

Mode: `ajouter` for the accepted proposal P-CV-WATERSHED-01. One card added,
CV-WATERSHED-006; the five existing cards were not re-audited in this pass (see the
[2026-11-14 report](../2026-11-14-reference-depth/91-otsu-distance-watershed.md)).
Self-review: Agent Claude Code (revue-cartes).
Editorial status: redige. Reference revision 6 → 7.

## Added card

| Card | Accuracy | Relevance | Gradability | Consistency | Family |
| --- | --- | --- | --- | --- | --- |
| CV-WATERSHED-006 | Priority = largest absolute B, G or R difference between neighbouring pixels, 0–255: segmentation.cpp L151–L159. `CV_8UC3` and `CV_32SC1` asserted: L161. Initial entries with the smallest difference to an adjacent marker: L183–L223. Lowest non-empty queue served first, FIFO within a level: L105–L109 comment, L239–L259. Two labels → $-1$, no propagation: L265–L293. Push with the difference to the newly labelled pixel: L295–L323. Tutorial floods the colour image (`cv.watershed(img,markers)`, L132), markers from $0.7\max D$ (L88–L89), partial success noted (L135–L136), intensity-as-altitude theory (L14–L19). "No contrast criterion" for overlapping grains and thalweg lines as watershed lines of the inverted distance function: Beucher & Meyer §VI.B, pp. 467–468. scikit-image floods `image` lowest values first (L99–L100) and its example calls `watershed(-distance, markers, mask=image)` (L208). The rim and scaled-$D$ outcomes: project constructions, recomputed on a port of the 4.13.0 code | Understanding: a frequent implementation misconception that silently misplaces boundaries while seed counts look right | 3 expected criteria (relief computed from colour differences; role of $D$ limited to markers, dams from colour differences or arrival order; flood $-D$ with another implementation); 520 lexical words | Notation $\delta(x,y)$ and the thalweg vocabulary as in the reference's "Marker-controlled watershed"; distinct from CV-WATERSHED-002, which rebuilds the pipeline and mentions the relief only in its explanation, and from CV-WATERSHED-004, which diagnoses seeds | Understanding |

The question names the tutorial call and the symptom (one seed per coin, dam off the
neck); it does not name colour differences, $-D$ or another library. The understanding
family was absent for this subject.

## Reference findings

- **Imprecise:** "Passing a scaled distance map as the image would flood its local
  differences, close to constant on a slope". Along a straight slope the differences are
  indeed nearly constant (12–13 per pixel in the constructed scene), but they fall to 0
  across the saddle between two maxima, so the neck becomes the cheapest crossing
  instead of a barrier: in the constructed scene, 899 of the large coin's 1,216 pixels
  receive the small coin's label. Source: segmentation.cpp L151–L159 and L295–L323,
  recomputed by the check script. The sentence now states both parts.
- **Added:** initial queue entry, queue service order and the `CV_8UC3` requirement
  with their lines; the consequences for the distance pipeline ($D$ decides markers and
  count; dams follow colour differences or FIFO arrival order); Beucher and Meyer's
  reason for the distance function and their thalweg definition, quoted; the tutorial's
  own note on partial success; scikit-image's `image` contract and docstring example;
  worked example D; a third cause in the failure-mode row "Counts right but boundaries
  misplaced".

## Applied corrections

- `vault/90-segmentation/91-otsu-distance-watershed.md`: CV-WATERSHED-006 appended.
- `vault/90-segmentation/references/91-otsu-distance-watershed.md`, revision 6 → 7:
  OpenCV relief paragraph corrected and developed; worked example D added after worked
  example B; failure-mode row extended; segmentation.cpp, tutorial and scikit-image
  source entries given the new line ranges; the card listed under related flashcards;
  closing provenance line extended.

## Proposals

P-CV-WATERSHED-01: accepted by the learner on 2026-11-15, completed as
CV-WATERSHED-006.

## Sources

Scientific sources:

- Beucher and Meyer 1993, [CMM PDF](https://people.cmm.minesparis.psl.eu/users/beucher/publi/SB_watershed.pdf),
  text extracted with `pdftotext`: §VI introduction and §VI.B (pp. 467–468, coffee
  grains, Fig. 26 caption), §VIII item 4 (closed contours, "no visible contour").

Implementation sources, read at tags on GitHub raw (docs.opencv.org returns HTTP 403
from this environment; Context7 is not available in this session):

- OpenCV 4.13.0 `modules/imgproc/src/segmentation.cpp` L85–L330 (`cv::watershed`).
- OpenCV 4.13.0 `modules/imgproc/include/opencv2/imgproc.hpp` L3470–L3500
  (`watershed` documentation).
- OpenCV 4.13.0 `doc/py_tutorials/py_imgproc/py_watershed/py_watershed.markdown`
  L1–L149.
- scikit-image v0.25.2 `skimage/segmentation/_watershed.py` L80–L242.
- OpenCV 4.11.0 `modules/imgproc/src/segmentation.cpp`, fetched only to diff
  `cv::watershed` against 4.13.0: the function bodies are identical.

No access failed.

## Checks and limitations

`python3 -I docs/revues/2026-11-15-accepted-proposals/checks/91-otsu-distance-watershed.py`
passes its 9 checks: geometry and neck value (9.0 px); one seed per coin at the
tutorial's $\alpha=0.7$, the small coin's being a single pixel; rim independence of $D$
and markers; colour-difference priorities 0, 60 and 170; dam at the neck for both
reliefs without the rim; 235 of 1,216 large-coin pixels mislabelled with the rim by the
port and none by the $-D$ flood; the $-1$ image frame; 899 pixels mislabelled when a
scaled $D$ is passed as the image.

Executed cross-check (scratch script outside the repository, `python3 -I`, installed
OpenCV 4.11.0, NumPy 2.2.6 and scikit-image 0.25.2): on the same scene, `cv2.watershed`
returned exactly the port's label maps without the rim, with the rim (235 mislabelled
pixels) and with the scaled $D$ (899); `cv2.distanceTransform(..., DIST_L2,
DIST_MASK_PRECISE)` matched the stdlib $D$ within $10^{-6}$ px; and
`skimage.segmentation.watershed(-D, seeds, mask=fg)` returned exactly the stdlib $-D$
flood's labels (0 mislabelled). The installed OpenCV is 4.11.0, not 4.13.0; the
`cv::watershed` source is identical in both tags. AnkiDroid rendering of the card is not
verified.
