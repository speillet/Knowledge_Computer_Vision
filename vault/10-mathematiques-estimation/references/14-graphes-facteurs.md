---
id: CV-FACTEURS
type: methode
domaine: d01
poles: [B, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 5
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

Un graphe de facteurs est un graphe biparti entre facteurs et variables ; il factorise une fonction, typiquement la densité a posteriori (GTSAM, §1 ; Kaess et al. 2012, §2). Chaque facteur relie les variables nécessaires à une observation ; un solveur linéarise et optimise. GTSAM sépare le graphe des `Values`, qui portent l'estimée initiale du MAP (§§2.3–2.4). Dans un pose graph, le prior sur la première pose est le seul facteur qui rattache le graphe à un repère global (§4.1). GTSAM fournit ces abstractions et iSAM2 une stratégie incrémentale avec rélinéarisation sélective (§7). Il reste à fournir les associations et fermetures de boucle du front-end, les modèles et covariances, l'initialisation et la jauge. Une fausse fermeture de boucle peut déformer tout le graphe.

## Mathématiques, conventions et unités

Pour des facteurs gaussiens conditionnellement indépendants, à covariances fixes définies positives, une forme MAP est $\min_x\sum_k\|r_k(x_k)\|^2_{\Sigma_k^{-1}}$. $x_k$ regroupe les variables du facteur ; le résidu est blanchi par sa covariance. Un prior ou une convention fixe les jauges globales ; un solveur n'invente pas une référence absolue absente des mesures. Dimension de la jauge : 7 pour un BA monoculaire, défini à une similitude près (Ceres, Gauge Invariance ; Zhang et al. 2018, §I), 4 en visuel-inertiel, la position et le lacet n'étant pas observables (Zhang et al. 2018, résumé). Pour un pose graph de mesures relatives en 3D, les 6 degrés d'une transformation rigide commune sont libres, déduction du projet cohérente avec GTSAM §4.1. Zhang et al. comparent trois traitements : fixer les paramètres, ajouter un prior, laisser la jauge libre avec une pseudo-inverse (table I). Ils trouvent précision et temps similaires, la jauge libre étant un peu plus rapide, et des covariances d'aspect très différent mais reliées.

## Paramètres et propriétés

Choisir facteurs, pertes robustes, priors, variables marginalisées et seuils de rélinéarisation. Marginaliser crée des contraintes corrélées ; cela ne signifie pas supprimer sans effet l'information des états passés.

## Coût et implémentation

La sparsité et l'ordre d'élimination changent temps/mémoire. Dans le cas gaussien, l'élimination des variables équivaut à une factorisation QR creuse du jacobien de mesure (Kaess et al. 2012, §2, Gaussian Case). Un mauvais ordre crée du remplissage (fill-in) ; iSAM2 réordonne incrémentalement la partie affectée, avec des résultats proches d'un COLAMD batch (§3.4). Incremental ne veut pas dire coût constant. Aucun appel GTSAM n'est exécuté ; les notions sont conceptuelles et reliées au BA.

Mise à jour d'iSAM2 (Kaess et al. 2012). Un nouveau facteur n'affecte que les chemins entre les cliques de ses variables et la racine (§3.3). L'algorithme 4 retire ces cliques, ajoute les nouveaux facteurs, réordonne, élimine, puis réinsère les sous-arbres orphelins. Les variables relinéarisées entraînent aussi le recalcul de leurs cliques et ancêtres (algorithmes 5–6), même sans nouveau facteur sur elles. La relinéarisation fluide ne relinéarise une variable que si son écart au point de linéarisation dépasse un seuil $\beta$ (§4.1) ; sur Manhattan, $\beta=0{,}1$ donne une solution presque exacte pour un coût nettement réduit. La mise à jour partielle arrête la rétro-substitution dans les sous-arbres dont le changement reste sous un seuil $\alpha$ (§4.2). Une grande boucle affecte une grande partie de l'arbre.

## Évaluation et variation contrôlée

Cas construit : ajouter une contrainte de boucle correcte puis une fausse. Prédire réduction de dérive dans le premier cas et déformation possible dans le second ; inspecter résidus par facteur et référence réservée, pas uniquement convergence du solveur.

## Échecs et diagnostic

Un solveur converge avec une trajectoire absurde : contrôler repères, information des priors, associations et facteurs incohérents ; une tolérance plus stricte n'est pas un diagnostic.

Fausses fermetures de boucle. Le perceptual aliasing rend irréaliste un front-end sans faux positifs (Agarwal et al. 2013, §II). Test heuristique du projet : suivre le résidu pondéré $\chi^2_l$ du facteur de boucle. Après optimisation sur les mêmes mesures, sa distribution dépend de l’ajustement et des corrélations ; un quantile $\chi^2$ de dimension 6 ne fournit pas automatiquement un taux de faux rejet calibré. Pour diagnostiquer, regarder la hausse des résidus d'odométrie voisins, puis réoptimiser sans ce facteur. Back-ends robustes :

- perte robuste sur les boucles (CV-SVD-008) ;
- contraintes commutables de Sünderhauf et Protzel : une variable $s_{ij}\in[0,1]$ par boucle, avec un prior qui la rappelle vers 1 ;
- DCS, qui en donne la valeur en forme close, $s=\min(1, 2\Phi/(\Phi+\chi^2_l))$, et met à l'échelle l'information de la boucle par $s^2$ sans variable supplémentaire (§IV, équation 15) ;
- RRR, qui rejette les boucles hors du plus grand ensemble cohérent au lieu de les garder avec un faible poids (§II).

## Alternatives et usages

Pose graph pour contraintes entre poses, BA pour poses et landmarks observés ; filtre pour état courant. Comparer mémoire, réestimation et latence.

## Sources et cartes

- [Ceres, Covariance Estimation, Gauge Invariance (consulté le 2026-10-18)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html#gauge-invariance).

- [Dellaert, Factor Graphs and GTSAM, §§1, 2.3–2.4, 4.1 et 7 (consulté le 2026-10-23)](https://gtsam.org/tutorials/intro.html) : définition biparti, `Values`, prior de première pose, iSAM et arbre de Bayes. La page ne dit pas explicitement que le MAP gaussien est un moindres carrés : cette équivalence est sourcée par Kaess et al.
- [Kaess et al. 2012, iSAM2, §2 Gaussian Case, §3.4 et §§4.1–4.2](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf) : moindres carrés non linéaires, élimination par QR creuse, ordre incrémental, relinéarisation fluide et mises à jour partielles.
- [Zhang, Gallego et Scaramuzza 2018, On the Comparison of Gauge Freedom Handling in Optimization-based Visual-Inertial State Estimation, RA-L](https://rpg.ifi.uzh.ch/docs/RAL18_Zhang.pdf) : prépublication des auteurs ; résumé, §I et table I.
- [Agarwal, Tipaldi, Spinello, Stachniss et Burgard 2013, Robust Map Optimization using Dynamic Covariance Scaling, ICRA](https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/agarwal13icra.pdf) : §II travaux liés dont RRR, §III contraintes commutables, §IV équation 15. L'article de Sünderhauf et Protzel 2012 n'a pas été lu directement.
- [Cartes associées](../14-graphes-facteurs.md) : CV-FACTEURS-001 à 005.

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet. Révisions 3 et 4 : auto-revue `revue-cartes` par Agent Claude Code le 2026-10-23, corrections puis enrichissements acceptés par l'apprenant, sans validation indépendante.
