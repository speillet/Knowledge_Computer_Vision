# Pilot data model

## reference note Canonical

Front matter: `id`, `type`, `domaine`, `poles`, `priorite`, `profondeur`, `statut`, `provenance`, `revision`, `tags`. The ID is stable and path independent. The prerequisites, skills, related notions, sources and flashcards are links in the body, readable without plugin. `provenance: agent` describes the writing.

Separate states: inventoried → written → reread. The review names its manager and its scope; self-review does not mean independent validation. Export and personal mastery are not states of writing.

## flashcard

A `CV-Pilote` note includes four ordered fields: `ID`, `Question`, `Reponse`, `Source`. A single template produces a single flashcard, without reverse. The `ID` field is an educational identifier such as `CV-SIFT-001`; it remains unchanged during a correction. `Source` connects the reference note and the primary passage. Above the block, metadata gives objective, family, and provenance. Domain, family and ID tags are also exported. The field `poles` is a non-empty list of single letters A to F; the flashcards carries the same attachments in tags `pole::A` to `pole::F`. These poles describe a course, not a certified aptitude. The controller refuses unknown letters, duplicates and disagreements between the reference note and its flashcards. Business cases also carry `cas_pole::<lettre>::conception` or `cas_pole::<lettre>::diagnostic`.

The numerical comment added by the plugin identifies a note Anki: it is distinct from the pedagogical ID, absent before the first synchronization, kept during a move and removed only when creating a new note.

## Coverage and Evidence

The inventory displays by input domain, type, priority, depth, prerequisites, skills, reference note/flashcards and gaps. It does not infer control of the presence of a flashcard. The evidence in the pilot’s log specifies environment, date, responsibility, observation and limits; an empty line means “untested”.

## Integrity

- A reference note ID and a flashcard ID are unique in their category.
- A flashcard has an existing reference note and an explicit primary source.
- Each response contains expected answer, further explanation and blocking errors.
- A relative link points to an existing file inside the vault.
- A verified export is only declared after creation, repetition, update, historical preservation and check of the rendering on AnkiDroid.
