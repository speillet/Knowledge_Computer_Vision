# Canny et Hough : contours, droites et segments — cartes

Fiche : [[30-traitement-image/references/32-canny-hough|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::30-traitement-image

## CV-CANNY-HOUGH-001

Objectif : expliquer l’hystérésis. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-CANNY-HOUGH-001
Question: Pourquoi Canny utilise-t-il deux seuils plutôt qu’un simple seuil de gradient ?
Reponse: **Noyau attendu** : Les contours forts amorcent des structures ; des réponses plus faibles peuvent être retenues lorsqu’elles sont reliées aux fortes selon l’hystérésis.

**Approfondissement** : La suppression des non-maxima amincit d’abord les réponses. Les seuils ne donnent aucune classe sémantique.

**Déroulement interprété** : le gradient mesure une variation locale d'intensité. La suppression des non-maxima conserve les crêtes dans la direction du gradient afin d'éviter des bandes épaisses. L'hystérésis décide ensuite quelles crêtes faibles prolongent une structure suffisamment forte. Le seuil bas permet une continuité conditionnelle ; il ne rend pas toutes les réponses faibles admissibles.

**Exemple construit** : une arête éclairée de façon inégale comporte une portion contrastée et une portion faible. Un seuil unique élevé fragmente l'arête ; un seuil unique bas retient aussi beaucoup de texture. Les deux seuils permettent de conserver certaines portions faibles reliées à la portion forte. Si tout le contour est faible et sans amorce forte, il peut rester absent. Le réglage dépend de l'échelle de lissage, du contraste et de la définition du gradient ; aucune de ces étapes ne distingue à elle seule arête de pièce et texture du fond.

**Erreurs bloquantes** : Décrire le seuil bas comme une seconde segmentation indépendante.
Source: [[30-traitement-image/references/32-canny-hough|Fiche complète]] ; [OpenCV 4.13.0, Canny, Non-maximum Suppression et Hysteresis Thresholding](https://docs.opencv.org/4.13.0/da/d22/tutorial_py_canny.html).
Tags: cv::pilote cv::d03 famille::algorithme cv_id::CV-CANNY-HOUGH-001 provenance::agent pole::B pole::E pole::F
END

## CV-CANNY-HOUGH-002

Objectif : interpréter un vote de Hough. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-CANNY-HOUGH-002
Question: Que représentent $\rho$ et $\theta$ dans $\rho=x\cos\theta+y\sin\theta$ ?
Reponse: **Noyau attendu** : Pour des coordonnées image $x,y$ en pixels, $\rho$ est la distance orientée à l’origine en pixels ; $\theta$ est l’angle de la normale en radians, selon la convention annoncée. Chaque point vote pour les droites qui le traversent.

**Approfondissement** : Les bins imposent une résolution ; un maximum peut regrouper plusieurs structures voisines.

**Lecture géométrique** : le vecteur $(\cos\theta,\sin\theta)$ est une normale unitaire. Le produit scalaire avec $(x,y)$ donne la projection du point sur cette normale ; tous les points d'une même droite partagent cette projection. Ainsi, pour $\theta=0$, l'équation devient $x=\rho$ : une droite verticale. Pour $\theta=\pi/2$, elle devient $y=\rho$ : une droite horizontale, dans les axes annoncés.

**Construction des votes** : chaque point de contour peut appartenir à plusieurs droites et vote donc pour plusieurs couples. Une accumulation élevée signifie qu'un ensemble de points soutient une hypothèse, sans certifier leur appartenance au même objet. Des bins trop larges mélangent des droites proches ; des bins trop fins dispersent les votes bruités. Si l'origine change après un crop, la valeur de $\rho$ change aussi : remettre les paramètres dans le repère original avant toute mesure physique.

**Erreurs bloquantes** : Confondre normale et direction de segment ou oublier l’unité pixel.
Source: [[30-traitement-image/references/32-canny-hough|Fiche complète]] ; [OpenCV 4.13.0, Hough, How does it work? et Standard and Probabilistic Hough Line Transform](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html).
Tags: cv::pilote cv::d03 famille::raisonnement cv_id::CV-CANNY-HOUGH-002 provenance::agent pole::B pole::E pole::F
END

## CV-CANNY-HOUGH-003

Objectif : distinguer droite et segment. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-CANNY-HOUGH-003
Question: Pourquoi une sortie de HoughLines ne donne-t-elle pas directement les extrémités d’un segment réel ?
Reponse: **Noyau attendu** : Elle paramètre une droite ; les limites de support doivent être estimées séparément ou avec une variante segment comme HoughLinesP.

**Approfondissement** : Vérifier longueur minimale, trous et région observée ; prolonger une droite hors support n’est pas une mesure.

**Différence entre modèle et support** : une droite est un ensemble infini de points satisfaisant une équation ; un segment ajoute deux extrémités et un support observé. Un maximum de votes indique une orientation et une position soutenues par des contours, mais des points éloignés ou plusieurs objets peuvent contribuer à ce même maximum.

**Exemple construit** : deux petits bords colinéaires séparés par un grand espace peuvent soutenir la même droite. Relier automatiquement les points les plus éloignés ferait passer le segment dans une zone sans observation. Pour mesurer une pièce, projeter les points de support sur la direction de la droite, examiner les interruptions et appliquer des contraintes de longueur et de continuité cohérentes avec la tâche. Une variante qui renvoie des segments utilise elle aussi des paramètres de regroupement. Ses extrémités ne deviennent pas pour autant des limites physiques exactes sans contrôle de l'image et de l'incertitude.

**Erreurs bloquantes** : Interpréter une droite infinie comme les contours complets d’une pièce.
Source: [[30-traitement-image/references/32-canny-hough|Fiche complète]] ; [OpenCV 4.13.0, Hough, How does it work? et Standard and Probabilistic Hough Line Transform](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html).
Tags: cv::pilote cv::d03 famille::comparaison cv_id::CV-CANNY-HOUGH-003 provenance::agent pole::B pole::E pole::F
END

## CV-CANNY-HOUGH-004

Objectif : départager texture et structure. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-CANNY-HOUGH-004
Question: Hough produit beaucoup de droites sur une surface texturée. Quel contrôle évite un réglage aveugle du seuil de vote ?
Reponse: **Noyau attendu** : Inspecter carte Canny, distribution angulaire, région utile et support spatial des candidats.

**Approfondissement** : Tester une perturbation contrôlée de texture et des contraintes métier avant de valider une ligne.

**Enquête proposée** : superposer les droites et leurs points de support à l'image. Si les votes proviennent de stries répétées, le détecteur répond peut-être correctement à des contours qui ne sont simplement pas ceux de la pièce. Examiner ensuite la distribution des angles et le nombre de fragments : cela distingue une texture structurée d'un bruit dispersé.

**Ablation construite** : fixer les bins et seuils, restreindre une région d'intérêt, puis modifier séparément le lissage et la contrainte d'orientation attendue. Mesurer lignes métier trouvées, faux candidats et erreur de position. Augmenter seulement le seuil de vote peut éliminer une arête utile peu contrastée tout en conservant une texture longue et répétitive. Une contrainte géométrique aide uniquement si elle reste valable pour les orientations réellement rencontrées. L'accumulateur compte un support photométrique ; la validation du modèle de pièce est une décision supplémentaire du pipeline.

**Erreurs bloquantes** : Conclure que chaque maximum d’accumulateur est une arête physique.
Source: [[30-traitement-image/references/32-canny-hough|Fiche complète]] ; [OpenCV 4.13.0, Hough, How does it work? et Standard and Probabilistic Hough Line Transform](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html) ; diagnostic de texture proposé par le projet.
Tags: cv::pilote cv::d03 famille::diagnostic cv_id::CV-CANNY-HOUGH-004 provenance::agent pole::B pole::E pole::F
END
