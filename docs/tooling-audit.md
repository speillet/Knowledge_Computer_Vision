# Audit of tooling

Verified on 18 October 2026 for `speillet/Knowledge_Computer_Vision`.

## Deposit and machine status

The repository initially contained only its license. No contribution workflow, local skill, or Spec Kit setup was present.

| Element | Checked statement |
| --- | --- |
| Git and remote repository | Available; remote GitHub configured |
| GitHub CLI | Authenticated for `speillet`, with repo access and workflow |
| Author identity Git | Absent; configuration postponed at user's request |
| Codex CLI and uv | Disponibles |
| Node.js, npm and npx | Absent from PATH; unnecessary for remote MCP retained |
| Specify CLI | Version 1.2.1 installed with uv; `specify check` succeeds |
| Spec Kit in the repository | Initialized Codex integration; 10 local skills |
| Constitution of the project | Generated template, to be filled in during framing |
| Context7 | Configured remote MCP; successful document resolution and playback |
| Obsidian and Anki | Unverified applications and synchronization during this audit |
| Hooks and CI | No automatic check added; documented conventions |

## Additional skills installed

These ten skills were installed in `~/.agents/skills/`, at the user level, on the audited machine. They're not in the depot. If a new installation does not appear in the selector, restart Codex, according to [Official Skills Documentation](https://developers.openai.com/codex/skills).

| Need | Skills | Source |
| --- | --- | --- |
| Clarify an idea | `grill-me`, `grilling` | [Matt Pocock](https://github.com/mattpocock/skills) |
| Write a spec and prepare your tracker | `to-spec`, `setup-matt-pocock-skills` | Matt Pocock |
| Write a PR and review the changes | `pr`, `code-review` | Matt Pocock |
| Preparing conventional commits | `git-commit` | [GitHub awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/git-commit) |
| Dealing with PR and CI returns | `gh-address-comments`, `gh-fix-ci` | [OpenAI skills](https://github.com/openai/skills/tree/main/skills/.curated) |
| Consult the current documentation | `context7-mcp` | [Upstash Context7](https://github.com/upstash/context7/tree/master/skills/context7-mcp) |

In the installed revision, `grill-me` delegates to `grilling`: both have been installed. `to-spec` synthesizes the discussion and publishes the spec in the configured tracker. Its destination remains to be chosen with `$setup-matt-pocock-skills`; no tracker, issue or remote label configuration has been created.

`code-review` depends on the conventions and the spec source of the project. Indicate a starting reference; `CONTRIBUTING.md` provides the conventions.

The skills were retrieved with the official `skill-installer` script at the following revisions, rather than at a mobile branch:

| Source repository | Installed revision |
| --- | --- |
| `mattpocock/skills` | `49dd158d1076134a641b33efb035946536778336` |
| `github/awesome-copilot` | `cb64ad12e32737ae764becd6885462e9b4c7cb00` |
| `openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` |
| `upstash/context7` | `6b636d3c35e051a1a653a236afb7f612c02a1ad3` |

## GitHub Spec Kit

[Spec Kit 1.2.1](https://github.com/github/spec-kit/releases/tag/v1.2.1) has been installed since its official filing with the published tag:

```sh
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.2.1
specify init --here --force --non-interactive --integration codex --script sh
```

The second command describes the initialization performed. For an update, reread the diff before any reset with `--force`.

The Codex skills are in `.agents/skills/` and are invoked in the conversation:

```text
$speckit-constitution $speckit-specify $speckit-clarify $speckit-plan $speckit-checklist $speckit-tasks $speckit-analyze $speckit-implement $speckit-converge
```

`$speckit-taskstoissues` is also installed; it is used to publish output tasks and should only be invoked when this publication is desired. The invocation with `$speckit-…` is the one documented for [Codex integration](https://github.github.com/spec-kit/reference/integrations.html).

## Local flashcards Review Skill

`.agents/skills/revue-cartes/` is a project-specific skill, versioned with the repository. It audits a reference note and its flashcards on accuracy, relevance, correctness and consistency, then it applies the corrections and records each change in the tracking log. It proposes enrichments, which are applied only after agreement. Codex invokes it with `$revue-cartes`. Claude Code accesses it via the symbolic link `.claude/skills/revue-cartes` and invokes it with `/revue-cartes`. Its `scripts/inventaire_cartes.py` script lists the read-only flashcards and compares two inventories to verify that Anki IDs and identities are preserved. The skill does not replace either `scripts/check_vault.py` or a replay by the learner.

## Context7: configuration and real use

The server is registered in `~/.codex/config.toml`:

```toml
[mcp_servers.context7]
url = "https://mcp.context7.com/mcp"
```

The configuration has been verified with `codex mcp get context7 --json`. Anonymous access allowed calls MCP `initialize`, `tools/list`, `resolve-library-id`, then `query-docs` on `/obsidiantoanki/obsidian_to_anki`. These calls were made directly in HTTP during the audit; the appearance of the tools in the selector of a new Codex session was not checked.

The addition by CLI proposed OAuth automatically; this path was interrupted, without an account connection, since anonymous reads were working. Authentication may be added if quotas require it; see [configuration officielle Context7](https://context7.com/docs/resources/all-clients). The catalog plugin Context7 has not been installed; the above local MCP configuration is the integration used here.

The recovered documentation confirms that Obsidian to Anki accepts multiline fields between `START` and `END` markers, and uses an identifier to retrieve notes during updates. Sources: [format of fields](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Field-formatting) and [update of notes](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Updating-existing-notes). This document verification does not constitute a synchronization test.

## Next decisions of the project

- Configure persistent Git identity whenever the user wants; a verified identity can be provided to commit commands from time to time.
- Pick the Matt Pocock specs destination via `$setup-matt-pocock-skills`.
- Completing the Spec Kit constitution with the principles agreed upon during framing.
- Choose the plugin Obsidian, the structure of vault and the format of flashcards.
- Check a creation/update cycle on some flashcards in Anki before producing a large volume of content.
