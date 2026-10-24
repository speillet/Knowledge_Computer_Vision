# MeanShift et CamShift — suivre une distribution d’apparence — cartes

Fiche : [[110-tracking-association/references/115-meanshift-camshift|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::110-tracking-association

## CV-MEANSHIFT-001

Objectif : expliquer une itération MeanShift. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-MEANSHIFT-001
Question: Que calcule une itération MeanShift sur une image de backprojection, et que faire si la fenêtre ne contient aucune masse ?
Reponse: **Noyau attendu** : Calculer le centroïde des scores dans la fenêtre, puis déplacer la fenêtre vers ce centre. Si la masse totale $M_{00}$ est nulle, le centroïde est indéfini : ne pas diviser et appliquer une politique de perte/recherche explicite.

**Approfondissement** : $x_c=M_{10}/M_{00}$ et $y_c=M_{01}/M_{00}$ utilisent les moments pondérés. Le processus cherche une concentration locale et dépend de l’initialisation. La backprojection ne certifie pas l’identité de l’objet.

**Erreurs bloquantes** : Diviser par une masse nulle ; présenter le mode atteint comme un maximum global garanti.
Source: [[110-tracking-association/references/115-meanshift-camshift|Fiche complète]] ; [OpenCV 4.13, Meanshift and Camshift, Theory et contrats de sortie](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html).
Tags: cv::pilote cv::d11 famille::algorithme cv_id::CV-MEANSHIFT-001 provenance::agent pole::C pole::D pole::E
END

## CV-MEANSHIFT-002

Objectif : distinguer MeanShift et CamShift. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-MEANSHIFT-002
Question: La cible se rapproche de la caméra, mais une fenêtre de suivi reste trop petite. Qu’apporte CamShift par rapport au MeanShift usuel ?
Reponse: **Noyau attendu** : Le MeanShift usuel déplace une fenêtre de taille fixe ; CamShift adapte taille et orientation à la distribution observée, en utilisant ses moments. Cela traite une variation d’apparence projetée, pas une estimation métrique de pose.

**Approfondissement** : Une adaptation peut aussi englober du fond ou un distracteur si la backprojection est mauvaise. Comparer les deux à histogramme et initialisation identiques, en mesurant overlap et pertes, sans conclure à une robustesse universelle.

**Erreurs bloquantes** : Confondre boîte orientée 2D et orientation 3D ; annoncer une adaptation fiable en toute occultation.
Source: [[110-tracking-association/references/115-meanshift-camshift|Fiche complète]] ; [OpenCV 4.13, Meanshift and Camshift, Theory et contrats de sortie](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html).
Tags: cv::pilote cv::d11 famille::comparaison cv_id::CV-MEANSHIFT-002 provenance::agent pole::C pole::D pole::E
END

## CV-MEANSHIFT-003

Objectif : diagnostiquer un distracteur de couleur. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-MEANSHIFT-003
Question: Un suivi CamShift saute sur une autre pièce de même couleur. Pourquoi augmenter le nombre d’itérations peut-il aggraver le problème ?
Reponse: **Noyau attendu** : Le modèle d’histogramme ne distingue pas nécessairement les deux pièces. Plus d’itérations peut converger davantage vers la mauvaise concentration. Inspecter la backprojection, la ROI et la séparation cible/fond avant de régler l’arrêt.

**Approfondissement** : Conserver une politique de perte, ajouter une information de texture ou un détecteur si l’identité importe. Un pic de couleur fort peut être correct pour le modèle statistique et faux pour le besoin métier.

**Erreurs bloquantes** : Assimiler convergence de MeanShift et bonne identité.
Source: [[110-tracking-association/references/115-meanshift-camshift|Fiche complète]] ; [OpenCV 4.13, Meanshift and Camshift, Theory et contrats de sortie](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html).
Tags: cv::pilote cv::d11 famille::diagnostic cv_id::CV-MEANSHIFT-003 provenance::agent pole::C pole::D pole::E
END

## CV-MEANSHIFT-004

Objectif : évaluer couleur et adaptation séparément. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-MEANSHIFT-004
Question: Quel essai permet de vérifier si une amélioration vient de l’adaptation CamShift plutôt que d’un nouvel histogramme ?
Reponse: **Noyau attendu** : Garder le même histogramme, les mêmes frames et la même initialisation ; comparer fenêtre fixe et fenêtre adaptative sur un changement d’échelle. Mesurer centre, overlap, taille et pertes, puis tester séparément un changement d’histogramme.

**Approfondissement** : Ajouter ensuite illumination et distracteurs un facteur à la fois. Les pixels peu saturés rendent la teinte peu informative ; documenter les masques et canaux utilisés. Ces variations sont proposées et n’ont pas été exécutées sur vidéo ici.

**Erreurs bloquantes** : Modifier simultanément histogramme, masque et tracker puis attribuer le résultat à CamShift seul.
Source: [[110-tracking-association/references/115-meanshift-camshift|Fiche complète]] ; [OpenCV 4.13, Meanshift and Camshift, Theory et contrats de sortie](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html).
Tags: cv::pilote cv::d11 famille::evaluation cv_id::CV-MEANSHIFT-004 provenance::agent pole::C pole::D pole::E
END
