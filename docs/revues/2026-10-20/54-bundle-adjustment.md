# Revue — Bundle adjustment et complément de Schur — 2026-10-20

## Synthèse

4 cartes auditées. 0 bloquant ; 2 importants (conditions algébriques et source de jauge) ; 1 mineur.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

4 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 1 importante, 1 mineure, 2 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-BA-001 | Confirmé : poses/points ; comparaison déduite des inconnues | identifier les inconnues d’un BA. | 54 mots à l’entrée ; un objectif ; détail facultatif distinct | Fiche et format contrôlés | Aucune | Conserver |
| CV-BA-002 | Confirmé : élimination et substitution | expliquer l’élimination de Schur. | 49 mots à l’entrée ; un objectif ; détail facultatif distinct | Fiche et format contrôlés | Aucune | Conserver |
| CV-BA-003 | Confirmé par Gauge Invariance ; source initiale insuffisante | ne pas masquer une jauge. | 55 mots à l’entrée ; un objectif ; détail facultatif distinct | Fiche et format contrôlés | Important | Source dédiée |
| CV-BA-004 | Raisonnement : flexibilité et stabilité | contrôler un modèle trop libre. | 39 mots à l’entrée ; un objectif ; détail facultatif distinct | Fiche et format contrôlés | Mineur | Attribution explicite |

### Affirmations de la fiche et des cartes

Confirmés : structure bipartite et bloc points diagonal, équation réduite et substitution, couplage des caméras après élimination ; robustification des résidus par rho et jauge monoculaire. Hypothèses de covariance et d’inversibilité ajoutées. Le coût d’ajustement peut décroître dans un espace de paramètres élargi ; une dégradation hors échantillon reste un risque conditionnel, pas une certitude.

## Corrections appliquées

Fiche révision 2 ; coût et Schur explicités ; sources 003–004 corrigées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Choisir ordre d’élimination et mesurer le fill-in | Compromis mémoire absent des questions | Pratique | Une carte, trois critères ; durée à mesurer | Ceres, Ordering et Schur solvers |

Familles absentes : algorithme, comparaison, conception, pratique. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [Ceres, DENSE_SCHUR/SPARSE_SCHUR, équations 10–12, consulté le 2026-10-20](https://ceres-solver.readthedocs.io/latest/nnls_solving.html)
- [Ceres, Covariance Estimation, Gauge Invariance, consulté le 2026-10-20](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html)
- [Ceres, LossFunction, motivation et équation du coût, consulté le 2026-10-20](https://ceres-solver.readthedocs.io/latest/nnls_modeling.html)

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
