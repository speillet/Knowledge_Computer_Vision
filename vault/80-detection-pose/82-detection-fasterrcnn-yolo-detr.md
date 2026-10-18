# Détection : Faster R-CNN, familles YOLO et DETR — cartes

Fiche : [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::80-detection-pose

## CV-DETECTEURS-001

Objectif : situer le partage de features. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-DETECTEURS-001
Question: Dans Faster R-CNN, traiter des régions implique-t-il de relancer le backbone complet sur chaque crop ?
Reponse: **Noyau attendu** : Non : la conception partage des features entre RPN et tête par régions, avec extraction de représentations régionales.

**Approfondissement** : Distinguer coût des propositions et de la tête ; mesurer le nombre de régions et la variante d’implémentation.

**Erreurs bloquantes** : Décrire deux étapes comme deux backbones complets obligatoires par région.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; [Faster R-CNN, §3](https://arxiv.org/abs/1506.01497) ; [YOLO original, §2](https://openaccess.thecvf.com/content_cvpr_2016/html/Redmon_You_Only_Look_CVPR_2016_paper.html) ; [DETR, §§3.1–3.2](https://arxiv.org/abs/2005.12872).
Tags: cv::pilote cv::d08 famille::comprehension cv_id::CV-DETECTEURS-001 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-002

Objectif : ne pas généraliser toute la famille YOLO. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-DETECTEURS-002
Question: Pourquoi faut-il nommer une version lorsqu’on décrit anchors, losses ou NMS d’un YOLO ?
Reponse: **Noyau attendu** : La famille contient des variantes et recettes hétérogènes ; ces choix ne se déduisent pas du seul nom YOLO.

**Approfondissement** : Comparer version/checkpoint/résolution et protocole complets.

**Erreurs bloquantes** : Attribuer les choix du YOLO original à toutes les générations.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; [Faster R-CNN, §3](https://arxiv.org/abs/1506.01497) ; [YOLO original, §2](https://openaccess.thecvf.com/content_cvpr_2016/html/Redmon_You_Only_Look_CVPR_2016_paper.html) ; [DETR, §§3.1–3.2](https://arxiv.org/abs/2005.12872).
Tags: cv::pilote cv::d08 famille::comparaison cv_id::CV-DETECTEURS-002 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-003

Objectif : distinguer les trois affectations. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-DETECTEURS-003
Question: En DETR, à quoi sert le matching Hungarian de l’entraînement et pourquoi n’est-ce pas une NMS ?
Reponse: **Noyau attendu** : Il associe cibles et requêtes pour définir la supervision, avec no-object pour les autres ; la NMS supprime des prédictions à l’inférence.

**Approfondissement** : L’appariement de l’évaluateur est encore une étape distincte. La prédiction d’ensemble peut éviter NMS dans cette conception.

**Erreurs bloquantes** : Décrire les trois mécanismes comme un seul matching interchangeable.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; [Faster R-CNN, §3](https://arxiv.org/abs/1506.01497) ; [YOLO original, §2](https://openaccess.thecvf.com/content_cvpr_2016/html/Redmon_You_Only_Look_CVPR_2016_paper.html) ; [DETR, §§3.1–3.2](https://arxiv.org/abs/2005.12872).
Tags: cv::pilote cv::d08 famille::algorithme cv_id::CV-DETECTEURS-003 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-004

Objectif : analyser les petits objets après resize. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-DETECTEURS-004
Question: Cas A — diagnostic : l’AP des petits objets chute après réduction de la résolution d’entrée. Que vérifier ?
Reponse: **Noyau attendu** : Propager les coordonnées/padding, mesurer taille effective et rappel avant/après posttraitement, puis examiner assignation et features multiéchelles.

**Approfondissement** : Comparer mêmes images et classes ; séparer bug de repère et perte réelle de détails. Une architecture plus grosse ne recrée pas les pixels disparus.

**Erreurs bloquantes** : Accuser uniquement le classifieur ou recalibrer le score sur le test.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; [Faster R-CNN, §3](https://arxiv.org/abs/1506.01497) ; [YOLO original, §2](https://openaccess.thecvf.com/content_cvpr_2016/html/Redmon_You_Only_Look_CVPR_2016_paper.html) ; [DETR, §§3.1–3.2](https://arxiv.org/abs/2005.12872).
Tags: cv::pilote cv::d08 famille::diagnostic cv_id::CV-DETECTEURS-004 provenance::agent pole::A pole::C pole::E cas_pole::A::diagnostic
END

## CV-DETECTEURS-005

Objectif : comparer des pipelines de détection. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-DETECTEURS-005
Question: Quelles informations joindre à une comparaison de vitesse entre deux détecteurs ?
Reponse: **Noyau attendu** : Matériel, backend/précision, résolution, batch, nombre d’objets, pré/posttraitements, transferts et protocole de latence/débit.

**Approfondissement** : Mesurer aussi qualité à seuils figés et tailles critiques. Un temps moteur seul n’est pas une latence caméra→décision.

**Erreurs bloquantes** : Comparer des FPS dont les périmètres diffèrent.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; [Faster R-CNN, §3](https://arxiv.org/abs/1506.01497) ; [YOLO original, §2](https://openaccess.thecvf.com/content_cvpr_2016/html/Redmon_You_Only_Look_CVPR_2016_paper.html) ; [DETR, §§3.1–3.2](https://arxiv.org/abs/2005.12872).
Tags: cv::pilote cv::d08 famille::evaluation cv_id::CV-DETECTEURS-005 provenance::agent pole::A pole::C pole::E
END
