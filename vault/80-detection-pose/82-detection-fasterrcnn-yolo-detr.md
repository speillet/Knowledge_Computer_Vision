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
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; [Faster R-CNN, §3 : partage des convolutions](https://arxiv.org/abs/1506.01497).
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
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; [YOLOv3, §2.1 : anchors](https://arxiv.org/abs/1804.02767) ; [YOLOX, §2.1 : anchor-free, tête découplée et assignation](https://arxiv.org/abs/2107.08430).
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
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; [DETR, §3.1, fig. 1 et équations 1–2](https://arxiv.org/abs/2005.12872).
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
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; Diagnostic construit du projet ; mécanismes multiéchelles et propositions : [Faster R-CNN, §3.1](https://arxiv.org/abs/1506.01497).
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
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; Protocole de comparaison proposé par le projet ; périmètres de calcul discutés dans [Faster R-CNN, §4.1](https://arxiv.org/abs/1506.01497).
Tags: cv::pilote cv::d08 famille::evaluation cv_id::CV-DETECTEURS-005 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-006

Objectif : reconstruire l'assignation des sites dans FCOS. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-DETECTEURS-006
Question: Dans le FCOS décrit aux §§3.1–3.2 de l'article, comment un site de prédiction reçoit-il sa cible à l'entraînement, y compris lorsque plusieurs boîtes annotées le contiennent ?
Reponse: **Noyau attendu** : Retenir les boîtes contenant le site et compatibles avec la plage de distances du niveau FPN. S'il en reste plusieurs, choisir celle de plus petite aire ; s'il n'en reste aucune, le site est négatif. La boîte retenue fournit la classe et les cibles de régression.

**Approfondissement** : La plage porte sur la plus grande des quatre distances aux bords. Il s'agit de la formulation décrite dans ces sections, avant les variantes avec center sampling : anchor-free ne signifie pas « sans assignation ».

**Erreurs bloquantes** : Attribuer la cible par NMS ou supposer que tout site intérieur est positif sur tous les niveaux.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; [FCOS, version 5, §§3.1–3.2](https://arxiv.org/html/1904.01355v5).
Tags: cv::pilote cv::d08 famille::algorithme cv_id::CV-DETECTEURS-006 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-007

Objectif : calculer les cibles de régression en distances. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-DETECTEURS-007
Question: Dans FCOS, un site image $(x,y)=(40,30)$ est associé à la boîte $(x_0,y_0,x_1,y_1)=(20,10,90,70)$. En coordonnées continues, en pixels d'entrée, origine en haut à gauche, quels sont ses quatre targets $(l,t,r,b)$ vers les bords gauche, haut, droit et bas ?
Reponse: **Noyau attendu** : $(l,t,r,b)=(x-x_0,y-y_0,x_1-x,y_1-y)=(20,20,50,40)$ pixels.

**Approfondissement** : Le décodage $(x-l,y-t,x+r,y+b)$ redonne $(20,10,90,70)$. Le site est déjà exprimé dans l'image : ne pas le multiplier à nouveau par le stride. Exemple analytique construit et calculé, sans réseau exécuté.

**Erreurs bloquantes** : Confondre ces distances avec centre/largeur/hauteur, les exprimer en cellules de feature map ou ajouter 1 aux différences de coordonnées continues.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; [FCOS, version 5, §3.1, équation 1 et décodage](https://arxiv.org/html/1904.01355v5) ; calcul du projet.
Tags: cv::pilote cv::d08 famille::pratique cv_id::CV-DETECTEURS-007 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-008

Objectif : expliquer la modulation des négatifs faciles par Focal Loss. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-DETECTEURS-008
Question: En détection dense, pourquoi Focal Loss réduit-elle la domination des très nombreux négatifs faciles, au-delà d'une simple pondération des classes ?
Reponse: **Noyau attendu** : Elle multiplie l'entropie croisée par $(1-p_t)^\gamma$, où $p_t$ est la probabilité du label correct et $\gamma>0$. Un négatif facile a $p_t$ proche de 1 : sa contribution diminue fortement. Une pondération de classe seule ne distingue pas exemples faciles et difficiles de cette classe.

**Approfondissement** : La forme complète est $-\alpha_t(1-p_t)^\gamma\log p_t$. $\alpha_t$ pondère la classe ; $\gamma=0$ redonne l'entropie croisée pondérée. À $\gamma=2$ et $p_t=0{,}9$, le facteur vaut $0{,}01$. L'accent relatif sur les cas difficiles ne protège pas des mauvaises annotations.

**Erreurs bloquantes** : Confondre $p_t$ avec la probabilité d'objet pour un négatif, ou dire que la loss élimine tous les négatifs.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; [Focal Loss, version 2, §§2 et 3.1–3.2, équation 5](https://arxiv.org/html/1708.02002v2).
Tags: cv::pilote cv::d08 famille::comprehension cv_id::CV-DETECTEURS-008 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-009

Objectif : expliquer le signal de GIoU pour des boîtes disjointes. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-DETECTEURS-009
Question: Deux boîtes rectangulaires $A$ et $B$, alignées sur les axes, restent strictement disjointes pendant un petit déplacement. Pourquoi la loss $1-\operatorname{IoU}$ ne guide-t-elle pas ce déplacement, et quel terme GIoU ajoute-t-elle ?
Reponse: **Noyau attendu** : L'intersection reste nulle, donc IoU reste nul et sa loss constante à 1. GIoU soustrait à IoU la fraction vide du plus petit rectangle aligné sur les axes contenant les deux boîtes : $|C\setminus(A\cup B)|/|C|$. Ce terme géométrique peut varier même sans recouvrement et fournir un signal à la régression.

**Approfondissement** : Pour $A=(0,0,2,2)$ et $B=(3,0,5,2)$ en coordonnées continues, l'union vaut 8 et $|C|=10$ : GIoU $=-0{,}2$, loss $=1{,}2$. Rapprocher $B$ en $(2{,}5,0,4{,}5,2)$ donne une loss de $10/9$, IoU toujours nul. Calcul synthétique ; pas de garantie générale de convergence.

**Erreurs bloquantes** : Affirmer qu'une absence de recouvrement impose GIoU nul, ou remplacer $C$ par l'union des deux boîtes.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; [GIoU, version 2, §3.1 et algorithmes 1–2](https://arxiv.org/html/1902.09630v2) ; calcul du projet.
Tags: cv::pilote cv::d08 famille::raisonnement cv_id::CV-DETECTEURS-009 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-010

Objectif : expliquer l'apport des connexions latérales de FPN. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-DETECTEURS-010
Question: Pour détecter de petits objets, que gagne une FPN avec ses connexions latérales par rapport au seul suréchantillonnage de la dernière feature map du backbone ?
Reponse: **Noyau attendu** : Elle associe les représentations sémantiques profondes remontées par le chemin descendant aux features plus fines et mieux localisées du backbone. Le seul suréchantillonnage de la carte profonde ne restitue pas l'information spatiale de ces niveaux fins.

**Approfondissement** : Dans FPN original, projection latérale $1\times1$, addition à résolution commune, puis convolution $3\times3$. C'est une pyramide de features issue d'une image, pas nécessairement plusieurs images redimensionnées. Elle ne garantit pas la récupération des détails déjà perdus par le resize d'entrée.

**Erreurs bloquantes** : Attribuer de nouveaux détails observés à l'interpolation seule, ou confondre FPN et pyramide d'images.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; [FPN, version 2, §3 et figure 3](https://arxiv.org/html/1612.03144v2).
Tags: cv::pilote cv::d08 famille::comprehension cv_id::CV-DETECTEURS-010 provenance::agent pole::A pole::C pole::E
END
