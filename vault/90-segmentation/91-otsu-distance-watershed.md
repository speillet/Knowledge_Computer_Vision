# Otsu, distance transform et watershed — cartes

Fiche : [[90-segmentation/references/91-otsu-distance-watershed|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::90-segmentation

## CV-WATERSHED-001

Objectif : interpréter l’objectif Otsu. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-WATERSHED-001
Question: Pourquoi un seuil Otsu optimal sur l’histogramme peut-il être mauvais pour segmenter les défauts ?
Reponse: **Noyau attendu** : L’objectif sépare des intensités selon une variance, pas des catégories métier ; éclairage, déséquilibre et bruit peuvent dominer.

**Approfondissement** : Tester un masque annoté et la taille des défauts ; comparer seuillage local ou une autre représentation si l’hypothèse échoue.

**Erreurs bloquantes** : Déduire l’optimalité sémantique de l’optimum d’un critère d’intensité.
Source: [[90-segmentation/references/91-otsu-distance-watershed|Fiche complète]] ; [OpenCV Otsu, théorie](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html) ; [OpenCV watershed, marqueurs et API](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html).
Tags: cv::pilote cv::d09 famille::raisonnement cv_id::CV-WATERSHED-001 provenance::agent pole::A pole::E
END

## CV-WATERSHED-002

Objectif : reconstruire le pipeline à marqueurs. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-WATERSHED-002
Question: Comment distance transform et watershed peuvent-ils séparer des objets qui se touchent ?
Reponse: **Noyau attendu** : Construire un masque, estimer des centres/marqueurs depuis les distances, identifier fond/inconnu puis propager les labels.

**Approfondissement** : Un même masque peut produire des séparations différentes selon les marqueurs ; valider chaque étape.

**Erreurs bloquantes** : Présenter la distance transform comme une segmentation d’instances autonome.
Source: [[90-segmentation/references/91-otsu-distance-watershed|Fiche complète]] ; [OpenCV Otsu, théorie](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html) ; [OpenCV watershed, marqueurs et API](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html).
Tags: cv::pilote cv::d09 famille::algorithme cv_id::CV-WATERSHED-002 provenance::agent pole::A pole::E
END

## CV-WATERSHED-003

Objectif : distinguer fond et inconnu. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-WATERSHED-003
Question: Dans les marqueurs watershed OpenCV documentés, pourquoi ne pas coder tout le fond connu et l’inconnu à zéro ?
Reponse: **Noyau attendu** : Zéro représente une zone à attribuer ; le fond déjà déterminé doit avoir un label positif comme les autres marqueurs connus.

**Approfondissement** : Les frontières produites valent −1 ; conserver type, forme et modification sur place selon l’API.

**Erreurs bloquantes** : Assimiler valeur 0 à un fond définitivement classé.
Source: [[90-segmentation/references/91-otsu-distance-watershed|Fiche complète]] ; [OpenCV Otsu, théorie](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html) ; [OpenCV watershed, marqueurs et API](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html).
Tags: cv::pilote cv::d09 famille::pratique cv_id::CV-WATERSHED-003 provenance::agent pole::A pole::E
END

## CV-WATERSHED-004

Objectif : localiser une sous-segmentation. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-WATERSHED-004
Question: Deux objets restent dans un bassin malgré un masque qui les couvre bien. Quelle vérification est discriminante ?
Reponse: **Noyau attendu** : Visualiser les marqueurs : s’il n’existe qu’un germe commun, revoir séparation des maxima et hypothèses de forme.

**Approfondissement** : Comparer à des marqueurs manuels sur une copie pour isoler le rôle des germes ; augmenter des seuils au hasard n’identifie pas la cause.

**Erreurs bloquantes** : Valider des instances sur la seule qualité du masque binaire.
Source: [[90-segmentation/references/91-otsu-distance-watershed|Fiche complète]] ; [OpenCV Otsu, théorie](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html) ; [OpenCV watershed, marqueurs et API](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html).
Tags: cv::pilote cv::d09 famille::diagnostic cv_id::CV-WATERSHED-004 provenance::agent pole::A pole::E
END

## CV-WATERSHED-005

Objectif : choisir une métrique d’instances classique. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-WATERSHED-005
Question: Pourquoi une IoU binaire élevée peut-elle masquer l’échec d’un pipeline de comptage watershed ?
Reponse: **Noyau attendu** : La fusion de plusieurs objets peut conserver presque toute la région de premier plan mais perdre le nombre et l’identité des instances.

**Approfondissement** : Mesurer fusions/séparations et protocole d’appariement des objets, en plus du masque global.

**Erreurs bloquantes** : Confondre recouvrement sémantique et comptage correct.
Source: [[90-segmentation/references/91-otsu-distance-watershed|Fiche complète]] ; [OpenCV Otsu, théorie](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html) ; [OpenCV watershed, marqueurs et API](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html).
Tags: cv::pilote cv::d09 famille::evaluation cv_id::CV-WATERSHED-005 provenance::agent pole::A pole::E
END
