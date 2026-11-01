# Publication of vault –  2026-10-18

The PRs were reread on conventions and conformance to framing, then merged by merge commit in order of dependencies, with no push force or bypass of check. The source commits remain in the history.

| PR | Subject matter | Fusion UTC | Merger commit |
| --- | --- | --- | --- |
| [4](https://github.com/speillet/Knowledge_Computer_Vision/pull/4) | docs(specs): define career paths and review conventions | 2026-10-18T13:55:29Z | `ed14604` |
| [5](https://github.com/speillet/Knowledge_Computer_Vision/pull/5) | feat(vault): add the Obsidian and Anki pilot | 2026-10-18T13:55:40Z | `0882f75` |
| [6](https://github.com/speillet/Knowledge_Computer_Vision/pull/6) | docs(curriculum): cover all CV themes with reference cards | 2026-10-18T13:55:51Z | `ecb42be` |

After the last merger, `main` to commit `ecb42be` was recovered by fast-forward. Its Git tree is identical to that of the re-read extension branch (`5c99d57`). All existing remote heads are ancestors of this `main`, including the three ancient branches of the PR 1 to 3. Branches are retained; their content is well integrated.

Controls executed on this `main`:

- 34 passed unit tests; controller: 125 documents, 52 reference notes and 224 flashcards.
- Catalogue: 18 generated documents, no discrepancies.
- Local links, JSON, SVG and diff controlled; initial 47 IDs retained.
- Official parser 3.6.0 rerun: 224 separate notes and IDs, 14 subdecks, then 224 updates and zero addition with simulated Anki identities.
- Local copy of `main` synchronized with `origin/main`, with no file to commit.

The [Merger Report](pre-merge-review.md) keeps the findings and their treatment. There are no CI GitHub Actions configured; these proofs are local. T022 is completed for this delivery. T009/T010/T013 remain open for applications and recall; T023 retains metadata of the 129 further study to be prepared before writing. No actual export or AnkiDroid rendering has been validated.

This document and the T022 status are the subject of a follow-up documentary PR, after the three content mergers; they do not modify any flashcard.
