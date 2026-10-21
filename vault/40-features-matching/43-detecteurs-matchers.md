# Détecteurs locaux, descripteurs et matchers — cartes

Fiche : [[40-features-matching/references/43-detecteurs-matchers|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::40-features-matching

## CV-MATCHING-001

Objectif : interpréter la matrice de structure. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-MATCHING-001
Question: Pourquoi un coin localise-t-il mieux un déplacement 2D qu’une arête seule dans un modèle par gradients ?
Reponse: **Noyau attendu** : Deux directions de variation contraignent le mouvement ; sur une arête, le déplacement tangent est peu observable.

**Approfondissement** : Inspecter les valeurs propres de la matrice locale, pas seulement le nombre de points détectés.

**Erreurs bloquantes** : Confondre un fort gradient unique et deux contraintes indépendantes.
Source: [[40-features-matching/references/43-detecteurs-matchers|Fiche complète]] ; [OpenCV Harris, théorie](https://docs.opencv.org/4.13.0/dc/d0d/tutorial_py_features_harris.html) ; [OpenCV Shi–Tomasi](https://docs.opencv.org/4.13.0/d4/d8c/tutorial_py_shi_tomasi.html) ; [OpenCV matching](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html).
Tags: cv::pilote cv::d04 famille::raisonnement cv_id::CV-MATCHING-001 provenance::agent pole::B pole::E
END

## CV-MATCHING-002

Objectif : séparer détecteur et descripteur. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-MATCHING-002
Question: Pourquoi FAST et BRIEF ne sont-ils pas deux alternatives remplissant exactement le même rôle ?
Reponse: **Noyau attendu** : FAST localise des points ; BRIEF décrit un patch en tests binaires.

**Approfondissement** : Un pipeline peut les combiner, avec orientation et échelle selon la méthode ; un matcher reste ensuite nécessaire.

**Erreurs bloquantes** : Attribuer des correspondances géométriquement vérifiées à un détecteur seul.
Source: [[40-features-matching/references/43-detecteurs-matchers|Fiche complète]] ; [OpenCV 4.13.0, FAST, Feature Detection](https://docs.opencv.org/4.13.0/df/d0c/tutorial_py_fast.html) ; [OpenCV 4.13.0, BRIEF, Theory](https://docs.opencv.org/4.13.0/dc/d7d/tutorial_py_brief.html).
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-MATCHING-002 provenance::agent pole::B pole::E
END

## CV-MATCHING-003

Objectif : mesurer une recherche approximative. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-MATCHING-003
Question: Que vérifier si FLANN accélère le matching mais dégrade le recalage ?
Reponse: **Noyau attendu** : Compatibilité de l’index et de la distance, rappel des voisins, filtre de correspondances et succès géométrique final.

**Approfondissement** : Comparer temps de construction et requêtes, mémoire et coût total ; une recherche plus rapide peut changer le ratio entre voisins.

**Erreurs bloquantes** : Évaluer seulement le temps de requête ou le nombre de matches.
Source: [[40-features-matching/references/43-detecteurs-matchers|Fiche complète]] ; [OpenCV 4.13.0, Feature Matching, FLANN based Matcher](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html) ; protocole aval et effet sur le ratio : raisonnements du projet.
Tags: cv::pilote cv::d04 famille::evaluation cv_id::CV-MATCHING-003 provenance::agent pole::B pole::E
END

## CV-MATCHING-004

Objectif : choisir un contrôle géométrique. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-MATCHING-004
Question: Deux logos répétés produisent des descripteurs proches. Quel composant permet de tester le modèle physique des correspondances ?
Reponse: **Noyau attendu** : Une vérification géométrique adaptée à la scène, avec résidus, seuils et couverture ; le matcher seul ne le garantit pas.

**Approfondissement** : Une symétrie peut rester cohérente ; chercher une observation distinctive ou une contrainte indépendante.

**Erreurs bloquantes** : Déduire la validité physique de la réciprocité des plus proches voisins.
Source: [[40-features-matching/references/43-detecteurs-matchers|Fiche complète]] ; [OpenCV 4.13.0, Feature Matching, FLANN based Matcher](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html) ; scénario de symétrie et vérification indépendante : raisonnements du projet.
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-MATCHING-004 provenance::agent pole::B pole::E
END
