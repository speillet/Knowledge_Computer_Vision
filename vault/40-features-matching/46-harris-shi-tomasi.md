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

**Interprétation des directions** : avec la première matrice, un déplacement dans la direction associée à la valeur 1 modifie peu le patch. La grande valeur 100 ne compense pas cette direction faible. Avec la seconde, un déplacement unitaire dans n'importe quelle direction propre produit la même courbure locale de 20.

**Utilisation proposée** : avant un suivi Lucas–Kanade, examiner donc le plus petit terme contraignant et la répartition des points. Un ensemble de coins bien conditionnés mais regroupés dans une petite zone ne garantit pas un recalage global stable. Les chiffres supposent le modèle local de petites translations et les mêmes unités de gradient ; comparer des matrices issues de normalisations différentes sans les aligner n'aurait pas le même sens.

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

**Dérivation d'échelle** : si les intensités sont multipliées par une constante $a$, les gradients sont multipliés par $a$ et les valeurs propres de $M$ par $a^2$, à opérateurs identiques. Le score Shi–Tomasi suit donc ce facteur, tandis que le score Harris suit $a^4$. Le même seuil numérique ne peut pas représenter la même sélectivité dans ces deux espaces.

**Décision proposée** : fixer plage d'intensité, échelle des dérivées et fenêtre avant de régler le seuil. Comparer ensuite localisation, couverture et stabilité sous les perturbations pertinentes. Une différence de compte de coins peut venir de la normalisation des scores plutôt que d'une supériorité du mécanisme. Les deux critères décrivent une information locale, pas une probabilité de correspondance correcte.

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

**Exemple de réglage interprété** : si le meilleur score vaut 100 et le seuil relatif vaut 0,1, le seuil de sélection est lié à 10 dans cette image. Ce raisonnement ne donne pas un niveau absolu de qualité valable sur toutes les acquisitions. Une image presque uniforme peut avoir un meilleur score faible, malgré un seuil relatif respecté.

**Effets distincts** : augmenter la distance minimale répartit les positions mais peut retirer des détails proches utiles ; augmenter le quota ne crée pas davantage de candidats satisfaisants. Régler chaque contrainte avec une carte spatiale des points et une mesure aval. Pour comparer des acquisitions, relever aussi les scores absolus et le contraste. La sélection répond à un budget et une couverture ; la suivabilité demande encore une vérification temporelle.

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

**Pourquoi les scores ne départagent pas les cases** : chaque intersection d'une grille peut présenter deux directions de gradient bien marquées. Le critère de coin confirme la localisation de chaque intersection, mais ne sait pas quelle intersection de la seconde image représente le même point du monde.

**Test construit** : conserver les positions détectées et visualiser les candidats de chaque descripteur. Comparer les hypothèses de décalage d'une période avec des repères distinctifs réservés. Vérifier ensuite que les inliers couvrent la surface à recaler et pas une seule bande. Si les localisations restent stables mais les associations changent de case, agir sur les indices distinctifs ou les contraintes du problème. Une meilleure sélection locale peut réduire du bruit ; elle ne résout pas à elle seule une symétrie d'apparence.

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

**Exemple de comparaison** : cent coins sur une seule texture peuvent être redondants et laisser la pièce utile sans observations. Cinquante points répartis peuvent mieux contraindre le mouvement demandé, mais seulement si leurs déplacements sont fiables. Le nombre ne décrit ni cette couverture ni la durée pendant laquelle les points restent visibles.

**Protocole construit** : fixer résolution, budget total et critères de suivi, puis varier séparément score de sélection et quotas spatiaux. Mesurer erreurs sur des trajectoires de points annotées ou sur une géométrie indépendante, en comptant aussi les points perdus. Un faible résidu photométrique peut rester trompeur en cas de répétition. Rapporter la performance sur flou, faible texture et occultation, avec les mêmes règles de rejet pour tous les réglages.

**Erreurs bloquantes** : Conclure sur le seul compteur de points ; changer plusieurs facteurs sans les consigner.
Source: [[40-features-matching/references/46-harris-shi-tomasi|Fiche complète]] ; [OpenCV 4.13, Shi–Tomasi, Theory et goodFeaturesToTrack](https://docs.opencv.org/4.13.0/d4/d8c/tutorial_py_shi_tomasi.html).
Tags: cv::pilote cv::d04 famille::evaluation cv_id::CV-CORNERS-005 provenance::agent pole::B pole::C pole::E
END
