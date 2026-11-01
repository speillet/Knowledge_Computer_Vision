# Implementation plan: vault driver

**Branche** : `feat/obsidian-pilot` · **Date** : 2026-10-18 **Entry** : [spec.md](spec.md), [Pedagogical Contract](learning-design.md).

## Summary

Create a stand-alone vault in `vault/`, with the initial seven pilot subjects, canonical reference notes, and detailed single-lens flashcards. The three extensions and the production of the catalog remain the next steps. The confirmed revision client is **AnkiDroid on Android**.

## Technical background

- Markdown UTF-8, simple YAML front matter, relative links and MathJax.
- Obsidian to read and edit; Obsidian_to_Anki 3.6.0 as export candidate **pilote**, explicit four-field model, one flashcard per note.
- Anki Desktop + AnkiConnect for export; AnkiWeb to join AnkiDroid. No personal application or account configuration changed.
- Python 3.9+ and standard library for arithmetic checks and experiments: no dependencies needed to read or verify the vault.
- No sync, drive or service added. The 2026-10-24 batch adds the `.apkg` generator described below.
- No objective of latency of the educational system; the performance of the methods are discussed with their conditions, without material promise.

## check principles

The constitution is still an unratified model: its examples are not obligations. The applicable rules come from AGENTS.md, the contract and the user request. Before and after conception: English, primary sources, stable IDs, evaluable responses, separate states and no generalization of the format as validated before the actual test are respected. No extension hook present.

## Phase 0 — Recherche

Keep the previous search; add the driver decisions to it. Check items SIFT, ORB, RANSAC, Zhang, SORT and the official COCO code. Use Context7 for the OpenCV APIs and plugin format, and then compare these results to official sources. Document protocol discrepancies.

The temporary choice of the plugin makes it possible to prepare the files of the driver; it does not validate their synchronization. Since Anki Desktop is not installed, the actual validation is an identified external dependency, with a protocol executable by the learner; it does not prevent editorial preparation.

## Phase 1 — Design

- [Data Model](data-model.md): Subjects, reference notes, flashcards and separate evidence.
- [Contrat Markdown–Anki](contracts/obsidian-anki.md): format and identity.
- [Validation Guide](quickstart.md): local controls and application testing.
- `vault/01-Parcours/Inventaire.md` keeps visible the fourteen domains and gaps; only entries with artifacts are written.

## Structure retenue

```text
vault/ .obsidian/app.json 00-Home.md 01-Parcours/             # inventory, guide and test log 40-features-matching/   # flashcards SIFT and ORB, index, complete references 50-calibration-geometrie/ 80-detection-pose/ 110-tracking-association/ 130-evaluation-fiabilite/ ...                     # 14 Themes, “Writing” for Others 99-Ressources/           # original anki/ # template, out of vault scanned examples/ # experiences without external dependency scripts/check_vault.py # check not a scripts/vault_sections.json exporter # correspondence domains / records / titles tests/ # Controller Error and Calculations
```

## Delivery and Limits

A first delivery includes the seven references, the flashcards and local controls. The reports remain “written / self-reviewed”, without independent validation or presumed mastery. recall sessions are left to complete. The twelve transfer cases covering the six families, the extensions, the Anki tests and the pedagogical measure remain visible in [tasks.md](tasks.md). The expanded editorial preparation is allowed by the current application; the technical and pedagogical pilot remains to be succeeded before adoption of the format.

## Organization requested after the first batch

The request of the 2026-10-18 retains a directory by theme, inspired by Knowledge_AI_Engineering. The flashcards are directly in the theme; the complete reference notes are grouped in its subfolder `references/`. The subdeck takes the name of the theme, the IDs remain stable, and the home links the fourteen indexes. Links, media, controller and parser test are adapted to this structure before any new publication.

## Thematic coverage package –  revision 6

The new request extends editorial preparation to the fourteen themes and six poles; application and recall essays remain open. The canonical reference notes is enriched with `poles`, the flashcards exports `pole::A` to `pole::F`. Shared topics remain in a single domain and file.

Search: check primary references by large families, Context7 for libraries. Framing corrections are based on priorities V0, observability and gauges VIO, implicit occupation/areas, boundary VLA/action, quantification conditioned to the backend and theme/variant distinction processed.

Design: Keep the four-field model and existing identities. Add structured reference notes and evaluable flashcards to existing directories, an inventory of individual entries, a view of poles and transfer cases. Navigation and accounts will be calculated from the content to avoid outdated totals. The tests check poles, parents and states; they do not certify scientific texts. No extension hook is present.

## Direct export –  lot of 2026-10-24

Publish the prepared local exporter on `feat/apkg-export`, with genanki 0.13.1 isolated by uv. The vault and the four-field model remain canonical; `modelId` takes that of the existing local packet (1153189853). The GUID depends on the name of the model and the pedagogical ID. This chain feeds a separate collection from that of the historical plugin.

Criteria: [direct export contract](../../docs/export-apkg.md). `build_apkg.py` builds and rereads ZIP/SQLite, compares manifests and embeds media; `simulate_anki_import.py` tests content, style, identities and history in a disposable collection with anki 26.9.3 and Python 3.12. AnkiDroid rendering and T010 application cases remain open. A merge releases the sources; packages in `dist/` are not versioned and a release requires a separate action.
