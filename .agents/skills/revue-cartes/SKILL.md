---
name: revue-cartes
description: "Audit and improve existing computer vision reference notes and Anki flashcards in vault/. Check relevance, scientific accuracy and grading criteria; preserve pedagogical IDs and Anki identities, record corrections and propose enrichments. Use for review, correction and improvement of existing content, not for creating an absent topic."
---

# Review vault reference notes and flashcards

The vault was authored by an agent and has received documentary self-review.
It serves an experienced CV engineer aiming for senior proficiency. A confidently
stated error, an ungradable answer or a low-value card can waste daily review time
and reinforce misconceptions. This skill performs a careful, sourced review.

Audit content, apply corrections, propose enrichments, update counts and produce
a report. This skill does not validate Anki export, AnkiDroid rendering or learner
mastery. Never mark a reference as independently reviewed: agent self-review does
not constitute independent review (FR-037).

## 0. Define the scope

Accept a flashcard file or its reference, such as
`vault/80-detection-pose/81-nms.md`, a reference ID (`CV-NMS`), a card ID
(`CV-NMS-003`), a topic directory (`vault/50-calibration-geometrie/`) or `all`.
Ask for scope when none is provided.

Work through one topic — a reference and its cards — per pass. Checking each
claim against a precise source takes time. For a directory or `all`, process
topics in sequence, produce a report for each, and offer stopping points between
topics. Follow the user's existing authorization for the requested scope.

## 1. Prepare

1. Run `git status --short` and record pre-existing changes; another agent may
   be working in the same repository.
2. Establish the baseline:

   ```sh
   python3 scripts/check_vault.py
   python3 -m unittest discover -s tests
   ```

   Report a failure before proceeding; do not mix a format repair with a content review.
3. Inventory the scope and retain a complete baseline outside the repository:

   ```sh
   python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py <file-or-folder>
   python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault --json > <tmp>/before.json
   ```

   The inventory reports each card's family, objective, answer length, sources
   and Anki identity, plus missing families and the next available ID.
4. Read, in order:
   - The flashcard file and its canonical note in `references/`.
   - The [review rubric](references/grille.md).
   - The sections “Flashcard contract,” “Expected answer and further explanation,”
     “Card families” and “Sources, review and corrections” in
     `specs/001-cv-knowledge-base/learning-design.md`.
   - Self-review and correction history in `vault/01-Parcours/Suivi-pilote.md`,
     to avoid repeating or contradicting earlier corrections.

## 2. Audit

Start with the reference note: cards cannot be more accurate than their source.
Then evaluate each card on the four axes detailed in the review rubric.

- **Accuracy.** Extract central claims from the expected answer and explanation.
  Open the precise cited passage: paper section, code line at a commit, or
  versioned documentation. Use web tools for papers and pages. For library APIs
  or parameters, use Context7 (`resolve-library-id`, then `query-docs`), followed
  by official documentation as required by `AGENTS.md`. Give each claim a verdict:
  confirmed, imprecise, false, unsupported by the citation, or unverifiable.
  Never mark a claim confirmed from memory. An inaccessible source leaves the
  claim unverifiable; report that limitation.
- **Relevance.** Does the card train a mechanism, decision, diagnosis or evaluation
  needed by a senior engineer? Require a coherent objective, an appropriate
  family and no redundant question within the topic.
- **Gradability.** The question stands alone; its front does not reveal the answer.
  The expected answer is a finite set of verifiable points, blocking errors are
  actual misconceptions, and optional detail is not required to pass. Report
  answer length without imposing a ceiling: the spec measures review load rather
  than capping it.
- **Consistency.** Check agreement with the reference and other cards, notation,
  frames, units, dated version-dependent claims and the
  [flashcard format](references/format-carte.md).

Assign severity to each finding:

- **Blocking**: scientific error, ungradable answer or answer revealed on the front.
- **Important**: misleading imprecision, unsupported citation, multiple independent
  objectives or redundant content.
- **Minor**: wording, notation or insufficiently precise source location.

## 3. Correct

Apply blocking and important corrections directly, along with low-risk minor fixes.
Preserve review history and traceability:

- Read each file again immediately before editing. If it changed since inspection,
  stop and report the conflict instead of overwriting another agent's work.
- Correct the reference first, then search the whole vault for cards repeating the
  claim, including other topics. Leave no contradictory active card (SC-007).
- Preserve `ID:` and the `## ID` heading. Preserve the plugin's `<!--ID: …-->`
  immediately before `END`; never generate one manually. It connects the card
  with its Anki note and history.
- If a correction changes the learning objective itself, propose a new card and
  a disposition for the old one rather than rewriting it under the same ID.
  Deleting Anki notes has not yet been tested.
- For learner-authored or mixed content (`apprenant` or `mixte` provenance),
  propose changes instead of applying them. After learner acceptance, use `mixte`.
- Increment the canonical note's `revision`; retain `statut: redige`.
- Write English prose with original technical names, `$…$`/`$$…$$` mathematics
  and no trailing whitespace. Preserve compatibility keys and identifiers.
- Record each correction in the correction-log table under the follow-up section
  of `vault/01-Parcours/Suivi-pilote.md`. Include date, reference and new revision,
  affected cards, error and source, correction, responsible author
  (“Agent Codex or Claude Code, self-review (`revue-cartes`)”), checks and export
  status. Use one row per distinct error. A card with a plugin identity needs
  resynchronization; otherwise mark it unsynchronized. Preserve dated evidence
  sections, which describe what was actually tested at that time.

## 4. Propose enrichment

Look for useful gaps for a senior engineer:

- A missing family with a meaningful question here; justify inapplicable families
  instead of filling every category.
- A central concept not tested by any card.
- A missing failure mode, industrial case or decision under constraints.
- Missing or empty contract sections, a baseline and controlled variation (FR-033),
  the distinction between scientific and implementation sources (FR-036), or an
  undated version-dependent claim.
- Career tracks A–F only when `poles` exists in the data model (T017); otherwise
  record a proposal without implementing that metadata.

Present proposals without adding cards:

| Proposal | Gap addressed | Family or section | Review cost | Intended primary source |
| --- | --- | --- | --- | --- |

Each added card is reviewed for months. Prefer a few valuable additions and state
their review cost. After explicit user acceptance:

1. Use the [template](references/format-carte.md), next available ID and
   `Provenance: agent`. Check every central claim as in step 2.
2. Link the reference to its new cards; expand it as needed and increment `revision`.
3. Update current counts from the inventory in the vault home, topic index,
   inventory, README, layout guide, Anki guide, export contract and batch header
   of the progress log. Preserve dated results such as “47 notes recognized.”
4. Record additions in the correction log like other changes.

## 5. Verify

```sh
python3 scripts/check_vault.py
python3 -m unittest discover -s tests
python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault --compare <tmp>/before.json
```

Require successful checks and matching inventory totals. The comparison must show
no missing ID or changed Anki identity; only explicitly accepted additions may
appear. Search for outdated current counts and review the complete scope diff.

## 6. Report

Use this structure:

```markdown
# Review — <topic> — <date>

## Overview
<cards audited; findings by severity; applied corrections; pending proposals>

## Findings by card
| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |

## Applied corrections
<file, change, rationale and consulted source>

## Proposed enrichments, pending acceptance
<proposal table from step 4>

## Sources
<passages actually consulted; unverifiable sources and reasons>

## Checks and limitations
<commands and results; remaining export, AnkiDroid rendering, learner mastery
and independent-validation checks>
```
