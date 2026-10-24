# Épipolaire, PnP et triangulation — cartes

Fiche : [[50-calibration-geometrie/references/53-epipolaire-pnp-triangulation|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::50-calibration-geometrie

## CV-EPIPOLAIRE-001

Objectif : distinguer E et F. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-EPIPOLAIRE-001
Question: Quelles coordonnées distinguent matrice essentielle et fondamentale ?
Reponse: **Noyau attendu** : E agit sur coordonnées caméra normalisées idéales ; F sur pixels idéaux avec intrinsèques absorbés.

**Approfondissement** : Corriger ou modéliser la distorsion ; utiliser les bonnes matrices et le sens de pose annoncé.

**Écriture cohérente** : pour $X_2=RX_1+t$, l'essentielle vaut $E=[t]_\times R$. La contrainte $x_2^TEx_1=0$ s'écrit avec des coordonnées normalisées idéales ; en pixels idéaux, $F=K_2^{-T}EK_1^{-1}$ absorbe les deux matrices intrinsèques. Le symbole homogène implique aussi une convention de normalisation.

**Exemple de contrôle** : si les points ont été undistordus vers des coordonnées normalisées, les réinjecter dans une fondamentale associée à d'autres matrices pixel mélange deux contrats. Vérifier un point connu et son lieu épipolaire avant d'interpréter le score. Un produit scalaire algébrique proche de zéro n'est pas directement une erreur euclidienne en pixels : le choix du résidu et de son seuil doit être explicité. La matrice choisie décrit la relation entre vues ; elle ne corrige pas implicitement toutes les distorsions ni les transformations de prétraitement appliquées ensuite.

**Erreurs bloquantes** : Appliquer E directement à des pixels bruts comme une règle universelle.
Source: [[50-calibration-geometrie/references/53-epipolaire-pnp-triangulation|Fiche complète]] ; [OpenCV calib3d, E/F/recoverPose/triangulatePoints](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) ; [OpenCV solvePnP, conventions et variantes](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html).
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-EPIPOLAIRE-001 provenance::agent pole::B pole::C
END

## CV-EPIPOLAIRE-002

Objectif : interpréter l’échelle de translation. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-EPIPOLAIRE-002
Question: Une pose récupérée depuis une essentielle monoculaire donne-t-elle directement la distance entre caméras en mètres ?
Reponse: **Noyau attendu** : Non : les deux vues seules donnent une direction et une reconstruction à une échelle près dans le cas général.

**Approfondissement** : Une mesure métrique supplémentaire, une baseline connue ou un capteur peut fixer l’échelle sous ses hypothèses.

**Ambiguïté d'échelle** : multiplier toutes les distances de la reconstruction et la translation entre caméras par la même constante positive peut laisser les projections identiques. Les images monoculaires ne distinguent donc pas ces scènes uniquement par cette géométrie. Une normalisation du vecteur de translation choisit une représentation commode de sa direction.

**Exemple construit** : deux reconstructions séparées d'un facteur dix peuvent expliquer les mêmes pixels. Interpréter arbitrairement la norme unitaire comme un mètre donne alors une vitesse et des dimensions arbitraires. Une baseline connue, un objet de dimension connue ou une fusion inertielle suffisamment informative peut fournir une contrainte supplémentaire, selon son modèle. Vérifier aussi parallaxe, ambiguïtés de pose et qualité des correspondances : fixer une échelle n'améliore pas automatiquement les autres composantes de l'estimation. La validation métrique doit citer la source réelle de cette information.

**Erreurs bloquantes** : Présenter la norme unitaire de t comme un mètre.
Source: [[50-calibration-geometrie/references/53-epipolaire-pnp-triangulation|Fiche complète]] ; [OpenCV calib3d, E/F/recoverPose/triangulatePoints](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) ; [OpenCV solvePnP, conventions et variantes](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html).
Tags: cv::pilote cv::d05 famille::comprehension cv_id::CV-EPIPOLAIRE-002 provenance::agent pole::B pole::C
END

## CV-EPIPOLAIRE-003

Objectif : choisir PnP ou triangulation. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-EPIPOLAIRE-003
Question: PnP et triangulation résolvent-ils la même inconnue ?
Reponse: **Noyau attendu** : PnP estime la pose à partir de points 3D et observations 2D ; la triangulation estime les points à partir de plusieurs poses/vues.

**Approfondissement** : Les deux peuvent s’enchaîner dans SfM et être affinés par BA ; les jauges et unités doivent rester cohérentes.

**Tableau mental des inconnues** : PnP utilise une carte de points 3D déjà exprimés dans un repère, puis cherche comment les projeter dans la caméra. La triangulation suppose des vues et leurs poses connues, puis cherche où se situe un point compatible avec les rayons observés. Le bundle adjustment peut ensuite ajuster ces deux types de variables ensemble.

**Exemple construit** : localiser une caméra devant une pièce CAO avec des points identifiés est un problème 3D–2D. Reconstruire le coin d'une pièce depuis deux caméras calibrées est un problème de triangulation. Dans les deux cas, une mauvaise association peut produire une solution numérique sans valeur physique. Conserver les unités des points connus, le sens des poses et les contrôles de visibilité. Une chaîne SfM peut alterner les opérations, mais cela ne rend pas leurs entrées ou leurs ambiguïtés interchangeables.

**Erreurs bloquantes** : Inverser les entrées et les inconnues sans le signaler.
Source: [[50-calibration-geometrie/references/53-epipolaire-pnp-triangulation|Fiche complète]] ; [OpenCV calib3d, E/F/recoverPose/triangulatePoints](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) ; [OpenCV solvePnP, conventions et variantes](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html).
Tags: cv::pilote cv::d05 famille::comparaison cv_id::CV-EPIPOLAIRE-003 provenance::agent pole::B pole::C
END

## CV-EPIPOLAIRE-004

Objectif : détecter une faible parallaxe. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-EPIPOLAIRE-004
Question: Pourquoi un point triangulé peut-il avoir une faible erreur de reprojection et une profondeur très incertaine ?
Reponse: **Noyau attendu** : Avec des rayons presque parallèles, plusieurs grandes profondeurs produisent des projections proches.

**Approfondissement** : Mesurer angle de parallaxe, sensibilité et référence 3D ; une meilleure baseline peut ajouter l’information manquante.

**Intuition de conditionnement** : deux rayons qui se coupent avec un angle très faible définissent leur intersection en profondeur de manière fragile. Une petite variation angulaire, issue du bruit de localisation, déplace beaucoup le point tout en modifiant peu ses projections. Ce mécanisme est analogue à une direction de paramètres peu contrainte dans un système linéaire.

**Protocole construit** : conserver le bruit image et comparer plusieurs distances ou baselines connues. Mesurer erreur de profondeur, angle entre rayons et résidus séparément. Rejeter ou signaler les points presque sans parallaxe plutôt que les considérer fiables parce que leur reprojection est bonne. Une plus grande baseline peut apporter de l'information, mais aussi rendre les correspondances plus difficiles ou provoquer des occultations ; son choix est donc un compromis de système. Vérifier également que les points sont devant les caméras et que l'échelle utilisée est réellement métrique.

**Erreurs bloquantes** : Déduire la précision 3D du seul résidu pixel.
Source: [[50-calibration-geometrie/references/53-epipolaire-pnp-triangulation|Fiche complète]] ; [OpenCV 4.13.0, decomposeEssentialMat, recoverPose, solveP3P et triangulatePoints](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) ; sensibilité à faible parallaxe : déduction géométrique du projet.
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-EPIPOLAIRE-004 provenance::agent pole::B pole::C
END

## CV-EPIPOLAIRE-005

Objectif : respecter la variante minimale de pose. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-EPIPOLAIRE-005
Question: Pourquoi le slogan « P3P = appeler solvePnP avec trois points quelconques » est-il trompeur ?
Reponse: **Noyau attendu** : Le problème peut avoir plusieurs solutions, les configurations peuvent être dégénérées et l’API sélectionnée peut demander un quatrième point.

**Approfondissement** : Nommer la variante, vérifier son contrat puis raffiner et tester la chiralité.

**Différence entre problème et fonction** : une formulation minimale indique combien de correspondances peuvent suffire sous des hypothèses géométriques. Une fonction peut ajouter une observation pour sélectionner une solution, retourner plusieurs hypothèses ou imposer d'autres contraintes de données. Son nom ne remplace donc pas la lecture du contrat de la variante utilisée.

**Protocole proposé** : consigner méthode et version, vérifier nombre et configuration des points, puis examiner les poses candidates avec des observations supplémentaires. Contrôler résidus, visibilité et plausibilité du mouvement dans les repères annoncés. Des points dégénérés ou presque dégénérés peuvent rester peu informatifs même si le nombre demandé est satisfait. Dans une application critique pour la précision, utiliser aussi des points réservés et un raffinement approprié. Ce raisonnement évite de confondre minimum algébrique, appel d'API réussi et pose effectivement validée dans la scène réelle.

**Erreurs bloquantes** : Confondre minimum théorique et contrat d’API.
Source: [[50-calibration-geometrie/references/53-epipolaire-pnp-triangulation|Fiche complète]] ; [OpenCV 4.13.0, solvePnP, Pose computation methods et P3P](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html) ; [OpenCV 4.13.0, decomposeEssentialMat, recoverPose, solveP3P et triangulatePoints](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::pratique cv_id::CV-EPIPOLAIRE-005 provenance::agent pole::B pole::C
END
