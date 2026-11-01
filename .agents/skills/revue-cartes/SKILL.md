---
name: revue-cartes
description: "Audit relevance, scientific accuracy and gradability of existing computer vision reference notes and Anki flashcards in vault/. Correct defects while preserving IDs, deepen answers by default, and track proposals for new cards through the learner's decision. Use for requests to check, review, audit, correct, deepen, develop, complete or enrich cards, Anki notes, references, a deck, a topic or the whole vault, even without an explicit skill invocation. Do not use to create an absent topic or build or publish an Anki package (use paquet-anki)."
---

# Vault card review

The vault's notes and cards are agent-authored and have received agent self-review.
They serve an experienced computer vision engineer progressing toward senior
proficiency. An incorrect claim, an answer that cannot be graded or an anecdotal
card wastes review time and can reinforce a misconception. Review slowly against
sources, rather than treating this as a style pass.

This skill validates neither AnkiDroid rendering nor the learner's proficiency.
Never mark a reference as independently reviewed: agent self-review does not
satisfy FR-037.

## Choose a mode

The mode determines the permitted changes. At the learner's request of
2026-10-30, the default is `approfondir` (deepen): invoking this skill authorizes
answer development. Always audit first; do not expand an unchecked answer.

| | `approfondir` (default) | `audit` | `ajouter` (add) |
| --- | --- | --- | --- |
| Trigger | Any review request unless specified otherwise | Explicit audit-only request | Learner accepts a registered proposal |
| ID, question, objective, family, tags | Preserved | Preserved | New IDs |
| Expected answer | Preserved except for sourced corrections | Corrected when contradicted by a source | Written |
| Further explanation | Corrected, then developed | Corrected | Written |
| Canonical reference | Corrected and aligned first | Corrected first | Extended |
| New cards | Proposed only | Proposed only | Written |

`approfondir` follows steps 1–4; `audit` skips step 4. Both finish with steps 5–7.

## 0. Define the scope

The argument may be a card or reference file
(`vault/80-detection-pose/81-nms.md`), a reference ID (`CV-NMS`), a card ID
(`CV-NMS-003`), a topic directory (`vault/50-calibration-geometrie/`) or the
whole vault. Ask for the scope if none is provided or inferable.

A work unit is one subject: its reference and cards. Checking each claim takes
time. For several subjects, write a scope record first, process subjects one
at a time with a report for each, and finish with an overview; see the
[report conventions](references/rapports.md). Offer a pause between subjects
unless the learner has requested continuous work.

## 1. Prepare

1. Run `git status --short` and `git branch --show-current`. Another agent may
   be working here; keep its changes separate. Use a dedicated review branch
   as described in `CONTRIBUTING.md`.
2. Establish the baseline and report existing failures before making changes:

   ```sh
   python3 scripts/check_vault.py
   python3 scripts/sync_catalog.py --check
   python3 scripts/learning_path.py
   uv run --no-project --with genanki==0.13.1 python -m unittest discover -s tests
   ```

3. Inventory the scope and save the full inventory outside the repository for
   the final comparison:

   ```sh
   python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py <file-or-directory>
   python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault --json > <tmp>/before.json
   ```

   For each card, inspect its family, objective, career tracks, answer length
   against the contract threshold, Anki GUID and sources. The inventory also
   flags unsupported export syntax and reports missing families and next free IDs.
4. Read only what is needed, without repeating completed checks unnecessarily:
   - the card file and canonical reference under `references/`;
   - the [review grid](references/grille.md);
   - the latest subject report under `docs/revues/`; do not contradict an earlier
     finding without a source;
   - relevant progress-log entries, using
     `rg -n "<reference-ID>" vault/01-Parcours/Suivi-pilote.md`;
   - the subject's entries in `docs/revues/propositions.md`;
   - when needed, the card contract, expected-answer and card-family sections
     of `specs/001-cv-knowledge-base/learning-design.md`.

## 2. Audit

Start with the reference, then assess every card against the review grid.

- **Accuracy:** list central claims in the expected answer and explanation,
  then consult their exact cited passage: paper section, code at a commit or
  versioned documentation. For APIs, use Context7 followed by official
  documentation as required by `AGENTS.md`. Classify each claim as confirmed,
  imprecise, false, unsupported by the cited passage or not verifiable. Memory
  does not establish confirmation. Record inaccessible sources and unverified claims.
- **Relevance:** judge whether the card trains a mechanism, decision, diagnosis
  or evaluation useful to a senior engineer. Require one objective, an appropriate
  family and no duplicate within the subject.
- **Gradability:** the question stands alone, the front does not reveal the
  answer, the expected answer has finite verifiable criteria, and blocking
  errors are plausible misconceptions. Answers meet the 180-lexical-word
  threshold checked by `learning_path.py`. Explanations develop a mechanism,
  example, assumption or limitation; optional details are not required for recall.
- **Consistency:** check the reference, related cards, notation, coordinate
  frames, units, dated version-specific claims, the
  [card template](references/format-carte.md) and package conversion.

Classify findings by severity:

- **Blocking:** scientific or numerical error, ungradable answer, answer exposed
  on the front or contradiction with the reference.
- **Important:** misleading omission, unsupported claim, multiple objectives,
  duplicate or answer below the threshold.
- **Minor:** wording, notation or an imprecise reference that still supports the claim.

## 3. Correct

Apply blocking and important corrections, and low-risk minor corrections.
Preserve review history and traceability:

- Reread a file immediately before editing. If it has changed, stop and report
  the concurrent edit instead of overwriting it.
- Correct the reference first, then use `rg` across the vault to find every
  card repeating the claim, including other topics. Leave no contradictory
  active card (SC-007).
- Preserve `ID:` and the `## ID` heading. The package derives Anki GUIDs from
  pedagogical IDs; changing an ID creates another phone note and leaves the
  old one and its history behind. Preserve any legacy `<!--ID: …-->` comment;
  never invent one.
- If a correction changes the recall objective, register a proposal instead
  of rewriting the same ID. State what should happen to the old card.
- Propose changes to learner-authored (`apprenant` or `mixte`) content rather
  than editing it. Accepted changes receive `mixte` provenance.
- Increment the canonical reference's `revision`; keep `statut: redige`.
- Write prose in English, preserving method names, compatibility identifiers
  and technical terms. Use `$…$` or `$$…$$`, avoid trailing whitespace, and do
  not put headings, tables or blockquotes inside card fields.
- Record each distinct correction in the correction log of
  `vault/01-Parcours/Suivi-pilote.md`: date, reference and revision, affected IDs,
  error and source, correction, responsible agent and self-review status,
  checks, and export status (`to republish with paquet-anki`). Do not rewrite
  dated validation evidence.

## 4. Deepen answers (default mode)

For each card, find what its recall objective still needs:

- an implicit mechanism, explained derivation or constructed calculation;
- an algorithm step, parameter effect or counterexample;
- equation symbols, dimensions, units and assumptions.

Align the reference first, then the card. Every addition contributes sourced or
explicitly constructed information. Label project calculations and protocols;
claim an executed experiment only with evidence. Do not paraphrase existing
paragraphs or pad an answer to reach the threshold. The expected answer remains
sufficient for recall. Preserve a card that is already complete and say so in
its report.

## 5. Propose, obtain decisions and add

Find gaps that matter to a senior engineer:

- an absent card family that has a useful objective for this subject;
- a central reference concept not tested by any card;
- a missing failure mode, industrial case or constrained decision;
- an absent or shallow reference section, baseline and controlled variation
  (FR-033), or distinction between scientific and implementation sources (FR-036).

Register each proposal with a stable ID in `docs/revues/propositions.md` using
its format. Check for duplicates and do not repeat rejected proposals without
new evidence. Prefer a few valuable proposals and state their review cost.

At the end, present pending proposals in the scope, ordered by usefulness, and
ask the learner to accept, reject or defer each. Record their decisions.

For an accepted proposal (`ajouter` mode):

1. Follow the [card template](references/format-carte.md), use the next free ID
   from the inventory and `Provenance: agent`. Verify claims as in step 2 and
   meet the answer-length threshold.
2. Link the reference to its new cards and increment `revision`.
3. Run `python3 scripts/sync_catalog.py`. Search for the old total in current
   non-generated documents under `docs/`, `specs/`,
   `vault/01-Parcours/Guide-Anki.md` and the batch heading of `Suivi-pilote.md`.
   Update current-state counts, preserving dated experiment results.
4. Mark the proposal completed with its new IDs and log the addition.

## 6. Verify

```sh
python3 scripts/check_vault.py
python3 scripts/sync_catalog.py --check
python3 scripts/learning_path.py
uv run --no-project --with genanki==0.13.1 python -m unittest discover -s tests
python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault
python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault --compare <tmp>/before.json
```

All checks must pass. Inventory totals must match the validator, without format,
conversion or answer-length anomalies. Compare IDs and legacy identity comments:
no removed ID, and additions only after approval. Review the complete scoped
diff. Explain that corrected cards reach the phone through a new package and
refer to `paquet-anki`.

## 7. Report

Write one report per subject under
`docs/revues/<YYYY-MM-DD>[-<purpose>]/<card-filename>.md`. For several subjects,
write `00-cadrage.md` first and `00-bilan.md` last, following the
[report conventions](references/rapports.md). Summarize findings by severity,
corrections, pending decisions, checks and limitations in the conversation.
