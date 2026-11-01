# Validate the first lot

From the root of the repository:

```sh
python3 scripts/sync_catalog.py --check
python3 scripts/check_vault.py
python3 -m unittest discover -s tests -v
python3 examples/pilot_math.py
python3 examples/curriculum_math.py
```

The controller must complete without errors: local links, identities, fields, metadata and correction criteria. The tests also check for intentional defects and expected numerical results; they do not prove the scientific accuracy of each sentence or the synchronization.

In Obsidian, open `vault/`, then `00-Accueil.md`. Read a reference note and open its flashcards file. The formulas must be legible, the links resolved and the schema SORT visible. The application procedure and templates are presented in [the Anki Guide](../../vault/01-Parcours/Guide-Anki.md).

The Anki test is done in the fourteen thematic subdecks of `CV::Pilote`, with the model `CV-Pilote`. File directives determine the subdeck. Check number of **and** notes of flashcards, repeat without duplicates, change a response after a real, identity and historical revision retained. Also test displacement/rename, deletion, and conflict on a test note. Synchronize vian AnkiWeb, wait for the media, then check on AnkiDroid the flashcards of the sample fixed in [The Journal](../../vault/01-Parcours/Suivi-pilote.md).

Record actual versions, observations, and failures. None of these application steps is marked successful by the presence of files.
