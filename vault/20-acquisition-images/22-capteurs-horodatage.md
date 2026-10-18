# Capteurs, rolling shutter et synchronisation — cartes

Fiche : [[20-acquisition-images/references/22-capteurs-horodatage|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::20-acquisition-images

## CV-CAPTEURS-001

Objectif : séparer exposition et lecture rolling shutter. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-CAPTEURS-001
Question: Une exposition très courte suffit-elle à supprimer toute déformation rolling shutter ?
Reponse: **Noyau attendu** : Non : elle réduit le flou par ligne, mais les lignes peuvent encore représenter des instants différents.

**Approfondissement** : Mesurer durée de lecture, mouvement et type de shutter ; tester global shutter ou correction adaptée.

**Erreurs bloquantes** : Confondre netteté de chaque ligne et simultanéité de toute l’image.
Source: [[20-acquisition-images/references/22-capteurs-horodatage|Fiche complète]] ; [Basler, electronic shutter types](https://docs.baslerweb.com/electronic-shutter-types) ; [Forster, IMU preintegration §§IV–VI](https://dellaert.github.io/files/Forster16tro.pdf).
Tags: cv::pilote cv::d02 famille::comparaison cv_id::CV-CAPTEURS-001 provenance::agent pole::B pole::C pole::E pole::F
END

## CV-CAPTEURS-002

Objectif : estimer un décalage temporel spatial. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-CAPTEURS-002
Question: Deux capteurs voient un objet à 2 m/s avec 50 ms de décalage. Quel ordre de grandeur d’erreur temporelle en translation uniforme ?
Reponse: **Noyau attendu** : 0,10 m, avant effets de rotation et d’estimation.

**Approfondissement** : Le calcul sert à départager timing et bruit spatial ; annoncer l’horloge et le mouvement supposés.

**Erreurs bloquantes** : Utiliser ce modèle pour toute scène en rotation sans autre hypothèse.
Source: [[20-acquisition-images/references/22-capteurs-horodatage|Fiche complète]] ; [Basler, electronic shutter types](https://docs.baslerweb.com/electronic-shutter-types) ; [Forster, IMU preintegration §§IV–VI](https://dellaert.github.io/files/Forster16tro.pdf).
Tags: cv::pilote cv::d02 famille::raisonnement cv_id::CV-CAPTEURS-002 provenance::agent pole::B pole::C pole::E pole::F
END

## CV-CAPTEURS-003

Objectif : départager calibration et temps. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-CAPTEURS-003
Question: Cas C — diagnostic : les obstacles caméra–LiDAR se dédoublent en virage mais semblent alignés à l’arrêt. Quelle enquête mener ?
Reponse: **Noyau attendu** : Vérifier offsets/dérive des horloges, temps par point du scan, deskew puis extrinsèques dans le même repère. Comparer séquences immobiles et mouvements contrôlés.

**Approfondissement** : Le mouvement rend visible un défaut temporel ; une calibration spatiale peut aussi être fausse. Mesurer résidus selon vitesse et rotation avant de choisir une correction.

**Erreurs bloquantes** : Corriger définitivement par une translation fixe sans examiner les timestamps.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[20-acquisition-images/references/22-capteurs-horodatage|Fiche complète]] ; [Basler, electronic shutter types](https://docs.baslerweb.com/electronic-shutter-types) ; [Forster, IMU preintegration §§IV–VI](https://dellaert.github.io/files/Forster16tro.pdf).
Tags: cv::pilote cv::d02 famille::diagnostic cv_id::CV-CAPTEURS-003 provenance::agent pole::B pole::C pole::E pole::F cas_pole::C::diagnostic
END

## CV-CAPTEURS-004

Objectif : interpréter les sorties de capteurs. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-CAPTEURS-004
Question: Pourquoi une mesure Doppler radar ne se substitue-t-elle pas directement à une vitesse cartésienne 3D ?
Reponse: **Noyau attendu** : Elle contraint la composante radiale relativement au capteur selon son modèle de mesure.

**Approfondissement** : Transformer repères et mouvement ego, puis fusionner d’autres observations pour les composantes non mesurées. Les covariances doivent suivre la transformation.

**Erreurs bloquantes** : Prendre une vitesse radiale pour les trois composantes du mouvement.
Source: [[20-acquisition-images/references/22-capteurs-horodatage|Fiche complète]] ; [Basler, electronic shutter types](https://docs.baslerweb.com/electronic-shutter-types) ; [Forster, IMU preintegration §§IV–VI](https://dellaert.github.io/files/Forster16tro.pdf).
Tags: cv::pilote cv::d02 famille::comprehension cv_id::CV-CAPTEURS-004 provenance::agent pole::B pole::C pole::E pole::F
END
