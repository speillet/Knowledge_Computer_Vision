# Line-scan, télédétection et volumes médicaux — cartes

Fiche : [[20-acquisition-images/references/23-imageries-specialisees|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::20-acquisition-images

## CV-IMAGERIES-001

Objectif : propager les unités d’un volume. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-IMAGERIES-001
Question: Pourquoi HD95 ne doit-il pas être calculé aveuglément en indices de voxels sur une IRM anisotrope ?
Reponse: **Noyau attendu** : Les axes peuvent avoir des espacements physiques différents ; convertir les distances dans le repère et l’unité annoncés.

**Approfondissement** : Conserver orientation, rééchantillonnage et protocole des masques vides. Une différence d’un voxel n’a pas la même longueur selon l’axe.

**Erreurs bloquantes** : Comparer des valeurs en voxels et en millimètres comme si elles étaient identiques.
Source: [[20-acquisition-images/references/23-imageries-specialisees|Fiche complète]] ; [NIfTI, standard et transformations](https://nifti.nimh.nih.gov/nifti-1/) ; [DICOM, standard courant](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html) ; [SpaceNet7, données multi-temporelles](https://spacenet.ai/spacenet-7-multi-temporal-urban-development-challenge/).
Tags: cv::pilote cv::d02 famille::pratique cv_id::CV-IMAGERIES-001 provenance::agent pole::E
END

## CV-IMAGERIES-002

Objectif : contrôler une acquisition line-scan. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-IMAGERIES-002
Question: Une pièce paraît allongée sur une image line-scan quand la vitesse du convoyeur change. Que tester ?
Reponse: **Noyau attendu** : La synchronisation entre lignes et déplacement, l’encodeur et l’échelle reconstruite dans le sens de mouvement.

**Approfondissement** : Tester une dimension connue à plusieurs vitesses ; distinguer ce défaut du grandissement optique et de la détection.

**Erreurs bloquantes** : Réentraîner sans vérifier le contrat spatial de l’image.
Source: [[20-acquisition-images/references/23-imageries-specialisees|Fiche complète]] ; [NIfTI, standard et transformations](https://nifti.nimh.nih.gov/nifti-1/) ; [DICOM, standard courant](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html) ; [SpaceNet7, données multi-temporelles](https://spacenet.ai/spacenet-7-multi-temporal-urban-development-challenge/).
Tags: cv::pilote cv::d02 famille::diagnostic cv_id::CV-IMAGERIES-002 provenance::agent pole::E
END

## CV-IMAGERIES-003

Objectif : éviter une fuite géographique. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-IMAGERIES-003
Question: Pourquoi des tuiles voisines réparties aléatoirement entre entraînement et test peuvent-elles surestimer la généralisation en télédétection ?
Reponse: **Noyau attendu** : Elles partagent scène, texture et contexte ; le test peut ressembler à l’entraînement au-delà du scénario futur visé.

**Approfondissement** : Séparer régions/dates/sites selon l’usage, contrôler les recouvrements et conserver une évaluation indépendante.

**Erreurs bloquantes** : Assimiler séparation de fichiers et indépendance statistique.
Source: [[20-acquisition-images/references/23-imageries-specialisees|Fiche complète]] ; [NIfTI, standard et transformations](https://nifti.nimh.nih.gov/nifti-1/) ; [DICOM, standard courant](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html) ; [SpaceNet7, données multi-temporelles](https://spacenet.ai/spacenet-7-multi-temporal-urban-development-challenge/).
Tags: cv::pilote cv::d02 famille::evaluation cv_id::CV-IMAGERIES-003 provenance::agent pole::E
END
