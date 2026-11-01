# Direct export contract to AnkiDroid

The lot of the 2026-10-24 publishes the local exporter and his skill. It makes it possible to import without installing Anki Desktop or AnkiConnect. The reference notes and flashcards of vault remain the canonical source; the pedagogical states remain unchanged.

## Criteria for acceptance

1. Refuse an invalid vault before construction. Each controlled block becomes a note `CV-Pilote`, four fields in the order `ID`, `Question`, `Reponse`, `Source`, a flashcard and the declared thematic subdeck. Preserve tags.
2. Keep the `modelId` 1153189853 from the pre-existing local packet and calculate the GUID with `genanki.guid_for("CV-Pilote", ID)`, regardless of content. Do not change fields, names, or number of templates without explicit migration.
3. Convert paragraphs, simple lists, bold, italic, code, formulas, and links from flashcards. Escape HTML text. Convert `$…$` to `\(…\)` and `$$…$$` to `\[…\]`, without transforming the dollar inside the code. Refuse titles, tables, quotes, orphaned dollars and images not found with the relevant flashcard ID. It's not a general Markdown engine.
4. Embed local images of the vault under their unique basename and use local templates and CSS. The reference links point to GitHub; opening them requires the Internet. The answers remain autonomous.
5. Generate `dist/CV-Pilote.apkg` and `dist/CV-Pilote-manifest.json`, without committing them. Read ZIP/SQLite and check IDs, GUID derived IDs, template, fields, tags, media and exactly one flashcard per note in its subdeck, without orphaned flashcard and with the only template expected. The manifesto retains commit, genanki version, accounts and footprints of content and tags. The comparison lists additions, corrections, and removals; it does not measure changes in CSS/gabarits or bytes of an image.
6. Test in a disposable collection a first import, three revisions, a content correction, and then a content and style correction. Refuse duplicates, recreated notes, unupdated content or style, and changed history. An engine simulation does not validate Android rendering or settings.

## Reproducible checks

```sh
python3 scripts/check_vault.py
python3 scripts/sync_catalog.py --check
uv run --no-project --with genanki==0.13.1 python -m unittest discover -s tests
uv run --no-project --with genanki==0.13.1 python scripts/build_apkg.py
python3 scripts/build_apkg.py --verifier dist/CV-Pilote.apkg
uv run --no-project --python 3.12 --with anki==26.9.3 --with genanki==0.13.1 \
  python scripts/simulate_anki_import.py
```

Compare two versions with `python3 scripts/build_apkg.py --comparer <ancien-manifeste.json>`; the old manifest must be saved before rebuilding. The results are recorded in the [The Pilot's Journal](../vault/01-Parcours/Suivi-pilote.md).

## update and limits

Import a newer package with update conditional notes and note types, without importing progress. A more recent edition in Anki can prevent the update: resolve the conflict in the vault, and then rebuild. A flashcard removed from the package remains in the collection until manually deleted. The `cv_id::<ID>` field and tag help to find the note.

The digital comments of the plugin remain intact in the vault but do not determine the GUIDs of this package. The two chains must not feed the same collection. No remote migration or removal tools are provided.

The tests do not affect any personal collection. MathJax rendering, SVG, code, links and dark mode, as well as reimporting after revision on the phone, remain to be tried. A release is distinct from a PR: the merge releases the code, and the local build is enough to get the importable file.

## Sources

- [genanki: identities of notes](https://github.com/kerrickstaley/genanki#note-guids), accessed via Context7 and then verified with GENANKI 0.13.1.
- [Anki: import and update packages](https://docs.ankiweb.net/manual/importing/packaged-decks).
- [AnkiDroid: import](https://docs.ankidroid.org/#_importing_anki_files).
