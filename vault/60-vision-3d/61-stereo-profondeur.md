# Stéréo rectifiée, SGM et profondeur — cartes

Fiche : [[60-vision-3d/references/61-stereo-profondeur|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::60-vision-3d

## CV-STEREO-001

Objectif : calculer une profondeur rectifiée. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-STEREO-001
Question: En stéréo rectifiée horizontale avec points principaux de même abscisse, pour f=1000 px, baseline 0,2 m et disparité gauche−droite 20 px, quelle profondeur ?
Reponse: **Noyau attendu** : 10 m par $Z=fB/d$.

**Approfondissement** : À 10 px de disparité, on obtiendrait 20 m. La formule suppose une géométrie rectifiée compatible et une disparité valide ; f et d doivent être dans la même unité pixel.

**Dérivation d'unités** : le quotient $f/d$ est sans unité si les deux grandeurs utilisent les pixels de la même grille rectifiée ; le résultat conserve donc l'unité de la baseline. La différence de coordonnées traduit la séparation des deux rayons pour un point donné. Une faible disparité correspond ici à une grande profondeur.

**Exemple de contrôle** : vérifier une cible à distance connue, puis doubler artificiellement la valeur de la baseline dans le calcul : la profondeur calculée doublerait aussi. Cela aide à localiser une erreur d'échelle sans modifier le matcher. La formule simplifiée suppose les points principaux alignés comme annoncé et une disparité physique valide. Une région occultée ou un mauvais match peut produire un nombre positif sans profondeur correcte. En géométrie rectifiée plus générale, utiliser la transformation de reprojection et ses conventions plutôt qu'appliquer cette formule à toute sortie appelée disparité.

**Erreurs bloquantes** : Utiliser une baseline en millimètres et annoncer directement des mètres.
Source: [[60-vision-3d/references/61-stereo-profondeur|Fiche complète]] ; [OpenCV 4.13.0, stereoRectify et reprojectImageTo3D](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) ; calcul analytique du projet.
Tags: cv::pilote cv::d06 famille::raisonnement cv_id::CV-STEREO-001 provenance::agent pole::B pole::C
END

## CV-STEREO-002

Objectif : interpréter l’incertitude de profondeur. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-STEREO-002
Question: Pourquoi la précision de profondeur stéréo se dégrade-t-elle souvent à longue distance ?
Reponse: **Noyau attendu** : La sensibilité à la disparité croît comme $fB/d^2$ ; de petites erreurs de d deviennent de grandes erreurs de Z quand d est faible.

**Approfondissement** : Comparer une erreur de reprojection et une erreur métrique sur distances connues.

**Sensibilité analytique** : dériver $Z=fB/d$ donne $\partial Z/\partial d=-fB/d^2$. À petite erreur, la valeur absolue de cette dérivée convertit l'incertitude de disparité en incertitude de profondeur. Quand la distance double dans ce modèle, la disparité est divisée par deux et cette sensibilité est multipliée par quatre.

**Exemple construit** : avec $fB=200$ px·m et une erreur de disparité de 0,5 px, l'approximation donne environ 0,25 m à $d=20$ px et 1 m à $d=10$ px. Ces chiffres supposent un petit bruit et des correspondances correctes ; ils ne décrivent pas les outliers d'occultation. Comparer séparément biais, dispersion et taux de pixels invalides. Augmenter la baseline peut aider la géométrie, mais peut aussi rendre le matching et le recouvrement plus difficiles : la décision relie précision, visibilité et tâche.

**Erreurs bloquantes** : Supposer un bruit de profondeur constant pour toute distance.
Source: [[60-vision-3d/references/61-stereo-profondeur|Fiche complète]] ; [OpenCV 4.13.0, stereoRectify et reprojectImageTo3D](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) ; dérivation de Z=fB/d, à f et B fixés.
Tags: cv::pilote cv::d06 famille::raisonnement cv_id::CV-STEREO-002 provenance::agent pole::B pole::C
END

## CV-STEREO-003

Objectif : décoder une disparité fixe. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-STEREO-003
Question: Une reconstruction SGBM a une échelle fausse malgré une bonne calibration. Quel contrat numérique vérifier ?
Reponse: **Noyau attendu** : Le stockage de la disparité et son facteur d’échelle, notamment les quatre bits fractionnaires des sorties concernées ; convertir et masquer les invalides.

**Approfondissement** : Vérifier aussi baseline et Q avant de corriger arbitrairement les coordonnées finales.

**Piège de représentation** : un entier peut coder une valeur réelle avec des bits fractionnaires. Si la sortie concernée stocke seize fois la disparité, une valeur 320 représente 20 pixels et non 320 pixels. Comme la profondeur est inversement proportionnelle à la disparité dans le cas simple, interpréter 320 comme des pixels réduirait la profondeur d'un facteur seize.

**Enquête proposée** : inspecter type, valeurs valides, sentinelle d'invalidité et documentation de la fonction exacte. Reprojeter ensuite un point connu en vérifiant la matrice associée à la rectification et les unités de baseline. Ne pas multiplier simplement le nuage final pour cacher un défaut de contrat : cela pourrait laisser incohérents masques et autres grandeurs aval. Une bonne calibration géométrique ne protège pas d'une mauvaise conversion numérique de la sortie du matcher.

**Erreurs bloquantes** : Reprojeter des entiers fixes comme des pixels de disparité ordinaires.
Source: [[60-vision-3d/references/61-stereo-profondeur|Fiche complète]] ; [OpenCV 4.13.0, StereoSGBM, Detailed Description et create](https://docs.opencv.org/4.13.0/d2/d85/classcv_1_1StereoSGBM.html) ; [OpenCV 4.13.0, stereoRectify et reprojectImageTo3D](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d06 famille::diagnostic cv_id::CV-STEREO-003 provenance::agent pole::B pole::C
END

## CV-STEREO-004

Objectif : séparer rectification et matching. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-STEREO-004
Question: La rectification garantit-elle une correspondance correcte à chaque pixel ?
Reponse: **Noyau attendu** : Non : elle simplifie la géométrie de recherche ; texture, répétition et occlusion peuvent encore rendre le matching ambigu.

**Approfondissement** : La confiance et les masques invalides doivent être évalués, pas remplis par une profondeur fictive.

**Ce que la rectification change** : elle réorganise les images pour simplifier les lieux de recherche compatibles avec la géométrie. Elle ne crée pas de texture et ne rend pas visible une surface cachée dans l'une des caméras. La recherche le long d'une ligne peut donc encore contenir plusieurs candidats ou aucun correspondant réel.

**Exemple construit** : une surface uniforme offre des coûts proches pour beaucoup de disparités ; une texture périodique peut favoriser la mauvaise période ; au bord d'un objet, un point peut n'être vu que d'un côté. Une régularisation peut sélectionner une valeur dans ces régions, mais cette valeur n'est pas une nouvelle observation. Conserver une information de validité et tester les cohérences disponibles, puis évaluer sur une référence indépendante. Distinguer densité de la carte produite et quantité de profondeur réellement fiable évite d'interpréter tout pixel rempli comme une mesure.

**Erreurs bloquantes** : Déduire une profondeur fiable de la seule horizontalité des lignes épipolaires.
Source: [[60-vision-3d/references/61-stereo-profondeur|Fiche complète]] ; [OpenCV StereoSGBM, description et compute](https://docs.opencv.org/4.13.0/d2/d85/classcv_1_1StereoSGBM.html) ; [OpenCV reprojectImageTo3D](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d06 famille::comparaison cv_id::CV-STEREO-004 provenance::agent pole::B pole::C
END
