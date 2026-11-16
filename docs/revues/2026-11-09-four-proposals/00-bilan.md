# Four approved cards — overview — 2026-11-16

## Result

On 2026-11-09 the learner accepted the four proposals then registered
([scope record](00-cadrage.md)). That session drafted CV-FUSION-007 without
delivering it; the work resumed on 2026-11-16 on `main` at `6cef833`, after
#27, #28 and #29.

- **Four proposals completed** in `ajouter` mode, one card each:
  294 → **298 cards**. No ID was removed, and no existing card, expected answer,
  objective, family, tag or target deck changed.
- **Four references** received exactly one revision increment and keep
  `statut: redige`. Verifying the cards found imprecise statements in three of
  them, corrected before the cards relied on them.
- **No new proposal.** The 94 proposals of 2026-11-14 remain pending.

This is agent self-review by Claude Code, not independent validation.

| Added card | Proposal | Family | Recall objective | Lexical words | Report |
| --- | --- | --- | --- | ---: | --- |
| CV-FUSION-007 | P-CV-FUSION-01 | evaluation | Evaluate innovation consistency beyond mean NIS | 420 | [CV-FUSION](13-kalman-ekf-eskf.md) |
| CV-SE3-007 | P-CV-SE3-01 | reasoning | Calculate a transported SE(3) covariance and interpret its coupling | 607 | [CV-SE3](12-rotations-se3.md) |
| CV-SEGMENTATION-005 | P-CV-SEGMENTATION-01 | evaluation | Calculate PQ through explicit segment matching and SQ/RQ decomposition | 631 | [CV-SEGMENTATION](93-semantique-instances-panoptique.md) |
| CV-METRIQUES-TEMPS-006 | P-CV-METRIQUES-TEMPS-01 | reasoning | Calculate global identity counts and IDF1 after a trajectory fragmentation | 608 | [CV-METRIQUES-TEMPS](132-tracking-trajectoires.md) |

The new answers run from 420 to 631 lexical words, median 607.5. Existing cards
of the same subjects run from 260 to 445. Three of the four cards are long
because each carries a full worked calculation, the evaluator or convention
rules that decide it, and the counterexamples behind its blocking errors. Each
expected answer still lists three gradable criteria. Length flags short
answers; it does not measure quality.

Each front gives the numbers needed and asks for the result and its
interpretation without naming the mechanism. CV-FUSION-007 states that every
NIS equals 2 on purpose: the card asks what that equality cannot establish.

## Main corrections

The [correction log](../../../vault/01-Parcours/Suivi-pilote.md#proposals-accepted-on-2026-11-09--completed-2026-11-16)
has one row per corrected statement. By kind:

- **Error propagation stated loosely**:
  - CV-SE3: a 0.01 rad yaw on a 0.5 m lever arm "implies 5 mm of camera-position
    uncertainty"; it adds 5 mm *in quadrature* to the 2 mm body term, giving
    5.39 mm, correlated with the yaw.
  - CV-SE3: large uncertainties make first-order *propagation* inaccurate, but
    adjoint transport by a known transformation is exact (Solà et al., §II-F,
    eq. 65 and 177).
- **Evaluator rules incomplete**:
  - CV-SEGMENTATION: an unmatched prediction is excused only when more than
    half its pixels lie in a group region of its own class, not when "mostly
    inside" one; the second void rule was missing. panopticapi at `7bb4655`
    adds the void and crowd fractions before comparing with 0.5, where the
    paper states two separate rules.
  - CV-METRIQUES-TEMPS: the IDF1 edge cost counts the pair's false-negative and
    false-positive frames, including frames where one trajectory is absent,
    with extra nodes for unmatched identities (Ristani et al., §3.3, eq. 3–4).
- **Draft fixed before delivery**: the 2026-11-09 CV-FUSION draft attributed a
  project conclusion to Gamse et al.; the paper lists the innovation
  assumptions and checks normality but does not test whiteness. A constructed
  gate example was added: with a true covariance $1.4\,S$, NIS values accepted
  by the 95% gate average about 2.00, while 11.8% of updates are rejected
  instead of 5%.

## Proposals awaiting decisions

The [register](../propositions.md#completion-of-2026-11-16) marks the four
proposals completed with their IDs. Its 2026-11-14 and 2026-11-15 sections,
written while the 2026-11-09 decision was still unmerged, describe them as
pending; they are left as written and the completion section explains why.
**94 proposals remain pending.** No rejection or deferral is inferred.

Points noted for a later pass, without a registered proposal:

- CV-SE3-003 says left/right covariance transport holds "in this local
  approximation". The transport is exact; the phrase is right only if it means
  the tangent-space Gaussian model. Its card was left unchanged, as `ajouter`
  mode requires.
- CV-SEGMENTATION-005 mentions in one sentence that the evaluator sums counts
  over images; its example is a single image and does not train the
  aggregation of P-CV-SEGMENTATION-02.

## Checks performed

Executed in a dedicated worktree on branch
`docs/add-four-approved-cards-20261109`, compared with a clean worktree of
`main` at `6cef833`.

| Executed check | Result |
| --- | --- |
| `python3 scripts/check_vault.py` | OK: 142 vault Markdown files, 60 references, 298 cards |
| `python3 scripts/sync_catalog.py --check` | 19 generated documents, 0 stale (8 regenerated by `sync_catalog.py`) |
| `python3 scripts/learning_path.py` | OK: 60 references, 298 cards, minimum 260 lexical words, 0 errors |
| `uv run --no-project --with genanki==0.13.1 python -m unittest discover -s tests` | 62 tests pass |
| `inventaire_cartes.py vault` and `--compare` with the starting inventory | 298 cards, no anomalies; 4 IDs added, none removed |
| `compare_protected.py` (2026-11-14 tool) against `6cef833` | 0 existing cards or expected answers changed; 4 additions, reported as ID-list changes; 4 references changed |
| `check_anchors.py` (2026-11-14 tool) on `vault/` and `docs/revues/` | 5,155 local links and heading anchors resolve |
| `python3 -I checks/<subject>.py` for the 4 subjects | 4 scripts pass (53 checks) |
| `git diff --check` | No whitespace errors |

## Sources and access

Each subject report lists the passages read. In short:

- **CV-FUSION**: Gamse et al. 2014, §2.2.2 and §3.4.2, through a fetch tool that
  returns short verbatim fragments and summaries.
- **CV-SE3**: Solà et al., arXiv 1812.01537v9, HTML read as text with its
  formulas (§II-E to §II-H, §III-B, App. B and D); GTSAM 4.2 `Pose3.h` and
  `Pose3.cpp`.
- **CV-SEGMENTATION**: Kirillov et al., arXiv 1801.00868v3 PDF (§3, §4.1–§4.3,
  §6); panopticapi `evaluation.py` at `7bb4655`, read in full.
- **CV-METRIQUES-TEMPS**: Ristani et al., arXiv 1609.01775v2 PDF (§2, §3.1–§3.5);
  Bernardin and Stiefelhagen 2008 from the KIT repository copy (§2.1.2, §2.1.3,
  §2.2); TrackEval `identity.py` and `clear.py` at `12c8791`.

Failed access: the Springer pages of Bernardin and Stiefelhagen returned a
JavaScript challenge or a login redirect; the KIT copy was used. Context7 was
unavailable; API and evaluator claims rest on versioned code.

## Limitations

This is agent self-review. It establishes neither independent scientific
validation (FR-037) nor learner proficiency. Every number is a constructed
example recomputed by a stdlib script; pycocotools-style evaluators,
panopticapi and TrackEval were re-implemented, not executed, and no filter,
camera or tracker was run. The HOTA columns of the CV-METRIQUES-TEMPS worked
example rest on the 2026-11-14 check and were not recomputed.

Three subagents wrote CV-SE3-007, CV-SEGMENTATION-005 and
CV-METRIQUES-TEMPS-006 from a shared brief; the coordinator recomputed their
numbers by hand, reviewed their cards and edited the shared files.

Obsidian and AnkiDroid rendering are not verified. To check on the phone: the
long fronts of CV-SE3-007 and CV-SEGMENTATION-005, and the bold sub-headings
inside the further explanations of the three long cards.

No Anki package is rebuilt. Release `anki-20261116-0021` contains the 294
earlier notes; the four new notes reach the phone only through a new package:
**to republish with `paquet-anki`**, then check the import (four additions,
294 unchanged) and the rendering on the device.
