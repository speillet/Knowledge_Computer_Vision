# SuperPoint, LightGlue et LoFTR — cartes

Fiche : [[40-features-matching/references/44-superpoint-lightglue-loftr|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::40-features-matching

## CV-MATCH-APPRIS-001

Objectif : attribuer le rôle des composants. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-MATCH-APPRIS-001
Question: Que fournit SuperPoint et que rajoute LightGlue pour un recalage entre deux images ?
Reponse: **Noyau attendu** : SuperPoint fournit des keypoints et des descripteurs ; LightGlue recherche les correspondances entre features compatibles.

**Approfondissement** : Une estimation géométrique et sa validation restent nécessaires après le matching.

**Erreurs bloquantes** : Présenter LightGlue comme un détecteur d’objets ou une calibration caméra.
Source: [[40-features-matching/references/44-superpoint-lightglue-loftr|Fiche complète]] ; [DeTone et al. 2018, SuperPoint, §§3 et 5](https://arxiv.org/abs/1712.07629) ; [LightGlue, README, Usage et Advanced configuration, consulté le 2026-10-20](https://github.com/cvg/LightGlue).
Tags: cv::pilote cv::d04 famille::comprehension cv_id::CV-MATCH-APPRIS-001 provenance::agent pole::B
END

## CV-MATCH-APPRIS-002

Objectif : distinguer detector-free et flot dense. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-MATCH-APPRIS-002
Question: LoFTR est detector-free : cela signifie-t-il une trajectoire fiable pour chaque pixel ?
Reponse: **Noyau attendu** : Non : il produit des correspondances coarse-to-fine sans détecteur sparse explicite ; ce n’est ni un flot garanti partout ni un tracker temporel complet.

**Approfondissement** : Définir repères, scores et validation géométrique comme pour toute proposition de matches.

**Erreurs bloquantes** : Assimiler detector-free à dense sans trous et sans erreurs.
Source: [[40-features-matching/references/44-superpoint-lightglue-loftr|Fiche complète]] ; [Sun et al. 2021, LoFTR, §§3.1–3.4 et 4.1–4.2](https://arxiv.org/abs/2104.00680).
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-MATCH-APPRIS-002 provenance::agent pole::B
END

## CV-MATCH-APPRIS-003

Objectif : garder des features compatibles. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-MATCH-APPRIS-003
Question: Pourquoi ne peut-on pas remplacer arbitrairement les descripteurs d’entrée d’un checkpoint de matcher appris ?
Reponse: **Noyau attendu** : Les poids et distributions attendues sont associés à une représentation ; dimensions égales ne garantissent pas la compatibilité.

**Approfondissement** : Vérifier feature extractor, normalisation, coordonnées et version du checkpoint, puis mesurer.

**Erreurs bloquantes** : Déduire la compatibilité du seul nombre de composantes.
Source: [[40-features-matching/references/44-superpoint-lightglue-loftr|Fiche complète]] ; [LightGlue, README, Usage et Advanced configuration, consulté le 2026-10-20](https://github.com/cvg/LightGlue).
Tags: cv::pilote cv::d04 famille::pratique cv_id::CV-MATCH-APPRIS-003 provenance::agent pole::B
END

## CV-MATCH-APPRIS-004

Objectif : construire une baseline comparable. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-MATCH-APPRIS-004
Question: Quelles conditions rendent crédible un gain annoncé de matching appris face à ORB/SIFT ?
Reponse: **Noyau attendu** : Même problème, paires/splits, résolution effective et validation géométrique ; compter le coût de toute la chaîne et les échecs.

**Approfondissement** : Rapporter couverture, robustesse et matériel ; le score d’un benchmark ne garantit pas le succès sur une nouvelle acquisition.

**Erreurs bloquantes** : Comparer des nombres bruts de matches ou des temps couvrant des étapes différentes.
Source: [[40-features-matching/references/44-superpoint-lightglue-loftr|Fiche complète]] ; [Sun et al. 2021, LoFTR, §§3.1–3.4 et 4.1–4.2](https://arxiv.org/abs/2104.00680) ; protocole comparatif proposé par le projet.
Tags: cv::pilote cv::d04 famille::evaluation cv_id::CV-MATCH-APPRIS-004 provenance::agent pole::B
END

## CV-MATCH-APPRIS-005

Objectif : contrôler les coordonnées du matching. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-MATCH-APPRIS-005
Question: Après ajout de padding, les matches semblent corrects visuellement mais l’homographie est biaisée. Que tester ?
Reponse: **Noyau attendu** : La conversion des positions depuis le repère du réseau vers chaque image réelle, y compris resize et offsets.

**Approfondissement** : Vérifier un point connu et l’échelle des résidus avant d’accuser le matcher.

**Erreurs bloquantes** : Mélanger coordonnées normalisées et pixels dans une même estimation.
Source: [[40-features-matching/references/44-superpoint-lightglue-loftr|Fiche complète]] ; [LightGlue, README, Usage et Advanced configuration, consulté le 2026-10-20](https://github.com/cvg/LightGlue) ; diagnostic de changement de repère déduit par le projet.
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-MATCH-APPRIS-005 provenance::agent pole::B
END
