# Calibration multicapteurs, hand-eye et temps — cartes

Fiche : [[50-calibration-geometrie/references/55-calibration-multicapteurs|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::50-calibration-geometrie

## CV-MULTICALIB-001

Objectif : interpréter hand-eye. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-MULTICALIB-001
Question: Pourquoi écrire $AX=XB$ ne suffit-il pas à appliquer une calibration hand-eye ?
Reponse: **Noyau attendu** : Il faut définir les repères, les mouvements relatifs A/B, leur sens et la transformation inconnue X.

**Approfondissement** : Vérifier une chaîne de transformations sur un point et des mouvements réservés ; des conventions différentes donnent des équations différentes.

**Erreurs bloquantes** : Copier les matrices d’une API sans vérifier leur sens.
Source: [[50-calibration-geometrie/references/55-calibration-multicapteurs|Fiche complète]] ; [OpenCV calib3d, calibrateHandEye et robot-world hand-eye](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::raisonnement cv_id::CV-MULTICALIB-001 provenance::agent pole::B pole::C pole::E
END

## CV-MULTICALIB-002

Objectif : évaluer des mouvements informatifs. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-MULTICALIB-002
Question: De nombreuses poses robot sur un même axe donnent une extrinsèque instable. Que changer ?
Reponse: **Noyau attendu** : Examiner l’observabilité et varier les rotations/positions qui contraignent les composantes manquantes.

**Approfondissement** : Comparer stabilité et validation sur une autre trajectoire, sans considérer le nombre brut de poses comme preuve.

**Erreurs bloquantes** : Répondre seulement « plus d’images » sans diversité de mouvement.
Source: [[50-calibration-geometrie/references/55-calibration-multicapteurs|Fiche complète]] ; [OpenCV calib3d, calibrateHandEye et robot-world hand-eye](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::diagnostic cv_id::CV-MULTICALIB-002 provenance::agent pole::B pole::C pole::E
END

## CV-MULTICALIB-003

Objectif : séparer intrinsèques extrinsèques et temps. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-MULTICALIB-003
Question: Pourquoi une faible reprojection intrinsèque ne valide-t-elle pas une fusion caméra–LiDAR en mouvement ?
Reponse: **Noyau attendu** : Elle ne teste pas à elle seule l’extrinsèque entre capteurs, leur offset temporel ou la déformation du scan.

**Approfondissement** : Valider séparément puis conjointement sur mouvements et scènes adaptés.

**Erreurs bloquantes** : Assimiler qualité d’une calibration caméra et qualité complète de fusion.
Source: [[50-calibration-geometrie/references/55-calibration-multicapteurs|Fiche complète]] ; [OpenCV calib3d, calibrateHandEye et robot-world hand-eye](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
Tags: cv::pilote cv::d05 famille::comparaison cv_id::CV-MULTICALIB-003 provenance::agent pole::B pole::C pole::E
END
