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

**Erreurs bloquantes** : Décrire le seuil bas comme une seconde segmentation indépendante.
Source: [[30-traitement-image/references/32-canny-hough|Fiche complète]] ; [OpenCV Canny, Theory](https://docs.opencv.org/4.13.0/da/d22/tutorial_py_canny.html) ; [OpenCV Hough, Theory](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html).
Tags: cv::pilote cv::d03 famille::algorithme cv_id::CV-CANNY-HOUGH-001 provenance::agent pole::B pole::E pole::F
END

## CV-CANNY-HOUGH-002

Objectif : interpréter un vote de Hough. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-CANNY-HOUGH-002
Question: Que représentent $\rho$ et $\theta$ dans $\rho=x\cos\theta+y\sin\theta$ ?
Reponse: **Noyau attendu** : La distance orientée de la droite à l’origine et l’orientation de sa normale selon la convention ; chaque point vote pour des droites compatibles.

**Approfondissement** : Les bins imposent une résolution ; un maximum peut regrouper plusieurs structures voisines.

**Erreurs bloquantes** : Confondre normale et direction de segment ou oublier l’unité pixel.
Source: [[30-traitement-image/references/32-canny-hough|Fiche complète]] ; [OpenCV Canny, Theory](https://docs.opencv.org/4.13.0/da/d22/tutorial_py_canny.html) ; [OpenCV Hough, Theory](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html).
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

**Erreurs bloquantes** : Interpréter une droite infinie comme les contours complets d’une pièce.
Source: [[30-traitement-image/references/32-canny-hough|Fiche complète]] ; [OpenCV Canny, Theory](https://docs.opencv.org/4.13.0/da/d22/tutorial_py_canny.html) ; [OpenCV Hough, Theory](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html).
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

**Erreurs bloquantes** : Conclure que chaque maximum d’accumulateur est une arête physique.
Source: [[30-traitement-image/references/32-canny-hough|Fiche complète]] ; [OpenCV Canny, Theory](https://docs.opencv.org/4.13.0/da/d22/tutorial_py_canny.html) ; [OpenCV Hough, Theory](https://docs.opencv.org/4.13.0/d9/db0/tutorial_hough_lines.html).
Tags: cv::pilote cv::d03 famille::diagnostic cv_id::CV-CANNY-HOUGH-004 provenance::agent pole::B pole::E pole::F
END
