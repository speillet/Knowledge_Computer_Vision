# Exposition, bruit, couleur et échantillonnage — cartes

Fiche : [[20-acquisition-images/references/21-exposition-bruit-echantillonnage|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::20-acquisition-images

## CV-ACQUISITION-001

Objectif : calculer un flou simplifié. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-ACQUISITION-001
Question: Un détail se déplace à 800 px/s et l’exposition est de 5 ms. Quel flou prévoir dans le modèle de mouvement uniforme ?
Reponse: **Noyau attendu** : Environ 4 px : 800 × 0,005. Doubler l’exposition donnerait 8 px dans ce modèle.

**Approfondissement** : Le calcul exclut accélération, rotation et vibrations ; il sert à concevoir un test, pas à certifier une caméra.

**Erreurs bloquantes** : Mélanger ms et s ou conclure à une PSF universelle.
Source: [[20-acquisition-images/references/21-exposition-bruit-echantillonnage|Fiche complète]] ; [EMVA1288 Linear 4.0 (2021), §§2.1, 2.4, 2.6–2.7](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf) ; calcul cinématique du projet sous mouvement image uniforme.
Tags: cv::pilote cv::d02 famille::raisonnement cv_id::CV-ACQUISITION-001 provenance::agent pole::A pole::B pole::C pole::E pole::F
END

## CV-ACQUISITION-002

Objectif : distinguer gain et exposition. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-ACQUISITION-002
Question: Pourquoi augmenter le gain numérique ne remplace-t-il pas augmenter le nombre de photons ?
Reponse: **Noyau attendu** : Il amplifie la mesure déjà acquise, sans créer d’information photonique ni réparer la saturation.

**Approfondissement** : Exposition/éclairage peuvent augmenter le signal mais modifient flou, saturation ou contraintes physiques ; mesurer SNR et défauts utiles.

**Erreurs bloquantes** : Dire que tout gain améliore mécaniquement le SNR.
Source: [[20-acquisition-images/references/21-exposition-bruit-echantillonnage|Fiche complète]] ; [EMVA1288 Linear 4.0 (2021), §§2.1, 2.4, 2.6–2.7](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf).
Tags: cv::pilote cv::d02 famille::comparaison cv_id::CV-ACQUISITION-002 provenance::agent pole::A pole::B pole::C pole::E pole::F
END

## CV-ACQUISITION-003

Objectif : reconnaître aliasing et prétraitement incohérent. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-ACQUISITION-003
Question: Un motif fin change brutalement d’apparence après réduction de taille. Que vérifier avant d’incriminer le modèle ?
Reponse: **Noyau attendu** : Le filtrage avant décimation, l’échelle du motif et la convention de resize ; un sous-échantillonnage peut créer de fausses basses fréquences.

**Approfondissement** : Comparer des réductions contrôlées sur mire et garder la même chaîne en train/test/inférence.

**Erreurs bloquantes** : Supposer que plus de pixels du capteur garantissent le détail après tout resize.
Source: [[20-acquisition-images/references/21-exposition-bruit-echantillonnage|Fiche complète]] ; [OpenCV 4.13.0, Image Pyramids, Gaussian Pyramid](https://docs.opencv.org/4.13.0/d4/d1f/tutorial_pyramids.html).
Tags: cv::pilote cv::d02 famille::diagnostic cv_id::CV-ACQUISITION-003 provenance::agent pole::A pole::B pole::C pole::E pole::F
END

## CV-ACQUISITION-004

Objectif : contrôler une entrée image. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-ACQUISITION-004
Question: Quels contrôles d’image faire lorsqu’un modèle transféré échoue sans changement apparent de scène ?
Reponse: **Noyau attendu** : Vérifier ordre couleur, gamme/normalisation, gamma, bit depth, exposition et saturation dans la chaîne réellement reçue.

**Approfondissement** : Comparer numériquement une même image avant et après chaque étape, puis les contrats d’entraînement et d’exploitation.

**Erreurs bloquantes** : Se fier seulement à une visualisation autoscalée.
Source: [[20-acquisition-images/references/21-exposition-bruit-echantillonnage|Fiche complète]] ; [sRGB, §§A.7–A.8 et B.1, conversion linéaire et fonction de transfert](https://www.w3.org/Graphics/Color/srgb) ; [EMVA1288 Linear 4.0 (2021), §§2.1, 2.4, 2.6–2.7](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf) ; checklist de diagnostic du projet.
Tags: cv::pilote cv::d02 famille::pratique cv_id::CV-ACQUISITION-004 provenance::agent pole::A pole::B pole::C pole::E pole::F
END
