# Flot optique : Lucas–Kanade, Farnebäck et RAFT — cartes

Fiche : [[100-mouvement-video/references/101-flot-optique|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::100-mouvement-video

## CV-FLOT-001

Objectif : interpréter la contrainte du flot. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-FLOT-001
Question: Pourquoi $I_xu+I_yv+I_t=0$ ne détermine-t-il pas un mouvement 2D unique à un pixel ?
Reponse: **Noyau attendu** : Une équation ne contraint pas deux inconnues sans hypothèses/voisinage ; une arête peut garder une ambiguïté tangentielle.

**Approfondissement** : Lucas–Kanade agrège localement et dépend du conditionnement ; la pyramide ne crée pas la texture absente.

**Lecture de la contrainte** : le gradient spatial fournit une direction selon laquelle une variation d'intensité renseigne le déplacement. Le mouvement tangent à une arête uniforme change peu les intensités : plusieurs vecteurs peuvent alors satisfaire la même équation. C'est un manque d'information locale, pas nécessairement une erreur du solveur.

**Exemple et limite** : un bord vertical qui glisse vers le haut peut sembler presque inchangé dans une petite fenêtre. Ajouter des pixels du même bord ne crée pas une seconde direction indépendante. Un voisinage comportant un coin peut mieux contraindre les deux composantes si le mouvement y reste suffisamment cohérent et la photométrie stable. Examiner conditionnement, taille de fenêtre et validité de l'hypothèse avant d'augmenter les itérations. Une régularisation peut choisir une solution parmi plusieurs plausibles ; elle ajoute alors une hypothèse, et non une observation certaine du déplacement.

**Erreurs bloquantes** : Dire qu’un gradient élevé garantit deux composantes précises.
Source: [[100-mouvement-video/references/101-flot-optique|Fiche complète]] ; [OpenCV, optical flow/Lucas–Kanade](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html) ; [RAFT, §§3.1–3.3](https://arxiv.org/abs/2003.12039).
Tags: cv::pilote cv::d10 famille::raisonnement cv_id::CV-FLOT-001 provenance::agent pole::B pole::C pole::D
END

## CV-FLOT-002

Objectif : respecter l’unité temporelle. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-FLOT-002
Question: Un flot vaut 4 pixels entre deux images. Est-ce une vitesse de 4 px/s ?
Reponse: **Noyau attendu** : Non : il faut l’intervalle temporel, par exemple 4 px à 20 ms donne 200 px/s dans ce modèle.

**Approfondissement** : Conserver sens du flux, résolution, timestamp et masques ; comparer des déplacements à cadence différente sans conversion est trompeur.

**Décomposition des unités** : le flot relie une position de l'image source à une position de l'image destination. Diviser le déplacement par la différence des timestamps donne une vitesse image moyenne sur cet intervalle, sous réserve que la correspondance soit valide. Ce n'est pas automatiquement une vitesse instantanée ni un mouvement dans le monde.

**Exemple construit** : quatre pixels en 40 ms donnent 100 px/s, deux fois moins que quatre pixels en 20 ms. Un resize par un facteur deux modifie aussi le nombre de pixels de déplacement, sans doubler la vitesse physique de l'objet. Pour passer en m/s, il faut une géométrie et une échelle adaptées, souvent liées à la profondeur. Une caméra mobile peut produire du flot sur un objet immobile. Conserver ces informations évite d'interpréter un grand vecteur comme une preuve de mouvement rapide de l'objet.

**Erreurs bloquantes** : Confondre déplacement par frame et vitesse par seconde.
Source: [[100-mouvement-video/references/101-flot-optique|Fiche complète]] ; [OpenCV, optical flow/Lucas–Kanade](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html) ; [RAFT, §§3.1–3.3](https://arxiv.org/abs/2003.12039).
Tags: cv::pilote cv::d10 famille::pratique cv_id::CV-FLOT-002 provenance::agent pole::B pole::C pole::D
END

## CV-FLOT-003

Objectif : situer RAFT. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-FLOT-003
Question: Quel rôle distinct jouent corrélations et mises à jour récurrentes dans RAFT ?
Reponse: **Noyau attendu** : Les corrélations représentent des compatibilités entre positions ; les mises à jour raffinent l’estimation du flot.

**Approfondissement** : La sortie est un déplacement dense entre deux images, pas la persistance d’un ID d’objet sur toute vidéo.

**Rôles dans le calcul** : la représentation de corrélation rassemble des compatibilités entre positions des deux images. Les mises à jour récurrentes interrogent cette information et le contexte pour corriger progressivement une estimation de déplacement. La répétition des mises à jour porte sur le raffinement de la paire observée ; elle ne suffit pas à définir une mémoire d'identité sur une séquence entière.

**Exemple de distinction** : deux personnes qui se croisent peuvent produire un champ de mouvement utile entre deux frames sans qu'une identité soit conservée après une longue occultation. Un système de tracking devra encore définir objets, associations et cycle de vie. Pour évaluer le flot, utiliser des déplacements de référence, les régions visibles et occultées et les unités de l'image. Augmenter le nombre d'itérations modifie un compromis de calcul ; cela ne garantit pas la disparition de toutes les ambiguïtés physiques.

**Erreurs bloquantes** : Décrire une mémoire récurrente de raffinement comme une réidentification garantie.
Source: [[100-mouvement-video/references/101-flot-optique|Fiche complète]] ; [OpenCV, optical flow/Lucas–Kanade](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html) ; [RAFT, §§3.1–3.3](https://arxiv.org/abs/2003.12039).
Tags: cv::pilote cv::d10 famille::comparaison cv_id::CV-FLOT-003 provenance::agent pole::B pole::C pole::D
END

## CV-FLOT-004

Objectif : traiter une occultation. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-FLOT-004
Question: Un point devient invisible mais le flot retourne encore un vecteur. Comment interpréter cette sortie ?
Reponse: **Noyau attendu** : Comme une estimation sous les hypothèses du modèle, sans correspondance observable garantie ; examiner masque d’occlusion et cohérence.

**Approfondissement** : Comparer aller-retour et référence quand possible, sans utiliser la visibilité vraie à l’inférence.

**Pourquoi la densité ne prouve rien** : un algorithme dense peut remplir des régions où les données ne contiennent plus de correspondant visible. La valeur produite peut venir du contexte, de la régularisation ou d'un modèle appris. Ces mécanismes donnent une hypothèse utile, mais pas une observation nouvelle de la surface cachée.

**Contrôle proposé** : distinguer occultation, sortie de champ et erreur de matching. Pour un aller-retour, évaluer le flot inverse à la position atteinte dans l'autre image, en tenant compte de l'interpolation et des limites du champ. Une incohérence signale un problème possible ; une cohérence ne garantit pas l'identité sur une texture répétitive. Mesurer séparément les régions selon un protocole de visibilité annoncé. À l'inférence, une vérité terrain d'occultation n'est pas disponible par magie : la politique de confiance doit utiliser uniquement les informations réellement fournies au système.

**Erreurs bloquantes** : Déclarer tout vecteur calculé comme déplacement physique validé.
Source: [[100-mouvement-video/references/101-flot-optique|Fiche complète]] ; [OpenCV, optical flow/Lucas–Kanade](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html) ; [RAFT, §§3.1–3.3](https://arxiv.org/abs/2003.12039).
Tags: cv::pilote cv::d10 famille::diagnostic cv_id::CV-FLOT-004 provenance::agent pole::B pole::C pole::D
END
