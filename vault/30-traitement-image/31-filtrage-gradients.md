# Filtres, gradients et pyramides — cartes

Fiche : [[30-traitement-image/references/31-filtrage-gradients|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::30-traitement-image

## CV-FILTRES-001

Objectif : choisir un filtre d’après le bruit. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-FILTRES-001
Question: Pourquoi le médian peut-il convenir à du bruit impulsionnel sans être un remplaçant universel du Gaussien ?
Reponse: **Noyau attendu** : Il rejette des valeurs extrêmes locales via l’ordre, tandis que le Gaussien moyenne ; l’effet dépend du bruit et des structures.

**Approfondissement** : Comparer conservation des petits détails et performance aval ; le médian reste non linéaire et peut modifier la géométrie.

**Erreurs bloquantes** : Annoncer un filtre meilleur pour tous bruits et toutes tâches.
Source: [[30-traitement-image/references/31-filtrage-gradients|Fiche complète]] ; [OpenCV 4.12.0, Smoothing Images, Gaussian/Median/Bilateral Filter](https://docs.opencv.org/4.12.0/dc/dd3/tutorial_gausian_median_blur_bilateral_filter.html).
Tags: cv::pilote cv::d03 famille::comparaison cv_id::CV-FILTRES-001 provenance::agent pole::A pole::B pole::E pole::F
END

## CV-FILTRES-002

Objectif : régler un bilatéral dans les bonnes unités. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-FILTRES-002
Question: Que change une normalisation d’intensité de [0,255] à [0,1] pour le sigma photométrique d’un bilatéral ?
Reponse: **Noyau attendu** : Diviser le sigma photométrique par 255, comme les différences d’intensité, pour conserver les mêmes poids. Garder le même nombre rend le filtrage moins sélectif en intensité.

**Approfondissement** : Le sigma spatial est en pixels et suit une autre logique. Consigner plage et espace couleur.

**Erreurs bloquantes** : Traiter tous les sigma comme des grandeurs sans unité.
Source: [[30-traitement-image/references/31-filtrage-gradients|Fiche complète]] ; [Tomasi et Manduchi 1998, Bilateral Filtering, §§2–3](https://users.soe.ucsc.edu/~manduchi/Papers/ICCV98.pdf).
Tags: cv::pilote cv::d03 famille::raisonnement cv_id::CV-FILTRES-002 provenance::agent pole::A pole::B pole::E pole::F
END

## CV-FILTRES-003

Objectif : protéger un détail métier. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-FILTRES-003
Question: Le débruitage améliore le PSNR mais fait disparaître des rayures. Comment évaluer le prétraitement ?
Reponse: **Noyau attendu** : Mesurer le rappel des défauts et l’erreur de localisation à échelle pertinente, avec images et annotations réservées.

**Approfondissement** : Un gain global de reconstruction peut masquer un défaut petit ou rare ; conserver la baseline sans filtrage.

**Erreurs bloquantes** : Décider au PSNR seul.
Source: [[30-traitement-image/references/31-filtrage-gradients|Fiche complète]] ; [OpenCV 4.12.0, Smoothing Images, Gaussian/Median/Bilateral Filter](https://docs.opencv.org/4.12.0/dc/dd3/tutorial_gausian_median_blur_bilateral_filter.html) ; protocole aval proposé par le projet.
Tags: cv::pilote cv::d03 famille::diagnostic cv_id::CV-FILTRES-003 provenance::agent pole::A pole::B pole::E pole::F
END

## CV-FILTRES-004

Objectif : expliquer une pyramide. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-FILTRES-004
Question: Pourquoi ne suffit-il pas de prendre un pixel sur deux pour construire une pyramide de matching ?
Reponse: **Noyau attendu** : La décimation sans filtrage peut replier les hautes fréquences en aliasing et changer les structures observées.

**Approfondissement** : Le filtre et l’échelle choisie conditionnent la répétabilité des features ; ils ne garantissent pas une invariance parfaite.

**Erreurs bloquantes** : Confondre sous-échantillonnage et perte contrôlée d’information.
Source: [[30-traitement-image/references/31-filtrage-gradients|Fiche complète]] ; [OpenCV 4.13.0, Image Pyramids, Gaussian Pyramid](https://docs.opencv.org/4.13.0/d4/d1f/tutorial_pyramids.html).
Tags: cv::pilote cv::d03 famille::comprehension cv_id::CV-FILTRES-004 provenance::agent pole::A pole::B pole::E pole::F
END
