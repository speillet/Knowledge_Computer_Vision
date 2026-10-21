# Détection 3D, pose d’objet et pose articulée — cartes

Fiche : [[80-detection-pose/references/84-detection-pose-3d|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::80-detection-pose

## CV-POSE3D-001

Objectif : nommer la sortie de pose. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-POSE3D-001
Question: Pourquoi ne pas comparer directement score de détection 3D et erreur de pose articulée ?
Reponse: **Noyau attendu** : Boîtes/classes et articulations sont des sorties différentes avec annotations, correspondances et métriques différentes.

**Approfondissement** : Définir le livrable, repère, visibilité et alignement avant de choisir la mesure.

**Erreurs bloquantes** : Assimiler tout problème appelé pose à la même métrique.
Source: [[80-detection-pose/references/84-detection-pose-3d|Fiche complète]] ; [CenterPoint, résumé et §4](https://arxiv.org/abs/2006.11275) ; [OpenPose, résumé et fig. 2](https://arxiv.org/abs/1611.08050).
Tags: cv::pilote cv::d08 famille::comparaison cv_id::CV-POSE3D-001 provenance::agent pole::A pole::C
END

## CV-POSE3D-002

Objectif : contrôler une boîte 3D. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-POSE3D-002
Question: Quels éléments vérifier si des boîtes 3D ont les bons centres mais des orientations/dimensions incohérentes ?
Reponse: **Noyau attendu** : Repère, ancrage du centre, ordre des dimensions, axe/signe du yaw et radians/degrés.

**Approfondissement** : Tester une boîte connue et sa transformation entre capteurs ; le problème peut être un contrat de données.

**Erreurs bloquantes** : Réentraîner sans contrôler la convention de boîte.
Source: [[80-detection-pose/references/84-detection-pose-3d|Fiche complète]] ; Diagnostic de conventions proposé par le projet ; [nuScenes, format et métriques](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md), consulté le 2026-10-20.
Tags: cv::pilote cv::d08 famille::pratique cv_id::CV-POSE3D-002 provenance::agent pole::A pole::C
END

## CV-POSE3D-003

Objectif : distinguer nuScenes et COCO. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-POSE3D-003
Question: Pourquoi une AP nuScenes 3D n’est-elle pas directement comparable à une AP bbox COCO ?
Reponse: **Noyau attendu** : L’association nuScenes utilise des distances de centres au sol et un protocole spécifique ; COCO bbox utilise des recouvrements et ses propres règles.

**Approfondissement** : NDS combine aussi erreurs d’attributs géométriques/dynamiques ; nommer version, filtres et unités.

**Erreurs bloquantes** : Transposer les seuils IoU COCO à tout benchmark 3D.
Source: [[80-detection-pose/references/84-detection-pose-3d|Fiche complète]] ; [nuScenes, Average Precision metric et nuScenes detection score](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md), consulté le 2026-10-20 ; [COCO bbox](https://cocodataset.org/#detection-eval).
Tags: cv::pilote cv::d08 famille::evaluation cv_id::CV-POSE3D-003 provenance::agent pole::A pole::C
END

## CV-POSE3D-004

Objectif : respecter les symétries de pose. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-POSE3D-004
Question: Un objet cylindrique est localisé correctement mais sa rotation autour de l’axe varie. Que vérifier ?
Reponse: **Noyau attendu** : La symétrie visuelle et la définition de pose/évaluation : cette composante peut être ambiguë avec les observations disponibles.

**Approfondissement** : Ajouter un indice distinctif si le produit exige cet angle ; un solveur plus précis ne crée pas un repère visible absent.

**Erreurs bloquantes** : Déclarer toute variation d’un angle symétrique comme une erreur observable.
Source: [[80-detection-pose/references/84-detection-pose-3d|Fiche complète]] ; [BOP, métriques VSD/MSSD/MSPD et symétries](https://bop.felk.cvut.cz/tasks/), consulté le 2026-10-20 ; application au cylindre : raisonnement du projet.
Tags: cv::pilote cv::d08 famille::diagnostic cv_id::CV-POSE3D-004 provenance::agent pole::A pole::C
END
