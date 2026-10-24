# Bundle adjustment et complément de Schur — cartes

Fiche : [[50-calibration-geometrie/references/54-bundle-adjustment|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::50-calibration-geometrie

## CV-BA-001

Objectif : identifier les inconnues d’un BA. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-BA-001
Question: Qu’optimise un bundle adjustment et pourquoi le distinguer d’un pose graph ?
Reponse: **Noyau attendu** : Le BA optimise poses et points, éventuellement intrinsics, à partir de reprojections ; un pose graph repose sur des contraintes entre poses.

**Approfondissement** : Le niveau d’information et la sparsité diffèrent. Une reprojection faible peut encore cacher une jauge ou un biais.

**Mécanisme** : chaque observation image lie une caméra et un landmark par un modèle de projection. Modifier un point influence ses observations dans plusieurs vues ; modifier une caméra influence les points qu'elle observe. Le BA recherche conjointement des valeurs qui expliquent ces observations, avec pondération et éventuellement robustification.

**Exemple construit** : une dérive de trajectoire et des positions de points erronées peuvent se compenser partiellement dans une vue, mais être incompatibles dans les autres. L'optimisation conjointe exploite ces liens. Un pose graph utilise déjà des contraintes résumées entre poses et ne conserve pas nécessairement chaque reprojection. Les coûts, les biais possibles et la structure des inconnues diffèrent donc. Vérifier jauge, initialisation, associations et résidus par observation : une diminution du coût global ne prouve ni l'échelle métrique ni la validité physique de tous les landmarks optimisés.

**Erreurs bloquantes** : Présenter BA comme un simple lissage des positions caméra.
Source: [[50-calibration-geometrie/references/54-bundle-adjustment|Fiche complète]] ; [Ceres, Schur solvers et équations blocs](https://ceres-solver.readthedocs.io/latest/nnls_solving.html).
Tags: cv::pilote cv::d05 famille::comprehension cv_id::CV-BA-001 provenance::agent pole::B pole::C
END

## CV-BA-002

Objectif : expliquer l’élimination de Schur. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-BA-002
Question: Éliminer les points avec Schur signifie-t-il les ignorer dans le BA ?
Reponse: **Noyau attendu** : Non : leur effet est transmis au système réduit des caméras, puis leurs incréments sont récupérés par substitution.

**Approfondissement** : La structure des observations rend le bloc points exploitable ; cela ne supprime ni non-linéarité ni minima locaux.

**Lecture du système en blocs** : les incréments caméra et points sont couplés. Résoudre algébriquement le bloc des points puis le remplacer dans les équations caméra donne le complément de Schur. Le système réduit conserve l'effet des points sur les caméras ; après résolution, une substitution récupère les incréments de points.

**Conséquence de sparsité** : plusieurs caméras qui voient un même landmark peuvent devenir couplées dans le système réduit. Le coût dépend donc des connexions et pas seulement du nombre total de points. Dans un exemple construit, deux jeux de même taille mais de visibilité différente peuvent présenter des coûts mémoire différents. Les inverses figurant dans la dérivation désignent des opérations algébriques ; une implémentation emploie des factorisations ou résolutions adaptées. L'élimination concerne le problème linéarisé courant et ne supprime ni le besoin de relinéariser ni la dépendance à l'initialisation.

**Erreurs bloquantes** : Dire que Schur retire les observations 3D du problème.
Source: [[50-calibration-geometrie/references/54-bundle-adjustment|Fiche complète]] ; [Ceres, Schur solvers et équations blocs](https://ceres-solver.readthedocs.io/latest/nnls_solving.html).
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-BA-002 provenance::agent pole::B pole::C
END

## CV-BA-003

Objectif : ne pas masquer une jauge. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-BA-003
Question: Un BA converge à plusieurs échelles avec le même coût sur une reconstruction monoculaire. Quel contrôle manque ?
Reponse: **Noyau attendu** : Vérifier la jauge d’échelle et la présence d’une référence métrique ; fixer une convention n’est pas mesurer cette échelle.

**Approfondissement** : Évaluer les paramètres avec un alignement autorisé par la tâche ; un coût pixel peut rester invariant à une transformation globale.

**Exemple d'invariance** : si toutes les positions des caméras et des points sont multipliées par un même facteur, les directions de projection d'une reconstruction monoculaire peuvent rester identiques. L'image ne fournit donc pas automatiquement la longueur correspondant à une unité du modèle. La convergence à des échelles différentes est compatible avec cette jauge.

**Validation proposée** : identifier la contrainte qui fournit réellement l'échelle, si le produit en a besoin, et vérifier son unité. Pour comparer des reconstructions, autoriser uniquement l'alignement justifié par la tâche. Une similitude peut être appropriée pour une reconstruction monoculaire à échelle libre, mais masquer un défaut d'échelle dans un système censé être métrique. Fixer un point ou une baseline pour rendre le calcul unique est une convention tant que sa valeur ne provient pas d'une mesure. La précision métrique exige donc une référence indépendante.

**Erreurs bloquantes** : Attribuer automatiquement la multiplicité à une panne du solveur.
Source: [[50-calibration-geometrie/references/54-bundle-adjustment|Fiche complète]] ; [Ceres, Covariance Estimation, Gauge Invariance, consulté le 2026-10-20](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html).
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-BA-003 provenance::agent pole::B pole::C
END

## CV-BA-004

Objectif : contrôler un modèle trop libre. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-BA-004
Question: Pourquoi libérer davantage de coefficients de caméra peut-il réduire le coût tout en dégradant la calibration ?
Reponse: **Noyau attendu** : Des paramètres supplémentaires peuvent surajuster un jeu peu informatif ou être corrélés.

**Approfondissement** : Mesurer stabilité par sous-ensembles et erreur sur observations indépendantes ; choisir les contraintes du modèle physiquement.

**Pourquoi le coût baisse** : un espace de paramètres plus grand peut contenir une solution qui ajuste davantage les observations d'entraînement. Cela ne dit pas si les paramètres supplémentaires représentent la caméra ou absorbent bruit, déformation de mire et erreurs de correspondance. Plusieurs paramètres peuvent aussi produire des effets proches sur une capture peu informative.

**Ablation construite** : conserver les observations et libérer un groupe de paramètres à la fois. Examiner leur dispersion par sous-ensembles, les corrélations et les résidus sur des vues réservées couvrant notamment les bords. Un meilleur coût d'ajustement accompagné d'une dégradation hors échantillon suggère un compromis défavorable. À l'inverse, un modèle trop contraint peut conserver un biais réel. Le choix doit s'appuyer sur l'optique, la diversité des données et l'usage, sans faire de la seule baisse du coût un critère de calibration.

**Erreurs bloquantes** : Comparer uniquement les coûts d’ajustement.
Source: [[50-calibration-geometrie/references/54-bundle-adjustment|Fiche complète]] ; [Ceres, Covariance Estimation, Gauge Invariance, consulté le 2026-10-20](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html) ; effet de paramètres libres et protocole de validation : déductions du projet.
Tags: cv::pilote cv::d05 famille::evaluation cv_id::CV-BA-004 provenance::agent pole::B pole::C
END
