# Pilot flashcard template

This is the format required by `scripts/check_vault.py` and exported to
AnkiDroid by `scripts/build_apkg.py` (note type `CV-Pilote`; see
`docs/export-apkg.md`). It remains experimental; coordinate changes with
the specification and `specs/001-cv-knowledge-base/contracts/obsidian-anki.md`.
Keep this template outside the vault: the validator rejects a `START` line
inside a guide, index or reference note.

## Block

```text
## CV-<TOPIC>-NNN

Objective: <verb and object>. Family: understanding. Provenance: agent.

START
CV-Pilote
ID: CV-<TOPIC>-NNN
Question: <context and standalone question without revealing the answer>
Reponse: **Expected answer**: <points required to satisfy the objective>

**Further explanation**: <mechanism, reasoning, limitations and example>

**Blocking errors**: <misconceptions that invalidate the answer>
Source: [[<folder>/references/<reference>|Reference <Name>]] ; [<Author year, §x>](https://…).
Tags: cv::pilote cv::dXX famille::comprehension cv_id::CV-<TOPIC>-NNN provenance::agent pole::B pole::E
END
```

## Rules

- **File**: one `TARGET DECK: CV::Pilote::<folder>` line at the beginning.
  `<folder>` is the topic directory, such as `40-features-matching`.
  Flashcards live at the topic root; their canonical reference note lives
  in `references/` under the same filename.
- **ID**: `CV-<TOPIC>-NNN`, matching `CV-[A-Z0-9-]+-\d{3}`. Use the next free
  number reported by the inventory. Never reuse or renumber an existing ID.
- **Header**: `## <ID>` and
  `Objective: <objective>. Family: <family>. Provenance: agent.` precede the block.
  Use the punctuation shown in the complete example.
- **Families**: English header labels map to stable internal tags:

  | Header label | Tag value |
  | --- | --- |
  | understanding | comprehension |
  | reasoning | raisonnement |
  | algorithm | algorithme |
  | comparison | comparaison |
  | diagnosis | diagnostic |
  | practice | pratique |
  | evaluation | evaluation |
  | design | conception |

  The header label and `famille::` tag must represent the same family.
- **Fields**: `ID`, `Question`, `Reponse` and `Source`, in that order. Preserve
  these internal field names. `Reponse` may span multiple lines and contain
  blank lines; all three bold English rubrics are required.
- **Source**: exactly one wikilink to the parent reference, relative to the
  vault root and without `.md`, plus at least one HTTPS primary source with
  its section, line or commit.
- **Tags**: one line immediately before `END`, containing `cv::pilote`, the
  reference's `cv::dXX` domain, `famille::…`, `cv_id::<ID>`,
  `provenance::agent` and one `pole::<letter>` tag per career track in the
  reference. Track tags must exactly match `poles`, without duplicates.
  The example uses `pole::B pole::E` for `poles: [B, E]`; adapt these to the
  parent reference. The pilot validator requires `provenance::agent`;
  learner-authored cards require a corresponding validator change.
- **Anki identity**: the package derives the note GUID from its pedagogical ID
  (`genanki.guid_for("CV-Pilote", ID)`), independently of content. Changing an
  existing ID creates another note on the phone and leaves the old one behind.
  Legacy plugin comments `<!--ID: …-->` are no longer produced; preserve any
  existing comment and never copy it to another card.
- **Content**: use `$…$` and `$$…$$` for mathematics. Paragraphs, simple lists,
  bold, italic, code and links are supported. Local image filenames must be
  unique across the vault. Avoid trailing whitespace. The package rejects
  headings, tables, blockquotes and `$` outside a formula; the inventory reports
  conversion errors.
- **Length**: at least 180 lexical words in `Reponse`, without an upper limit
  or padding. The expected answer remains concise and gradable.
