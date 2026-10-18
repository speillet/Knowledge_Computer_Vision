# Segmentation sémantique, instances et panoptique — cartes

Fiche : [[90-segmentation/references/93-semantique-instances-panoptique|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::90-segmentation

## CV-SEGMENTATION-001

Objectif : choisir la sortie de segmentation. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-SEGMENTATION-001
Question: Quelle différence sépare segmentation sémantique, d’instances et panoptique ?
Reponse: **Noyau attendu** : Sémantique : classe par pixel ; instances : séparer objets comptables ; panoptique : classe et instance pour things, classe pour stuff.

**Approfondissement** : Le masque d’un objet sans classe ne remplit pas automatiquement le contrat panoptique.

**Erreurs bloquantes** : Assimiler classe identique et identité d’instance identique.
Source: [[90-segmentation/references/93-semantique-instances-panoptique|Fiche complète]] ; [U-Net](https://arxiv.org/abs/1505.04597) ; [DeepLabv3+](https://arxiv.org/abs/1802.02611) ; [Mask R-CNN](https://arxiv.org/abs/1703.06870) ; [Panoptic Segmentation, tâche/PQ](https://arxiv.org/abs/1801.00868) ; [nnU-Net, pipeline](https://doi.org/10.1038/s41592-020-01008-z).
Tags: cv::pilote cv::d09 famille::comparaison cv_id::CV-SEGMENTATION-001 provenance::agent pole::A pole::E
END

## CV-SEGMENTATION-002

Objectif : détecter une mauvaise définition de tâche. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-SEGMENTATION-002
Question: Un modèle sémantique segmente très bien un tas de pièces mais ne permet pas leur comptage. Est-ce nécessairement un échec de réseau ?
Reponse: **Noyau attendu** : Non : la sortie peut ne pas séparer les instances. Vérifier tâche, labels et métrique avant la capacité du réseau.

**Approfondissement** : Ajouter un pipeline d’instances ou des marqueurs selon acquisition, puis évaluer fusions/séparations.

**Erreurs bloquantes** : Déduire le nombre d’objets d’une bonne mIoU.
Source: [[90-segmentation/references/93-semantique-instances-panoptique|Fiche complète]] ; [U-Net](https://arxiv.org/abs/1505.04597) ; [DeepLabv3+](https://arxiv.org/abs/1802.02611) ; [Mask R-CNN](https://arxiv.org/abs/1703.06870) ; [Panoptic Segmentation, tâche/PQ](https://arxiv.org/abs/1801.00868) ; [nnU-Net, pipeline](https://doi.org/10.1038/s41592-020-01008-z).
Tags: cv::pilote cv::d09 famille::diagnostic cv_id::CV-SEGMENTATION-002 provenance::agent pole::A pole::E
END

## CV-SEGMENTATION-003

Objectif : propager une augmentation dense. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-SEGMENTATION-003
Question: Pourquoi une augmentation géométrique d’image doit-elle être appliquée différemment mais de façon cohérente au masque de classes ?
Reponse: **Noyau attendu** : La géométrie doit rester alignée ; l’interpolation du masque doit préserver les labels discrets selon le contrat.

**Approfondissement** : Contrôler aussi void, crops/padding et reconstruction de l’image complète. Une interpolation continue peut créer des labels artificiels.

**Erreurs bloquantes** : Transformer l’image seule ou lisser les IDs de classe comme des intensités.
Source: [[90-segmentation/references/93-semantique-instances-panoptique|Fiche complète]] ; [U-Net](https://arxiv.org/abs/1505.04597) ; [DeepLabv3+](https://arxiv.org/abs/1802.02611) ; [Mask R-CNN](https://arxiv.org/abs/1703.06870) ; [Panoptic Segmentation, tâche/PQ](https://arxiv.org/abs/1801.00868) ; [nnU-Net, pipeline](https://doi.org/10.1038/s41592-020-01008-z).
Tags: cv::pilote cv::d09 famille::pratique cv_id::CV-SEGMENTATION-003 provenance::agent pole::A pole::E
END

## CV-SEGMENTATION-004

Objectif : évaluer une segmentation médicale. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-SEGMENTATION-004
Question: Pourquoi une bonne Dice moyenne ne suffit-elle pas pour conclure à l’utilité d’une segmentation médicale ?
Reponse: **Noyau attendu** : Elle mesure un recouvrement selon protocole ; validation externe, frontières, cas rares, unités physiques et usage visé apportent d’autres preuves.

**Approfondissement** : Séparer patients/sites et rapporter cas vides ou échecs ; aucun score seul ne démontre une décision clinique utile.

**Erreurs bloquantes** : Déduire une utilité clinique du seul benchmark interne.
Source: [[90-segmentation/references/93-semantique-instances-panoptique|Fiche complète]] ; [U-Net](https://arxiv.org/abs/1505.04597) ; [DeepLabv3+](https://arxiv.org/abs/1802.02611) ; [Mask R-CNN](https://arxiv.org/abs/1703.06870) ; [Panoptic Segmentation, tâche/PQ](https://arxiv.org/abs/1801.00868) ; [nnU-Net, pipeline](https://doi.org/10.1038/s41592-020-01008-z).
Tags: cv::pilote cv::d09 famille::evaluation cv_id::CV-SEGMENTATION-004 provenance::agent pole::A pole::E
END
