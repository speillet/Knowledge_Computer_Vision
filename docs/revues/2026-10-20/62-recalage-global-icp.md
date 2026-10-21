# Revue — Recalage global et ICP local — 2026-10-20

## Synthèse

5 cartes auditées. 0 bloquant, 0 important ; 1 mineur partagé (version des sources).
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

5 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 0 mineure, 5 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ICP-001 | Confirmé : init globale puis convergence locale | séparer initialisation globale et raffinement. | 53 mots à l’entrée ; étapes cohérentes | Fiche et format contrôlés | Aucune | Conserver |
| CV-ICP-002 | Confirmé : projection sur normale ; plan déduit | interpréter un résidu point-to-plane. | 47 mots à l’entrée ; scalaire et unité | Fiche et format contrôlés | Aucune | Conserver |
| CV-ICP-003 | Confirmé pour paires retenues ; diagnostic déduit | refuser un petit consensus trompeur. | 43 mots à l’entrée ; mesures complémentaires | Fiche et format contrôlés | Aucune | Conserver |
| CV-ICP-004 | Confirmé par conversion d’unités | garder les unités du recalage. | 41 mots à l’entrée ; noyau correct ; 0,02 m=20 mm | Fiche et format contrôlés | Aucune | Conserver |
| CV-ICP-005 | Dépendance aux normales confirmée ; observabilité déduite | choisir une variante ICP. | 49 mots à l’entrée ; comparaison conditionnelle | Fiche et format contrôlés | Aucune | Conserver |

### Affirmations de la fiche et des cartes

Équations point-to-point/plane concordantes après échange de noms source/cible ; signe du résidu sans effet sur son carré. Les mouvements tangents d’un plan ne sont pas contraints par sa normale. FPFH 33D, seuil de distance et initialisation corroborés. Le cas 1D de curriculum_math est un calcul d’associations, pas un ICP exécuté. Aucun gain universel ni benchmark revendiqué.

## Corrections appliquées

Fiche révision 2 ; labels des sources datés par version.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Distinguer coût point-to-plane et inlier_rmse rapporté | Une métrique de sortie peut différer de l’objectif optimisé | Évaluation | Une carte, deux critères ; durée à mesurer | Open3D RegistrationResult et code au tag v0.19.0 |

Familles absentes : comprehension, conception, evaluation. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [Open3D 0.19.0, ICP registration, Input, Point-to-point et Point-to-plane](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html)
- [Open3D 0.19.0, Global registration, Extract geometric feature et RANSAC](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html)

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
