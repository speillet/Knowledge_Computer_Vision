# Exporting the driver to AnkiDroid

**Target confirmed**: AnkiDroid on Android. **Status at 2026-10-24**: Package built, imported and simulated updates with Anki engine 26.9.3; rendered on phone and personal sync not verified.

## Direct import of the package –  current driver path

From the root of the repository, build and then check:

```sh
uv run --no-project --with genanki==0.13.1 python scripts/build_apkg.py
python3 scripts/build_apkg.py --verifier dist/CV-Pilote.apkg
```

Copy `dist/CV-Pilote.apkg` to the phone and then open the file with AnkiDroid, or select it from its **Importer** menu. The package contains 282 notes, one flashcard per note, 14 subdecks and the SVG image. The manifest `dist/CV-Pilote-manifest.json` allows to compare two constructions. Creating a public release is a separate operation from merging a PR: no release download links are guaranteed before publication.

Reimport a newer package with the update of notes and note types if newer, without importing any learning progress. Identities come from educational IDs: keep these IDs, `modelId` and the structure of the model. Disposable collection trials retain the history after a response correction and a CSS change. They do not prove the behavior of the installed version of AnkiDroid: try first on a test deck.

The vault is the source of the content. A newer edition on the phone can prevent a conditional update; resolve the conflict manually in the source, and then rebuild. Removing a flashcard from the vault does not remove it from the collection: find `tag:cv_id::<ID>` and manually delete the note. Do not feed the same collection with the plugin and package: their Anki identities differ and duplicates may appear.

The converter uses local HTML and CSS, MathJax delimiters from Anki and embedded media. The "reference note" links open the references on GitHub and request the Internet; the answers are complete without these links. Check Android for formulas, lists, code, SVG, dark mode, and offline playback, and then re-import after a review.

Sources : [Packages and Updates Anki](https://docs.ankiweb.net/manual/importing/packaged-decks), [import AnkiDroid](https://docs.ankidroid.org/#_importing_anki_files), [Genanki Identities](https://github.com/kerrickstaley/genanki#note-guids).

## Plugin history string –  protocol still not executed

The following sections retain the original candidate's protocol. They concern a separate test collection from the one fed by the package.

Obsidian on computer → Obsidian_to_Anki → AnkiConnect in Anki Desktop → AnkiWeb → AnkiDroid. The 3.6.0 plugin is desktop only; it does not run in AnkiDroid. Formulas and answers must remain usable without access to the reference note or the Internet during the recall.

Sources : [plugin officiel](https://github.com/ObsidianToAnki/Obsidian_to_Anki), [synchronisation Anki](https://docs.ankiweb.net/manual/syncing), [Manual AnkiDroid](https://docs.ankidroid.org/#_using_anki_desktop_with_ankidroid).

## Prepare an isolated test

1. Open the `vault/` folder as vault Obsidian.
2. Prepare Anki Desktop and [AnkiConnect](https://ankiweb.net/shared/info/2055492159). In the AnkiConnect configuration, keep the necessary settings and allow `app://obsidian.md` in `webCorsOriginList`, then restart Anki. Keep access local: There is no network port to open for this driver.
3. In Anki, create the `CV::Pilote` parent deck and a **CV-Pilote** note type. File directives distribute the flashcards into thematic subdecks such as `CV::Pilote::40-features-matching`. From a simple type to a single flashcard. Create/rename and order exactly the four fields **ID**, **Question**, **Reponse**, **Source**.
4. Keep a single `Rappel` template. Copy the contents of `anki/front.html`, `anki/back.html` and `anki/style.css` from the repository in front, back and style. `anki/model.json` describes these matches; this file is not an importable package in Anki. For this string, the model is created manually; the `.apkg` generator automatically provides it in its own package.

The accounts and the Anki collection remain those of the learner. For a first AnkiWeb already filled in, follow the sync manual before choosing a forwarding direction; an empty local collection should not overwrite the existing one.

## Install the candidate and limit the scan

The official registry consulted on 2026-10-18 does not list this plugin. If this situation persists in the application, the documented manual installation uses the assets `main.js`, `manifest.json`, `styles.css` of the [release officielle 3.6.0](https://github.com/ObsidianToAnki/Obsidian_to_Anki/releases/tag/3.6.0), in `.obsidian/plugins/obsidian-to-anki-plugin/` of the vault, and then activation in the community plugins. These local files are not versioned here. Do not install an unknown copy to bypass the catalog.

Plugin settings, to be confirmed in the version actually used:

| Setting | Value for the pilot |
| --- | --- |
| Scan Directory | Empty to scan the root of the vault and its subfolders; a single thematic folder for a restricted trial |
| Scheduling Interval | `0`, lancement manuel |
| ID Comments | Activated |
| Custom Regex for CV-Pilot | Empty; ordinary START/END blocks |
| Add Context / CurlyCloze / Add Obsidian Tags | Disabled |
| Add File Link | Optional, field **Source** if enabled |

Only thematic flashcards files contain blocks of notes. Markers present in Markdown examples can also be recognized by the parser: keep these examples and templates out of the vault. The controller rejects any isolated block start markers in a guide, index, or reference. Sources: [format of notes](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Note-formatting), [champs](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Field-formatting).

## First export and check on Android

1. With Anki Desktop open, manually run the scan of the vault driver. The current number is given by the catalog and the controller; each note must produce a flashcard. The current batch includes **282 notes and 282 flashcards**, distributed in the 14 thematic subdecks. Check these two numbers in the browser, not the daily deck counter, which depends on the revision limits.
2. Verify that the identity comments added by the plugin are unique, then restart without modification: the two numbers must remain the same.
3. Review a flashcard, write down its identity and history, change its back in the vault, and then restart. The same note and the same history must remain.
4. Synchronize Desktop with AnkiWeb, then AnkiDroid with the same account. Also wait for the media to sync. Check the flashcards of [the fixed sample](Suivi-pilote.md), and then play them offline.

Check developed texts, lists, inline/block and matrix formulas, code indentation, SORT image, dark mode and long equation scrolling. The template provides a basic local style; the 3.6.0 converter can add a remote CSS sheet for coloring. Offline readability should therefore be tested even if the coloring looks correct online.

reference note wikilinks are converted to Obsidian links. They only open a reference note on Android if the vault and the expected name exist there. Test this link separately; the flashcards contain their full response and HTTPS sources. Setting up a synchronization of the vault itself is not included here.

## Identities, media and corrections

The educational ID `CV-…-…` is stable, present in a field and a tag. The digital comment of the plugin identifies a note Anki; do not copy it into a new flashcard. For an instructional copy, change the ID and tag, and then remove only the Anki identity from the new note.

Media is exported by **file name**: do not reuse the same basename for two different images. If a modified image with the same name is not transferred, check the media cache of the plugin before concluding an AnkiWeb problem; log the manipulation in the log.

A scientific correction begins in the reference note and all its flashcards, which can be found by ID, links and research. Preserve identities during a simple correction; redo the controls and return the content to be reread.

Sources : [Updates](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Updating-existing-notes), [images](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Image-formatting), [MathJax AnkiDroid](https://docs.ankidroid.org/#_mathjax_support).

## Deletions and conflicts: mandatory test before extension

On a **separate test note**, try separately moving/renaming the file while keeping the identity, deleting on the source side, deleting on the Anki side and concurrent changes. Record numbers, identity, and content after each operation; do not assume that erasing the Markdown erases the note Anki.

The proposed working rule is: canonical pedagogical content in the vault, manual conflict resolution in the trial deck. The actual removal behavior remains to be observed. Stop format extension if duplicates, history lost or made essential unreadable; fix the driver or re-evaluate the candidate before producing more flashcards.
