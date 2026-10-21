# Revue — Détection : Faster R-CNN, familles YOLO et DETR — 2026-10-20

## Synthèse

5 cartes auditées. Un manque important de justification de la diversité YOLO corrigé ; sources des autres cartes précisées.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

5 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 1 importante, 4 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-DETECTEURS-001 | Confirmé après précision de source | situer le partage de features. | 50 mots à l’entrée ; Noyau fini, objectif conservé | Fiche et format contrôlés | mineur | Cibler la source |
| CV-DETECTEURS-002 | Confirmé avec sources complémentaires | ne pas généraliser toute la famille YOLO. | 40 mots à l’entrée ; Objectif unique | Fiche et format contrôlés | important | Ajouter preuves de variantes |
| CV-DETECTEURS-003 | Confirmé après précision de source | distinguer les trois affectations. | 57 mots à l’entrée ; Noyau fini, objectif conservé | Fiche et format contrôlés | mineur | Cibler la source |
| CV-DETECTEURS-004 | Raisonnement du projet explicité | analyser les petits objets après resize. | 82 mots à l’entrée ; Critères finis ; cas non exécuté | Fiche et format contrôlés | mineur | Préciser attribution |
| CV-DETECTEURS-005 | Raisonnement du projet explicité | comparer des pipelines de détection. | 48 mots à l’entrée ; Critères finis ; cas non exécuté | Fiche et format contrôlés | mineur | Préciser attribution |

### Affirmations de la fiche et des cartes

- Confirmé : RPN et tête de détection partagent les convolutions de l'image (Faster R-CNN §3).
- La diversité YOLO était non soutenue par le seul article original : YOLOv3 §2.1 décrit ses anchors ; YOLOX §2.1 décrit explicitement le passage anchor-free, la tête et SimOTA. Sources ajoutées, sans étendre le programme des cartes.
- Confirmé : DETR §3.1 affecte par matching biparti les prédictions à un ensemble de cibles complété par no-object ; supervision et NMS ont des fonctions distinctes.
- Les contrôles de resize, le choix d'un split et les conditions de chronométrage sont des propositions de protocole, pas des résultats empiriques de ces articles.

## Corrections appliquées

Fiche révisée puis sources des cinq cartes ciblées ; réponses et IDs conservés.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Aucune addition prioritaire | Les objectifs existants suffisent au périmètre annoncé | — | Aucun rappel ajouté | Sources ci-dessous |

Familles absentes : conception, pratique, raisonnement. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [Faster R-CNN, §3 et introduction](https://arxiv.org/abs/1506.01497).
- [DETR, §3.1, fig. 1 et équations 1–2](https://arxiv.org/abs/2005.12872).
- [YOLOv3, §2.1](https://arxiv.org/abs/1804.02767) ; [YOLOX, §2.1, paragraphes Anchor-free/Decoupled head](https://arxiv.org/abs/2107.08430).

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
