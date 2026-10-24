# Harris et Shi–Tomasi — structure locale et points suivables — cartes

Fiche : [[40-features-matching/references/46-harris-shi-tomasi|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::40-features-matching

## CV-CORNERS-001

Objectif : interpréter les valeurs propres locales. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-CORNERS-001
Question: Une fenêtre donne $M=\mathrm{diag}(100,1)$, une autre $M=\mathrm{diag}(20,20)$. Laquelle contraint mieux un petit déplacement 2D, et pourquoi ?
Reponse: **Noyau attendu** : La seconde : sa plus petite valeur propre vaut 20 au lieu de 1. Les deux directions y sont contraintes ; la première ressemble à une arête, même si son gradient total est plus fort.

**Approfondissement** : $E(d)\approx d^TMd$ approxime la variation d’intensité pour un petit déplacement $d$ en pixels. La direction associée à la petite valeur propre est difficile à observer. Il reste à vérifier stabilité photométrique et absence d’occultation.

**Erreurs bloquantes** : Choisir uniquement la plus grande valeur propre ; confondre coin fort et correspondance certaine.
Source: [[40-features-matching/references/46-harris-shi-tomasi|Fiche complète]] ; [Harris et Stephens 1988, auto-corrélation et réponse de coin](https://www.bmva-archive.org.uk/bmvc/1988/avc-88-023.pdf).
Tags: cv::pilote cv::d04 famille::raisonnement cv_id::CV-CORNERS-001 provenance::agent pole::B pole::C pole::E
END

## CV-CORNERS-002

Objectif : distinguer scores Harris et Shi–Tomasi. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-CORNERS-002
Question: Que changent Harris et Shi–Tomasi dans la sélection de coins, et peut-on conserver le même seuil numérique ?
Reponse: **Noyau attendu** : Harris prend $\lambda_1\lambda_2-k(\lambda_1+\lambda_2)^2$ ; Shi–Tomasi prend $\min(\lambda_1,\lambda_2)$. Les valeurs propres viennent de la matrice locale des produits de gradients. Les scores ont des échelles et unités différentes : recalibrer les seuils.

**Approfondissement** : Shi–Tomasi teste directement la direction la moins informative. Harris pénalise une forte anisotropie via son paramètre $k$. Le choix dépend du pipeline ; aucune formule n’impose une meilleure performance sur toute scène.

**Erreurs bloquantes** : Réutiliser le même seuil sans normalisation ; annoncer un classement universel.
Source: [[40-features-matching/references/46-harris-shi-tomasi|Fiche complète]] ; [OpenCV 4.13, Shi–Tomasi, Theory et goodFeaturesToTrack](https://docs.opencv.org/4.13.0/d4/d8c/tutorial_py_shi_tomasi.html).
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-CORNERS-002 provenance::agent pole::B pole::C pole::E
END

## CV-CORNERS-003

Objectif : régler une sélection de coins. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-CORNERS-003
Question: Dans OpenCV goodFeaturesToTrack 4.13, comment distinguer qualityLevel, minDistance et maxCorners ?
Reponse: **Noyau attendu** : `qualityLevel` fixe un seuil relatif au meilleur score ; `minDistance` impose un espacement minimal en pixels ; `maxCorners` borne le nombre retourné. Ces réglages servent trois contraintes différentes.

**Approfondissement** : Une image de contraste faible peut conserver des points avec un seuil relatif faible sans les rendre suivables. Vérifier aussi leur couverture spatiale et leur conditionnement. L’image et la dérivation doivent respecter le contrat du détecteur.

**Erreurs bloquantes** : Lire qualityLevel comme une probabilité ; convertir minDistance en intensité.
Source: [[40-features-matching/references/46-harris-shi-tomasi|Fiche complète]] ; [OpenCV 4.13, Shi–Tomasi, Theory et goodFeaturesToTrack](https://docs.opencv.org/4.13.0/d4/d8c/tutorial_py_shi_tomasi.html).
Tags: cv::pilote cv::d04 famille::pratique cv_id::CV-CORNERS-003 provenance::agent pole::B pole::C pole::E
END

## CV-CORNERS-004

Objectif : distinguer détection et ambiguïté de matching. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-CORNERS-004
Question: Des coins très forts sur une grille répétitive donnent pourtant une mauvaise homographie. Quelles vérifications départagent un problème de détection d’un problème d’association ?
Reponse: **Noyau attendu** : Vérifier répétabilité et localisation des coins, puis ambiguïté des descripteurs, répartition des matches et résidus géométriques. Des coins forts peuvent se ressembler et produire des associations fausses.

**Approfondissement** : Un contrôle construit consiste à conserver le détecteur et changer le filtrage des matches, puis inverser l’expérience. Le score local ne vérifie ni identité du point ni modèle d’homographie. Une forte concentration spatiale peut aussi mal contraindre l’estimation.

**Erreurs bloquantes** : Augmenter seulement le nombre de coins ; assimiler score Harris et confiance de match.
Source: [[40-features-matching/references/46-harris-shi-tomasi|Fiche complète]] ; [Harris et Stephens 1988, auto-corrélation et réponse de coin](https://www.bmva-archive.org.uk/bmvc/1988/avc-88-023.pdf).
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-CORNERS-004 provenance::agent pole::B pole::C pole::E
END

## CV-CORNERS-005

Objectif : évaluer une sélection pour le tracking. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-CORNERS-005
Question: Pourquoi le nombre de coins détectés ne suffit-il pas pour comparer deux réglages destinés à Lucas–Kanade ?
Reponse: **Noyau attendu** : Mesurer survie, erreur de déplacement, couverture spatiale et erreur de géométrie à budget et résolution comparables. Un réglage produisant davantage de points peut ajouter du bruit ou des points redondants.

**Approfondissement** : Variation proposée : imposer des quotas par cellules avec le même nombre total de points. Séparer séquences d’ajustement et d’évaluation ; noter flou et occultations. Ce protocole est une proposition du projet, pas un résultat publié.

**Erreurs bloquantes** : Conclure sur le seul compteur de points ; changer plusieurs facteurs sans les consigner.
Source: [[40-features-matching/references/46-harris-shi-tomasi|Fiche complète]] ; [OpenCV 4.13, Shi–Tomasi, Theory et goodFeaturesToTrack](https://docs.opencv.org/4.13.0/d4/d8c/tutorial_py_shi_tomasi.html).
Tags: cv::pilote cv::d04 famille::evaluation cv_id::CV-CORNERS-005 provenance::agent pole::B pole::C pole::E
END
