# Revue — Moindres carrés, SVD et conditionnement — 2026-10-18

## Synthèse

4 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 3 importante, 1 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

Auto-revue : Agent Codex (`revue-cartes`). Le statut éditorial reste `redige`.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SVD-001 | Confirmé : rang et sensibilité ; diagnostic déduit | Diagnostic utile | 42 mots ; noyau identifiable | Source précisée | Important (source) | Référence Ceres |
| CV-SVD-002 | Confirmé à rang colonne plein | Choix de solveur utile | 52 mots ; une justification | Accord fiche | Mineur | Passage Eigen précisé |
| CV-SVD-003 | Imprécis puis corrigé : blanchiment et covariance | Pondération utile | 51 mots avant correction ; un objectif | Accord fiche corrigée | Important | Hypothèse et source corrigées |
| CV-SVD-004 | Diagnostic déduit ; source initiale insuffisante | Robustesse ≠ identifiabilité | 42 mots ; critère fini | Accord homographie | Important (source) | Sources dédiées |

### Affirmations de la fiche et des cartes

Confirmés : objectif quadratique, conditionnement au carré à rang plein, rôle du rang et pondération. Imprécis corrigé : covariance inversible et distinction blanchiment/coût. Les recommandations de couverture spatiale, perturbation et jeu réservé sont des déductions du projet, pas des résultats attribués à Eigen. Régulariser change le problème ; aucune précision expérimentale n’est annoncée.

## Corrections appliquées

Fiche `vault/10-mathematiques-estimation/references/11-moindres-carres-svd.md`, révision 2 ; fichier de cartes homonyme : définition du blanchiment, hypothèse de covariance et références adaptées. IDs inchangés.

## Enrichissements proposés (en attente d’accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Propager une incertitude après résolution | Interpréter une covariance sans confondre observabilité et précision | Raisonnement ; une carte | 3 critères, durée à mesurer | Ceres, Covariance Estimation, Introduction et Gauge Invariance |

## Sources

- [Eigen, Using normal equations](https://libeigen.gitlab.io/eigen/docs-nightly/group__LeastSquares.html), conditionnement au carré ; version affichée 5.0.1-dev+7c7d8473.
- [Ceres, Covariance Estimation, Introduction et Rank of the Jacobian (consulté le 2026-10-18)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html) : pondération, rang et exemple presque singulier.
- [Ceres, Modeling Non-linear Least Squares, Introduction (consulté le 2026-10-18)](https://ceres-solver.readthedocs.io/latest/nnls_modeling.html) : rôle des pertes robustes. Le domaine ceres-solver.org a renvoyé une erreur 502 ; miroir officiel Read the Docs consulté.

## Contrôles et limites

Contrôles de référence : 52 fiches, 224 cartes, 34 tests réussis. Les contrôles après modification et la conservation des identifiants sont consignés dans le [bilan commun](../2026-10-20/00-bilan.md). Context7 indisponible : accès direct aux documentations officielles quand nécessaire.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l’apprenant et validation scientifique indépendante non vérifiés. Les scénarios et recommandations de diagnostic sont des raisonnements du projet, sauf résultat explicitement attribué. Les familles absentes ne justifient pas à elles seules de nouvelles cartes.
