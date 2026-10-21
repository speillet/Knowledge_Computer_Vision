# Revue — SORT — tracking multiobjet par mouvement et association — 2026-10-20

## Synthèse

8 cartes auditées. Deux imprécisions importantes et des renvois périmés corrigés ; mécanismes confirmés.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

8 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 2 importante, 0 mineure, 6 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SORT-001 | Confirmé ; critère clarifié | séparer les responsabilités du tracker. | 105 mots à l’entrée ; Un contresens bloquant désormais précis | Fiche et format contrôlés | important | Corriger critère |
| CV-SORT-002 | Confirmé | interpréter un état et ses unités. | 119 mots à l’entrée ; Objectif unique, noyau fini | Fiche et format contrôlés | — | Conserver |
| CV-SORT-003 | Confirmé | interpréter le poids d'une mesure. | 99 mots à l’entrée ; Objectif unique, noyau fini | Fiche et format contrôlés | — | Conserver |
| CV-SORT-004 | Confirmé ; entrée vide précisée | distinguer mémoire et émission. | 103 mots à l’entrée ; Cas fini sur deux frames | Fiche et format contrôlés | important | Préciser tableau 2D |
| CV-SORT-005 | Confirmé | comprendre le rejet après affectation. | 105 mots à l’entrée ; Objectif unique, noyau fini | Fiche et format contrôlés | — | Conserver |
| CV-SORT-006 | Déduction explicite du projet | établir un diagnostic discriminant. | 106 mots à l’entrée ; Cas et vérifications finis | Fiche et format contrôlés | — | Conserver |
| CV-SORT-007 | Confirmé | distinguer les tâches temporelles. | 100 mots à l’entrée ; Objectif unique, noyau fini | Fiche et format contrôlés | — | Conserver |
| CV-SORT-008 | Déduction explicite du projet | définir une mesure de performance complète. | 106 mots à l’entrée ; Cas et vérifications finis | Fiche et format contrôlés | — | Conserver |

### Affirmations de la fiche et des cartes

- Confirmé : SORT traite les détections image par image, sans apparence ni futur ; état centre/aire/ratio et trois vitesses, transition F à pas unitaire dans le code épinglé.
- Confirmé par lecture du code : max_age=1, min_hits=3, seuil 0,3 ; suppression si âge > maximum, émission seulement après mise à jour et condition de hit_streak/exception de démarrage.
- Confirmé : association par IoU, raccourci pour paires non ambiguës puis affectation et rejet sous seuil. Le contre-exemple matriciel est un calcul construit : 0,90 > 0,62 puis une seule paire retenue.
- Exemple Kalman recalculé avec `examples/pilot_math.py` : 107,352941 px et variance 6,617647 ; R=100 donne 102 px. Ce n'est pas une exécution de SORT.
- Corrigibilité : le critère 001 sur « sortie indépendante » était ambigu ; remplacé par le contresens net du tracker qui ferait lui-même la détection.
- API : la documentation du code exige un tableau vide (0,5), pas une liste Python vide. Correction 004.
- Les diagnostics 006/008 sont des protocoles à exécuter ; aucun résultat vidéo déduit du papier.

## Corrections appliquées

Fiche révisée ; critère de correction 001 et contrat d’entrée vide 004 précisés ; liens vers sujets désormais existants.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Aucune addition prioritaire | Les objectifs existants suffisent au périmètre annoncé | — | Aucun rappel ajouté | Sources ci-dessous |

Familles absentes : conception. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [SORT, §§3.1–3.4 et §4](https://arxiv.org/abs/1602.00763).
- [Code officiel commit 2236dff, convert_bbox_to_z, KalmanBoxTracker, association et Sort.update](https://github.com/abewley/sort/blob/2236dff5019565958b84df7d871d41cc1db58ac7/sort.py), lu via raw.

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
