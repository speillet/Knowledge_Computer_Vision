# Revue — Cartes pilotes — SIFT — 2026-10-18

## Synthèse

7 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 1 mineure, 6 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

Auto-revue : Agent Codex (`revue-cartes`). Le statut éditorial reste `redige`.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SIFT-001 | Confirmé : extraction distincte de géométrie | situer les composants d'un pipeline de correspondances. | Noyau fini ; 103 mots | Accord fiche et format | Aucune | Conserver |
| CV-SIFT-002 | Confirmé : DoG et 26 voisins | expliquer la recherche d'une échelle caractéristique. | Noyau fini ; 120 mots | Accord fiche et format | Aucune | Conserver |
| CV-SIFT-003 | Confirmé : orientation, 128, normalisations | justifier la construction du descripteur. | Noyau fini ; 105 mots | Accord fiche et format | Aucune | Conserver |
| CV-SIFT-004 | Confirmé ; ratios recalculés | interpréter le ratio test. | Noyau fini ; 101 mots | Accord fiche et format | Aucune | Conserver |
| CV-SIFT-005 | Confirmé : limites aux vues obliques | distinguer les limites des invariances. | Noyau fini ; 106 mots | Accord fiche et format | Aucune | Conserver |
| CV-SIFT-006 | Scénario explicitement construit ; cohérent | diagnostiquer un consensus trompeur. | Noyau fini ; 105 mots | Accord fiche et format | Aucune | Conserver |
| CV-SIFT-007 | Protocole du projet ; références précisées | construire une comparaison sous contrainte. | Noyau fini ; 102 mots | Accord fiche et format | Mineur | Sources d’évaluation ciblées |

### Affirmations de la fiche et des cartes

Confirmés : DoG avec facteur d’échelle constant, 26 voisins, orientation et description, normalisation photométrique limitée, ratio et vue oblique. Calculs : 20/21≈0,95238 et 35/80=0,4375. Les cas de façade et le protocole industriel sont des raisonnements explicitement proposés. Complexité exhaustive déduite du nombre de comparaisons. Code inspecté face à la documentation, non exécuté.

## Corrections appliquées

Fiche révision 3 : une expérience future n’est plus nommée référence analytique. Carte 007 : sources précises. Les autres cartes sont conservées.

## Enrichissements proposés (en attente d’accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Expliquer le rejet d’une réponse DoG sur une arête | Une étape centrale de localisation encore non interrogée | Raisonnement ; une carte | 2 critères ; durée à mesurer | Lowe §4.1, Eliminating edge responses |

## Sources

- [Lowe 2004](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf), §§3–4, 5–6, 7.1 et 8 : PDF téléchargé, passages lus.
- [Rublee et al. 2011, copie universitaire](https://sites.cc.gatech.edu/classes/AY2024/cs4475_summer/images/ORB_an_efficient_alternative_to_SIFT_or_SURF.pdf), §§4.4, 5.3 et 6.1.
- [OpenCV 4.13, matching](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html), Brute-Force Matching with SIFT Descriptors and Ratio Test.

## Contrôles et limites

Contrôles de référence : 52 fiches, 224 cartes, 34 tests réussis. Les contrôles après modification et la conservation des identifiants sont consignés dans le [bilan commun](../2026-10-20/00-bilan.md). Context7 indisponible : accès direct aux documentations officielles quand nécessaire.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l’apprenant et validation scientifique indépendante non vérifiés. Les scénarios et recommandations de diagnostic sont des raisonnements du projet, sauf résultat explicitement attribué. Les familles absentes ne justifient pas à elles seules de nouvelles cartes.

Les réponses sont plus développées que dans les nouveaux sujets : conserver les détails facultatifs distincts du noyau et mesurer la charge en rappel réel.
