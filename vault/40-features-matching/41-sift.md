# Cartes pilotes — SIFT

Fiche : [[40-features-matching/references/41-sift|SIFT]]. Provenance de rédaction : agent.
Format expérimental, pas encore synchronisé ni évalué en rappel différé.

TARGET DECK: CV::Pilote::40-features-matching

## CV-SIFT-001

Objectif : situer les composants d'un pipeline de correspondances. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-SIFT-001
Question: Pour recaler deux photos d'une étiquette plane, que fournit SIFT et quelles étapes restent nécessaires pour obtenir une transformation fiable ?
Reponse: **Noyau attendu** : SIFT fournit des keypoints et leurs descripteurs locaux. Le matcher propose des paires ; un filtrage limite les ambiguïtés ; une estimation géométrique teste une transformation adaptée au plan. Les matches ne sont pas une preuve de recalage.

**Approfondissement** : la détection décide où décrire ; la description représente le voisinage. On peut utiliser distance L2, ratio test puis RANSAC/homographie, avec inspection des résidus et de la couverture spatiale. Le choix d'une homographie dépend de la scène, pas de l'emploi de SIFT.

**Chaîne de décision construite** : pour une étiquette connue plane, conserver les coordonnées des keypoints dans chaque image, calculer les candidats et inspecter leur distribution avant d'estimer le warp. Quatre correspondances mal placées ou plusieurs paires ambiguës ne deviennent pas fiables parce qu'elles proviennent de SIFT. Un consensus concentré dans un coin peut également mal contraindre l'extrapolation vers l'autre bord.

**Interprétation du résultat** : contrôler une géométrie sur des points non utilisés pour son ajustement et dans la zone où le produit doit agir. Une pièce en relief peut exiger un autre modèle qu'une homographie unique. La responsabilité de SIFT est la représentation locale ; celle du pipeline est d'établir qu'une transformation explique suffisamment bien les observations pour l'usage annoncé.

**Erreurs bloquantes** : dire que le descripteur estime directement la pose ou que chaque plus proche voisin est une correspondance vraie.
Source: [[40-features-matching/references/41-sift|Fiche SIFT]] ; [Lowe 2004, §§3–7](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf).
Tags: cv::pilote cv::d04 famille::comprehension cv_id::CV-SIFT-001 provenance::agent pole::B pole::E
END

## CV-SIFT-002

Objectif : expliquer la recherche d'une échelle caractéristique. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-SIFT-002
Question: Dans SIFT, que compare la différence de gaussiennes et pourquoi rechercher des extrema aussi dans la direction d'échelle ?
Reponse: **Noyau attendu** : $D(x,y,\sigma)=L(x,y,k\sigma)-L(x,y,\sigma)$ compare deux lissages voisins, avec $L=G_\sigma*I$. Rechercher un extremum spatial et d'échelle vise à retrouver une structure à son échelle caractéristique, plutôt qu'à un rayon fixé arbitrairement.

**Approfondissement** : $\sigma$ est une échelle en pixels, $k>1$ le rapport entre niveaux, et $G_\sigma$ un noyau gaussien normalisé. La DoG approxime un Laplacien normalisé en échelle. Le candidat est comparé à 26 voisins : huit dans son niveau et neuf dans chacun des niveaux adjacents. Échantillonnage, bruit et perte de détails limitent la répétabilité.

**Pourquoi l'échelle intervient** : un même détail couvre davantage de pixels lorsque la caméra se rapproche. Chercher seulement des maxima dans une image lissée à rayon fixe impose alors un voisinage différent dans les deux vues. La recherche dans les niveaux vise une taille caractéristique de la structure, qui sert ensuite au calcul du descripteur.

**Exemple interprété** : une petite tache et la même tache agrandie peuvent être sélectionnées à des niveaux différents. Si l'image réduite ne contient plus assez d'échantillons pour la représenter, aucun niveau ne recrée la tache. Le mécanisme aide donc à retrouver une structure encore observable ; il ne supprime ni le rôle de l'optique ni celui du préfiltrage avant réduction.

**Erreurs bloquantes** : confondre échelle et orientation, ou annoncer une invariance parfaite pour n'importe quel changement de résolution.
Source: [[40-features-matching/references/41-sift|Fiche SIFT]] ; [Lowe, §3](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf).
Tags: cv::pilote cv::d04 famille::raisonnement cv_id::CV-SIFT-002 provenance::agent pole::B pole::E
END

## CV-SIFT-003

Objectif : justifier la construction du descripteur. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-SIFT-003
Question: Une fois un keypoint SIFT localisé, comment construit-on son descripteur classique et que cherchent à stabiliser les étapes principales ?
Reponse: **Noyau attendu** : attribuer une orientation dominante, décrire les gradients dans un voisinage adapté à l'échelle et orienté, puis former $4\times4$ cellules à huit orientations, soit 128 composantes. Normaliser, écrêter les grandes composantes puis renormaliser.

**Approfondissement** : la représentation par histogrammes et l'interpolation réduisent la sensibilité à de petits déplacements. L'orientation et l'échelle donnent un repère local. La normalisation atténue certains changements de contraste, mais ne recrée pas les gradients perdus par saturation ou flou. Une structure à plusieurs orientations dominantes peut donner plusieurs descripteurs.

**Lecture de la représentation** : les composantes représentent une répartition de directions de gradient dans des cellules du voisinage, exprimées par rapport à l'orientation locale. Deux patches légèrement décalés peuvent conserver des histogrammes proches sans avoir des pixels identiques. Le découpage spatial maintient toutefois une information de disposition : un simple histogramme global perdrait davantage cette organisation.

**Exemple de limite** : une zone saturée peut rendre plusieurs intensités identiques et supprimer un bord. La normalisation du vecteur ne peut pas restaurer ce gradient absent. Pour diagnostiquer une chute de matching, distinguer alors keypoint non redétecté, orientation instable et descripteur peu distinctif. La dimension 128 explique la structure choisie, mais ne constitue pas une mesure de qualité du match ni une garantie d'identification.

**Erreurs bloquantes** : décrire 128 pixels bruts, ou prétendre que la normalisation garantit l'invariance à tout éclairage.
Source: [[40-features-matching/references/41-sift|Fiche SIFT]] ; [Lowe, §§5–6](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf).
Tags: cv::pilote cv::d04 famille::algorithme cv_id::CV-SIFT-003 provenance::agent pole::B pole::E
END

## CV-SIFT-004

Objectif : interpréter le ratio test. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-SIFT-004
Question: Deux descripteurs requêtes ont des distances L2 aux deux meilleurs voisins $(20,21)$ et $(35,80)$. Avec un ratio test à 0,8, lequel garder et que permet de conclure ce test ?
Reponse: **Noyau attendu** : rejeter le premier ($20/21\approx0,952$), garder le second ($35/80=0,4375$). Le test recherche un voisin nettement plus distinctif que son concurrent ; une petite distance absolue ne suffit pas.

**Approfondissement** : on vérifie $d_1<0,8d_2$ avec $d_1\le d_2$. Le choix du seuil relève de la validation. Même accepté, le match peut être faux dans une structure répétitive : une vérification géométrique reste nécessaire. Traiter explicitement l'absence de deux voisins et les distances toutes deux nulles.

**Lecture du test** : le premier candidat est proche en valeur absolue mais son concurrent l'est presque autant : la requête distingue mal les deux. Le second candidat est plus éloigné, mais nettement séparé de son concurrent. Le ratio compare cette ambiguïté relative et ne fournit pas une probabilité de correspondance correcte.

**Cas construit pour le réglage** : sur une texture répétitive, durcir le seuil peut éliminer une grande fraction des points et laisser trop peu de couverture pour l'homographie. Sur une image distinctive, un seuil trop permissif peut augmenter les faux candidats. Choisir donc le réglage sur le succès géométrique et les erreurs de projection, en conservant une référence exacte des deux voisins lorsque la recherche est approchée.

**Erreurs bloquantes** : garder automatiquement le match de distance 20, inverser le ratio, ou interpréter l'acceptation comme une vérité physique.
Source: [[40-features-matching/references/41-sift|Fiche SIFT]] ; [Lowe, §7.1](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf).
Tags: cv::pilote cv::d04 famille::pratique cv_id::CV-SIFT-004 provenance::agent pole::B pole::E
END

## CV-SIFT-005

Objectif : distinguer les limites des invariances. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-SIFT-005
Question: Un objet plan est d'abord tourné dans l'image, puis observé sous un angle très oblique. Pourquoi ces deux variations ne posent-elles pas le même problème à SIFT ?
Reponse: **Noyau attendu** : SIFT normalise explicitement une orientation et une échelle locales. Une forte vue oblique déforme le patch de façon affine/projective et peut modifier sa visibilité ; elle n'est pas compensée en général par une simple rotation et une échelle.

**Approfondissement** : les invariances recherchées restent limitées par la détection et l'échantillonnage. L'existence d'une homographie entre plans images ne signifie pas que le descripteur est invariant à cette homographie. Évaluer la plage angulaire réelle et comparer une stratégie adaptée si le taux de correspondances devient insuffisant.

**Décomposition géométrique** : une rotation dans le plan préserve la forme locale à une rotation près. Une vue oblique comprime différemment les directions du patch et peut faire apparaître ou disparaître certaines surfaces. Les gradients ne sont donc plus seulement exprimés dans une orientation différente ; leur arrangement peut changer.

**Test proposé** : prendre une étiquette plane, fixer éclairage et netteté, puis séparer rotation dans le plan et inclinaison de la caméra. Mesurer redétection et précision des correspondances pour chaque variation, au lieu d'un seul taux global. Une homographie peut décrire la projection du plan tout en étant difficile à estimer faute de matches fiables. Distinguer ainsi validité du modèle de scène et robustesse du descripteur évite de chercher le mauvais correctif.

**Erreurs bloquantes** : annoncer une invariance projective universelle ou déduire celle du descripteur de celle du modèle géométrique.
Source: [[40-features-matching/references/41-sift|Fiche SIFT]] ; [Lowe, résumé et §§5–6](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf).
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-SIFT-005 provenance::agent pole::B pole::E
END

## CV-SIFT-006

Objectif : diagnostiquer un consensus trompeur. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-SIFT-006
Question: Une façade répétitive donne beaucoup de matches SIFT et un fort taux d'inliers, mais la localisation est décalée d'une fenêtre. Quel diagnostic proposer et comment le vérifier ?
Reponse: **Noyau attendu** : la répétition peut produire des correspondances cohérentes mais sémantiquement décalées. Vérifier les positions des matches, la couverture et des points ou indices indépendants du consensus ; ne pas conclure à partir du nombre d'inliers seul.

**Approfondissement** : inspecter ratios et résidus, tester des zones distinctives ou une contrainte de position, puis valider la transformation sur des observations non utilisées. Une baisse de seuil peut retirer des outliers aléatoires sans résoudre une ambiguïté géométriquement cohérente. C'est un cas de raisonnement proposé, pas une expérience mesurée.

**Pourquoi RANSAC ne suffit pas ici** : ses résidus testent la cohérence avec un modèle, pas le sens du motif reconnu. Un décalage d'une période sur une façade peut produire un ensemble de paires qui soutient une autre transformation presque aussi bien. Ajouter davantage d'observations du même motif renforce éventuellement cette ambiguïté.

**Vérification indépendante construite** : choisir une enseigne, une bordure ou un point dont la position absolue est connue, sans l'utiliser pour l'ajustement initial. Comparer les transformations candidates sur cette observation, ainsi que sur la zone utile. Une contrainte de déplacement maximal peut aider si elle est justifiée par l'installation ; elle serait trompeuse si le mouvement réel dépasse ce domaine. Un faible résidu ne remplace donc pas l'identifiabilité du problème.

**Erreurs bloquantes** : affirmer qu'un consensus majoritaire garantit la bonne fenêtre ou prescrire plus de points sans test discriminant.
Source: [[40-features-matching/references/41-sift|Fiche SIFT]] ; [Lowe, §7](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf).
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-SIFT-006 provenance::agent pole::B pole::E
END

## CV-SIFT-007

Objectif : construire une comparaison sous contrainte. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-SIFT-007
Question: Pour choisir SIFT ou ORB sur une ligne industrielle avec recalage de pièces, quelles mesures rendent la comparaison utile au produit ?
Reponse: **Noyau attendu** : utiliser les mêmes paires représentatives et une géométrie de référence ; mesurer succès de recalage, erreurs, couverture et coût complet sur le matériel cible. Régler sur validation puis figer pour le test.

**Approfondissement** : stratifier par rotation, échelle, flou et lumière ; inclure extraction, matching et validation géométrique dans la latence et examiner les échecs rares. Les nombres de points ou les temps publiés sur un autre matériel ne suffisent pas. Le protocole est proposé ; aucun gagnant ni résultat industriel n'est annoncé ici.

**Critère produit proposé** : convertir l'erreur de recalage en conséquence métier, par exemple une région d'inspection décalée par rapport au défaut. Fixer une tolérance et compter les succès, refus et erreurs dangereuses. Deux méthodes aux résidus moyens voisins peuvent différer fortement sur les vues obliques ou les pièces peu texturées.

**Mesure complète** : consigner résolution, nombre de points et mêmes étapes incluses dans le chronométrage. Un extracteur plus rapide qui produit beaucoup de candidats ambigus peut déplacer le coût vers le matching et RANSAC. Examiner aussi mémoire et latence des cas difficiles. La bonne décision dépend du compromis observé sur le matériel cible et des conséquences d'un échec, pas d'une préférence générale pour une méthode classique ou binaire.

**Erreurs bloquantes** : choisir uniquement au nombre de matches ou comparer des temps qui n'incluent pas les mêmes étapes.
Source: [[40-features-matching/references/41-sift|Fiche SIFT]] ; [Lowe, §§6.2–6.4 et 8](https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf) ; [Rublee et al., §§4.4, 5.3 et 6.1](https://doi.org/10.1109/ICCV.2011.6126544).
Tags: cv::pilote cv::d04 famille::evaluation cv_id::CV-SIFT-007 provenance::agent pole::B pole::E
END
