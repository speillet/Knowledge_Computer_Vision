---
id: CV-BA
type: methode
domaine: d05
poles: [B, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 2
prerequis: ["CV-SVD", "CV-EPIPOLAIRE", "CV-FACTEURS"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d05]
---
# Bundle adjustment et complément de Schur

## Problème, données et hypothèses

Affiner poses et landmarks par leurs observations image communes. Entrées : associations 2D–3D, paramètres initiaux, intrinsèques et bruit ; sorties : états optimisés et diagnostic de résidus. Une mauvaise association ou jauge ne disparaît pas avec plus d'itérations.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-SVD](../../10-mathematiques-estimation/references/11-moindres-carres-svd.md) ; [CV-EPIPOLAIRE](53-epipolaire-pnp-triangulation.md) ; [CV-FACTEURS](../../10-mathematiques-estimation/references/14-graphes-facteurs.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Linéariser les projections, résoudre un incrément creux, accepter un pas puis réitérer. Les observations relient chacune une caméra et un point ; cette structure permet d'éliminer efficacement les incréments de points avec Schur, puis de les retrouver.

## Mathématiques, conventions et unités

Minimiser $\sum_{ij}\rho(r_{ij}^T\Sigma_{ij}^{-1}r_{ij})$, où $r_{ij}$ est un résidu pixel, $\Sigma_{ij}$ sa covariance définie positive et $\rho$ une perte robuste appliquée à sa norme blanchie au carré. Pour les blocs caméra/points B,E,C et seconds membres v,w, résoudre $(B-EC^{-1}E^T)\delta_c=v-EC^{-1}w$, puis récupérer $\delta_p=C^{-1}(w-E^T\delta_c)$. Cette écriture suppose les blocs de $C$ inversibles ; contraintes et/ou amortissement doivent traiter les directions singulières. Les inverses notées décrivent l'algèbre ; l'implémentation utilise des résolutions adaptées.

## Paramètres et propriétés

Fixer jauge, paramètres intrinsics libres, perte robuste et critères d'arrêt. Des captures pauvres ou paramètres corrélés peuvent rester mal identifiés. La robustification atténue certains grands résidus sans prouver les associations.

## Coût et implémentation

Sparsité, nombre d'observations et ordre d'élimination dominent ; Schur peut générer des interactions entre caméras. Aucun solveur Ceres n'est exécuté ici.

## Évaluation et variation contrôlée

Variation proposée : conserver les observations et libérer progressivement des paramètres intrinsèques. Prédire une possible baisse du coût avec une stabilité moindre ; mesurer sur vues réservées et contrôler les unités.

## Échecs et diagnostic

Coût faible mais échelle incorrecte : vérifier référence métrique et jauge. Caméra qui s'écroule après ajout d'une piste : inspecter l'association et les résidus par observation.

## Alternatives et usages

Pose graph optimise principalement poses/contraintes relatives ; BA conserve les observations des landmarks. Le choix dépend des inconnues et de l'information à garder.

## Sources et cartes

- [Ceres, Covariance Estimation, Gauge Invariance, consulté le 2026-10-20](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html)
- [Ceres, LossFunction, motivation et équation du coût, consulté le 2026-10-20](https://ceres-solver.readthedocs.io/latest/nnls_modeling.html)

- [Ceres, Schur solvers et équations blocs](https://ceres-solver.readthedocs.io/latest/nnls_solving.html).
- [Cartes associées](../54-bundle-adjustment.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
