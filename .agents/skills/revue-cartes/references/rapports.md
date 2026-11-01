# Review report conventions

Reports record what was checked, against which sources and with which limits.
They establish neither independent review nor learner proficiency. Existing
reports under `docs/revues/` follow these conventions.

1. [Location](#location)
2. [Scope record](#scope-record)
3. [Subject report](#subject-report)
4. [Review overview](#review-overview)
5. [Proposal register](#proposal-register)

## Location

```text
docs/revues/
  propositions.md                      # one register across all review passes
  <YYYY-MM-DD>[-<purpose>]/             # one directory per pass; purpose optional
    00-cadrage.md                      # required for multiple subjects
    <card-filename>.md                 # one report per subject, e.g. 81-nms.md
    00-bilan.md                        # required for multiple subjects
```

Use the subject's card filename for its report, so that
`ls docs/revues/*/81-nms.md` retrieves its history. Do not rewrite a report from
an earlier pass; create a new report for the new pass.

## Scope record

Write this before the first subject in a pass covering several subjects.

```markdown
# <Review purpose> — <YYYY-MM-DD>

Request: <faithful restatement, including accepted additions>.
Mode: <approfondir (default) | audit only>.
Scope: <subjects and counts of references and cards>.

## Delivery criteria

- <permitted changes and invariants: IDs, questions, expected answers, etc.>
- <source requirements>
- <checks required at completion>
```

## Subject report

```markdown
# Review — <reference title> — <YYYY-MM-DD>

## Overview

<n> cards audited in <mode>. Highest severity per card before correction:
<b> blocking, <i> important, <m> minor, <s> with no defect identified.
Self-review: Agent <Codex or Claude Code> (revue-cartes).
Editorial status: redige.

## Findings by card

| Card | Accuracy | Relevance | Gradability | Consistency | Severity | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-NMS-004 | Unsupported: final threshold attributed to §4, described in §5 | Senior task: processing order after score penalty | 2 expected criteria; 234 words | IoU arguments omitted | Important | Corrected source and notation |

## Reference findings

<checked claims, source disagreements and shallow sections>

## Applied corrections

<file, change, reason, consulted source and reference revision>

## Proposals

<register IDs created or updated in this pass, with their status>

## Sources

<passages actually consulted, failed accesses and claims not revalidated>

## Checks and limitations

<commands and results; unverified AnkiDroid rendering, learner proficiency
and independent validation>
```

In the findings table:

- **Accuracy** names the claim and verdict, rather than just saying confirmed.
- **Relevance** explains what the card trains (mechanism, choice, diagnosis,
  evaluation), or why it is weak (anecdote, duplicate or generic DL material).
- **Gradability** gives the number of expected criteria and lexical words.
- **Severity** records the highest severity for that card.
- No defect identified does not constitute certification.

## Review overview

```markdown
# <Review purpose> — overview — <YYYY-MM-DD>

## Result

<subjects and cards examined; cards changed or retained; IDs added or removed>

| Highest severity per card before correction | Cards |
| --- | ---: |
| Blocking | |
| Important | |
| Minor | |
| No defect identified | |
| Total | |

## Main corrections

<grouped by source, convention, expected-answer criteria or another useful category>

## Proposals awaiting decisions

<register excerpt, most useful first, including any learner decisions>

## Checks performed

<commands, results and inventory comparison>

## Limitations
```

In `approfondir` mode, add a before/after table of answer word counts (minimum,
median and maximum). Explain that the count flags short answers and does not
measure their quality.

## Proposal register

`docs/revues/propositions.md` contains one table, with one row per proposal.
Use stable IDs `P-<reference-ID>-<NN>`, for example `P-CV-NMS-01`.

| ID | Reference | Proposal | Gap addressed | Family or section | Review cost | Intended primary source | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |

Supported statuses:

- `pending`: awaiting the learner's decision;
- `accepted (YYYY-MM-DD)`: to be written in `ajouter` mode;
- `rejected (YYYY-MM-DD): <reason>`: do not propose again without new evidence;
- `deferred (YYYY-MM-DD)`;
- `completed (YYYY-MM-DD): <created IDs>`.

A proposal that only deepens an existing card, without a new ID, belongs to
`approfondir` mode and may be applied in the default pass. Record that in its status.
