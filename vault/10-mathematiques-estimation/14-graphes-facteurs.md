# Graphes de facteurs et optimisation incrémentale — cartes

Fiche : [[10-mathematiques-estimation/references/14-graphes-facteurs|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::10-mathematiques-estimation

## CV-FACTEURS-001

Objectif : séparer représentation et solveur. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-FACTEURS-001
Question: Un graphe de facteurs est souvent présenté comme « le SLAM » d'un système. Que représente-t-il exactement, et que reste-t-il à fournir ou à choisir pour obtenir une trajectoire ?
Reponse: **Noyau attendu** : c'est un graphe biparti entre variables (poses, amers, biais) et facteurs (mesures, priors) qui factorise la densité a posteriori. Avec des modèles de mesure gaussiens, le MAP devient un moindres carrés non linéaire sur des résidus pondérés par leur covariance (distance de Mahalanobis). Il reste à fournir les associations et fermetures de boucle venues du front-end, les modèles de mesure et leurs covariances, une estimée initiale et un ancrage de la jauge. Il faut aussi choisir l'inférence : optimisation batch, iSAM2, pertes robustes.

**Approfondissement** : GTSAM sépare le graphe des `Values` qui portent l'estimée initiale. La structure du graphe fixe la sparsité : dans le cas gaussien, éliminer les variables équivaut à une factorisation QR creuse du jacobien, dont le coût dépend de l'ordre d'élimination. Un graphe bien construit ne rend pas correct un facteur faux.

**Erreurs bloquantes** : déduire une trajectoire fiable de la seule présence d'un graphe ; confondre représentation et solveur.
Source: [[10-mathematiques-estimation/references/14-graphes-facteurs|Fiche complète]] ; [Dellaert, Factor Graphs and GTSAM, §§1, 2.3–2.4, 4.1 et 7 (consulté le 2026-10-23)](https://gtsam.org/tutorials/intro.html) ; [Kaess et al. 2012, iSAM2, §2, Gaussian Case](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf).
Tags: cv::pilote cv::d01 famille::comprehension cv_id::CV-FACTEURS-001 provenance::agent pole::B pole::C
END

## CV-FACTEURS-002

Objectif : expliquer une jauge. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-FACTEURS-002
Question: Pourquoi une optimisation de poses relatives peut-elle exiger un ancrage malgré des observations nombreuses ?
Reponse: **Noyau attendu** : Les observations relatives ne définissent pas nécessairement le repère global ; des transformations communes peuvent laisser les résidus inchangés.

**Approfondissement** : fixer une jauge enlève une ambiguïté de représentation, sans ajouter une mesure absolue. Le nombre de degrés libres dépend des capteurs : 6 pour un pose graph de mesures relatives en 3D, 7 pour un BA monoculaire, défini à une similitude près, 4 en visuel-inertiel, où la gravité rend roulis et tangage observables mais pas la position ni le lacet. Trois traitements existent : fixer ces paramètres, leur ajouter un prior ou laisser la jauge libre. Zhang et al. obtiennent précision et temps similaires, et des covariances d'aspect très différent mais reliées.

**Erreurs bloquantes** : Interpréter un prior arbitraire comme une preuve de précision globale.
Source: [[10-mathematiques-estimation/references/14-graphes-facteurs|Fiche complète]] ; [Ceres, Covariance Estimation, Gauge Invariance (consulté le 2026-10-23)](https://ceres-solver.readthedocs.io/latest/nnls_covariance.html#gauge-invariance) ; [Zhang, Gallego et Scaramuzza 2018, RA-L, résumé, §I et table I](https://rpg.ifi.uzh.ch/docs/RAL18_Zhang.pdf) ; 6 degrés du pose graph déduits par le projet.
Tags: cv::pilote cv::d01 famille::raisonnement cv_id::CV-FACTEURS-002 provenance::agent pole::B pole::C
END

## CV-FACTEURS-003

Objectif : vérifier une fermeture de boucle. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-FACTEURS-003
Question: Après loop closure, le coût diminue mais la carte se plie de façon incohérente. Que tester ?
Reponse: **Noyau attendu** : Vérifier l’association de lieux, la transformation relative, les repères et le poids du facteur de boucle.

**Approfondissement** : une fausse contrainte forte peut être satisfaite au détriment du reste. Test chiffré : après optimisation, comparer le résidu blanchi au carré $\chi^2_l$ du facteur de boucle à un quantile du $\chi^2$ de sa dimension, 6 pour une pose relative 3D, et regarder la hausse des résidus d'odométrie voisins. Après ajustement sur les mêmes mesures, ce seuil est une heuristique : le résidu dépend de l’estimée et des corrélations, sa covariance n’est pas simplement celle de la mesure. Une loi $\chi^2_6$ calibrée exige un modèle de résidu approprié ; ne pas lui attribuer automatiquement un taux de faux rejet. Réoptimiser sans ce facteur départage : si la carte se redresse, la boucle est suspecte. Conserver vérification géométrique et observations indépendantes ; un back-end robuste est traité en CV-FACTEURS-004.

**Erreurs bloquantes** : Augmenter les itérations sans inspecter le facteur ajouté.
Source: [[10-mathematiques-estimation/references/14-graphes-facteurs|Fiche complète]] ; [Dellaert, Factor Graphs and GTSAM, §§2.3–2.4, 4.1 et 7 (consulté le 2026-10-23)](https://gtsam.org/tutorials/intro.html) ; [Agarwal et al. 2013, DCS, §III, équation 1](https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/agarwal13icra.pdf) ; scénario de faux facteur et tests proposés par le projet.
Tags: cv::pilote cv::d01 famille::diagnostic cv_id::CV-FACTEURS-003 provenance::agent pole::B pole::C
END

## CV-FACTEURS-004

Objectif : choisir un back-end robuste aux fausses boucles. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-FACTEURS-004
Question: Un front-end de reconnaissance de lieux produit inévitablement quelques fausses fermetures de boucle, par exemple dans des couloirs identiques. Quelles stratégies de back-end comparer pour qu'elles ne plient pas la carte, et selon quels critères choisir ?
Reponse: **Noyau attendu** : une perte robuste sur les facteurs de boucle réduit le poids des grands résidus ; c'est simple, mais sensible à l'initialisation et à l'échelle choisie. Les contraintes commutables ajoutent une variable $s_{ij}\in[0,1]$ par boucle, optimisée avec la carte et rappelée vers 1 par un prior : elles désactivent les boucles incohérentes, au prix de variables en plus et d'une convergence plus lente. DCS calcule ce poids en forme close, $s=\min\left(1,\frac{2\Phi}{\Phi+\chi^2_l}\right)$, d'après l'erreur courante $\chi^2_l$ de la boucle : même idée, sans variable ajoutée et avec une convergence plus rapide. Choisir selon le taux de fausses boucles attendu, le budget de calcul et le besoin d'une décision explicite.

**Approfondissement** : DCS met à l'échelle la matrice d'information de chaque boucle par $s^2$ ; $\Phi$ règle la tolérance. Ces méthodes gardent une boucle rejetée avec un faible poids ; RRR cherche au contraire le plus grand ensemble de boucles mutuellement cohérentes et rejette les autres. Raisonnement du projet : aucune ne compense un front-end dont les fausses boucles sont nombreuses et cohérentes entre elles.

**Erreurs bloquantes** : croire qu'un back-end robuste rend inutile la vérification géométrique du front-end ; réduire DCS à un seuil binaire.
Source: [[10-mathematiques-estimation/references/14-graphes-facteurs|Fiche complète]] ; [Agarwal et al. 2013, Robust Map Optimization using Dynamic Covariance Scaling, résumé, §§II–IV, équations 2 et 15](https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/agarwal13icra.pdf) ; contraintes commutables de Sünderhauf et Protzel 2012 lues à travers leur présentation par Agarwal et al.
Tags: cv::pilote cv::d01 famille::comparaison cv_id::CV-FACTEURS-004 provenance::agent pole::B pole::C
END

## CV-FACTEURS-005

Objectif : expliquer la mise à jour incrémentale d'iSAM2. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-FACTEURS-005
Question: À l'arrivée de nouvelles mesures, qu'est-ce qu'iSAM2 recalcule réellement dans son arbre de Bayes, et quels deux seuils limitent la relinéarisation et la mise à jour des estimées ?
Reponse: **Noyau attendu** : seules les cliques situées sur les chemins entre les variables touchées par les nouveaux facteurs ou sélectionnées pour relinéarisation et la racine sont retirées, réordonnées et re-éliminées avec ces facteurs ; les sous-arbres non affectés sont réinsérés tels quels. Relinéarisation fluide : une variable n'est relinéarisée que si son estimée s'écarte de son point de linéarisation de plus d'un seuil $\beta$. Mise à jour partielle : la rétro-substitution s'arrête dans les sous-arbres où les changements restent sous un seuil $\alpha$.

**Approfondissement** : l'ordre des variables de la partie affectée est recalculé à chaque mise à jour, avec une qualité proche d'un COLAMD batch, pour limiter le remplissage. Une grande fermeture de boucle affecte une grande partie de l'arbre : incrémental ne veut pas dire coût constant. Sur Manhattan, $\beta=0{,}1$ donne une solution presque exacte pour un coût nettement réduit ; les seuils échangent précision et calcul.

**Erreurs bloquantes** : croire qu'iSAM2 ne relinéarise jamais ou refait tout à chaque pas ; promettre un coût constant par mesure.
Source: [[10-mathematiques-estimation/references/14-graphes-facteurs|Fiche complète]] ; [Kaess et al. 2012, iSAM2, §3.3, algorithme 4, §3.4 et §§4.1–4.2](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf).
Tags: cv::pilote cv::d01 famille::algorithme cv_id::CV-FACTEURS-005 provenance::agent pole::B pole::C
END
