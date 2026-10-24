# SO(3), SE(3) et conventions de transformation — cartes

Fiche : [[10-mathematiques-estimation/references/12-rotations-se3|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::10-mathematiques-estimation

## CV-SE3-001

Objectif : composer avec des repères nommés. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-SE3-001
Question: Un SLAM fournit pour deux images les poses $T_{wc_1}$ et $T_{wc_2}$, qui envoient les coordonnées caméra vers le monde : $p_w=T_{wc_i}\,p_{c_i}$. Quelle transformation exprime dans la caméra 1 un point connu dans la caméra 2 ?
Reponse: **Noyau attendu** : $T_{c_1c_2}=T_{wc_1}^{-1}T_{wc_2}=T_{c_1w}T_{wc_2}$ : remonter de $c_2$ vers le monde, puis du monde vers $c_1$. Les indices adjacents doivent coïncider ($c_1w$ puis $wc_2$) ; la composition n'est pas commutative.

**Approfondissement** : avec $T_{ab}=(R_{ab},t_{ab})$, $T_{ab}T_{bc}=(R_{ab}R_{bc},\;t_{ab}+R_{ab}t_{bc})$ : la translation $t_{bc}$, exprimée dans $b$, est tournée dans $a$ avant l'addition. Contrôle : $T_{c_1c_2}$ appliquée à l'origine de $c_2$ doit donner la position de la caméra 2 vue de la caméra 1. Si les poses fournies vont du monde vers la caméra, comme `rvec`/`tvec` d'OpenCV, les inverses changent de place : $T_{c_1c_2}=T_{c_1w}T_{c_2w}^{-1}$.

**Exemple construit** : avec deux orientations identiques et des centres décalés sur un axe monde, le point origine de la seconde caméra doit apparaître à ce même décalage dans la première. Faire ensuite tourner seulement la première caméra oblige à exprimer ce décalage dans ses axes. Ce test simple révèle une translation additionnée dans le mauvais repère, qu'une multiplication de matrices apparemment valide peut laisser passer.

**Erreurs bloquantes** : calculer $T_{wc_2}T_{wc_1}^{-1}$ ou $T_{wc_1}T_{wc_2}$ ; supposer la composition commutative.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Fiche complète]] ; [Solà et al., A micro Lie theory, annexe D-A, équations 170–171](https://arxiv.org/html/1812.01537v9#A4.SS1).
Tags: cv::pilote cv::d01 famille::raisonnement cv_id::CV-SE3-001 provenance::agent pole::B pole::C
END

## CV-SE3-002

Objectif : inverser une pose rigide. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-SE3-002
Question: Pour $p_c=Rp_w+t$, comment retrouver le centre caméra dans le repère monde ?
Reponse: **Noyau attendu** : $C_w=-R^Tt$ ; la pose inverse est $(R^T,-R^Tt)$.

**Approfondissement** : Le centre caméra a coordonnées nulles dans son propre repère. La translation t n’est donc pas directement sa position monde.

**Dérivation étape par étape** : le centre optique est le point qui a coordonnées $p_c=0$ dans le repère caméra. En le remplaçant dans $p_c=Rp_w+t$, on obtient $RC_w+t=0$, donc $C_w=-R^{-1}t=-R^Tt$ pour une rotation orthonormale. L'inverse de pose utilise la même rotation inverse et cette translation réexprimée dans le monde.

**Exemple interprété** : si $R=I$ et $t=(1,0,0)^T$ m, le centre caméra est $(-1,0,0)^T$ m dans le monde. Le signe opposé vient du sens monde→caméra annoncé. Si la caméra est tournée, changer seulement le signe sans appliquer $R^T$ donne une position dans les mauvais axes. Vérifier numériquement que le centre trouvé se projette à l'origine caméra avant toute division perspective. Cette convention est fondamentale pour composer calibration, PnP et trajectoire ; une translation extrinsèque n'est pas une position universelle indépendante du sens de transformation.

**Erreurs bloquantes** : Répondre simplement t ou −t sans rotation.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Fiche complète]] ; [Solà et al., A micro Lie theory, annexe D-A, équations 170–171](https://arxiv.org/html/1812.01537v9#A4.SS1).
Tags: cv::pilote cv::d01 famille::pratique cv_id::CV-SE3-002 provenance::agent pole::B pole::C
END

## CV-SE3-003

Objectif : distinguer perturbations locale et globale. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-SE3-003
Question: Deux implémentations du même coût paramètrent l'incrément de rotation par un petit vecteur $\delta\theta$ et obtiennent des jacobiennes différentes, chacune validée par différences finies. Quelle différence de convention l'explique, comment passer de l'une à l'autre et laquelle choisir ?
Reponse: **Noyau attendu** : l'une perturbe à droite, $R\operatorname{Exp}(\delta\theta_L)$, avec un incrément exprimé dans le repère local ; l'autre à gauche, $\operatorname{Exp}(\delta\theta_G)R$, avec un incrément dans le repère global. L'adjoint les relie : $\operatorname{Exp}(R\,\delta\theta_L)\,R=R\operatorname{Exp}(\delta\theta_L)$, soit $\delta\theta_G=R\,\delta\theta_L$ ; jacobiennes et covariances se transforment par $R$, par exemple $J_L=J_GR$. Choisir le côté où l'incertitude est naturellement exprimée, repère capteur ou repère monde, et l'annoncer.

**Approfondissement** : pour SO(3), $\mathrm{Ad}_R=R$ ; pour SE(3), l'adjoint mélange rotation et translation. Solà adopte par défaut la perturbation locale. Une covariance de gyroscope s'exprime naturellement dans le repère du capteur, une erreur de cap fournie par un GNSS dans le repère monde : ces exemples relèvent du raisonnement du projet.

**Contrôle proposé** : appliquer un même petit déplacement physique aux deux paramétrisations et comparer le point transformé, pas seulement les composantes des incréments. Si les jacobiennes ont été validées dans leurs conventions respectives, leur différence peut être attendue. Toute covariance associée doit suivre le même changement de coordonnées.

**Erreurs bloquantes** : copier une jacobienne sans vérifier où agit la perturbation ; croire qu'une des deux conventions est fausse.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Fiche complète]] ; [Solà et al., A micro Lie theory, §II-E, équations 25–28, et §II-F, équations 29–32](https://arxiv.org/html/1812.01537v9#S2.SS5) ; [annexe B-C, équation 139](https://arxiv.org/html/1812.01537v9).
Tags: cv::pilote cv::d01 famille::comparaison cv_id::CV-SE3-003 provenance::agent pole::B pole::C
END

## CV-SE3-004

Objectif : contrôler un quaternion. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-SE3-004
Question: Une extrinsèque caméra–IMU passe d'une bibliothèque à une autre sous forme de quaternion unitaire et de translation ; la reprojection devient fausse alors que la norme du quaternion vaut bien 1. Quelles conventions vérifier, et quel test les départage ?
Reponse: **Noyau attendu** : vérifier l'ordre des composantes (scalaire en premier ou en dernier), l'algèbre de multiplication (Hamilton ou JPL), le sens de la transformation (capteur vers référence ou l'inverse) et les axes des repères. La norme unité ne contraint que la représentation. Test : transformer un point ou un axe connu par les deux chaînes et comparer les résultats, plutôt que les quatre nombres.

**Approfondissement** : Solà distingue quatre choix binaires : ordre, algèbre, fonction active ou passive, sens local→global ou l'inverse. Exemples : le constructeur `Quaternion(w,x,y,z)` d'Eigen prend le scalaire en premier mais stocke `[x,y,z,w]` ; `Rotation.from_quat` de SciPy suppose par défaut le scalaire en dernier. $q$ et $-q$ représentent la même rotation : comparer des rotations, pas des composantes.

**Test construit** : choisir une rotation simple de quart de tour et un axe de référence, puis comparer les coordonnées résultantes dans les deux bibliothèques. Ajouter ensuite une translation non nulle afin de tester aussi son repère et son unité. Une rotation identité seule laisse plusieurs erreurs d'ordre ou de sens invisibles ; elle est donc un contrôle insuffisant de l'interface.

**Erreurs bloquantes** : assimiler quatre nombres de norme un à une convention universelle ; conclure à deux rotations différentes parce que $q$ et $-q$ diffèrent.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Fiche complète]] ; [Solà, Quaternion kinematics, §3.1, équations 140–143 et table 2](https://arxiv.org/abs/1711.02508) ; [Eigen 5.0.1-dev, Quaternion, constructeur (consulté le 2026-10-23)](https://libeigen.gitlab.io/eigen/docs-nightly/classEigen_1_1Quaternion.html) ; [SciPy 1.18.0, Rotation.from_quat (consulté le 2026-10-23)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_quat.html).
Tags: cv::pilote cv::d01 famille::diagnostic cv_id::CV-SE3-004 provenance::agent pole::B pole::C
END

## CV-SE3-005

Objectif : mesurer un écart de rotation. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-SE3-005
Question: Pour évaluer une orientation estimée $\hat R$ contre une vérité terrain $R$, un rapport compare les angles d'Euler composante par composante, un autre les quaternions. Quelle mesure utiliser à la place, et pourquoi ces deux comparaisons peuvent-elles tromper ?
Reponse: **Noyau attendu** : mesurer l'angle de la rotation résiduelle $R^T\hat R$ : $\theta=\arccos\frac{\operatorname{tr}(R^T\hat R)-1}{2}$, indépendant de la paramétrisation. Les angles d'Euler dépendent de la convention et sont singuliers : près d'un tangage de 90°, de grands écarts de lacet et de roulis se compensent. $q$ et $-q$ représentent la même rotation : leurs composantes peuvent différer de 2 pour une erreur nulle ; depuis des quaternions unitaires, utiliser $\theta=2\arccos|\langle q_1,q_2\rangle|$.

**Approfondissement** : cas calculé par le projet : les rotations ZYX $(30°;89{,}9°;0°)$ et $(0°;89{,}9°;-30°)$ diffèrent de 30° sur deux angles d'Euler, mais leur angle géodésique vaut 0,05°. Borner l'argument de l'arccos dans $[-1,1]$ contre les arrondis. REP 103 déconseille les angles d'Euler, qui admettent 24 conventions « valides ». Ne pas moyenner des angles d'Euler pour agréger des erreurs.

**Lecture du score** : l'erreur angulaire mesure la rotation relative nécessaire pour aligner les orientations, pas leur distance à une origine d'angles particulière. Garder radians et degrés explicites dans le calcul et le rapport, puis examiner la distribution des erreurs au lieu d'une seule moyenne.

**Erreurs bloquantes** : rapporter des écarts d'angles d'Euler comme erreur de rotation ; conclure à une erreur parce que $q$ et $-q$ diffèrent.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Fiche complète]] ; [Solà et al., A micro Lie theory, annexe B, double couverture et Log de SO(3), équation 135](https://arxiv.org/html/1812.01537v9) ; [REP 103, Rotation Representation, commit 6fbda48](https://github.com/ros-infrastructure/rep/blob/6fbda48350825b28aec74609b29c7ee18c8e619a/rep-0103.rst) ; calcul et formule par quaternion dérivés par le projet.
Tags: cv::pilote cv::d01 famille::evaluation cv_id::CV-SE3-005 provenance::agent pole::B pole::C
END

## CV-SE3-006

Objectif : convertir entre conventions d'axes caméra. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-SE3-006
Question: Une pose caméra estimée avec OpenCV est transmise à un moteur de rendu OpenGL et à un nœud ROS ; dans le rendu, la scène apparaît retournée ou derrière la caméra. Quelles conventions d'axes comparer, et quelle transformation relie OpenCV et OpenGL ?
Reponse: **Noyau attendu** : OpenCV place $x$ à droite, $y$ vers le bas et $z$ vers l'avant, les points visibles ayant $Z_c>0$ ; en OpenGL, la caméra vise $-z$ avec $y$ vers le haut ; ROS place le corps en $x$ avant, $y$ gauche, $z$ haut, et son repère `_optical` suit la convention d'OpenCV. Passer d'OpenCV à OpenGL revient à tourner de 180° autour de $x$ : $M=\mathrm{diag}(1,-1,-1)$, de déterminant $+1$. Pour composer des poses homogènes $4\times4$, utiliser $M_h=\mathrm{diag}(1,-1,-1,1)$ : à droite d’une pose caméra→monde, $T^{gl}_{wc}=T^{cv}_{wc}M_h$, ou à gauche d’une matrice monde→caméra, $T^{gl}_{cw}=M_hT^{cv}_{cw}$. Vérifier qu'un point connu devant la caméra le reste dans chaque convention.

**Approfondissement** : chez OpenCV, $x'=X_c/Z_c$, puis $v=f_yy'+c_y$ avec des lignes de pixels qui croissent vers le bas : pour $f_y>0$, $Y_c$ pointe vers le bas. `gluLookAt` envoie le point visé sur l'axe $-z$ et la direction « haut » sur $+y$. Confondre repère corps et repère `_optical` dans ROS fait viser la caméra vers le haut ou sur le côté. Inverser un seul axe donne un déterminant $-1$ : c'est une réflexion, pas un changement de repère rigide.

**Erreurs bloquantes** : inverser un seul axe ; appliquer la conversion du mauvais côté de la pose ; supposer que toutes les bibliothèques partagent les axes d'OpenCV.
Source: [[10-mathematiques-estimation/references/12-rotations-se3|Fiche complète]] ; [OpenCV 4.13.0, `calib3d.hpp`, modèle sténopé, l. 94–118](https://github.com/opencv/opencv/blob/4.13.0/modules/calib3d/include/opencv2/calib3d.hpp#L94-L118) ; [Khronos, gluLookAt, Description](https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml) ; [REP 103, Axis Orientation et Suffix Frames, commit 6fbda48](https://github.com/ros-infrastructure/rep/blob/6fbda48350825b28aec74609b29c7ee18c8e619a/rep-0103.rst) ; diagnostic et côté de composition déduits par le projet.
Tags: cv::pilote cv::d01 famille::diagnostic cv_id::CV-SE3-006 provenance::agent pole::B pole::C
END
