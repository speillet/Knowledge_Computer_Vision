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

**Mécanisme concret** : dans un voisinage où la plupart des intensités valent environ 100 et une valeur vaut 255, une moyenne propage l'influence de cette impulsion à sa sortie, tandis qu'une médiane peut rester proche du niveau majoritaire. En revanche, une rayure réelle très fine peut elle aussi devenir minoritaire dans le voisinage et disparaître. Le filtre ne sait pas distinguer une impulsion parasite d'un défaut utile sur leur seule taille.

**Choix proposé** : comparer plusieurs supports sur un lot contenant bruit, bords et détails critiques. Garder identiques les étapes aval, puis mesurer défauts manqués et erreurs de localisation. Un support plus grand augmente l'échelle de modification de l'image. Le médian ne se décrit pas comme une convolution linéaire ; le Gaussien réalise une moyenne pondérée dont le comportement fréquentiel aide à construire des pyramides. Ces différences expliquent le choix, sans établir de classement universel.

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

**Dérivation** : le poids photométrique dépend du rapport $|I(p)-I(q)|/\sigma_r$. Si l'intensité et $\sigma_r$ sont divisés par la même constante positive, ce rapport reste identique et donc le poids associé aussi, à support et calcul numérique inchangés. Modifier uniquement l'intensité rend les écarts relativement plus petits : davantage de voisins deviennent photométriquement semblables.

**Exemple construit** : un écart de 20 niveaux comparé à un sigma de 10 représente deux sigma. Après division par 255, l'écart vaut environ 0,0784 et le sigma cohérent environ 0,0392 ; le rapport reste deux. Conserver un sigma de 10 dans cette nouvelle plage écrase cette distinction. Cette équivalence suppose une transformation linéaire de l'intensité : un gamma ou un changement d'espace couleur ne se traite pas par une simple division commune. Le sigma spatial et les conventions de bord restent séparés.

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

**Origine du paradoxe** : le PSNR résume une erreur de reconstruction sur l'ensemble des pixels. Une grande zone de fond mieux débruitée peut dominer cette mesure, alors qu'une petite rayure, pourtant décisive pour le métier, est effacée. Améliorer la ressemblance moyenne à une référence ne garantit donc pas de préserver le signal que le détecteur doit utiliser.

**Expérience proposée** : comparer les pipelines avec et sans filtre sur les mêmes pièces et annotations, en isolant rayures fines, faibles contrastes et zones texturées. Faire varier uniquement le filtre et son échelle, puis examiner faux négatifs, faux positifs et localisation, à un point de fonctionnement explicite. Conserver quelques profils d'intensité avant/après sur les détails ratés. Si l'image paraît plus propre mais le rappel baisse, le filtre introduit un compromis défavorable à cette tâche. Le test réservé ne sert pas à choisir indéfiniment les paramètres.

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

**Chaîne de raisonnement** : réduire la grille diminue la fréquence spatiale maximale représentable. Une alternance rapide d'intensités peut alors être interprétée comme un motif plus lent si l'on décime directement. Le lissage préalable atténue les composantes incompatibles avec la nouvelle grille ; la décimation réduit ensuite le nombre d'échantillons. Le préfiltre choisit donc ce qui est conservé avant la perte de résolution.

**Conséquence pour le matching** : les gradients et extrema utilisés comme features changent si la texture est repliée. Deux vues du même objet peuvent produire des descripteurs instables simplement à cause du rééchantillonnage. Dans un test construit, comparer le nombre de correspondances géométriquement vérifiées sur une mire réduite avec et sans préfiltre, à détecteur constant. Une meilleure stabilité ne constitue pas une invariance parfaite à l'échelle : un détail trop petit finit par disparaître même avec une pyramide correctement filtrée.

**Erreurs bloquantes** : Confondre sous-échantillonnage et perte contrôlée d’information.
Source: [[30-traitement-image/references/31-filtrage-gradients|Fiche complète]] ; [OpenCV 4.13.0, Image Pyramids, Gaussian Pyramid](https://docs.opencv.org/4.13.0/d4/d1f/tutorial_pyramids.html).
Tags: cv::pilote cv::d03 famille::comprehension cv_id::CV-FILTRES-004 provenance::agent pole::A pole::B pole::E pole::F
END
