# Repository language migration — 2026-10-31

The learner requested an English version of the entire repository. English is
now the language for learning content, specifications, contributor documentation,
agent instructions, review reports, examples and user-facing validation messages.
This request supersedes the earlier preference for French prose.

## Acceptance criteria

- Translate the complete existing explanations, including the preceding
  enrichment of all 282 cards; do not shorten answers or replace them with summaries.
- Use consistent computer vision terminology and retain original method names,
  mathematical notation, units, numbers, citations and execution qualifications.
- Translate the 60 canonical reference notes before the corresponding cards,
  increment their revisions once, and keep their draft status and provenance.
- Preserve pedagogical IDs, Anki GUIDs, note type ID, field names, templates,
  tags, deck names, file paths and machine-readable metadata keys. These are
  compatibility identifiers; their historical spelling does not determine the
  language displayed to the learner.
- Translate the visible labels in the SORT diagram while preserving its filename.
- Update generators and format validators together with their English output,
  including meaningful regression coverage for the language migration.
- Keep internal links usable after headings change. Preserve dates and recorded
  outcomes in historical reports; translation is not a new execution of those tests.
- Regenerate the catalogue and learning path, check all cards and links, rebuild
  the local Anki package and simulate an update from the pre-translation package.
- Report translation coverage, validation results and any remaining limitations.
  Do not claim independent scientific review or a real AnkiDroid display test.

The translation started from the uncommitted content enrichment of 2026-10-30.
That work is included in this migration and preserved in a
pre-translation snapshot outside the repository. Generated packages stay in
`dist/` and are not committed.

## Translation method

Translation is performed locally with the
[Helsinki-NLP OPUS-MT French-to-English model](https://huggingface.co/Helsinki-NLP/opus-mt-tc-big-fr-en)
(CC BY 4.0), using CTranslate2 and SentencePiece outside the repository's runtime.
The initial smaller-model pass was superseded after review found omissions and
literal terminology. The retained pass translates complete sentences while
protecting equations, links, identifiers and numbers, then receives terminology,
format and targeted technical review. No repository text is submitted to an
external translation service. No translation-model dependency is added to the
project.

CTranslate2 usage and conversion were checked with Context7 against the official
project documentation. Language-candidate scanning uses langid's official
repository documentation as a fallback because the library was not found in
Context7. That heuristic supports review; it does not certify fluent English or
scientific correctness.

The learning contract, agent instructions, contribution guide, catalogue and
curriculum generators were edited directly in English. English CLI options
(`--output`, `--reference-url`, `--verify`, `--compare`) are available alongside
compatible legacy options.

Targeted terminology review corrected ambiguities between learning cards and
spatial maps, norms and standards, sparse matrices, whitening, Bayes-tree cliques
and geometric conventions. It also checked sentence polarity and preserved
reference IDs mentioned in prose, not only identifiers in metadata and Anki fields.

## Validation results

- All **282 existing cards**, **60 canonical reference notes** and **14 topics**
  retain their content and identities. Answers contain **253–406 lexical words**,
  with a median of **295**. All 282 questions were translated directly, and
  402 repeated case questions in reference notes were aligned with those fronts.
- Each canonical revision increased once. Other metadata, pedagogical IDs, tags,
  decks, math fragments and source URLs are unchanged. Notes retain
  `statut: redige` and their authorship provenance.
- **58 unit tests pass**, including two English-format regressions. Vault,
  curriculum-order and catalogue checks pass. Both numerical example scripts
  produce the same 21 reported values as the pre-translation snapshot.
- **395 heading links were updated**; the link audit checked **2,975 local
  Markdown links** without a missing file or heading. Vault wikilinks also pass
  the existing validator. Historical checklist completion states are unchanged.
- The local package contains **282 notes/cards**, **14 subdecks** and the translated
  SORT SVG. Its manifest has **282 modified**, **0 added** and **0 removed** cards.
  All GUIDs and target decks are preserved; Anki model, fields, templates and style
  are byte-identical to the snapshot.
- Anki 26.9.3 imported the French package, reviewed three cards and imported the
  English package: all 282 note IDs were retained and updated. Scheduling and
  history were preserved for the reviewed cards; another English import created
  no duplicates. The standard content/style update simulation also passes.
- The translated SVG was rendered locally and visually checked for clipping.

Detailed results and canonical revisions appear in the
[validation record](english-translation-validation.json).

## Limits and publication state

Before merging on 2026-11-01, the Standards and Spec reviews identified technical
mistranslations that structural checks had missed. A targeted correction pass
restored the French source meanings and updated affected canonical revisions;
see the [pre-merge review](revues/2026-11-01-traduction/00-bilan.md). The initial
validation results above and their 2026-10-31 revision record remain historical.
The integration with PR #24 adds four regression tests for the English inventory.

This is a local, machine-assisted translation with direct translation of all
questions and targeted terminology and structural review. It is not independent
scientific validation or a complete native-speaker proofread of every paragraph.
Existing scientific qualifications and unexecuted-example labels still apply.
No new image/video experiment or professional proficiency result is claimed.

Actual AnkiDroid rendering, MathJax, links and phone reimport after review remain
to be checked on the learner's device. The generated package stays in `dist/`.
The delivery branch is `docs/english-repository-20261031`. Pushing this branch
does not merge it into `main` or publish an Anki release. Until the English
branch is merged, package links to references on GitHub `main` continue to open
the previously published content.
