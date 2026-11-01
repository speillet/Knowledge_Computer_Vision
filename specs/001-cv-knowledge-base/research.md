# Search: interoperability Obsidian and Anki

**Document verification**: 2026-10-18. **Status**: Design search; no installation or synchronization performed.

## Plugin probably corresponding to the memory

The likely candidate is **Obsidian_to_Anki**, also presented as "Obsidian to Anki", with the identifier `obsidian-to-anki-plugin`. The manifest of the [projet officiel](https://github.com/ObsidianToAnki/Obsidian_to_Anki) consulted indicates the version 3.6.0 and use on computer. This does not allow to identify with certainty the plugin that the user remembers.

His [reference note in the directory Obsidian](https://community.obsidian.md/plugins/obsidian-to-anki-plugin) was accessible. On the other hand, the JSON downloaded from the [registre officiel](https://github.com/obsidianmd/obsidian-releases/blob/master/community-plugins.json) did not contain this identifier. The reason for this discrepancy has not been established. Availability in the integrated catalogue must be checked before adoption.

The API GitHub, consulted on 2026-10-18, indicates for this deposit a last release 3.6.0 published on 2024-01-24, a last commit the 2024-02-01 and 277 open issues; the deposit is not archived. Almost three years without release make it necessary to check compatibility with the current versions of Obsidian, Anki and AnkiConnect, and justify a fallback solution.

## Documented capabilities

| Need | Documentary findings | Consequences for the pilot |
| --- | --- | --- |
| Several flashcards in one document | Multiple blocks of notes can coexist in a file | Compatible in principle with several flashcards linked to a reference note |
| Answers developed | Documented multi-line fields, paragraphs, and lists | Check a long answer and its readability |
| Equations | Maths inline and block documented | Check symbols, matrices and conventions used |
| Local Images | Markdown links and documented Obsidian embeds | Check resolution and media transfer to Anki |
| Code | Inline and documented blocks; release test 3.6.0 confirms coloring with remote CSS | Provide a local style and check offline playback on AnkiDroid |
| update | Identifier added to the source to find the note Anki | Preserve the identifier and test for no duplicates |
| Communication | Anki Open Desktop and AnkiConnect required | Check the test environment |

Primary sources:

- [Format of fields](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Field-formatting).
- [Mathematics](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Math-formatting).
- [Rendering, media and code examples](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/test).
- [update of notes](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Updating-existing-notes).

The installation documentation of the project requires that you allow `app://obsidian.md` in AnkiConnect, then restart Anki. No settings for personal applications were changed during this framing.

## Identities and canonical source

The plugin can add a comment of the form `<!--ID: …-->`. This synchronization identity should not be copied to a new note. The stable pedagogical identifier and synchronization identity have distinct roles.

The note template and field names actually present in Anki must be checked: the labels of an example do not guarantee those of a localized installation. Numbers of notes and flashcards generated are two separate measures.

Deletion or conflicting behavior is not inferred from the operation of updates. Educational changes are made in the vault; exceptions and covers will be documented after observation of the pilot.

## Identified Alternative

[Yanki](https://github.com/kitschpatrol/yanki-obsidian) appears in the accessed registry and documents MathJax, media and code coloring. It associates a Obsidian file with an Anki note. This constraint changes the organization with respect to several blocks in the same reference note; Yanki remains an alternative to evaluate, not an implicitly adopted decision.

The requirements remain formulated by abilities to allow this choice without rewriting the educational objectives.

## Folder solution: generated `.apkg` package

A library like [genanki](https://github.com/kerrickstaley/genanki) generates a `.apkg` package to import into Anki. According to its documentation, a note imported with the same GUID as an existing note replaces it if the templates have the same fields. Diverting the GUID from the stable pedagogical identifier would therefore directly link the source and the note, without AnkiConnect or identity commentary in the vault.

This option remains to be tried: retention of the revision history after reimportation, options of update from the importer of Anki and media transfer. It is a custom tool, excluded from the current phase; it is only considered in case of failure of the driver with a plugin.

## Review client

The client confirmed during implementation is **AnkiDroid on Android**. Formulas, images and blocks of code must be checked on this client: a correct rendering on a computer does not guarantee that of a mobile.

## Use of Context7

The search called the remote MCP Context7: `resolve-library-id`, then `query-docs` on `/obsidiantoanki/obsidian_to_anki`. The results were corroborated in the primary sources above.

Context7 was also asked about `/websites/opencv_4_13_0` for matching and calibration. The reference notes will have to check the details in the official references: a documentation synthesis is not enough to guarantee the properties of all the variants of an API.

## Export driver to be carried out during the design

| Validation | Expected result | State |
| --- | --- | --- |
| Availability and prerequisites | Reproducible installation of the successful candidate, recorded versions | Not executed |
| Model and fields | Documented mapping with real names | Not executed |
| First creation | Number of notes/flashcards conforming to the model, distinct identities | Not executed |
| Repeated export without modification | No duplicates, unchanged numbers | Not executed |
| Modification of a verso | Same note update, historical preserved to unchanged model | Not executed |
| Text developed | Legible paragraphs and lists, without essential truncation | Not executed |
| Formules | Maths inline, readable block and matrix | Not executed |
| Media | Local image visible in Anki; documented displacement | Not executed |
| Code | Indentation, characters and line returns preserved | Not executed |
| Review client | Customer-readable formulas, image and code actually used | Not executed |
| Labels | Domain and family present as labels in Anki | Not executed |
| Identifiants | Copy of a new flashcard and displacement of an existing flashcard distinguished | Not executed |
| Deletion and conflict | Documented behavior before use on a real deck | Not executed |

The historical preservation test requires a flashcard actually revised in the test deck before modification. Retention of an identifier alone does not constitute proof of retention of the history.

The production syntax remains conditioned to this driver. An experimental contract and a guide are now provided for the initial seven subjects; no actual export validation is inferred from their presence.

## Design decisions for the first batch –  2026-10-18

**Decision**: test Obsidian_to_Anki 3.6.0 on the driver's seven flashcards files, four-field `CV-Pilote` model and one flashcard per note. These files are now distributed in five thematic directories, at the request of the user; the other themes remain to be written. **Reason**: Keep several flashcards per subject, explicit fields and stable pedagogical ID, without depending on the localised name of the Basic model. **Alternatives**: Yanki remains possible but changes the organization; `.apkg` remains a fallback solution, no custom exporters are added.

**Decision**: Continue editorial preparation without installing Anki in personal applications. **Reason**: Anki Desktop is missing; the official parser can be tested in isolation but does not simulate an actual collection. **Alternative**: Wait for applications; it is not necessary to write the authorized driver. Application testing remains open.

Context7: resolution of OpenCV then query `/websites/opencv_4_13_0` on standards and matching; plugin resolution and query performed in format search. Results against official APIs and code.

The [contrat](contracts/obsidian-anki.md), [The vault](../../vault/01-Parcours/Guide-Anki.md) and [Journal of Evidence](../../vault/01-Parcours/Suivi-pilote.md) specify versions, controls performed and limits. The coloring and behavior of wikilinks have been fixed from the local runtime of the converter.

## Organization by theme –  request from 2026-10-18

**Decision**: take the directories numbered by ten and the central summary of the [Deposit Indicated](https://github.com/speillet/Knowledge_AI_Engineering/tree/5fdbfe259e53d01361cf6337f6c494b4663db592). Each theme contains its flashcards and a subfolder of references; the pedagogical IDs remain unchanged, the target deck follows the theme. **Reason**: find the organization already used by the learner and revise a theme in Anki. Names and domains are in `vault_sections.json`.

The empty root scan setting and the recursive scan were rechecked via Context7, then in `main.ts` and `src/settings.ts` of the release 3.6.0: the empty setting selects the Markdown files of the vault. Templates and syntax examples remain out of vault, and the controller rejects note markers in guides, indexes, and references.

## Extension to fourteen themes –  2026-10-18

The request for expanded coverage allows the drafting of additional 45 topics. The seven subjects and 47 flashcards above designate the initial batch; the current catalog contains 52 reference notes and 224 flashcards. It keeps 129 subjects to explore individually. The three complementary researches have confronted the central claims with primary sources; they are not worth independent scientific proofreading or validation of all sentences.

Context7 was asked about the APIs OpenCV 4.13 (calibration, geometry, thresholds, watershed, flow), Open3D (registration global/ICP) and TensorRT (quantification, measurement and limits of the support). The results were compared with the official pages and articles cited in the reference notes. The OpenCV tutorials quoted in 4.12 and the version-dependent settings keep their version explicit. The current TensorRT documentation is scalable; no universal hardware support or gain INT8/FP8 is inferred.

Central passages consulted, by family:

| Family | Primary source and controlled point |
| --- | --- |
| Estimation | [Eigen, least squares](https://eigen.tuxfamily.org/dox/group__LeastSquares.html), normal equation conditioning; [Solà](https://arxiv.org/abs/1711.02508), rotation error conventions and reset ESKF |
| Geometry | [OpenCV solvePnP](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html), minimum API and coordinate frames; [Open3D ICP](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html), local initialization; [Zhang/Scaramuzza](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf), alignment gauges VO/VIO |
| Matching and segmentation | [LightGlue](https://github.com/cvg/LightGlue), sparse matches; [LoFTR](https://arxiv.org/abs/2104.00680), detector-free; [SAM](https://arxiv.org/abs/2304.02643) and [SAM 2](https://arxiv.org/abs/2408.00714), prompt, memory and causality |
| Detection and tracking | [DETR](https://arxiv.org/abs/2005.12872), drive assignment and ensemble prediction; [ByteTrack](https://arxiv.org/abs/2110.06864), association of weak detections; [HOTA](https://arxiv.org/abs/2009.07736), aggregation by threshold |
| Representations | [CLIP](https://arxiv.org/abs/2103.00020) and [SigLIP](https://arxiv.org/abs/2303.15343), goals and score limits; [PatchCore](https://arxiv.org/abs/2106.08265), patch memory and score weighting |
| Imaging and Metrics | [DICOM C.7.6.2](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html), coordinate frames/spacing; [Metrics Reloaded](https://doi.org/10.1038/s41592-023-02151-z), choice of metrics according to the task |
| Systems | [TensorRT, quantification](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/work-quantized-types.html), conditional support; [GStreamer tail](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html), meaning of leaky policies |

The constructed analytical equations and scenarios are distinguished from the authors' results. Only `examples/pilot_math.py` and `examples/curriculum_math.py` have been executed: no training, tracking sequence, registration 3D, actual export or GPU benchmark has been performed. The journal records separately the execution of the official parser on 224 notes and its simulation limits.
