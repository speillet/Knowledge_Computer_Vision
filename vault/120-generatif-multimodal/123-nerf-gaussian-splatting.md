# NeRF, 3D Gaussian Splatting et reconstruction — cartes

Fiche : [[120-generatif-multimodal/references/123-nerf-gaussian-splatting|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::120-generatif-multimodal

## CV-RENDU3D-001

Objectif : distinguer représentation implicite et primitives. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-RENDU3D-001
Question: Quelle différence centrale sépare NeRF et 3D Gaussian Splatting ?
Reponse: **Noyau attendu** : NeRF utilise un champ de densité/radiance avec rendu volumique ; 3DGS une représentation explicite de gaussiennes optimisées et un rendu par splatting.

**Approfondissement** : Comparer optimisation, mémoire et rendu sous même scène/matériel ; aucune vitesse universelle ne suit du nom.

**Erreurs bloquantes** : Assimiler les deux à un maillage métrique garanti.
Source: [[120-generatif-multimodal/references/123-nerf-gaussian-splatting|Fiche complète]] ; [NeRF, page et papier des auteurs](https://www.matthewtancik.com/nerf) ; [3D Gaussian Splatting, auteurs](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/).
Tags: cv::pilote cv::d12 famille::comparaison cv_id::CV-RENDU3D-001 provenance::agent pole::B pole::D
END

## CV-RENDU3D-002

Objectif : séparer rendu et géométrie. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-RENDU3D-002
Question: Pourquoi une excellente PSNR de nouvelles vues ne suffit-elle pas à valider une reconstruction pour métrologie ?
Reponse: **Noyau attendu** : Elle évalue une ressemblance d’image sous protocole, pas directement l’exactitude d’une surface ou d’une dimension physique.

**Approfondissement** : Utiliser une référence géométrique, unités et angles réservés ; examiner les zones jamais observées.

**Erreurs bloquantes** : Déduire une précision en millimètres d’un score perceptuel ou pixel.
Source: [[120-generatif-multimodal/references/123-nerf-gaussian-splatting|Fiche complète]] ; [NeRF, page et papier des auteurs](https://www.matthewtancik.com/nerf) ; [3D Gaussian Splatting, auteurs](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/).
Tags: cv::pilote cv::d12 famille::evaluation cv_id::CV-RENDU3D-002 provenance::agent pole::B pole::D
END

## CV-RENDU3D-003

Objectif : vérifier une scène peu observée. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-RENDU3D-003
Question: Des vues d’entraînement sont plausibles mais une rotation de caméra révèle des artefacts. Que tester ?
Reponse: **Noyau attendu** : Couverture angulaire, poses et hypothèse de scène statique, puis régions insuffisamment contraintes.

**Approfondissement** : Comparer à des vues réservées ; augmenter les itérations sans nouvelles contraintes peut seulement surajuster.

**Erreurs bloquantes** : Considérer les vues d’entraînement comme une validation complète.
Source: [[120-generatif-multimodal/references/123-nerf-gaussian-splatting|Fiche complète]] ; [NeRF, page et papier des auteurs](https://www.matthewtancik.com/nerf) ; [3D Gaussian Splatting, auteurs](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/).
Tags: cv::pilote cv::d12 famille::diagnostic cv_id::CV-RENDU3D-003 provenance::agent pole::B pole::D
END
