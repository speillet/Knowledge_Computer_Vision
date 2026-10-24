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

**Mécanisme interprété** : ECC cherche des paramètres de transformation en comparant directement les intensités sur une zone commune. Les correspondances ne sont pas d'abord exprimées comme une liste de patches détectés. SIFT et RANSAC peuvent proposer une transformation à partir de points distinctifs ; un raffinement photométrique peut ensuite être essayé si le modèle et le recouvrement s'y prêtent.

**Exemple construit** : pour deux vues proches d'une étiquette, une initialisation convenable peut rendre utile l'optimisation des intensités. Pour un grand déplacement avec faible recouvrement, la même procédure peut atteindre un mauvais optimum ou échouer. Vérifier séparément initialisation, masque, variations photométriques et modèle de mouvement. Une corrélation normalisée peut tolérer un gain positif et un offset globaux sur un support fixé non constant ; cette propriété algébrique ne couvre pas une ombre locale, une occultation ou une convergence globale du recalage.

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

**Origine de l'ambiguïté** : une translation d'une période d'une grille peut aligner des intensités semblables presque aussi bien que la translation vraie. Le critère numérique voit alors plusieurs solutions plausibles dans l'image ; une convergence stable signifie seulement que l'optimiseur s'est arrêté selon ses critères.

**Validation construite** : ajouter au contrôle une marque unique ou des points réservés dont la position est connue, puis comparer l'erreur des solutions obtenues depuis plusieurs initialisations plausibles. Examiner le recouvrement réellement utilisé et les parties masquées. Une contrainte de mouvement doit provenir du système observé et rester explicitement bornée. Si les seules observations sont parfaitement répétitives, reconnaître que le déplacement absolu peut rester ambigu. Ce diagnostic distingue optimisation et identifiabilité : davantage d'itérations améliore éventuellement un ajustement local, mais n'apporte pas l'information distinctive absente de la scène.

Une observation distinctive réservée sert alors à départager les solutions, sans modifier les pixels utilisés par l'optimiseur.

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

**Raisonnement sur les degrés de liberté** : un modèle de translation impose que tous les points partagent deux déplacements ; une homographie autorise une déformation projective plus générale. Cette souplesse peut expliquer de vraies variations de vue sur un plan, mais aussi absorber du bruit ou une perturbation photométrique lorsque les données contraignent mal ses paramètres.

**Comparaison construite** : sur une installation où le mouvement prévu est une petite translation, ajuster d'abord ce modèle, puis un modèle plus riche avec les mêmes images et zone utile. Comparer erreurs sur des points réservés, stabilité des paramètres et extrapolation près des bords. Un meilleur score sur les pixels d'ajustement ne suffit pas. Inversement, conserver une translation si la perspective change réellement introduit un biais. Le choix relie donc la géométrie de capture, la richesse des observations et l'erreur admise, plutôt qu'un principe de simplicité ou de flexibilité appliqué aveuglément.

**Erreurs bloquantes** : Assimiler flexibilité maximale et précision maximale.
Source: [[40-features-matching/references/45-recalage-ecc|Fiche complète]] ; [OpenCV 4.13.0, findTransformECC, modèle, initialisation et inverse warping](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html) ; compromis entre flexibilité et stabilité déduit par le projet.
Tags: cv::pilote cv::d04 famille::pratique cv_id::CV-ECC-003 provenance::agent pole::B pole::E
END
