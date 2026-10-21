# Recalage par intensités et ECC — cartes

Fiche : [[40-features-matching/references/45-recalage-ecc|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::40-features-matching

## CV-ECC-001

Objectif : choisir matching ou optimisation photométrique. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-ECC-001
Question: Quel contrat distingue ECC d’un pipeline SIFT + RANSAC ?
Reponse: **Noyau attendu** : ECC optimise un critère d’intensité sur un warp initialisé ; SIFT propose des paires puis une géométrie robuste.

**Approfondissement** : Bassin de convergence, recouvrement et invariances diffèrent ; ils peuvent être combinés pour initialisation et raffinement.

**Erreurs bloquantes** : Décrire ECC comme un descripteur sparse.
Source: [[40-features-matching/references/45-recalage-ecc|Fiche complète]] ; [OpenCV 4.13.0, findTransformECC, modèle, initialisation et inverse warping](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html).
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-ECC-001 provenance::agent pole::B pole::E
END

## CV-ECC-002

Objectif : interpréter une convergence ECC. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-ECC-002
Question: ECC converge avec forte corrélation sur une grille répétitive mais le déplacement est faux. Comment valider ?
Reponse: **Noyau attendu** : Comparer à des points/structures réservés et aux contraintes de mouvement ; la corrélation peut avoir plusieurs maxima.

**Approfondissement** : Inspecter initialisation, recouvrement et sens du warp.

**Erreurs bloquantes** : Prendre convergence numérique pour vérité physique.
Source: [[40-features-matching/references/45-recalage-ecc|Fiche complète]] ; [OpenCV 4.13.0, findTransformECC, modèle, initialisation et inverse warping](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html) ; cas répétitif et protocole de validation déduits par le projet.
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-ECC-002 provenance::agent pole::B pole::E
END

## CV-ECC-003

Objectif : choisir un modèle de mouvement. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-ECC-003
Question: Pourquoi ne pas choisir systématiquement une homographie dans un recalage ECC ?
Reponse: **Noyau attendu** : Plus de paramètres peuvent surajuster ou réduire la stabilité alors qu’une translation ou un affine suffit au besoin.

**Approfondissement** : Le modèle doit expliquer la capture et être validé sur des observations indépendantes.

**Erreurs bloquantes** : Assimiler flexibilité maximale et précision maximale.
Source: [[40-features-matching/references/45-recalage-ecc|Fiche complète]] ; [OpenCV 4.13.0, findTransformECC, modèle, initialisation et inverse warping](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html) ; compromis entre flexibilité et stabilité déduit par le projet.
Tags: cv::pilote cv::d04 famille::pratique cv_id::CV-ECC-003 provenance::agent pole::B pole::E
END
