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

**Modèle local** : pour un petit déplacement $d$, la variation photométrique se rapproche d'une forme quadratique $d^TMd$. La matrice $M$ rassemble les produits des gradients dans le voisinage. Ses directions propres indiquent les directions de déplacement qui changent beaucoup ou peu l'apparence.

**Exemple construit** : sur un bord vertical uniforme, déplacer le patch horizontalement change son contenu ; le déplacer le long du bord peut presque le laisser identique. Un coin visible présente au contraire des changements dans deux directions, ce qui aide à localiser un déplacement. Cela n'implique pas qu'il soit unique dans l'image : les coins d'une grille peuvent tous se ressembler. Distinguer donc information locale de localisation et ambiguïté d'association entre images. Une fenêtre mal éclairée, occultée ou trop grande peut également invalider le petit modèle photométrique malgré des valeurs propres favorables.

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

**Décomposition des entrées et sorties** : FAST prend une image et repère des positions candidates à partir de comparaisons locales. BRIEF prend des voisinages autour de positions choisies et produit des chaînes de tests binaires. Un matcher compare ensuite ces chaînes, puis une étape géométrique examine si les paires expliquent une transformation plausible.

**Exemple de diagnostic construit** : si aucune position n'est détectée sur une pièce floue, changer la distance du matcher ne peut pas créer les keypoints manquants. Si les points sont stables mais les descripteurs tournent mal avec la pièce, le défaut peut être dans la description ou son repère. Décrire chaque étape par son contrat évite de remplacer un composant qui ne traite pas la cause observée. Une chaîne complète comme ORB ajoute des choix de pyramide et d'orientation ; elle ne rend pas FAST et BRIEF synonymes.

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

**Pourquoi l'approximation intervient** : un index rapide explore moins de candidats qu'une recherche exhaustive. Il peut manquer le meilleur voisin ou le concurrent utilisé pour estimer l'ambiguïté. Un ratio apparemment meilleur peut ainsi résulter d'un deuxième voisin trop éloigné, et non d'une correspondance plus fiable.

**Ablation proposée** : conserver descripteurs et images, recalculer les deux voisins par recherche exacte sur un échantillon, puis comparer les paires avant et après filtrage. Examiner enfin les inliers et l'erreur sur la région utile. Faire varier le budget de recherche sans changer simultanément le détecteur. Inclure construction de l'index et éventuelles reconstructions dans le temps total. Un recul du succès géométrique peut venir de l'approximation, d'une mauvaise métrique ou de données ambiguës ; la comparaison contrôlée sert à les départager plutôt qu'à déclarer FLANN incorrect en général.

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

**Ce que teste la géométrie** : une homographie pour un plan, ou une contrainte multivue appropriée, relie les positions des candidats dans les images. Le résidu exprime leur désaccord avec ce modèle dans une unité définie. Un matcher choisit des voisins dans une représentation d'apparence ; ces deux problèmes sont différents.

**Limite construite** : deux logos identiques sur un même support peuvent produire un groupe de matches et une transformation cohérents mais correspondant au mauvais logo. Un modèle géométrique ne résout pas nécessairement une symétrie de la scène. Chercher une marque unique, une position attendue ou une observation supplémentaire qui distingue les hypothèses. Contrôler aussi le support spatial des points et des observations réservées. Cette étape fournit des raisons d'accepter une transformation pour un usage précis, sans transformer automatiquement le consensus en preuve d'identité de l'objet.

**Erreurs bloquantes** : Déduire la validité physique de la réciprocité des plus proches voisins.
Source: [[40-features-matching/references/43-detecteurs-matchers|Fiche complète]] ; [OpenCV 4.13.0, Feature Matching, FLANN based Matcher](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html) ; scénario de symétrie et vérification indépendante : raisonnements du projet.
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-MATCHING-004 provenance::agent pole::B pole::E
END
