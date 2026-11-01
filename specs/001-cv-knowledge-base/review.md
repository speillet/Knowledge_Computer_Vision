# Review of relevance and completeness of specs

> Language update — 2026-10-31: this review records the earlier design decision. The learner has since requested English throughout the repository; FR-002 and the learning contract now require English.

**Date**: 2026-10-18 **Perimeter**: specification, mapping, teaching contract and export research. **Type of review**: self-review assisted by the authoring agent, confronted with primary sources; it does not constitute independent scientific expertise. **Result**: Editorial revisions 2 to 6 of the draft, always to read with the user. The revision 3 comes from the complementary review below, the revision 4 of the thematic organization of the vault (FR-039) and the revision 5 of the addition of business divisions.

## Assessment

The structure responds well to the confirmed profile: experienced engineer, acquired ML/DL bases, need for specific vision and industrial judgment. French, the answers developed and the mathematical/code complements remain adapted to this demand.

The first version, however, was more specific about the presence of documents and export than about depth per family and knowledge transfer. The main headings also left several families with little representation. The revision clarifies these points without promising universal completeness.

## Findings and corrections

The impact levels below describe the effect on the project, not a quality scientific score. "Corrected in requirements" does not mean that the reference notes exist or that the pedagogical result is demonstrated.

| ID | Impact | Weakness of the first version | Correction of revision 2 | State |
| --- | --- | --- | --- | --- |
| RV-01 | High | Named domains could mask absent subfamilies, including classical segmentation and learned matching | Enriched inventory: Otsu/watershed/GrabCut, LightGlue/LoFTR, ICP, points tracking, anomalies and acquisition | Corrected in cartography; content to produce |
| RV-02 | High | A reading priority did not indicate the depth to be reached | Identification, operational use and further explanation, with skills and dependencies by method; FR-030 | Corrected in requirements |
| RV-03 | High | Presence of a reference note and flashcards incorrectly equated to an applicable skill | Baseline, controlled variation and new cases of choice/diagnosis; FR-033/034, SC-006/009 | Corrected; tests to be carried out |
| RV-04 | High | A very detailed answer had no clear line between essential and optional | expected answer, further explanation and blocking errors; FR-015, SC-003 | Corrected in the teaching contract |
| RV-05 | Medium | The six pilot subjects were focused on the classic 2D | Three contrasting extensions: classic segmentation, learned matching, registration 3D; SC-004 | Reinforced proposal, to be reviewed |
| RV-06 | High | Data contract and timing errors remained unclear | coordinate frames, types/beaches, normalization, crops and targets, cadence and causation; FR-031/032 | Corrected in requirements |
| RV-07 | Medium | A single primary source did not distinguish between general property and library peculiarity. | Scientific traceability/implementation, processing of discrepancies and proof of review; FR-036/037 | Corrected in the contract |
| RV-08 | Medium | The initial form review did not measure the real utility of the flashcards | First attempt, delayed recall, ambiguities and corrections; FR-035, SC-008 | Defined protocol; no results yet obtained |
| RV-09 | Medium | The capabilities of a documented plugin could be confused with a validated integration | Research and essays remain separate; editorial preparation possible during the choice of the plugin; FR-028 | Open dependency, explicitly preserved |

## Complementary review (revision 3)

**Type**: Reviewed by a second agent (Claude Code) of the documents of the revision 2; no independent scientific expertise, nor testing in Obsidian or Anki.

| ID | Impact | Weakness of the revision 2 | Correction of revision 3 | State |
| --- | --- | --- | --- | --- |
| RV-10 | High | The writing mode was not specified: a source present is not a verified source, and re-reading a generated content learns less than producing it | Source of writing, confrontation of central statements at the source; FR-038, SC-010; distribution proposed in the hypotheses | Corrected in requirements; allocation to be decided |
| RV-11 | High | The actual revision cost of the developed flashcards was not measured | Duration by flashcard and projected load of the first batch, without a priori ceiling; FR-035, SC-008 | Protocol defined; no measures yet |
| RV-12 | Medium | The export candidate, without release since 2024-01, had no fallback solution or verification on the revision client | Maintenance found, package `.apkg` in plan B, rendered on the customer used; [recherche](research.md) | Research completed; tests to be carried out |
| RV-13 | Medium | No pilot subject experienced the reference note metric/protocol type | IoU and AP (COCO) added to the first floor; SC-004 | Proposal, to be reviewed |
| RV-14 | Medium | The end-to-end design judgment had no family of flashcards | System Design family; 14 domain inventory; cases from the learner experience, anonymized | Corrected in the contract |
| RV-15 | Faible | FR-014 listed six families of flashcards against seven in the contract; "P1" designated two scales; "fourteen domains" was hard-coded | FR-014 refers to contract; V0 – V2 waves; domain accounts removed | Corrected |
| RV-16 | Faible | No way to follow the mastery, yet distinct from the editorial states | Domain and family exported as labels; FR-026 | Corrected in requirements |

Points examined without modification: FR-007 to FR-010 take up the section “Equations, code and illustrations” of the contract, but their numbers are cited by this review and by the relevance checklist; they are kept. The principles for the constitution are listed in the assumptions of the spec, without being added to the constitution.

## Enrichment by business units (revision 5)

**Demande** (2026-10-18): Cover six business family-related clusters, from A (Image Understanding) to F (Vision Systems & Deployment). **Type**: enrichment by an agent (Claude Code) according to the decisions of the user; no reference note or flashcard produced.

User's decisions:

- the poles form an overlay of the existing domains, which remain the organization of the vault;
- "Plinth first": V0 unchanged, key inputs of the poles in V1, the rest in V2;
- the specs are enriched first; the carry-over in the vault follows by the tasks T015 to T018.

Changes: [cartographie](curriculum.md) “Business Poles” section; 6, FR-040 to FR-043, SC-011/012 and “Business Pole” entity in the spec; pole labels in the flashcards contract; CHK025 to CHK027.

Limitations: Pole entries are names of methods and tools to be documented; their primary sources will be checked at the writing of each reference note, as for the rest of the inventory. The entrances to the D and F poles evolve quickly: they will be dated and re-examined at each lot.

## Traceability of expected results

| Groupe | Exigences | Related criteria |
| --- | --- | --- |
| Profile, Coverage and Navigation | FR-001 to FR-005, FR-025 to FR-027, FR-029/030 | SC-001 to SC-003 |
| Accuracy, contracts and evidence | FR-006 to FR-013, FR-031/032, FR-036 to FR-038 | SC-002, SC-004, SC-009/010 |
| Review, Judgement and Transfer | FR-014 to FR-019, FR-033 to FR-035 | SC-002/003, SC-006, SC-008/009 |
| Export and maintenance of relationships | FR-020 to FR-024, FR-028, FR-039 | SC-004/005, SC-007 |
| Business divisions | FR-040 to FR-043 | SC-011/012 |

This correspondence links requirements and results. The plan and tasks now exist; the 6 revision below specifies their actual state.

## Primary sources of the journal

Additions are coverage choices offered for this profile. The following sources verify the existence and nature of the families concerned, without establishing that each variant should be deepened at the same level.

- OpenCV: [Threshold and Otsu](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html), [watershed](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html) and [GrabCut](https://docs.opencv.org/4.13.0/d8/d83/tutorial_py_grabcut.html) make the classic segmentation coverage concrete.
- The [LightGlue](https://github.com/cvg/LightGlue) and [LoFTR](https://github.com/zju3dv/LoFTR) authors' repositories support the addition of learned matching and its differences in components and representation.
- [Open3D : recalage global](https://www.open3d.org/docs/latest/tutorial/pipelines/global_registration.html) presents the relationship between matches, global initialization, and local ICP refinement, absent from the previous detailed 3D inventory.
- [RAFT](https://github.com/princeton-vl/RAFT) and [CoTracker](https://github.com/facebookresearch/co-tracker) respectively represent families of optical flow learned and tracking points, to be distinguished from tracking object identities.
- [OpenCV calib3d](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) documents in particular calibration, stereo and hand-eye; [ECC Alignment](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html) justifies also covering the registration by intensities.
- [PatchCore in Anomalib](https://anomalib.readthedocs.io/en/latest/markdown/guides/reference/models/image/patchcore.html) provides a concrete input for anomaly/location inspection.
- [The KITTI tracking protocol](https://www.cvlibs.net/datasets/kitti/eval_tracking.php) illustrates the importance of metric conventions and the measured time perimeter.
- [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) supports the testing/data/monitoring coverage of an ML system; only vision-specific implications are explored here.

Context7 was actually consulted during this review: resolution OpenCV and Open3D, then targeted queries on `/websites/opencv_4_13_0` for the classic segmentation and `/websites/open3d` for the registration. Official references were then read to corroborate the summaries.

## Limitations and decisions still open

- The catalogue is more representative, but remains a research inventory: the reference notes and flashcards have not yet demonstrated their accuracy or usefulness.
- Priorities, depths and enhanced driver are propositions, not new choices attributed to the user.
- The export plugin and note templates remain to be validated in the applications.
- The distribution of the writing between the learner and an agent remains to be decided (FR-038).
- The division of production into batches after the pilot remains to be decided.
- No pole is yet chosen as a career target; raising the priority of a pole is a decision of the learner.
- The constitution has not been ratified. No principle has been implicitly added to it.
- The formal checklist Spec Kit required a `plan.md`, which was absent during the first framing. The order has indicated this requirement; this review and [sa checklist](checklists/relevance.md) are editorial and manual.
- The formal cross-analysis spec/plan/tasks will take place when the three documents are analyzed according to its workflow; this consistency review does not present itself as an execution of `$speckit-analyze`.

## Review of the update and implementation –  revision 6

The six poles are relevant as complementary routes to the base. They remain an overlay, with a canonical reference note per subject and no promise of suitability for a position. Corrections applied:

| ID | Constat | Correction |
| --- | --- | --- |
| RV-17 | V0 and priority V1 of the pole inputs could contradict each other | Keep V0 for an already priority topic |
| RV-18 | SC-011 only requested statements despite FR-042 | Require reference answers and correction criteria |
| RV-19 | The former perimeter forbade an expanded drafting now requested | Allow editorial preparation, keep export and trial gates |
| RV-20 | Scale/yaw VIO, occupation and VLA could mix tasks and gauges | Conventions, observability and defined perception/action boundaries |
| RV-21 | INT8/FP8 could suggest universal support or gain | Runtime conditioning, operators and equipment; measuring end to end |
| RV-22 | Medical formats, biometrics and metrics could mask their protocol | Units, external validation, FMR/FNMR/PAD and specified limits |
| RV-23 | A file or name cited could be counted as a detailed cover | SC-013 and inventory separate 52 reference notes written, 224 flashcards and further study open |

The 45 new reference notes and 177 new flashcards complete the fourteen themes. Advanced topics have a depth displayed; 129 entries of further explanation remain identified individually. Business cases are linked by ID and the twelve transfer cases have reserved corrections. Executable checks and evidence can be found in the vault log. No reminder session, independent validation, or actual synchronization is declared successful.

## Relevant next step

Try the driver in the applications, then measure the initial and delayed recall on the sample set before results. The pilot must be able to modify the contract if it generates filling, impossible-to-correct answers or insufficiently justified comparisons.

## Review before publication

The two-axis review is recorded in the [Delivery Report](../../docs/pre-merge-review.md). The local skill template now includes the expected pole tags. The APP entries have a thematic link, but their skills and dependencies remain to be prepared (T023): SC-001 is partially satisfied for this backlog, without calling into question the thematic coverage of the lot delivered (SC-013).
