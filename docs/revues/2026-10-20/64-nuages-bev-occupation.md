# Revue — Nuages, BEV et représentations d’occupation — 2026-10-20

## Synthèse

5 cartes auditées. 0 bloquant ; 1 important (sources manquantes dans la fiche et 003) ; 1 mineur partagé.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

5 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 1 importante, 4 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-BEV-001 | Confirmé : colonne verticale et pseudo-image | distinguer voxel pilier et BEV. | 51 mots à l’entrée ; une comparaison spatiale | Fiche et format contrôlés | Mineur | Source ciblée |
| CV-BEV-002 | Confirmé : inconnu distinct du libre | préserver l’inconnu. | 47 mots à l’entrée ; un contrat de visibilité | Fiche et format contrôlés | Mineur | Source ciblée |
| CV-BEV-003 | Confirmé : classification implicite et SDF distinctes | séparer les sens d’occupation. | 52 mots à l’entrée ; deux objets mathématiques | Fiche et format contrôlés | Important | Source ciblée |
| CV-BEV-004 | Déduit de compensation ego et acquisition temporelle | vérifier une fusion BEV. | 46 mots à l’entrée ; diagnostic discriminant | Fiche et format contrôlés | Mineur | Source ciblée |
| CV-BEV-005 | Cas construit ; distinction visibilité/sécurité correcte | concevoir une perception d’entrepôt. | 83 mots à l’entrée ; carte de conception, charge à mesurer | Fiche et format contrôlés | Mineur | Source ciblée |

### Affirmations de la fiche et des cartes

Confirmés : PointPillars encode sans bins de hauteur, BEVFormer aligne les features historiques et traite les vues ; OctoMap encode l’inconnu ; Occupancy Networks prédit un score d’intérieur/extérieur, DeepSDF une distance signée. Les résumés primaires suffisent aux mentions de PointNet++, LSS et BEVFusion, sans auditer leurs architectures complètes. Aucune garantie de collision ni sécurité n’est tirée des scores.

## Corrections appliquées

Fiche révision 2 ; références ajoutées ; sources des cartes ciblées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Quantifier mémoire d’une grille et taille de cellule | Choix résolution/portée sous budget | Raisonnement | Une carte, un calcul ; durée à mesurer | PointPillars §7.1 ; comptage de cellules du projet |

Familles absentes : algorithme, evaluation, pratique, raisonnement. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [Lang et al., PointPillars, §2.1](https://arxiv.org/abs/1812.05784) : HTML §2.1.
- [Li et al., BEVFormer, §§3.3–3.4](https://arxiv.org/abs/2203.17270) : HTML §3.4, alignement ego.
- [OctoMap, Full 3D model, consulté le 2026-10-20](https://octomap.github.io/)
- [Mescheder et al., Occupancy Networks, §3.1](https://arxiv.org/abs/1812.03828) : équations 1–2.
- [Park et al., DeepSDF, §3](https://arxiv.org/abs/1901.05103) : zéro et signe au §3.
- [Qi et al., PointNet++, résumé](https://arxiv.org/abs/1706.02413)
- [Philion–Fidler, Lift-Splat-Shoot, résumé](https://arxiv.org/abs/2008.05711)
- [Liu et al., BEVFusion, résumé (version v3)](https://arxiv.org/abs/2205.13542)

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API. Pages CVF indisponibles via le lecteur web ; textes arXiv des mêmes articles consultés.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
