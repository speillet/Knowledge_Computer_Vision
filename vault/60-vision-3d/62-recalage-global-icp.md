# Recalage global et ICP local — cartes

Fiche : [[60-vision-3d/references/62-recalage-global-icp|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::60-vision-3d

## CV-ICP-001

Objectif : séparer initialisation globale et raffinement. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-ICP-001
Question: Pourquoi combiner FPFH/RANSAC puis ICP plutôt que lancer ICP depuis n’importe quelle pose ?
Reponse: **Noyau attendu** : L’initialisation globale cherche une zone compatible à partir de correspondances ; ICP affine localement et peut converger sur de mauvaises associations.

**Approfondissement** : FPFH décrit la géométrie ; la pose doit être estimée puis validée. Le succès dépend aussi du recouvrement et des symétries.

**Erreurs bloquantes** : Présenter ICP comme un solveur global garanti.
Source: [[60-vision-3d/references/62-recalage-global-icp|Fiche complète]] ; [Open3D 0.19.0, ICP point-to-point et point-to-plane](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html) ; [Open3D 0.19.0, global registration FPFH/RANSAC](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html).
Tags: cv::pilote cv::d06 famille::algorithme cv_id::CV-ICP-001 provenance::agent pole::B pole::C
END

## CV-ICP-002

Objectif : interpréter un résidu point-to-plane. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-ICP-002
Question: Que mesure $n^T(Rp+t-q)$ dans ICP point-to-plane ?
Reponse: **Noyau attendu** : La composante du désalignement selon la normale cible unitaire, en unité de longueur.

**Approfondissement** : Sur un plan, un déplacement tangent peut peu changer ce résidu ; contrôler observabilité et pose, pas seulement RMSE.

**Erreurs bloquantes** : Prendre ce scalaire pour une erreur complète 3D dans toutes directions.
Source: [[60-vision-3d/references/62-recalage-global-icp|Fiche complète]] ; [Open3D 0.19.0, ICP point-to-point et point-to-plane](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html) ; [Open3D 0.19.0, global registration FPFH/RANSAC](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html).
Tags: cv::pilote cv::d06 famille::raisonnement cv_id::CV-ICP-002 provenance::agent pole::B pole::C
END

## CV-ICP-003

Objectif : refuser un petit consensus trompeur. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-ICP-003
Question: ICP annonce un petit RMSE mais n’aligne qu’un coin de deux nuages. Que rapporter ?
Reponse: **Noyau attendu** : Recouvrement, seuil, distribution des correspondances et erreur de pose sur référence indépendante.

**Approfondissement** : Le RMSE conditionne son résultat aux paires retenues ; réduire le consensus peut faire baisser le nombre sans améliorer la tâche.

**Erreurs bloquantes** : Classer la pose au RMSE seul.
Source: [[60-vision-3d/references/62-recalage-global-icp|Fiche complète]] ; [Open3D 0.19.0, ICP point-to-point et point-to-plane](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html) ; [Open3D 0.19.0, global registration FPFH/RANSAC](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html).
Tags: cv::pilote cv::d06 famille::diagnostic cv_id::CV-ICP-003 provenance::agent pole::B pole::C
END

## CV-ICP-004

Objectif : garder les unités du recalage. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-ICP-004
Question: Pourquoi réutiliser un seuil ICP de 0,02 après passage des nuages de mètres à millimètres change-t-il le problème ?
Reponse: **Noyau attendu** : Le seuil est une longueur dans l’unité des coordonnées ; il faut propager l’échelle aux paramètres pertinents.

**Approfondissement** : Vérifier voxel et voisinages aussi, puis le modèle de bruit.

**Erreurs bloquantes** : Traiter le seuil comme un nombre sans unité.
Source: [[60-vision-3d/references/62-recalage-global-icp|Fiche complète]] ; [Open3D 0.19.0, ICP point-to-point et point-to-plane](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html) ; [Open3D 0.19.0, global registration FPFH/RANSAC](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html).
Tags: cv::pilote cv::d06 famille::pratique cv_id::CV-ICP-004 provenance::agent pole::B pole::C
END

## CV-ICP-005

Objectif : choisir une variante ICP. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-ICP-005
Question: Point-to-plane remplace-t-il toujours avantageusement point-to-point ?
Reponse: **Noyau attendu** : Il exploite des normales fiables et une géométrie qui contraint les mouvements utiles ; il peut être mal posé sur certaines surfaces ou normales bruitées.

**Approfondissement** : Comparer initialisation, estimation des normales et précision de pose dans le protocole cible.

**Erreurs bloquantes** : Annoncer une domination universelle d’une variante.
Source: [[60-vision-3d/references/62-recalage-global-icp|Fiche complète]] ; [Open3D 0.19.0, ICP point-to-point et point-to-plane](https://www.open3d.org/docs/release/tutorial/pipelines/icp_registration.html) ; [Open3D 0.19.0, global registration FPFH/RANSAC](https://www.open3d.org/docs/release/tutorial/pipelines/global_registration.html).
Tags: cv::pilote cv::d06 famille::comparaison cv_id::CV-ICP-005 provenance::agent pole::B pole::C
END
