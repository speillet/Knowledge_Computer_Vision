# Publication du vault — 2026-10-18

Les PR ont été relues sur les conventions et la conformité au cadrage, puis
fusionnées par merge commit dans l’ordre des dépendances, sans force push
ni contournement de contrôle. Les commits sources restent dans l’historique.

| PR | Objet | Fusion UTC | Commit de fusion |
| --- | --- | --- | --- |
| [4](https://github.com/speillet/Knowledge_Computer_Vision/pull/4) | docs(specs): define career paths and review conventions | 2026-10-18T13:55:29Z | `ed14604` |
| [5](https://github.com/speillet/Knowledge_Computer_Vision/pull/5) | feat(vault): add the Obsidian and Anki pilot | 2026-10-18T13:55:40Z | `0882f75` |
| [6](https://github.com/speillet/Knowledge_Computer_Vision/pull/6) | docs(curriculum): cover all CV themes with reference cards | 2026-10-18T13:55:51Z | `ecb42be` |

Après la dernière fusion, `main` au commit `ecb42be` a été récupérée par
fast-forward. Son arbre Git est identique à celui de la branche d’extension
relue (`5c99d57`). Toutes les têtes distantes existantes sont des ancêtres de
ce `main`, y compris les trois anciennes branches des PR 1 à 3.
Les branches sont conservées ; leur contenu est bien intégré.

Contrôles exécutés sur ce `main` :

- 34 tests unitaires réussis ; contrôleur : 125 documents, 52 fiches et 224 cartes.
- Catalogue : 18 documents générés, aucune divergence.
- Liens locaux, JSON, SVG et diff contrôlés ; 47 IDs initiaux conservés.
- Parseur officiel 3.6.0 réexécuté : 224 notes et IDs distincts, 14 sous-decks,
  puis 224 mises à jour et zéro ajout avec des identités Anki simulées.
- Copie locale de `main` synchronisée avec `origin/main`, sans fichier à committer.

Le [rapport avant fusion](pre-merge-review.md) conserve les constats et leur
traitement. Il n’y a pas de CI GitHub Actions configurée ; ces preuves sont
locales. T022 est accomplie pour cette livraison. T009/T010/T013 restent ouverts
pour les applications et le rappel ; T023 conserve les métadonnées des
129 approfondissements à préparer avant rédaction. Aucun export réel ni rendu
AnkiDroid n’a été validé.

Ce document et le statut T022 font l’objet d’une PR documentaire de suivi,
après les trois fusions de contenu ; ils ne modifient aucune carte.
