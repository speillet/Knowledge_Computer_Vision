# GrabCut, régions et modèles d’apparence — cartes

Fiche : [[90-segmentation/references/92-grabcut-regions|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::90-segmentation

## CV-GRABCUT-001

Objectif : expliquer l’alternance GrabCut. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-GRABCUT-001
Question: Quelles deux opérations principales GrabCut alterne-t-il ?
Reponse: **Noyau attendu** : Estimer les modèles d’apparence fond/objet puis optimiser les labels via graph cut dans l’énergie définie.

**Approfondissement** : Les contraintes sûres et probables de l’initialisation ont un rôle distinct ; le procédé n’est pas un classifieur sémantique générique.

**Erreurs bloquantes** : Décrire seulement un seuil de couleur fixe.
Source: [[90-segmentation/references/92-grabcut-regions|Fiche complète]] ; [OpenCV GrabCut, théorie et masques](https://docs.opencv.org/4.13.0/d8/d83/tutorial_py_grabcut.html).
Tags: cv::pilote cv::d09 famille::algorithme cv_id::CV-GRABCUT-001 provenance::agent pole::A pole::E
END

## CV-GRABCUT-002

Objectif : contrôler une contrainte d’initialisation. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-GRABCUT-002
Question: GrabCut exclut toujours une partie d’objet malgré plus d’itérations. Que vérifier d’abord ?
Reponse: **Noyau attendu** : La zone initiale et les labels de fond sûr : une région utile peut être rendue impossible par la contrainte.

**Approfondissement** : Tester une correction manuelle des labels sur copie puis observer le masque ; distinguer initialisation et apparence insuffisante.

**Erreurs bloquantes** : Supposer que la convergence doit annuler toute contrainte erronée.
Source: [[90-segmentation/references/92-grabcut-regions|Fiche complète]] ; [OpenCV GrabCut, théorie et masques](https://docs.opencv.org/4.13.0/d8/d83/tutorial_py_grabcut.html).
Tags: cv::pilote cv::d09 famille::diagnostic cv_id::CV-GRABCUT-002 provenance::agent pole::A pole::E
END

## CV-GRABCUT-003

Objectif : choisir une interaction. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-GRABCUT-003
Question: Pour extraire un objet avec couleurs proches du fond, pourquoi comparer coût d’interaction et hypothèses plutôt que seulement temps d’optimisation ?
Reponse: **Noyau attendu** : Les labels ajoutés par l’utilisateur peuvent fournir l’information manquante ; une solution rapide peut demander beaucoup de corrections.

**Approfondissement** : Évaluer masque, nombre de corrections et robustesse sur images réservées ; un optimum d’énergie ne suffit pas.

**Erreurs bloquantes** : Présenter un temps de calcul faible comme performance complète du processus.
Source: [[90-segmentation/references/92-grabcut-regions|Fiche complète]] ; [OpenCV GrabCut, théorie et masques](https://docs.opencv.org/4.13.0/d8/d83/tutorial_py_grabcut.html).
Tags: cv::pilote cv::d09 famille::comparaison cv_id::CV-GRABCUT-003 provenance::agent pole::A pole::E
END
