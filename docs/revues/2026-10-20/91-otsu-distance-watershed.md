# Revue — Otsu, distance transform et watershed — 2026-10-20

## Synthèse

5 cartes auditées. Aucun défaut nécessitant correction dans les cinq cartes. Les diagnostics restent des cas construits.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

5 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 0 mineure, 5 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-WATERSHED-001 | Raisonnement explicite du projet | interpréter l’objectif Otsu. | 55 mots à l’entrée ; Vérifications finies, sans promesse de résultat | Fiche et format contrôlés | — | Conserver |
| CV-WATERSHED-002 | Confirmé | reconstruire le pipeline à marqueurs. | 46 mots à l’entrée ; Noyau fini et autonome | Fiche et format contrôlés | — | Conserver |
| CV-WATERSHED-003 | Confirmé | distinguer fond et inconnu. | 48 mots à l’entrée ; Noyau fini et autonome | Fiche et format contrôlés | — | Conserver |
| CV-WATERSHED-004 | Raisonnement explicite du projet | localiser une sous-segmentation. | 58 mots à l’entrée ; Vérifications finies, sans promesse de résultat | Fiche et format contrôlés | — | Conserver |
| CV-WATERSHED-005 | Raisonnement explicite du projet | choisir une métrique d’instances classique. | 48 mots à l’entrée ; Vérifications finies, sans promesse de résultat | Fiche et format contrôlés | — | Conserver |

### Affirmations de la fiche et des cartes

- Confirmé : minimisation de la variance intra-classe pondérée dans OpenCV, équivalence à la variance inter-classe par décomposition de la variance totale.
- Confirmé : `distanceTransform` mesure la distance au pixel nul le plus proche ; la métrique et le masque importent. Un maximum ne constitue pas une classe sémantique.
- Confirmé : marqueurs int32 de même taille, labels positifs, 0 inconnu, frontières −1 et modification du tableau ; le tutoriel distingue explicitement fond connu et inconnu.
- Diagnostics et protocole d'instances : déductions du projet. Une union de deux objets peut garder le même masque binaire après fusion, donc l'IoU binaire ne teste pas le comptage.
- L'exemple Otsu du dépôt est un calcul d'histogramme ; aucune exécution OpenCV ou validation sur image revendiquée.

## Corrections appliquées

Aucune correction nécessaire.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Aucune addition prioritaire | Les objectifs existants suffisent au périmètre annoncé | — | Aucun rappel ajouté | Sources ci-dessous |

Familles absentes : comparaison, comprehension, conception. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [OpenCV 4.13.0, Otsu’s Binarization et How does… work](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html).
- [OpenCV 4.13.0, watershed, Theory et Code : distance et marqueurs](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html).

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
