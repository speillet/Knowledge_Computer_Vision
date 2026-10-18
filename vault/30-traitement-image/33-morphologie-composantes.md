# Morphologie et composantes connexes — cartes

Fiche : [[30-traitement-image/references/33-morphologie-composantes|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::30-traitement-image

## CV-MORPHO-001

Objectif : distinguer ouverture et fermeture. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-MORPHO-001
Question: Quel effet géométrique distingue ouverture et fermeture binaires, et pourquoi choisir la taille du structurant avec la tâche ?
Reponse: **Noyau attendu** : L’ouverture érode puis dilate ; la fermeture dilate puis érode. Elles modifient des structures à l’échelle du structurant.

**Approfondissement** : Retirer un petit objet peut nettoyer du bruit ou effacer un défaut ; valider sur tailles et formes critiques.

**Erreurs bloquantes** : Décrire ces opérations comme des filtres sémantiques garantis.
Source: [[30-traitement-image/references/33-morphologie-composantes|Fiche complète]] ; [OpenCV, morphological transformations](https://docs.opencv.org/4.13.0/d9/d61/tutorial_py_morphological_ops.html).
Tags: cv::pilote cv::d03 famille::comparaison cv_id::CV-MORPHO-001 provenance::agent pole::A pole::E
END

## CV-MORPHO-002

Objectif : choisir une connectivité. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-MORPHO-002
Question: Deux pixels de premier plan se touchent uniquement par un coin. Combien de composantes en connectivité 4 puis 8 ?
Reponse: **Noyau attendu** : Deux en connectivité 4 ; une en connectivité 8.

**Approfondissement** : La convention doit être conservée dans l’évaluation et les mesures de trous/objets.

**Erreurs bloquantes** : Annoncer un nombre sans connectivité.
Source: [[30-traitement-image/references/33-morphologie-composantes|Fiche complète]] ; [OpenCV, morphological transformations](https://docs.opencv.org/4.13.0/d9/d61/tutorial_py_morphological_ops.html).
Tags: cv::pilote cv::d03 famille::raisonnement cv_id::CV-MORPHO-002 provenance::agent pole::A pole::E
END

## CV-MORPHO-003

Objectif : expliquer une fusion de pièces. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-MORPHO-003
Question: Après fermeture morphologique, deux pièces proches sont comptées comme une seule. Quelle hypothèse vérifier ?
Reponse: **Noyau attendu** : Le structurant peut avoir créé un pont ; inspecter le masque avant/après et la distance entre objets.

**Approfondissement** : Réduire ou adapter l’opération sous contrôle, puis envisager une séparation à marqueurs ; ne pas seulement changer le filtre d’aire.

**Erreurs bloquantes** : Prendre une composante connexe pour un objet garanti.
Source: [[30-traitement-image/references/33-morphologie-composantes|Fiche complète]] ; [OpenCV, morphological transformations](https://docs.opencv.org/4.13.0/d9/d61/tutorial_py_morphological_ops.html).
Tags: cv::pilote cv::d03 famille::diagnostic cv_id::CV-MORPHO-003 provenance::agent pole::A pole::E
END
