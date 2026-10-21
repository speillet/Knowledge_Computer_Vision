---
id: CV-SVD
type: methode
domaine: d01
poles: [B, C]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 2
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d01]
---
# Moindres carrés, SVD et conditionnement

## Problème, données et hypothèses

Estimer des paramètres géométriques à partir d'observations bruitées. Entrées : $A\in\mathbb R^{m\times n}$, $b\in\mathbb R^m$ et leur contrat d'unités ; sortie : paramètres et diagnostic de rang. Un modèle linéarisé n'est valable que près de son point de développement. Des outliers nécessitent un traitement robuste distinct du choix du solveur.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Projeter les observations sur l'espace expliqué par le modèle ; résoudre par QR ou SVD, inspecter valeurs singulières et résidus, puis confronter la solution à des observations réservées. La SVD décompose les directions bien ou mal contraintes ; une petite erreur d'ajustement n'atteste pas l'identifiabilité.

## Mathématiques, conventions et unités

On minimise $\|Ax-b\|_2^2$. Si $A=U\Sigma V^T$, les petites valeurs singulières de $\Sigma$ signalent des directions sensibles. À rang colonne plein, $\kappa_2(A^TA)=\kappa_2(A)^2$ : les équations normales amplifient le conditionnement. Pour un résidu $r$ et sa covariance $C$ définie positive, $r^TC^{-1}r$ est sans unité. Blanchir signifie former $L^{-1}r$ avec $C=LL^T$ ; la forme quadratique est sa norme au carré. Une covariance singulière impose de traiter les contraintes ou le sous-espace observable séparément ; mélanger pixels et mètres sans pondération modifie arbitrairement l'objectif.

## Paramètres et propriétés

Centrer/mettre à l'échelle les variables, fixer la tolérance de rang et justifier une régularisation. Rang déficient, mauvais conditionnement et mauvaise adéquation physique sont trois diagnostics différents. Régulariser ajoute une hypothèse ; cela ne crée pas une observation.

## Coût et implémentation

SVD facilite le diagnostic de rang mais peut coûter davantage qu'un QR adapté. Exploiter les matrices creuses en reconstruction. Aucun appel Eigen/Ceres n'est exécuté ici ; éviter de matérialiser une inverse comme recette par défaut.

## Évaluation et variation contrôlée

Cas analytique : deux colonnes presque identiques donnent une direction peu contrainte. Perturber légèrement b en gardant A fixe : prédire une forte variation des paramètres dans cette direction, même si les résidus changent peu. Comparer QR/SVD et stabilité, pas seulement le coût minimal.

## Échecs et diagnostic

Des paramètres énormes avec petit résidu suggèrent ambiguïté, unités ou conditionnement. Inspecter spectre singulier et contraintes physiques ; injecter des mesures indépendantes avant de seulement augmenter le nombre d'itérations.

## Alternatives et usages

QR pour un problème bien posé, SVD pour diagnostic de rang, solveur creux pour grandes reconstructions, estimation robuste contre outliers. Le choix dépend des données et du système linéaire.

## Sources et cartes

- [Ceres, Covariance Estimation, Introduction et Rank of the Jacobian (consulté le 2026-10-18)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html).
- [Ceres, Modeling Non-linear Least Squares, Introduction (consulté le 2026-10-18)](https://ceres-solver.readthedocs.io/latest/nnls_modeling.html).

Ces documentations étayent les solveurs, le blanchiment et le traitement des outliers. Le cas de perturbation et le diagnostic de géométrie sont des raisonnements algébriques du projet ; ils ne constituent pas une expérience publiée.

- [Eigen, Solving linear least squares systems, Using the SVD decomposition / Using normal equations (documentation consultée le 2026-10-18)](https://eigen.tuxfamily.org/dox/group__LeastSquares.html).
- [Cartes associées](../11-moindres-carres-svd.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
