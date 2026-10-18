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

**Erreurs bloquantes** : Déclarer tout vecteur calculé comme déplacement physique validé.
Source: [[100-mouvement-video/references/101-flot-optique|Fiche complète]] ; [OpenCV, optical flow/Lucas–Kanade](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html) ; [RAFT, §§3.1–3.3](https://arxiv.org/abs/2003.12039).
Tags: cv::pilote cv::d10 famille::diagnostic cv_id::CV-FLOT-004 provenance::agent pole::B pole::C pole::D
END
