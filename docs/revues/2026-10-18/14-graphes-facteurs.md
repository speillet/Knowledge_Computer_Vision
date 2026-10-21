# Revue — Graphes de facteurs et optimisation incrémentale — 2026-10-18

## Synthèse

3 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 3 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

Auto-revue : Agent Codex (`revue-cartes`). Le statut éditorial reste `redige`.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FACTEURS-001 | Confirmé : graphe ≠ solution | séparer représentation et solveur. | Noyau fini ; 48 mots | Accord fiche et format | Mineur | Passages ciblés |
| CV-FACTEURS-002 | Confirmé : ambiguïté globale | expliquer une jauge. | Noyau fini ; 52 mots | Accord fiche et format | Mineur | Source sur la jauge |
| CV-FACTEURS-003 | Diagnostic déduit du rôle des facteurs | vérifier une fermeture de boucle. | Noyau fini ; 47 mots | Accord fiche et format | Mineur | Cas distingué des résultats publiés |

### Affirmations de la fiche et des cartes

Confirmés : factorisation distincte du solveur ; version incrémentale avec rélinéarisation sélective ; coût dépendant de sparsité et ordre ; jauge sans référence absolue. Imprécis corrigé : objectif MAP quadratique sous hypothèses gaussiennes et covariances fixes. Une fausse loop closure et les contrôles proposés sont un scénario du projet.

## Corrections appliquées

Fiche révision 2 : hypothèses de la formulation et sources. Les cartes gardent leur noyau ; sources mieux ciblées.

## Enrichissements proposés (en attente d’accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Expliquer ce que conserve une marginalisation | Éviter de supprimer l’information avec les anciens états | Raisonnement ; une carte | 3 critères ; durée à mesurer | Kaess et al., §3, Bayes tree |

## Sources

- [Dellaert, Factor Graphs and GTSAM, §§2.3–2.4, 4.1 et 7 (consulté le 2026-10-18)](https://gtsam.org/tutorials/intro.html).
- [Kaess et al. 2012, iSAM2, §2 Gaussian Case et §4](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf) : PDF téléchargé directement et texte extrait, après échec du lecteur web ; §2 distingue le cas gaussien, §4 décrit rélinéarisation et réordonnancement.
- [Ceres, Covariance Estimation, Gauge Invariance (consulté le 2026-10-18)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html#gauge-invariance).

## Contrôles et limites

Contrôles de référence : 52 fiches, 224 cartes, 34 tests réussis. Les contrôles après modification et la conservation des identifiants sont consignés dans le [bilan commun](../2026-10-20/00-bilan.md). Context7 indisponible : accès direct aux documentations officielles quand nécessaire.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l’apprenant et validation scientifique indépendante non vérifiés. Les scénarios et recommandations de diagnostic sont des raisonnements du projet, sauf résultat explicitement attribué. Les familles absentes ne justifient pas à elles seules de nouvelles cartes.
