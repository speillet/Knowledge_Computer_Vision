# Revue — Tracking monoobjet : corrélation, siamois et MeanShift — 2026-10-20

## Synthèse

2 cartes auditées. Une justification importante corrigée : SiamFC n’actualise pas le template du cas 002.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

2 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 1 importante, 1 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SOT-001 | Confirmé ; source précisée | distinguer SOT et MOT. | 49 mots à l’entrée ; Objectif conservé | Fiche et format contrôlés | mineur | Cibler source |
| CV-SOT-002 | Non soutenu par SiamFC ; corrigé | comprendre une dérive de template. | 47 mots à l’entrée ; Cas conditionnel, objectif de dérive conservé | Fiche et format contrôlés | important | Citer KCF et préciser portée |

### Affirmations de la fiche et des cartes

- Confirmé : MeanShift déplace une fenêtre vers un mode de distribution, avec histogramme rétroprojeté dans le tutoriel ; CamShift adapte la fenêtre. Il ne s'agit pas d'un MOT automatique.
- Confirmé : SiamFC compare cible initiale et recherche avec un réseau siamois ; il dit explicitement ne pas actualiser le modèle d'apparence. Il ne pouvait donc pas servir d'exemple de dérive due à cette mise à jour.
- Correction : la fiche distingue les variantes adaptatives de SiamFC. KCF décrit entraînement à la nouvelle position et interpolation du modèle ; la contamination par un distracteur est une déduction du projet sur ce mécanisme.
- La région de recherche limite le déplacement capturable dans ces pipelines locaux ; la fiche n'annonce pas une limite universelle pour tout tracker.
- Les politiques de gel, perte et réinitialisation sont des propositions à tester.

## Corrections appliquées

Fiche révisée pour borner la mise à jour aux variantes concernées ; KCF ajouté et sources des cartes corrigées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Aucune addition prioritaire | Les objectifs existants suffisent au périmètre annoncé | — | Aucun rappel ajouté | Sources ci-dessous |

Familles absentes : algorithme, comprehension, conception, evaluation, pratique, raisonnement. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [OpenCV 4.13.0, Meanshift/Camshift, introduction et boucle du template](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html).
- [SiamFC, introduction et §4 : template fixe](https://arxiv.org/abs/1606.09549).
- [KCF, pipeline de tracking et interpolation du modèle](https://arxiv.org/abs/1404.7584).
- [SORT, §3](https://arxiv.org/abs/1602.00763).

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
