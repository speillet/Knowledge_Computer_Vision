# Revue — Canny et Hough : contours, droites et segments — 2026-10-18

## Synthèse

4 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 1 importante, 1 mineure, 2 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

Auto-revue : Agent Codex (`revue-cartes`). Le statut éditorial reste `redige`.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CANNY-HOUGH-001 | Confirmé : connexion aux réponses fortes | expliquer l’hystérésis. | Noyau fini ; 53 mots | Accord fiche et format | Aucune | Passage ciblé |
| CV-CANNY-HOUGH-002 | Confirmé ; unités rendues évaluables | interpréter un vote de Hough. | Noyau fini ; 68 mots | Accord fiche et format | Important | Noyau précisé |
| CV-CANNY-HOUGH-003 | Confirmé : droite vs extrémités | distinguer droite et segment. | Noyau fini ; 52 mots | Accord fiche et format | Aucune | Passage ciblé |
| CV-CANNY-HOUGH-004 | Diagnostic du projet, cohérent avec les votes | départager texture et structure. | Noyau fini ; 42 mots | Accord fiche et format | Mineur | Attribution explicite |

### Affirmations de la fiche et des cartes

Confirmés : hystérésis après suppression des non-maxima ; paramétrisation normale ; droite infinie versus segment. Corrigibilité améliorée : unité exigée incluse au noyau. La note prudente sur le lissage interne est conservée ; aucun appel OpenCV n’est exécuté. Les contrôles sur la texture et les choix métier sont des raisonnements du projet.

## Corrections appliquées

Fiche révision 2 ; noyau de la carte 002 et passages Source précisés ; objectifs inchangés.

## Enrichissements proposés (en attente d’accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Quantifier une erreur angulaire de Hough | Relier bins, longueur observée et erreur de localisation | Raisonnement ; une carte | 2 calculs simples ; durée à mesurer | Duda–Hart 1972 ; documentation Hough |

## Sources

- [OpenCV 4.13.0, Canny, Non-maximum Suppression et Hysteresis Thresholding](https://docs.opencv.org/4.13.0/da/d22/tutorial_py_canny.html) : étapes et norme L1/L2.
- [OpenCV 4.13.0, Hough, How does it work? et Standard and Probabilistic Hough Line Transform](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html) : paramétrisation, votes et sorties des deux variantes.

## Contrôles et limites

Contrôles de référence : 52 fiches, 224 cartes, 34 tests réussis. Les contrôles après modification et la conservation des identifiants sont consignés dans le [bilan commun](../2026-10-20/00-bilan.md). Context7 indisponible : accès direct aux documentations officielles quand nécessaire.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l’apprenant et validation scientifique indépendante non vérifiés. Les scénarios et recommandations de diagnostic sont des raisonnements du projet, sauf résultat explicitement attribué. Les familles absentes ne justifient pas à elles seules de nouvelles cartes.
