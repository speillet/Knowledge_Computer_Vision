# Source access and evidence limits — 2026-11-08

The subject reports identify the primary passages used for the checked
mechanisms. A source supports those claims, not every retained historical
paragraph, constructed example or proposed experiment. This is agent
self-review, not independent scientific validation.

## Access issues and fallbacks

| Source attempted | Observed result | Resolution and limit |
| --- | --- | --- |
| NIfTI qform/sform documentation | HTTP 403 | Physical coordinates checked against the accessible DICOM image-plane specification; no new NIfTI API claim |
| Original Willow Garage ORB PDF | Inaccessible | Official OpenCV 4.13 ORB documentation and Context7 used for mechanisms and norm contract; historical paper benchmarks not revalidated |
| LoFTR HTML v2 | HTTP 404 | Primary arXiv PDF accessible and used for §3 |
| PointPillars CVF HTML | HTTP 403 | Primary arXiv PDF accessible and used for pillar encoding |
| Occupancy Networks CVF PDF | HTTP 403 | Primary arXiv HTML v1 accessible; §3 distinguishes the occupancy classifier from a distance field |
| SigLIP HTML v4 | HTTP 404 | Primary arXiv PDF accessible and used for the pairwise loss |
| ArcFace PDF | Browsing tool size limit | Primary arXiv HTML v4 accessible and used for the identity objective |
| GIoU HTML v12 | HTTP 404 | Cited v2 HTML accessible and used; no v12 claim retained |
| First MOSSE author-site path | HTTP 403 | The author's `~draper/papers/bolme_cvpr10.pdf` copy was accessible |
| Kaess iSAM2 PDF | Initial extraction succeeded; later passage requests timed out | Incremental/Bayes-tree material retains its primary citation; the timeout is not counted as confirmation of a later passage |
| Farnebäck PDF | Initial extraction succeeded; a later request timed out | Polynomial model visible in the initial extraction; added coefficient identities also derived explicitly by the project |

## Implementation documentation

Context7 identifiers were resolved before querying Ceres Solver, OpenCV,
Open3D, TorchVision and ONNX Runtime. Official documentation was also opened.
OpenCV contracts use version 4.13; the ICP comparison uses Open3D 0.19.
The new prose does not introduce executable library examples or promise
backend-specific support. Mutable ONNX Runtime, TensorRT and GStreamer pages
were consulted on 2026-11-08; their support matrices and defaults are not
generalized to every installed version.

SORT and COCO lifecycle/evaluation checks use the existing pinned commits
`2236dff5019565958b84df7d871d41cc1db58ac7` and
`8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9`.

## Distinct kinds of evidence

- Source passages establish the named mathematical or algorithmic mechanism
  under their assumptions.
- Constructed examples and deductions illustrate that mechanism. Executed
  arithmetic is identified separately in the numerical evidence.
- Suggested ablations, device tests and acquisition protocols remain proposed.
- Structural validators and unit tests check repository behavior; they do not
  certify all scientific prose, learning effectiveness or application rendering.

No new image/video model experiment, hardware benchmark, Obsidian display test,
AnkiDroid import or independent review is claimed.
