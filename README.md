# Knowledge Computer Vision

An Obsidian knowledge vault and detailed flashcards for progression toward
senior computer vision engineering proficiency.

The reference notes and flashcards cover classical and modern foundations in
English, with original technical terms, explained equations, comparisons and
diagnostic reasoning. Current totals appear in the catalogue below.

Open [`vault/`](vault/00-Accueil.md) as a vault in Obsidian and start from its
home page. The [export guide](vault/01-Parcours/Guide-Anki.md) explains how to
build an `.apkg` package for **AnkiDroid**. Creation and updates are tested in a
disposable Anki collection; rendering on Android still needs verification.
The Obsidian_to_Anki route remains documented as a historical experiment with
separate identities.

The vault follows the topic-based organization of
[Knowledge_AI_Engineering](https://github.com/speillet/Knowledge_AI_Engineering):
14 numbered folders with indexes, flashcards at the root of each topic, and
complete reference notes in `references/`. Each topic has its own Anki subdeck
and editorial status; variants requiring further study remain visible in the
inventory. See the [layout conventions](docs/vault-layout.md).

The [senior curriculum](vault/01-Parcours/Parcours-senior.md) orders the 60
subjects into nine stages, with prerequisites, progression criteria and
integration cases. Every flashcard has a detailed answer; the expected answer
provides a grading rule without requiring recitation of every explanation.

The [English migration record](docs/english-translation.md) describes the scope
and validation. Historical filenames, metadata keys, tags, deck names and Anki
fields retain their spelling to preserve links and review history.

## Current coverage

<!-- cv-catalog:start -->
**60 reference notes and 282 flashcards**, spanning 14 of 14 topics. Agent-authored content; actual device import, recall and personal mastery remain unvalidated.

| Topic | Reference notes | Flashcards |
| --- | ---: | ---: |
| [Mathematics and estimation](vault/10-mathematiques-estimation/00-index.md) | 4 | 26 |
| [Image formation and acquisition](vault/20-acquisition-images/00-index.md) | 3 | 11 |
| [Classical image processing](vault/30-traitement-image/00-index.md) | 3 | 11 |
| [Features, matching and registration](vault/40-features-matching/00-index.md) | 8 | 39 |
| [Calibration and multiview geometry](vault/50-calibration-geometrie/00-index.md) | 7 | 36 |
| [3D vision](vault/60-vision-3d/00-index.md) | 4 | 19 |
| [Recognition and representations](vault/70-reconnaissance-representations/00-index.md) | 5 | 18 |
| [Detection and pose](vault/80-detection-pose/00-index.md) | 4 | 26 |
| [Segmentation](vault/90-segmentation/00-index.md) | 4 | 15 |
| [Motion and video](vault/100-mouvement-video/00-index.md) | 3 | 13 |
| [Tracking and association](vault/110-tracking-association/00-index.md) | 5 | 23 |
| [Generative and multimodal vision](vault/120-generatif-multimodal/00-index.md) | 3 | 10 |
| [Data, evaluation and reliability](vault/130-evaluation-fiabilite/00-index.md) | 4 | 21 |
| [Vision systems engineering](vault/140-ingenierie-systemes/00-index.md) | 3 | 14 |
<!-- cv-catalog:end -->

## Local validation

Python 3.9+, with no additional dependencies:

```sh
python3 scripts/check_vault.py
python3 scripts/learning_path.py
python3 scripts/sync_catalog.py --check
python3 -m unittest discover -s tests -v
python3 examples/pilot_math.py
```

The [evidence and remaining trials](vault/01-Parcours/Suivi-pilote.md)
distinguish local checks, agent self-review, application tests and personal mastery.

To generate the package with [uv](https://docs.astral.sh/uv/) without changing
the dependencies of the current environment:

```sh
uv run --no-project --with genanki==0.13.1 python scripts/build_apkg.py
python3 scripts/build_apkg.py --verify dist/CV-Pilote.apkg
```

Import `dist/CV-Pilote.apkg` into AnkiDroid. Generated files remain outside Git.
See the [export contract and checks](docs/export-apkg.md).

## Working tools

- [Contribution conventions](CONTRIBUTING.md): branches, commits and PRs.
- [Agent instructions](AGENTS.md): repository objectives and rules.
- [Tooling audit](docs/tooling-audit.md): installed skills, versions, checks and
  remaining configuration.
- [Flashcard review skill](.agents/skills/revue-cartes/SKILL.md):
  `$revue-cartes` (Codex) or `/revue-cartes` (Claude Code) audits and corrects
  a reference note and its flashcards, and proposes enrichments.
- [Anki package skill](.agents/skills/paquet-anki/SKILL.md):
  `$paquet-anki` builds, verifies and compares packages; releases are published
  on request.

## Current specification

The [draft specification](specs/001-cv-knowledge-base/spec.md) records the
experienced learner profile, objectives and confirmed educational choices.
Supporting documents include:

- The [coverage map](specs/001-cv-knowledge-base/curriculum.md).
- The [reference and flashcard contract](specs/001-cv-knowledge-base/learning-design.md).
- The [Obsidian–Anki export research](specs/001-cv-knowledge-base/research.md).
- The [relevance review and corrections](specs/001-cv-knowledge-base/review.md).

The [implementation plan](specs/001-cv-knowledge-base/plan.md) and its
[tasks](specs/001-cv-knowledge-base/tasks.md) describe the initial batch and pilot
follow-up. The complete catalogue, extensions and educational validation still
need work; the content is not declared exhaustive.

GitHub Spec Kit 1.2.1 is initialized for Codex. Its skills are versioned in
`.agents/skills/`; templates and scripts are in `.specify/`. Their
[origin and license](.specify/NOTICE.md) are retained in this repository.
The generated constitution remains a template to complete with
`$speckit-constitution` after clarifying the project's principles.

Matt Pocock's complementary skills and the commit and PR skills are installed
at user level. They are not included in a repository clone; their sources and
revisions are recorded in the audit.

## Continue scoping

1. Read the draft and coverage map; use `$grill-me` for open decisions,
   including the pilot and export workflow.
2. Define principles with `$speckit-constitution` and refine the draft with
   `$speckit-clarify`. Subsequent steps are `$speckit-plan`, `$speckit-tasks`
   and `$speckit-analyze` as needed.
3. To also use `$to-spec`, configure its destination first with
   `$setup-matt-pocock-skills`. Link artifacts instead of maintaining
   conflicting specifications.

On the audited machine, Context7 is configured as a remote MCP server in Codex.
This user configuration is not included in a clone. Use Context7 to verify
the documentation of tools and libraries; base scientific concepts on papers
and other primary sources.
