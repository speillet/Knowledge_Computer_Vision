# Revue — Détection 3D, pose d’objet et pose articulée — 2026-10-20

## Synthèse

4 cartes auditées. Deux manques de sources importants corrigés, sans changer les objectifs.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

4 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 2 importante, 2 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-POSE3D-001 | Confirmé avec source ajoutée | nommer la sortie de pose. | 40 mots à l’entrée ; Distinction finie | Fiche et format contrôlés | important | Ajouter OpenPose |
| CV-POSE3D-002 | Raisonnement du projet explicité | contrôler une boîte 3D. | 43 mots à l’entrée ; Critères finis ; cas non exécuté | Fiche et format contrôlés | mineur | Préciser attribution |
| CV-POSE3D-003 | Confirmé après précision de source | distinguer nuScenes et COCO. | 50 mots à l’entrée ; Noyau fini, objectif conservé | Fiche et format contrôlés | mineur | Cibler la source |
| CV-POSE3D-004 | Confirmé avec source ajoutée | respecter les symétries de pose. | 55 mots à l’entrée ; Ambiguïté conditionnée par observations | Fiche et format contrôlés | important | Ajouter BOP |

### Affirmations de la fiche et des cartes

- Confirmé : PointPillars produit une pseudo-image de piliers ; CenterPoint détecte centres et propriétés 3D (résumé).
- Non soutenue initialement par les sources de détection seules, la partie pose articulée est étayée par OpenPose, fig. 2 ; les métriques BOP étayent les symétries et l'ambiguïté visible.
- Confirmé : nuScenes utilise la distance 2D au sol, avec seuils 0,5/1/2/4 m pour AP ; NDS pondère mAP et cinq erreurs. Les cartes n'assimilent pas ce protocole à COCO.
- La rotation d'un cylindre est ambiguë seulement si les observations ne brisent pas sa symétrie ; cette condition est déjà présente dans la réponse. Les contrôles d'axes/unités sont un diagnostic construit.

## Corrections appliquées

Bibliographie de la fiche complétée et sources des quatre cartes ciblées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Aucune addition prioritaire | Les objectifs existants suffisent au périmètre annoncé | — | Aucun rappel ajouté | Sources ci-dessous |

Familles absentes : algorithme, comprehension, conception, raisonnement. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [PointPillars, architecture §2.1](https://arxiv.org/abs/1812.05784), également contrôlé dans la revue 64.
- [CenterPoint, résumé](https://arxiv.org/abs/2006.11275).
- [OpenPose, résumé et fig. 2](https://arxiv.org/abs/1611.08050).
- [BOP, tâches et métriques](https://bop.felk.cvut.cz/tasks/), consulté le 20 octobre 2026.
- [nuScenes, fichier officiel lu via sa version raw, Metrics](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md), consulté le 20 octobre 2026.

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
