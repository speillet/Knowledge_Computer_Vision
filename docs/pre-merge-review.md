# Review before merger –  2026-10-18

Fixed base: `19c54feb830c459858850030880432c2f466e6d2`, old `origin/main`. Scope: specs, review workflow, base Obsidian/Anki and extension to fourteen themes. Two agents examined the diff separately with `code-review`. The initial review was about `3fa8127`; unreleased commits were then reordered to include template correction from the first PR. This review does not constitute independent scientific expertise.

## Standards

**P2 –  Incomplete flashcard template.** The skill model omits pole tags while the controller requires their exact match to the reference note. **Corrected** in commit `db664e5`: example `pole::B pole::E` and matching rule with `poles`, no duplicates. No existing ID changed.

No other blocking deviations identified. Commits Conventional Commits, French prose, organization by theme, provenance and limits of evidence are consistent with conventions. No design smell justifies a restructuring in this lot. The limited duplication of parsing between tools is a maintenance point, not a documented violation.

## Spec

**P2 –  Metadata of partial further study.** FR-030 and SC-001 require skills and dependencies per method. The 129 APP entries have priority, depth and connection, with no proper skills or validated mandatory prerequisites. **Tracked open in T023**; the columns and states of the inventory explicitly indicate this limit. SC-001 remains partially satisfied for this backlog. This gap does not block the provisional publication covering the fourteen themes according to SC-013.

Application and pedagogical validations remain open in T009/T010/T013. The parser simulation is not substituted for them. No unjustified perimeter overflow or other incorrectly implemented requirement identified in this passage. The six poles have their cases conception and diagnosis; the twelve cases of transfer cover the six families with corrected. The inspected prerequisites are linked and cycle-free.

## Checks and limitations

34 successful tests; controller: 125 Markdown documents, 52 reference notes and 224 flashcards; catalog without divergence; inventory without anomaly; local links, JSON, SVG and end-of-line spaces checked. The official parser 3.6.0 recognized 224 notes, then 224 updates and zero addition with simulated IDs. These checks do not prove the accuracy of each sentence, nor the actual export, Android rendering or control of the learner. No CI check is configured.

Standards: a corrected observation; Spec: a follow-up observation in T023 and the application/educational validations already open. No merger blocking identified for the authorized editorial perimeter.
