# Agent instructions

## Objective

This repository contains an Obsidian knowledge vault and computer vision
flashcards for progression toward senior engineering proficiency.

- Preserve the requested depth: problem, intuition, formulation, assumptions,
  tradeoffs, limitations and applications.
- Give each question an explicit recall objective and an answer that can be
  graded. Detailed answers are welcome when they serve that objective.
- Distinguish sourced facts from assumptions and project decisions.
- Do not claim exhaustive coverage without mapping the curriculum and checking
  its gaps.
- Select and validate the export plugin before adopting an Anki syntax throughout
  the vault. Preserve any synchronization identifiers it generates.
- Write all new and revised prose in English, following the learner's request
  of 2026-10-31. Preserve method names and compatibility identifiers; see
  `docs/english-translation.md`.

## Workflow

Read `CONTRIBUTING.md` before preparing a commit or PR.

Clarify requirements before implementing a structural decision. Matt Pocock's
skills are installed at user level; Spec Kit integration is local to this
repository. See `docs/tooling-audit.md` for the audited installation state.

The constitution at `.specify/memory/constitution.md` is still the template
provided by Spec Kit. Do not treat its examples and placeholders as ratified
decisions. Complete it during project scoping.

The tracker destination for Matt Pocock's skills has not yet been chosen.
Use `$setup-matt-pocock-skills` before the first `$to-spec` to configure that
destination. This preparation does not authorize publishing issues or PRs.

## Vault organization

Organize flashcards by topic according to `scripts/vault_sections.json`:
one numbered directory per domain, an index named `00-index.md`, flashcard
files directly inside the topic directory, and canonical reference notes in
`references/`. Detailed conventions appear in `docs/vault-layout.md`.
Preserve pedagogical IDs and Anki identities when moving files; update links,
media, target decks and validation evidence. An empty directory still needs
content: its existence does not establish topic coverage.

To audit, correct or enrich existing reference notes and flashcards, use the
repository's `revue-cartes` skill (`$revue-cartes` in Codex, `/revue-cartes`
in Claude Code). It checks claims against sources, preserves the IDs from which
Anki note identities are derived, records corrections and deepens answers by
default (audit only on request). It tracks proposals through the learner's
decision in `docs/revues/propositions.md`.

## Sources and documentation

Use Context7 to verify library APIs, versions, configurations and examples:
resolve the identifier with `resolve-library-id`, then call `query-docs`
with a specific question. Prefer official projects over forks.
If a library is absent from Context7, consult its official documentation and
report that fallback.

For computer vision concepts, consult relevant primary papers and official
reference material; Context7 does not replace a scientific bibliography.

## Validation

Match checks to the change. For documentation, review links, examples and the
diff. For flashcard export, test creation and update in a disposable deck;
check equations, media and duplicate prevention. For a script, verify the
relevant behavior and error cases.

Do not describe an installed skill as CI or an automated check. State what
was verified and what remains to be validated in Obsidian and Anki.
