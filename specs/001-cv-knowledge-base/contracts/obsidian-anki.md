# Experimental contract Obsidian – Anki

**Version**: 2, 2026-10-24 driver. Generalize only after the actual tests.

The current path builds a `.apkg` package from the same Markdown; the plugin described below remains a historical candidate. The complementary contract [Direct Export](../../../docs/export-apkg.md) sets the identities, conversion, acceptance criteria and limits of this chain. No package and plugin imports should feed the same collection.

The `vault/` folder is the root to open in Obsidian. The flashcards are classified in the thematic directories defined by `scripts/vault_sections.json`, with their complete reference notes in `references/` and one `00-index.md` per theme. An empty root scan covers all these folders; a thematic folder allows a restricted trial. Only flashcards files contain blocks of notes. Examples of syntax and templates remain outside vault. The controller checks that no notepads are added to the guides or references. The configuration is done in the application, without embedding its private files or the plugin code in Git.

The Anki model is called exactly `CV-Pilote` (`modelId: 1153189853` for packages), with the fields `ID`, `Question`, `Reponse`, `Source` in that order. The three templates are in `anki/`. The `ID` field does not appear on the front. The canonical source remains the Markdown; the answers are not modified in parallel in Anki.

Each flashcards file defines a single `CV::Pilote::<topic-directory>` target deck, e.g. `CV::Pilote::40-features-matching`. The fourteen subdecks include 282 notes and 282 flashcards. The status remains written and the export experimental; the totals and poles are verified in the generated catalog. A block starts with `START` on a single line, followed by the model name and its four fields; field names are not translated. `Tags:` precedes `END`. After synchronization, the plugin can add its comment ID before `END`: preserve it. Never make such a comment before exporting.

flashcards use wikilinks from the root of vault to their reference notes and searchable HTTPS sources on Android. The link of reference note in Anki depends on the conversion of the plugin and the presence of the vault on the device: it is to be tested, not presented as a guaranteed mobile navigation. The answer contains the necessary for the revision without this link.

Maths `$…$` and `$$…$$`, code blocks without color dependency, original SVG local image. The template contains no remote scripts. The plugin's converter can add a remote CSS coloring; the local style must maintain offline readability, which remains to be checked on the client. The SVG is part of the media transfer test; its display on Android cannot be certified by a static check.

The deletions, renamings and conflicts remain experimental: exercise them on copies dedicated to the test according to the guide, never deduce them from the update of a simple verso. The final adoption of the plugin is subject to testing.
