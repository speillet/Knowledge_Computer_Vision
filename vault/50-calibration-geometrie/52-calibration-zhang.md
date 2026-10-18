# Cartes pilotes — calibration de Zhang

Fiche : [[50-calibration-geometrie/references/52-calibration-zhang|Calibration]]. Provenance : agent.

TARGET DECK: CV::Pilote::50-calibration-geometrie

## CV-ZHANG-001

Objectif : distinguer trois objectifs géométriques. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-ZHANG-001
Question: Quelle différence sépare calibration caméra, estimation de pose et recalage de deux images ?
Reponse: **Noyau attendu** : la calibration estime des paramètres de formation de l'image, notamment intrinsèques et distorsion ; la pose décrit une transformation de repères ; le recalage aligne des observations selon un modèle choisi.

**Approfondissement** : une procédure de calibration de Zhang estime aussi une pose de mire par vue, mais cela ne rend pas les objectifs équivalents. PnP peut estimer une pose avec une caméra déjà calibrée ; une homographie peut recaler un plan sans retrouver tous les intrinsèques. La calibration des scores d'un réseau est encore un autre problème.

**Erreurs bloquantes** : assimiler ces trois sorties ou croire qu'une homographie est toujours une calibration complète.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|Fiche calibration]] ; [Zhang, §§2–3](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf).
Tags: cv::pilote cv::d05 famille::comprehension cv_id::CV-ZHANG-001 provenance::agent pole::B pole::C pole::E
END

## CV-ZHANG-002

Objectif : interpréter les conventions de projection. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-ZHANG-002
Question: Dans $X_c=RX_w+t$ et $s\tilde x=K[R\mid t]\tilde X_w$, que représentent les repères, les unités et les paramètres de $K$ ?
Reponse: **Noyau attendu** : $R$ transforme le repère monde/mire vers caméra ; $t$ est exprimé dans le repère caméra et dans l'unité des points monde. $K$ transforme les coordonnées caméra normalisées en pixels :
$$K=\begin{bmatrix}f_x&\gamma&c_x\\0&f_y&c_y\\0&0&1\end{bmatrix}.$$
Les focales et le point principal sont en pixels ; $s$ est un facteur homogène.

**Approfondissement** : $\gamma$ est le skew, souvent fixé à zéro selon le modèle. La distorsion n'est pas incluse dans cette multiplication projective idéale. Une taille de carré en millimètres donne des translations dans cette unité, sans changer les dimensions pixel des intrinsèques.

**Erreurs bloquantes** : inverser le sens de $R$ sans transformer la formule, confondre mètres et pixels ou inclure toute distorsion dans $K$ seul.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|Fiche calibration]] ; [Zhang, §2.2](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf).
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-ZHANG-002 provenance::agent pole::B pole::C pole::E
END

## CV-ZHANG-003

Objectif : expliquer les contraintes multi-vues. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-ZHANG-003
Question: Comment des homographies d'une mire plane contraignent-elles les intrinsèques dans la méthode de Zhang, et pourquoi varier seulement la translation est-il insuffisant ?
Reponse: **Noyau attendu** : $H\sim K[r_1\ r_2\ t]$. Avec $B=K^{-T}K^{-1}$, les colonnes $h_1,h_2$ donnent $h_1^TBh_2=0$ et $h_1^TBh_1=h_2^TBh_2$. Ces contraintes reposent sur les axes orthogonaux de rotation ; des orientations répétées ne fournissent pas la diversité nécessaire.

**Approfondissement** : chaque vue apporte deux contraintes. Trois vues indépendantes sont nécessaires en général pour cinq intrinsèques libres ; deux peuvent suffire avec skew nul imposé. Les minima algébriques ne garantissent pas une calibration précise sur des images bruitées ; la capture doit aussi couvrir la zone utile.

**Erreurs bloquantes** : dire que deux photos quelconques suffisent toujours ou que de simples translations rendent tous les intrinsèques observables.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|Fiche calibration]] ; [Zhang, §§3.1 et 4](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf).
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-ZHANG-003 provenance::agent pole::B pole::C pole::E
END

## CV-ZHANG-004

Objectif : interpréter un RMS sans conclusion abusive. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-ZHANG-004
Question: Une calibration affiche un faible RMS de reprojection. Que mesure-t-il et quelle validation supplémentaire proposer pour une mesure dimensionnelle industrielle ?
Reponse: **Noyau attendu** : le RMS mesure l'ajustement des projections aux coins observés, dans une convention et une unité données, généralement pixels. Il ne prouve ni l'absence de biais ni la précision métrique. Valider sur captures réservées et une mesure indépendante adaptée à l'usage.

**Approfondissement** : consigner si la moyenne porte sur points ou coordonnées, analyser les résidus par vue et position. Proposition du projet : fixer intrinsèques/distorsion, estimer une pose avec une partie des coins réservés et tester les autres, puis vérifier une dimension connue. Ne pas choisir un seuil universel sans tolérance métier.

**Erreurs bloquantes** : conclure à une précision en millimètres à partir du seul RMS pixel d'ajustement.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|Fiche calibration]] ; [Zhang, §3.2](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf) ; [OpenCV calibrateCamera](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::evaluation cv_id::CV-ZHANG-004 provenance::agent pole::B pole::C pole::E
END

## CV-ZHANG-005

Objectif : propager une transformation pixel. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-ZHANG-005
Question: Une image calibrée est redimensionnée par un facteur uniforme $a$, puis recadrée de $(b_x,b_y)$ pixels dans ce nouveau repère. Comment adapter les intrinsèques sans changement physique de l'optique ?
Reponse: **Noyau attendu** : multiplier focales et skew par $a$ et transformer le point principal en $(ac_x-b_x,ac_y-b_y)$. Plus généralement, $K'=AK$ avec $A$ la transformation pixel appliquée à l'image.

**Approfondissement** : $A$ a ici diagonale $(a,a,1)$ et translation $(-b_x,-b_y)$. Cette dérivation suppose exactement le resize/crop décrit et un modèle optique inchangé ; vérifier la convention des centres de pixels de l'outil. Une distorsion exprimée en coordonnées caméra normalisées n'est pas multipliée comme une focale pixel. Focus/zoom modifiés nécessitent un autre diagnostic.

**Erreurs bloquantes** : garder $K$ identique après crop ou multiplier indistinctement tous les coefficients de distorsion par $a$.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|Fiche calibration]] ; [OpenCV, camera model](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::pratique cv_id::CV-ZHANG-005 provenance::agent pole::B pole::C pole::E
END

## CV-ZHANG-006

Objectif : diagnostiquer l'observabilité. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-ZHANG-006
Question: Vingt vues presque frontales donnent un faible RMS, mais les intrinsèques changent fortement quand on retire quelques vues. Que vérifier et quelle nouvelle acquisition est informative ?
Reponse: **Noyau attendu** : suspecter une capture peu informative et un modèle mal contraint, tout en vérifiant coins et paramètres libres. Ajouter des orientations diverses et une couverture spatiale utile ; la quantité de vues presque identiques ne remplace pas leur diversité.

**Approfondissement** : comparer stabilité par sous-ensembles, cartes de résidus et validation réservée ; vérifier planéité, netteté et modèle de distorsion. Ne pas conclure automatiquement que l'optimiseur est défectueux. Fixer un paramètre n'est justifié que par le modèle et le besoin, pas pour obtenir un plus joli score.

**Erreurs bloquantes** : déclarer la calibration bonne uniquement parce que vingt images ont été utilisées ou que le RMS est faible.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|Fiche calibration]] ; [Zhang, §4](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf).
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-ZHANG-006 provenance::agent pole::B pole::C pole::E
END

## CV-ZHANG-007

Objectif : construire une collecte et une validation cohérentes. Famille : conception. Provenance : agent.

START
CV-Pilote
ID: CV-ZHANG-007
Question: Pour contrôler des dimensions de pièces avec une caméra fixe, quelles décisions rendent une calibration sur mire exploitable au-delà d'une démonstration ?
Reponse: **Noyau attendu** : définir tolérance métier, résolution/focus stables, modèle optique et unités ; capturer une mire plane connue sous orientations et positions informatives ; vérifier les coins ; conserver des observations et une référence métrique indépendantes pour valider.

**Approfondissement** : consigner versions, flags, captures exclues et résidus ; tester la zone et les distances d'exploitation. Séparer calibration intrinsèque et pose de la caméra dans la cellule. Prévoir une nouvelle validation après modification de l'optique ou du montage. Ce scénario décrit un protocole proposé, sans essai terrain réalisé.

**Erreurs bloquantes** : réutiliser aveuglément les paramètres après changement de focus, ou ignorer la taille réelle de la mire.
Source: [[50-calibration-geometrie/references/52-calibration-zhang|Fiche calibration]] ; [Zhang, §§2–4](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf).
Tags: cv::pilote cv::d05 famille::conception cv_id::CV-ZHANG-007 provenance::agent pole::B pole::C pole::E
END
