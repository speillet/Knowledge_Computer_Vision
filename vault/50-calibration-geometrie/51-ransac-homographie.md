# Cartes pilotes — RANSAC et homographie

Fiche : [[50-calibration-geometrie/references/51-ransac-homographie|RANSAC/homographie]]. Provenance : agent.

TARGET DECK: CV::Pilote::50-calibration-geometrie

## CV-HOMOGRAPHIE-001

Objectif : choisir un modèle géométrique. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-HOMOGRAPHIE-001
Question: Pour relier deux images, dans quelles situations une homographie globale est-elle un modèle approprié, et quelle variation la met généralement en défaut ?
Reponse: **Noyau attendu** : elle convient pour les points d'un même plan, ou une rotation pure de caméra dans le modèle perspective idéal. Une translation devant des profondeurs différentes crée généralement une parallaxe incompatible avec un seul modèle global.

**Approfondissement** : le rôle du capteur, de la distorsion et du prétraitement doit être cohérent avec ce modèle. Une homographie d'un plan particulier peut rester valable dans une scène 3D sans décrire les autres points. Selon le besoin, examiner modèle épipolaire, pose ou plusieurs plans.

**Exemple construit** : pour une étiquette plane rigide, ses points peuvent suivre une même transformation projective entre deux prises de vue, même si le fond est à une autre profondeur. Accepter cette homographie pour l'étiquette n'autorise pas à l'étendre au fond.

**Contrôle du modèle** : afficher les vecteurs de résidus par région. Si les erreurs sont structurées selon la profondeur sous translation, ajouter des tirages robustes ne crée pas le modèle 3D manquant. Si elles sont plutôt aléatoires et localisées sur quelques paires, des outliers ou une mauvaise localisation restent plausibles. La décision de modèle précède donc le réglage du seuil de consensus et se rapporte à la zone où l'alignement sera utilisé.

**Erreurs bloquantes** : dire qu'une homographie relie toujours deux photos quelconques ou que davantage de tirages RANSAC supprime la parallaxe.
Source: [[50-calibration-geometrie/references/51-ransac-homographie|Fiche homographie]] ; [OpenCV, géométrie de l'homographie](https://docs.opencv.org/4.13.0/d9/dab/tutorial_homography.html).
Tags: cv::pilote cv::d05 famille::comparaison cv_id::CV-HOMOGRAPHIE-001 provenance::agent pole::B pole::E
END

## CV-HOMOGRAPHIE-002

Objectif : relier degrés de liberté et dégénérescence. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-HOMOGRAPHIE-002
Question: Pourquoi quatre paires ne suffisent-elles pas toujours à estimer une homographie malgré ses huit degrés de liberté ?
Reponse: **Noyau attendu** : quatre paires fournissent le minimum de contraintes seulement en position générale. Une configuration colinéaire ou autrement dégénérée ne détermine pas le modèle ; presque dégénérée, elle peut le rendre instable.

**Approfondissement** : $H$ est une matrice $3\times3$ à un facteur près. Dans un ensemble minimal, éviter les triplets colinéaires dans chaque image. La normalisation des coordonnées améliore le conditionnement numérique sans recréer des contraintes absentes. Examiner aussi la couverture pour éviter une extrapolation fragile.

**Pourquoi le comptage ne suffit pas** : les contraintes doivent être indépendantes. Plusieurs points sur une même droite renseignent cette droite, mais ne fixent pas librement le comportement du plan dans les autres directions. Des points presque colinéaires peuvent donner une solution numérique tout en la rendant très sensible au bruit.

**Vérification proposée** : visualiser les points avant le solveur, examiner le rang après normalisation et contrôler la projection sur des observations réservées éloignées de l'ensemble minimal. Ajouter davantage de points concentrés dans la même zone peut conserver une mauvaise extrapolation. Le minimum algébrique explique quand une solution est envisageable ; le protocole de capture doit encore rendre cette solution informative et stable pour l'usage.

**Erreurs bloquantes** : compter neuf degrés de liberté indépendants ou affirmer que quatre matches quelconques garantissent une estimation exploitable.
Source: [[50-calibration-geometrie/references/51-ransac-homographie|Fiche homographie]] ; [OpenCV findHomography](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-HOMOGRAPHIE-002 provenance::agent pole::B pole::E
END

## CV-HOMOGRAPHIE-003

Objectif : reconstruire une itération robuste. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-HOMOGRAPHIE-003
Question: Décris une itération de RANSAC pour une homographie, puis l'étape utile après sélection du meilleur consensus.
Reponse: **Noyau attendu** : tirer un ensemble minimal non dégénéré, estimer un candidat, calculer un résidu sur toutes les paires, compter ou scorer les inliers selon un seuil explicite. Après sélection, réestimer sur les inliers et contrôler les résidus.

**Approfondissement** : le tirage protège de certains outliers au lieu de les inclure tous dans une estimation initiale. Le score, le résidu, le tirage et le raffinement varient selon les variantes. Contrôler le résultat sur la zone utile et des points non utilisés ; une étape de consensus ne prouve pas la validité du modèle physique.

**Rôle de chaque opération** : le petit tirage évite de faire entrer immédiatement tous les outliers dans le solveur ; le score sur l'ensemble compare l'explication apportée par les candidats ; le réajustement utilise davantage de mesures compatibles pour réduire la dépendance au seul échantillon initial.

**Exemple de limite** : une répétition régulière peut fournir un large ensemble de paires fausses mais cohérentes. Le meilleur consensus selon le score peut alors être le mauvais alignement physique. Après raffinement, vérifier couverture, sens du warp et points indépendants. Consigner aussi variante, seuil et budget pour reproduire un échec. Cette décomposition permet de distinguer manque de tirages, mauvaise géométrie et ambiguïté de scène, au lieu d'attribuer toute erreur au hasard du tirage.

**Erreurs bloquantes** : n'évaluer le candidat que sur les quatre points tirés ou traiter tout consensus comme la vérité terrain.
Source: [[50-calibration-geometrie/references/51-ransac-homographie|Fiche homographie]] ; [Fischler et Bolles, §II](https://www.sri.com/wp-content/uploads/2021/12/ransac-publication.pdf).
Tags: cv::pilote cv::d05 famille::algorithme cv_id::CV-HOMOGRAPHIE-003 provenance::agent pole::B pole::E
END

## CV-HOMOGRAPHIE-004

Objectif : interpréter le budget nominal de RANSAC. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-HOMOGRAPHIE-004
Question: Pour une homographie avec proportion supposée d'inliers $w=0,5$, pourquoi vise-t-on 72 tirages pour une confiance nominale de 0,99, et que signifie cette confiance ?
Reponse: **Noyau attendu** : un tirage de quatre points est tout-inlier avec probabilité $w^4$. Sous le modèle indépendant, demander $1-(1-w^4)^N\ge0,99$ donne
$$N=\left\lceil\frac{\log(1-0,99)}{\log(1-0,5^4)}\right\rceil=72.$$
La confiance concerne l'existence d'au moins un tirage tout-inlier, pas la vérité physique du résultat final.

**Approfondissement** : un échantillon tout-inlier peut rester dégénéré ; $w$ peut être mal estimé et les hypothèses de tirage imparfaites. Le budget est donc nominal. Une meilleure proportion d'inliers peut réduire fortement le coût : avec 0,8 dans le même calcul, neuf tirages suffisent.

**Lecture probabiliste** : l'événement contraire est de ne tirer aucun échantillon tout-inlier, avec probabilité nominale $(1-w^4)^N$. Le logarithme traduit la baisse de cet événement avec le budget. Une baisse de proportion d'inliers peut donc faire exploser le nombre de tentatives nécessaires.

**Décision pratique proposée** : améliorer les correspondances en amont peut réduire ce coût, mais un filtrage trop strict peut aussi dégrader leur couverture. Il faut mesurer les deux effets. Une structure répétitive cohérente ou un échantillon dégénéré n'entre pas dans la promesse simplifiée du calcul : même un grand budget ne garantit pas de distinguer une mauvaise hypothèse physique. La confiance d'arrêt et la validation du recalage sont deux informations différentes.

**Erreurs bloquantes** : annoncer 99 % de probabilité que la pose soit correcte, sans les hypothèses du calcul.
Source: [[50-calibration-geometrie/references/51-ransac-homographie|Fiche homographie]] ; [Fischler et Bolles, §II](https://www.sri.com/wp-content/uploads/2021/12/ransac-publication.pdf).
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-HOMOGRAPHIE-004 provenance::agent pole::B pole::E
END

## CV-HOMOGRAPHIE-005

Objectif : interpréter l'unité d'un seuil de résidu. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-HOMOGRAPHIE-005
Question: Un seuil RANSAC de trois pixels fonctionnait avant réduction de résolution. Pourquoi le conserver sans réflexion peut-il changer la sélection des inliers ?
Reponse: **Noyau attendu** : le résidu direct est mesuré dans le repère destination : $e=\|x'-\pi(H\tilde x)\|_2$. Une réduction de résolution change l'échelle des coordonnées, des erreurs et éventuellement du bruit de localisation ; trois pixels n'ont plus le même sens.

**Approfondissement** : conserver la transformation entre repères, revoir le seuil en lien avec l'incertitude réelle et vérifier résidus et taux de succès. En resize uniforme idéal de facteur $a$, les mêmes erreurs géométriques sont multipliées par $a$, mais réextraire les features peut aussi changer leur bruit. Un seuil plus large peut masquer un modèle erroné.

**Exemple d'échelle** : après un resize uniforme à la moitié, un écart géométrique de quatre pixels dans l'image initiale devient idéalement deux pixels dans la nouvelle. Conserver trois pixels devient alors plus permissif pour cet écart physique. Mais une extraction refaite à plus petite résolution peut modifier la localisation des features ; la simple multiplication du seuil n'est donc qu'un point de départ raisonné.

**Validation proposée** : conserver quelques correspondances connues à travers le changement de repère et comparer leurs résidus avant de relancer la détection. Cela isole la transformation de coordonnées de la qualité des nouvelles features. Revoir ensuite seuil et mesure de succès sur la zone utile, en annonçant clairement les unités.

**Erreurs bloquantes** : traiter le seuil comme une grandeur sans unité ou supposer que changer le seuil répare toute parallaxe.
Source: [[50-calibration-geometrie/references/51-ransac-homographie|Fiche homographie]] ; [OpenCV findHomography](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::pratique cv_id::CV-HOMOGRAPHIE-005 provenance::agent pole::B pole::E
END

## CV-HOMOGRAPHIE-006

Objectif : diagnostiquer un modèle extrapolé. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-HOMOGRAPHIE-006
Question: Une homographie a 90 % d'inliers, tous concentrés dans un coin, mais projette mal le bord opposé. Quelles vérifications distinguent qualité du consensus et qualité du recalage ?
Reponse: **Noyau attendu** : examiner couverture spatiale, conditionnement et erreur sur des points réservés répartis dans la zone utile. Le consensus peut être bon localement tout en contraignant mal l'extrapolation.

**Approfondissement** : comparer les estimations sur sous-ensembles, vérifier l'absence d'alignement et le modèle plan, puis rechercher des observations informatives ailleurs. Rapporter la région dans laquelle la précision est établie. Augmenter le seuil ou le nombre de tirages ne fournit pas les contraintes spatiales manquantes.

**Intuition d'extrapolation** : plusieurs transformations proches peuvent presque coïncider sur un petit voisinage et diverger loin de celui-ci. Les points du consensus établissent donc une précision locale ; le pourcentage d'inliers ne décrit pas l'étendue dans laquelle les paramètres sont bien contraints.

**Expérience construite** : réestimer avec différents sous-ensembles de la zone concentrée, puis projeter les mêmes coins périphériques. Si ces coins varient fortement malgré des résidus locaux faibles, rechercher des contraintes ailleurs ou limiter l'usage à la région validée. Une meilleure normalisation améliore le calcul, sans créer de support spatial supplémentaire. Le rapport devrait préciser région de confiance et erreurs observées, plutôt qu'annoncer une qualité globale sur toute l'image.

**Erreurs bloquantes** : déclarer le recalage validé sur le seul pourcentage d'inliers ou conclure automatiquement à un bug du descripteur.
Source: [[50-calibration-geometrie/references/51-ransac-homographie|Fiche homographie]] ; [OpenCV 4.13.0, homographie, Basic theory](https://docs.opencv.org/4.13.0/d9/dab/tutorial_homography.html) ; scénario de couverture et protocole de diagnostic proposés par le projet.
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-HOMOGRAPHIE-006 provenance::agent pole::B pole::E
END

## CV-HOMOGRAPHIE-007

Objectif : expliquer une incompatibilité de modèle. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-HOMOGRAPHIE-007
Question: Pour assembler un panorama pris avec translation, les points proches et lointains ont des résidus systématiquement différents. Que tester avant de rendre RANSAC plus tolérant ?
Reponse: **Noyau attendu** : tester une parallaxe due aux différentes profondeurs, donc l'inadéquation d'une homographie globale. Examiner les résidus par zone/profondeur et la géométrie de capture avant de modifier le seuil.

**Approfondissement** : un seul plan dominant peut expliquer une partie de l'image et laisser le reste incompatible. Selon le produit, changer la capture vers une rotation autour du centre optique, limiter la zone au plan utile ou choisir une reconstruction/modélisation adaptée. Un grand seuil peut seulement appeler « inliers » des points mal expliqués.

**Pourquoi le relief compte** : sous translation de caméra, le déplacement apparent dépend notamment de la profondeur. Des points proches et lointains peuvent exiger des déformations différentes, alors qu'une homographie globale impose une relation unique. Un consensus dominé par l'arrière-plan peut ainsi laisser un objet proche visiblement dédoublé.

**Ablation proposée** : sélectionner séparément des correspondances sur chaque plan, comparer leurs modèles et contrôler les résidus croisés. Si deux modèles locaux expliquent des groupes différents, cela soutient l'hypothèse de parallaxe sans prouver que toutes les associations soient correctes. Choisir ensuite une capture ou une modélisation adaptée au produit. Élargir le seuil mélange seulement davantage de groupes dans la même catégorie d'inliers et peut cacher la structure de l'erreur.

**Erreurs bloquantes** : promettre qu'un budget RANSAC suffisant supprimera les effets de relief sous translation.
Source: [[50-calibration-geometrie/references/51-ransac-homographie|Fiche homographie]] ; [OpenCV, conditions géométriques](https://docs.opencv.org/4.13.0/d9/dab/tutorial_homography.html).
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-HOMOGRAPHIE-007 provenance::agent pole::B pole::E
END
