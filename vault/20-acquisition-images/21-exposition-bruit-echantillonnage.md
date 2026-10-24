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

**Lecture physique et exemple construit** : le pixel reçoit de la lumière pendant toute l'exposition ; il additionne donc les positions successives du détail. Le produit $v_{px}t_e$ est une longueur dans l'image, pas une distance dans le monde. Pour un défaut large de deux pixels, une traînée de quatre pixels peut mélanger son signal avec le fond, même si l'image conserve une luminosité convenable. Une compensation du déplacement entre frames ne restitue pas automatiquement ce mélange à l'intérieur d'une frame.

**Décision sous contrainte** : pour viser au plus un pixel de déplacement avec la même vitesse, le modèle donne $t_e\le1/800$ s, soit 1,25 ms. C'est un budget analytique, pas une garantie de détection. Réduire l'exposition oblige à reconsidérer l'éclairage et le bruit. Mesurer le mouvement dans la zone utile : une vitesse moyenne sur toute l'image peut masquer un détail plus rapide.

**Erreurs bloquantes** : Mélanger ms et s ou conclure à une PSF universelle.
Source: [[20-acquisition-images/references/21-exposition-bruit-echantillonnage|Fiche complète]] ; [EMVA1288 Linear 4.0 (2021), §§2.1, 2.4, 2.6–2.7](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf) ; calcul cinématique du projet sous mouvement image uniforme.
Tags: cv::pilote cv::d02 famille::raisonnement cv_id::CV-ACQUISITION-001 provenance::agent pole::A pole::B pole::C pole::E pole::F
END

## CV-ACQUISITION-002

Objectif : distinguer gain et exposition. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-ACQUISITION-002
Question: Une image de contrôle est trop sombre. On peut doubler le gain de la caméra, ou doubler la lumière reçue en allongeant l’exposition ou en renforçant l’éclairage. Que change chacun des deux réglages pour le SNR, le flou et la saturation ?
Reponse: **Noyau attendu** : doubler la lumière double les photoélectrons et augmente le SNR : d’un facteur $\sqrt2$ quand le bruit photonique domine, jusqu’à 2 quand le bruit de lecture domine ; une exposition plus longue augmente aussi le flou de bougé. Doubler le gain multiplie signal et bruit déjà acquis : hors bruit de quantification, le SNR ne change pas, et la valeur numérique maximale est atteinte avec deux fois moins d’électrons, ce qui réduit la dynamique. Le gain ne crée pas d’information photonique et ne répare pas une saturation.

**Approfondissement** : selon EMVA 1288, $\mathrm{SNR}=\eta\mu_p/\sqrt{\sigma_d^2+\sigma_q^2/K^2+\eta\mu_p}$ : le gain système $K$ ne joue que par la quantification. $\eta$ est le rendement quantique, $\mu_p$ le nombre moyen de photons reçus par pixel pendant l’exposition ; $\eta\mu_p$ est le nombre moyen de photoélectrons. $K$ est le gain système en DN/e⁻, et $\sigma_q^2$ la variance de quantification en DN². Le modèle suppose une réponse linéaire non saturée à un point de fonctionnement fixé.  Exemple du projet avec un bruit de lecture $\sigma_d=5$ e⁻ : 100 e⁻ donnent un SNR de 8,9, 200 e⁻ un SNR de 13,3, et doubler $K$ laisse 8,9. Renforcer l’éclairage plutôt que l’exposition double le signal sans allonger le flou. Le modèle décrit un point de fonctionnement : mesurer le SNR à chaque réglage réellement utilisé.

**Lien avec le choix d'acquisition** : commencer par vérifier si le défaut utile est limité par le manque de photons, par le mouvement ou par une zone saturée. Dans le premier cas, renforcer l'éclairage peut aider ; dans le second, allonger l'exposition peut détruire le détail ; dans le troisième, amplifier davantage aggrave l'écrêtage. Ce diagnostic conduit à comparer les réglages sur les pixels critiques, et pas seulement sur la moyenne de luminosité de l'image.

**Erreurs bloquantes** : dire que tout gain améliore le SNR ; oublier qu’une exposition plus longue augmente le flou.
Source: [[20-acquisition-images/references/21-exposition-bruit-echantillonnage|Fiche complète]] ; [EMVA1288 Linear 4.0 (2021), §2.4, équations 13–14, §2.6, équations 21–22, et §2.7](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf) ; exemple chiffré du projet.
Tags: cv::pilote cv::d02 famille::comparaison cv_id::CV-ACQUISITION-002 provenance::agent pole::A pole::B pole::C pole::E pole::F
END

## CV-ACQUISITION-003

Objectif : reconnaître aliasing et prétraitement incohérent. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-ACQUISITION-003
Question: Un motif fin change brutalement d’apparence après réduction de taille. Que vérifier avant d’incriminer le modèle ?
Reponse: **Noyau attendu** : Le filtrage avant décimation, l’échelle du motif et la convention de resize ; un sous-échantillonnage peut créer de fausses basses fréquences.

**Approfondissement** : sans préfiltre adapté au facteur de réduction, les hautes fréquences se replient dans l'image réduite. Parmar et al. observent de l’aliasing pour les configurations OpenCV, TensorFlow et PyTorch évaluées en 2022, face aux filtres adaptatifs de PIL. Ce constat dépend de l’API, de la version et des options ; `torchvision.transforms.Resize` 0.24 active par défaut l’antialiasing, contrairement à ses anciennes versions. Vérifier interpolation, facteur de réduction et antialiasing dans les deux chaînes. Comparer des réductions contrôlées sur mire et garder la même chaîne en train/test/inférence.

**Exemple interprété** : un motif alternant des bandes claires et sombres peut devenir uniforme ou produire des bandes plus larges selon la phase d'échantillonnage. Le réseau voit alors un nouveau motif qui n'existait pas dans la scène. Un filtre préalable atténue les fréquences incompatibles avec la grille finale, au prix d'une perte de détail. Ajouter ensuite une interpolation plus sophistiquée ne reconstruit pas l'information déjà repliée.

**Contrôle discriminant proposé** : comparer plusieurs phases du même motif et plusieurs facteurs de réduction, en gardant le réseau et les annotations fixes. Si les prédictions changent surtout avec la phase de resize, examiner la chaîne d'image avant d'ajouter des augmentations. L'objectif est de conserver un signal utile et cohérent, pas de rendre toute image visuellement plus lisse.

**Erreurs bloquantes** : Supposer que plus de pixels du capteur garantissent le détail après tout resize.
Source: [[20-acquisition-images/references/21-exposition-bruit-echantillonnage|Fiche complète]] ; [Parmar, Zhang et Zhu 2022, On Aliased Resizing and Surprising Subtleties in GAN Evaluation, CVPR, §§1, 2, 3.2 et 6.3](https://arxiv.org/abs/2104.11222) ; [torchvision 0.24, Resize, antialias](https://docs.pytorch.org/vision/0.24/generated/torchvision.transforms.Resize.html) ; [OpenCV 4.13.0, Image Pyramids, Gaussian Pyramid](https://docs.opencv.org/4.13.0/d4/d1f/tutorial_pyramids.html).
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

**Pourquoi ces contrôles départagent les causes** : deux tableaux de même forme peuvent représenter des couleurs ou des quantités physiques différentes. Un canal rouge interprété comme bleu change les contrastes appris ; une division supplémentaire par 255 modifie l'échelle ; un passage en entier peut écrêter des valeurs. Une visualisation qui ajuste automatiquement son contraste peut rendre ces tableaux presque identiques à l'œil.

**Enquête reproductible proposée** : choisir une image témoin, conserver son fichier original et relever, à chaque étape, forme, type, minimum, maximum et valeurs de quelques pixels connus. Comparer ensuite le tenseur effectivement reçu par le modèle avec celui de la chaîne d'entraînement. Tester une seule correction à la fois. Une amélioration après remise en conformité soutient une cause de prétraitement ; elle ne dispense pas d'évaluer les autres images et les cas difficiles du nouveau capteur.

**Erreurs bloquantes** : Se fier seulement à une visualisation autoscalée.
Source: [[20-acquisition-images/references/21-exposition-bruit-echantillonnage|Fiche complète]] ; [sRGB, §§A.7–A.8 et B.1, conversion linéaire et fonction de transfert](https://www.w3.org/Graphics/Color/srgb) ; [EMVA1288 Linear 4.0 (2021), §§2.1, 2.4, 2.6–2.7](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf) ; checklist de diagnostic du projet.
Tags: cv::pilote cv::d02 famille::pratique cv_id::CV-ACQUISITION-004 provenance::agent pole::A pole::B pole::C pole::E pole::F
END
