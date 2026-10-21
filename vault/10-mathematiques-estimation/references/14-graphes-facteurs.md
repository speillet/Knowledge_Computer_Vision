---
id: CV-FACTEURS
type: methode
domaine: d01
poles: [B, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 2
prerequis: ["CV-SVD", "CV-SE3"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d01]
---
# Graphes de facteurs et optimisation incrémentale

## Problème, données et hypothèses

Représenter poses, vitesses, biais et observations comme un problème d'inférence. Entrées : états, facteurs, covariance et initialisation ; sortie : estimation conjointe. Un graphe de facteurs décrit une factorisation, pas à lui seul un optimiseur.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-SVD](11-moindres-carres-svd.md) ; [CV-SE3](12-rotations-se3.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Chaque facteur relie les variables nécessaires à une observation ; un solveur linéarise et optimise. GTSAM fournit ces abstractions et iSAM2 une stratégie incrémentale avec rélinéarisation sélective. Une fausse fermeture de boucle peut déformer tout le graphe.

## Mathématiques, conventions et unités

Pour des facteurs gaussiens conditionnellement indépendants, à covariances fixes définies positives, une forme MAP est $\min_x\sum_k\|r_k(x_k)\|^2_{\Sigma_k^{-1}}$. $x_k$ regroupe les variables du facteur ; le résidu est blanchi par sa covariance. Un prior ou une convention fixe les jauges globales ; un solveur n'invente pas une référence absolue absente des mesures.

## Paramètres et propriétés

Choisir facteurs, pertes robustes, priors, variables marginalisées et seuils de rélinéarisation. Marginaliser crée des contraintes corrélées ; cela ne signifie pas supprimer sans effet l'information des états passés.

## Coût et implémentation

La sparsité et l'ordre d'élimination changent temps/mémoire. Incremental ne veut pas dire coût constant. Aucun appel GTSAM n'est exécuté ; les notions sont conceptuelles et reliées au BA.

## Évaluation et variation contrôlée

Cas construit : ajouter une contrainte de boucle correcte puis une fausse. Prédire réduction de dérive dans le premier cas et déformation possible dans le second ; inspecter résidus par facteur et référence réservée, pas uniquement convergence du solveur.

## Échecs et diagnostic

Un solveur converge avec une trajectoire absurde : contrôler repères, information des priors, associations et facteurs incohérents ; une tolérance plus stricte n'est pas un diagnostic.

## Alternatives et usages

Pose graph pour contraintes entre poses, BA pour poses et landmarks observés ; filtre pour état courant. Comparer mémoire, réestimation et latence.

## Sources et cartes

- [Ceres, Covariance Estimation, Gauge Invariance (consulté le 2026-10-18)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html#gauge-invariance).

- [Dellaert, Factor Graphs and GTSAM, §§2.3–2.4, 4.1 et 7 (consulté le 2026-10-18)](https://gtsam.org/tutorials/intro.html).
- [Kaess et al. 2012, iSAM2, §2 Gaussian Case et §4](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf).
- [Cartes associées](../14-graphes-facteurs.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
