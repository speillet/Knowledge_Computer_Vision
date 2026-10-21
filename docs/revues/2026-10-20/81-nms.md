# Revue — NMS — supprimer des détections redondantes — 2026-10-20

## Synthèse

5 cartes auditées. Aucun défaut nouveau dans le périmètre des cinq cartes ; les distinctions de conventions déjà présentes sont confirmées.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

5 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 0 mineure, 5 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-NMS-001 | Confirmé | dérouler hard NMS. | 100 mots à l’entrée ; Noyau fini, question autonome | Fiche et format contrôlés | — | Conserver |
| CV-NMS-002 | Confirmé | distinguer trois seuils. | 117 mots à l’entrée ; Noyau fini, question autonome | Fiche et format contrôlés | — | Conserver |
| CV-NMS-003 | Confirmé | choisir le périmètre d'une suppression. | 101 mots à l’entrée ; Noyau fini, question autonome | Fiche et format contrôlés | — | Conserver |
| CV-NMS-004 | Confirmé | expliquer l'effet de Soft-NMS. | 125 mots à l’entrée ; Noyau fini, question autonome | Fiche et format contrôlés | — | Conserver |
| CV-NMS-005 | Confirmé | localiser la cause d'une disparition. | 110 mots à l’entrée ; Noyau fini, question autonome | Fiche et format contrôlés | — | Conserver |

### Affirmations de la fiche et des cartes

- Confirmé : suppression strictement au-dessus du seuil dans Torchvision et le code original ; le papier présente aussi la convention ≥. Le départage par indice est une décision du pilote, pas une promesse CPU/GPU.
- Confirmé : la pénalité gaussienne porte sur toutes les candidates ; nouveau maximum recherché et élimination sous seuil dans le code original.
- Confirmé par calcul exécuté : IoU 2/3, sorties A,C à 0,5 et A,B,C à 0,7 (`examples/pilot_math.py`).
- Confirmé : `batched_nms` ne supprime pas entre catégories ; le choix métier et le diagnostic 005 sont des raisonnements du projet.
- Complexités : déduction pour le pseudocode naïf ; aucun benchmark de l'API annoncé. Les rôles NMS/évaluation sont distincts, également vérifiés avec COCO dans la revue 131.

## Corrections appliquées

Aucune correction nécessaire.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Aucune addition prioritaire | Les objectifs existants suffisent au périmètre annoncé | — | Aucun rappel ajouté | Sources ci-dessous |

Familles absentes : conception, evaluation, pratique. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [Soft-NMS, §4 équations et §5 seuil de score](https://arxiv.org/abs/1704.04503).
- [Code original b8e69bd, boucle du maximum, pénalités et seuil](https://github.com/bharatsingh430/soft-nms/blob/b8e69bdf8df2ad53025c9d198ded909b50471d4f/lib/nms/cpu_nms.pyx).
- [Torchvision nms, convention et égalités](https://docs.pytorch.org/vision/stable/generated/torchvision.ops.nms.html) ; [batched_nms](https://docs.pytorch.org/vision/stable/generated/torchvision.ops.batched_nms.html), consultés le 20 octobre 2026.
- [DETR, résumé et §3.1](https://arxiv.org/abs/2005.12872).

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
