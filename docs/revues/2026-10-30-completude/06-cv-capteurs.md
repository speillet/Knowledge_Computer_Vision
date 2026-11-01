# Review –  Sensors, rolling shutter and synchronization –  2026-10-30

## Overview

4 enriched flashcards; reference note scope of revision 3 to 4, status `redige`. Complements authorized by the learner request: mechanisms, equations, hypotheses and controls. No new ID. 0 minor reference correction; no new blocking or important findings identified in the targeted scope. This is not a certification of all previous claims.

The documentary confrontation focuses on the new mechanisms mentioned below; the cases, derivations and protocols of the project remain reported as such. Previous cores and objectives are retained, without a new full scientific validation line by line of their history.

## Views by flashcard

| flashcard | Exactitude | Pertinence | Corrigibility | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CAPTEURS-001 | Deduction/Assumption Cases; Documentary Context Below | Time model per line: specifies the existing question | Finished core preserved; 187 → 298 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-CAPTEURS-002 | Project Deduction/Protocol; no new external confirmation claimed | Moving to an image measurement: specifies the existing question | Finished core preserved; 188 → 305 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-CAPTEURS-003 | Deduction/Assumption Cases; Documentary Context Below | Chain of transformations to be explained: specifies the existing question | Finished core preserved; 224 → 337 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |
| CV-CAPTEURS-004 | Deduction/Assumption Cases; Documentary Context Below | Basic observationability: specifies the existing question | Finished core preserved; 192 → 301 words, optional addition | Same addition in reference note; ID/deck/tags retained | –  (enrichment) | Applied Supplement |

## Corrections applied

reference note: [CV-CAPTEURS](../../../vault/20-acquisition-images/references/22-capteurs-horodatage.md); [flashcards](../../../vault/20-acquisition-images/22-capteurs-horodatage.md). reference note modified before the flashcards.

- **CV-CAPTEURS-001 –  Time model per line**: write $t(y)=t_0+y\tau_r$, where $y$ is the line index, $\tau_r$ is the offset between exposure starts in seconds per line, and $t_0$ is the offset of the first line. For a constant horizontal translation $v_{px}$, the offset between first and last line is approximately $v_{px}(H-1)\tau_r$, with $H$ the height. It depends on the total scan time, distinct from the local drag $|v_{px}|t_e$. It is an ideal built-in model: reading direction, overlay modes and timestamp definition vary depending on the camera. Even a global shutter can transmit its lines successively while having exposed the pixels simultaneously.

- **CV-CAPTEURS-002 –  Switching to an image measurement**: under perspective projection $u=f_xX/Z+c_x$, a small time error gives $\Delta u\approx f_x(v_XZ-Xv_Z)\Delta t/Z^2$. Here $X,Z$ are the camera coordinates in meters, $v_X,v_Z$ their derivatives in m/s, $f_x$ is in pixels and $c_x$ the main point. The derivative is local and here ignores the rotation; it shows why 0,10 m error world does not correspond to a universal number of pixels. For a target in the center, at 10 m, with $f_x=1000$ px and a transverse movement of 2 m/s, 50 ms give about 10 px. The sign depends on the relative movement and the direction of the shift.

- **CV-CAPTEURS-003 –  String of transformations to be explained**: if $T_{AB}$ transforms B to A, a point LiDAR $p_L$ acquired at $t_L$ can be brought to the camera of $t_C$ by $p_C=T_{CW}(t_C)T_{WL}(t_L)p_L$ in homogeneous coordinates. Under rigid mounting and consistent clocks, the fixed extrinsics are composed with the time-dependent poses. Implicitly replacing $t_L$ with $t_C$ removes the movement to be compensated and creates a structured error, especially in rotation or at great distance. The deskew requires the time of each point, an interpolated pose and an announced reference time. If objects move independently of the vehicle, the ego movement alone is not enough to make them static.

- **CV-CAPTEURS-004 –  Elemental Observability**: for $H=\hat r^T$, the scalar measurement $z=Hv_{rel}+\epsilon$ constrains only one direction of a vector with three components. Its zero space has two dimensions: adding an orthogonal velocity to $\hat r$ leaves $z$ unchanged. A Cartesian velocity becomes conceivable with several independent directions and a model linking their observations to the same movement; three quasi-parallel measurements can remain very poorly conditioned. A rotation of coordinate frame gives $v'=Rv$ and $P'=RPR^T$ for a covariance $P$ and an exact rotation $R$. It re-expresses the available information without creating the two missing components; the uncertainty of the calibration may need to be added separately.

## Proposed enrichments (pending agreement)

| Proposition | Gap filled | Family or category | Cost of revision | Planned primary source |
| --- | --- | --- | --- | --- |
| No new flashcard proposed in this passage | further explanation of existing answers allowed and applied | Objectives and families preserved | Real revision time to observe; no new flashcard | View sources of the topic |

The open 119 further study of the general inventory remains open; this passage does not claim coverage.

## Sources

- [Basler, Electronic Shutter Types](https://docs.baslerweb.com/electronic-shutter-types) –  Global and Rolling Shutter. View on 2026-10-30.
- [Zhang and Singh, LOAM](https://www.roboticsproceedings.org/rss10/p07.pdf) –  §§II and V, acquisition and distortion of movement. View on 2026-10-30.
- [TI TIDUF01](https://www.ti.com/lit/ug/tiduf01/tiduf01.pdf) –  §2.4.9, radial velocity. View on 2026-10-30.

**Verdicts of evidence**: the passages consulted document the mechanism they name; they are not presented as a validation of all the industrial scenarios added. Calculations are deductions from the project; non-executed protocols remain proposals. A lengthy formulation does not prove the accuracy of all previous claims.

## Checks and limitations

Common controls recorded in the [bilan](README.md): vault, path and catalog OK; 56 tests; comparison of 282 IDs, questions, kernels, blocking errors, tags, decks and GUIDs without change; 60 reference notes aligned. The [Synthetic calculations](61-controles-numeriques.json)s are only for the flashcards listed in this evidence.

check distinct from the contents: rebuilt local package, 282 notes/flashcards, 14 decks, an SVG; successful simulation Anki 26.9.3 for import, update and history preservation of three flashcards trial. No image/video CV experience, no hardware benchmark or actual AnkiDroid rendering validated here. Self-reviewed by Agent Codex (`revue-cartes`), without independent scientific validation or proof of mastery of the learner.
