# Évaluer identités, trajectoires et localisation 3D — cartes

Fiche : [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::130-evaluation-fiabilite

## CV-METRIQUES-TEMPS-001

Objectif : séparer détection et identité. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-METRIQUES-TEMPS-001
Question: Comment deux systèmes peuvent-ils avoir la même AP frame par frame et des qualités de tracking différentes ?
Reponse: **Noyau attendu** : Les boîtes/classes peuvent être identiques tandis que les IDs sont échangés ou fragmentés ; AP ne mesure pas cette continuité.

**Approfondissement** : Utiliser métriques et diagnostics d’association sous protocole de séquence identique.

**Erreurs bloquantes** : Déduire qualité d’identité de l’AP seule.
Source: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Fiche complète]] ; [HOTA, §§5–6](https://arxiv.org/abs/2009.07736) ; [Zhang–Scaramuzza, §III/TableI et évaluation](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf) ; [nuScenes, métriques de détection](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md).
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-METRIQUES-TEMPS-001 provenance::agent pole::B pole::C pole::D
END

## CV-METRIQUES-TEMPS-002

Objectif : respecter l’agrégation HOTA. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-METRIQUES-TEMPS-002
Question: Pourquoi calculer sqrt(moyenne DetA × moyenne AssA) ne reproduit-il pas nécessairement HOTA ?
Reponse: **Noyau attendu** : La référence calcule la racine du produit à chaque seuil puis moyenne ces scores ; les opérations ne commutent pas en général.

**Approfondissement** : Conserver aussi conventions de matching, ignore et localisation ; un résumé de formule n’est pas tout l’évaluateur.

**Erreurs bloquantes** : Intervertir librement moyenne et racine.
Source: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Fiche complète]] ; [HOTA, §§5–6](https://arxiv.org/abs/2009.07736) ; [Zhang–Scaramuzza, §III/TableI et évaluation](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf) ; [nuScenes, métriques de détection](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md).
Tags: cv::pilote cv::d13 famille::raisonnement cv_id::CV-METRIQUES-TEMPS-002 provenance::agent pole::B pole::C pole::D
END

## CV-METRIQUES-TEMPS-003

Objectif : choisir un alignement de trajectoire. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-METRIQUES-TEMPS-003
Question: Pourquoi une Sim(3) peut-elle être un mauvais choix pour évaluer un VIO censé être métrique ?
Reponse: **Noyau attendu** : Elle ajuste l’échelle et peut donc masquer une erreur métrique que le système devait éviter.

**Approfondissement** : Le groupe d’alignement doit suivre les jauges et l’objectif ; avec gravité fixée, une rotation libre peut aussi masquer des erreurs d’inclinaison.

**Erreurs bloquantes** : Optimiser l’alignement pour obtenir le meilleur score sans justification.
Source: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Fiche complète]] ; [HOTA, §§5–6](https://arxiv.org/abs/2009.07736) ; [Zhang–Scaramuzza, §III/TableI et évaluation](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf) ; [nuScenes, métriques de détection](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md).
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-METRIQUES-TEMPS-003 provenance::agent pole::B pole::C pole::D
END

## CV-METRIQUES-TEMPS-004

Objectif : distinguer ATE et RPE. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-METRIQUES-TEMPS-004
Question: ATE et RPE répondent-elles exactement à la même question ?
Reponse: **Noyau attendu** : ATE évalue une trajectoire après alignement ; RPE des déplacements relatifs à des intervalles définis.

**Approfondissement** : Préciser temps/distance d’intervalle, agrégation, translation/rotation et échecs ; longueur du trajet et bouclage influencent l’interprétation.

**Erreurs bloquantes** : Comparer des nombres sans protocole, unité ou intervalle.
Source: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Fiche complète]] ; [HOTA, §§5–6](https://arxiv.org/abs/2009.07736) ; [Zhang–Scaramuzza, §III/TableI et évaluation](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf) ; [nuScenes, métriques de détection](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md).
Tags: cv::pilote cv::d13 famille::comparaison cv_id::CV-METRIQUES-TEMPS-004 provenance::agent pole::B pole::C pole::D
END

## CV-METRIQUES-TEMPS-005

Objectif : comparer des évaluateurs temporels. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-METRIQUES-TEMPS-005
Question: Deux outils donnent des erreurs de trajectoire différentes pour les mêmes poses. Que contrôler ?
Reponse: **Noyau attendu** : Appariement temporel, interpolation, conventions de pose, alignement, intervalles et traitement des pertes.

**Approfondissement** : Rejouer un petit cas connu puis le même fichier/version ; ne pas attribuer l’écart immédiatement à l’estimateur.

**Erreurs bloquantes** : Comparer seulement le nom ATE affiché par les outils.
Source: [[130-evaluation-fiabilite/references/132-tracking-trajectoires|Fiche complète]] ; [HOTA, §§5–6](https://arxiv.org/abs/2009.07736) ; [Zhang–Scaramuzza, §III/TableI et évaluation](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf) ; [nuScenes, métriques de détection](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md).
Tags: cv::pilote cv::d13 famille::diagnostic cv_id::CV-METRIQUES-TEMPS-005 provenance::agent pole::B pole::C pole::D
END
