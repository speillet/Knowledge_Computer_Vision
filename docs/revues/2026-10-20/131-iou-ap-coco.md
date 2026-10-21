# Revue — IoU et AP — protocole COCO de détection — 2026-10-20

## Synthèse

7 cartes auditées. Aucun défaut scientifique nouveau ; une coquille de fiche corrigée.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

7 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 0 mineure, 7 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-IOU-AP-001 | Confirmé | calculer un recouvrement dans le bon contrat. | 98 mots à l’entrée ; Noyau fini, contexte et conventions explicites | Fiche et format contrôlés | — | Conserver |
| CV-IOU-AP-002 | Confirmé | distinguer mesure locale et protocole agrégé. | 124 mots à l’entrée ; Noyau fini, contexte et conventions explicites | Fiche et format contrôlés | — | Conserver |
| CV-IOU-AP-003 | Confirmé | expliquer la pénalité d'un doublon. | 94 mots à l’entrée ; Noyau fini, contexte et conventions explicites | Fiche et format contrôlés | — | Conserver |
| CV-IOU-AP-004 | Confirmé | reconstruire une AP interpolée simple. | 110 mots à l’entrée ; Noyau fini, contexte et conventions explicites | Fiche et format contrôlés | — | Conserver |
| CV-IOU-AP-005 | Confirmé | comparer des évaluateurs avec prudence. | 113 mots à l’entrée ; Noyau fini, contexte et conventions explicites | Fiche et format contrôlés | — | Conserver |
| CV-IOU-AP-006 | Déduction du protocole | diagnostiquer un écart selon l'exigence de localisation. | 103 mots à l’entrée ; Diagnostic fini ; pas de cause affirmée sans preuve | Fiche et format contrôlés | — | Conserver |
| CV-IOU-AP-007 | Déduction du protocole | relier moyenne benchmark et décision métier. | 103 mots à l’entrée ; Diagnostic fini ; pas de cause affirmée sans preuve | Fiche et format contrôlés | — | Conserver |

### Affirmations de la fiche et des cartes

- Confirmé : format officiel bbox [x,y,width,height], coordonnées flottantes ; `maskApi.c` calcule les aires continues sans +1. L'IoU du pilote est sans unité.
- Confirmé par `evaluateImg` : tri des détections par score, GT ordinaire associée au plus une fois, crowd réutilisable, cas ignorés et filtres d'aire distincts.
- Confirmé par `accumulate`/`Params` : enveloppe de précision, 101 rappels, dix seuils IoU ; catégories sans GT valide laissées à −1 puis exclues, catégorie valide sans détection à zéro.
- Divergence réellement constatée : la page officielle dit top-100 toutes classes ; le code épinglé découpe par image/catégorie lorsque useCats=1 avant de tronquer maxDet. La nuance existante est donc conservée.
- Recalcul exécuté : TP/FP/TP donne 0,834983 ; une seule GT détectée sur deux donne 0,504950. La variation de rang est une déduction de l'enveloppe, sans conclusion sur le coût métier d'un FP.
- Les cartes 006/007 sont des protocoles de diagnostic/évaluation proposés, pas des mesures du projet.

## Corrections appliquées

Accord grammatical dans la fiche ; sept cartes conservées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Aucune addition prioritaire | Les objectifs existants suffisent au périmètre annoncé | — | Aucun rappel ajouté | Sources ci-dessous |

Familles absentes : comparaison, conception. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [COCO, page effectivement chargée : detection-eval.htm](https://cocodataset.org/dataset/detection-eval.htm), métriques et point 6.
- [COCO, format-results.htm](https://cocodataset.org/dataset/format-results.htm), Object Detection.
- [cocoeval.py, commit 8c9bcc3, evaluateImg/accumulate/Params](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py), lu via raw.
- [maskApi.c, même commit, bbIou/rleIou](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/common/maskApi.c).

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API. Le code épinglé utilise notamment np.float : il a été lu, pas exécuté avec un environnement NumPy actuel. Aucun fonctionnement logiciel actuel de cet ancien commit n’est revendiqué.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
