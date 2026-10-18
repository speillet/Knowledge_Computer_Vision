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

**Erreurs bloquantes** : Déduire la précision 3D du seul résidu pixel.
Source: [[50-calibration-geometrie/references/53-epipolaire-pnp-triangulation|Fiche complète]] ; [OpenCV calib3d, E/F/recoverPose/triangulatePoints](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) ; [OpenCV solvePnP, conventions et variantes](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html).
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

**Erreurs bloquantes** : Confondre minimum théorique et contrat d’API.
Source: [[50-calibration-geometrie/references/53-epipolaire-pnp-triangulation|Fiche complète]] ; [OpenCV calib3d, E/F/recoverPose/triangulatePoints](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html) ; [OpenCV solvePnP, conventions et variantes](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html).
Tags: cv::pilote cv::d05 famille::pratique cv_id::CV-EPIPOLAIRE-005 provenance::agent pole::B pole::C
END
