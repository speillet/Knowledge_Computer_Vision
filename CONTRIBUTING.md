# Contributing

## Changes

Work on a dedicated branch, such as `docs/camera-calibration` or
`chore/development-workflow`. Keep each commit focused on one intent and each
PR small enough to review alongside its sources and validation evidence.
Write prose in English; retain stable paths, IDs and Anki schema names.

For structural changes, write acceptance criteria before implementation.
Spec Kit and Matt Pocock's skills are described in the
[tooling audit](docs/tooling-audit.md).

## Commits

Follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
with a short, precise, imperative description in English:

```text
docs(calibration): explain reprojection error
fix(anki): preserve note ids during updates
chore(tooling): configure specification workflow
```

Use `docs` for learning content, `feat` for a new capability, `fix` for a defect,
`test` for tests, `ci` for continuous integration, and `chore` for tooling.
The scope is optional. Mark incompatible changes with `!` or a
`BREAKING CHANGE:` footer.

Before committing, inspect `git status`, the diff and staged files. Stage files
by path and run `git diff --cached --check`. The `$git-commit` skill helps
prepare the message and group files by intent.

Check the existing author identity with `git var GIT_AUTHOR_IDENT`. Respect the
user's configuration. An explicitly verified identity can be supplied without
changing their settings. To configure the usual identity for this repository later:

```sh
git config --local user.name "Your name"
git config --local user.email "your-commit-address"
```

## Pull requests

PR titles follow the same convention as commits:
`<type>[optional scope]: <description>`, for example
`docs(specs): define the computer vision learning requirements`.
After review, the title can serve as the squash merge message.

Use the repository template: describe the change, validation evidence and merge
impact. Link the specification or issue when available. `$pr` helps write the
body; `$code-review` compares changes against conventions and the specification.
Give it a resolvable starting reference, such as `origin/main`.

For a flashcard, check scientific accuracy, assumptions, notation consistency,
sources and whether the question is understandable on its own. For a format
change, also test export in a disposable deck.

For learning content changes, run `python3 scripts/learning_path.py`: each
reference note must appear once in the curriculum, after its prerequisites,
and every answer must meet the editorial depth threshold. Also review the
mechanism, example and limitations: length does not establish relevance.
Add new subjects to `scripts/learning_path.json`, then regenerate the catalogue
with `python3 scripts/sync_catalog.py`; do not edit the generated path by hand.

The `$gh-address-comments` and `$gh-fix-ci` skills help address review comments
and diagnose GitHub Actions failures, respectively. The conventions above are
not currently enforced by hooks or CI.
