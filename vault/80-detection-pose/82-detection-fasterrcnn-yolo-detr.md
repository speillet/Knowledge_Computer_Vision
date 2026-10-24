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

**Lecture du partage de calcul** : le backbone transforme l'image en cartes de features communes. Le réseau de propositions et la tête exploitent ensuite ces représentations selon la variante. Le traitement par régions ajoute un coût lié au nombre et à la taille des représentations régionales, sans imposer de refaire toute l'extraction sur l'image brute pour chacune.

**Exemple de comparaison construite** : deux implémentations peuvent avoir le même backbone mais des nombres de propositions différents, et donc des temps de tête différents. Mesurer extraction, propositions, opérations régionales et posttraitement séparément pour identifier le goulet. Une catégorie two-stage décrit l'organisation des décisions ; elle ne donne pas une formule universelle de latence. Conserver résolution, batch et seuils dans le protocole, et comparer aussi la qualité sur les petits objets et scènes denses. Le choix produit repose sur ce bilan complet, plutôt que sur le seul nombre d'étapes annoncé.

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

**Pourquoi le nom ne suffit pas** : une famille peut évoluer dans la représentation des boîtes, l'assignation d'entraînement, les losses et la sélection finale. Une explication correcte pour un article peut devenir fausse si on l'applique à un checkpoint issu d'une autre recette portant un nom voisin.

**Fiche de configuration proposée** : relever dépôt et révision, architecture, données, prétraitement, résolution, stratégie de supervision et posttraitement réellement exécuté. Vérifier quelques boîtes connues à travers encodage et décodage. Comparer ensuite les systèmes sur les mêmes annotations, critères et coûts inclus. Une variation dite anchor-free ne supprime pas la nécessité d'assigner des cibles d'apprentissage. Une sortie sans NMS doit elle aussi être décrite par son contrat. Ce niveau de précision permet de relier une erreur à une décision de conception au lieu de généraliser un détail à toutes les générations.

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

**Déroulement de la supervision** : les prédictions de requêtes sont comparées aux cibles pour choisir une correspondance de coût minimal. La loss utilise cette correspondance pour apprendre les classes et les boîtes ; les requêtes restantes apprennent l'absence d'objet selon la formulation. Cette décision utilise les annotations pendant l'entraînement.

**Contraste avec l'inférence** : une NMS compare entre elles des prédictions disponibles sans annotations pour réduire les doublons. L'évaluateur compare encore autrement prédictions et vérité terrain afin de compter erreurs et succès. Les trois opérations peuvent parler d'appariement ou de boîtes, mais leurs entrées, objectifs et moments d'utilisation diffèrent. Dans un diagnostic construit, examiner d'abord à quel stade un objet est mal supervisé, supprimé ou compté. Le matching biparti n'est donc ni une recette universelle de posttraitement ni une preuve automatique d'absence de doublons pour toute variante déployée.

**Erreurs bloquantes** : Décrire les trois mécanismes comme un seul matching interchangeable.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; [DETR, §3.1, fig. 1 et équations 1–2](https://arxiv.org/abs/2005.12872).
Tags: cv::pilote cv::d08 famille::algorithme cv_id::CV-DETECTEURS-003 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-004

Objectif : analyser les petits objets après resize. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-DETECTEURS-004
Question: Cas A — diagnostic : à checkpoint et images fixés, l'AP des petits objets chute quand des images $1920\times1080$ passent à une entrée $640\times640$ avec conservation du ratio et padding centré. Certains objets font $12\times9$ pixels à l'origine. Quels contrôles distinguent les causes possibles ?
Reponse: **Noyau attendu** : Vérifier d'abord l'aller-retour des boîtes avec resize et padding. Mesurer ensuite leur taille effective et le rappel de ces mêmes objets avant filtrage, après seuil de score, puis après NMS éventuelle. Une GT couverte avant mais plus après désigne une perte de sélection ; si aucune candidate correcte n'existe en amont, examiner échelle, features et assignation d'entraînement.

**Approfondissement** : Le facteur est $1/3$, le padding vertical 140 pixels par côté, l'objet devient $4\times3$. La fiche calcule un cas où une boîte parfaite de score $0{,}8$ disparaît au profit d'une boîte moins bien localisée de score $0{,}9$. Conserver classes, seuil IoU et strates de taille d'origine pour comparer le rappel. La petite taille seule ne prouve pas une perte d'information responsable de l'échec.

**Erreurs bloquantes** : Oublier d'inverser le padding, compter les doublons comme du rappel, ou régler les seuils sur le test.

**Critères de correction du cas** : trois contrôles discriminants (géométrie, échelle, filtrage), hypothèses explicites et conclusion conditionnelle. Cas construit ; calcul géométrique vérifié, aucune observation terrain.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; diagnostic et calculs du projet ; [FPN, version 2, §3](https://arxiv.org/html/1612.03144v2) ; [Soft-NMS, §4](https://arxiv.org/html/1704.04503).
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

**Comparer la même grandeur** : le débit en batch mesure une quantité d'images traitées par unité de temps ; la latence décrit le délai subi par une observation. Un moteur peut améliorer le premier tout en ajoutant de l'attente avant de traiter une image isolée.

**Protocole proposé** : annoncer échauffement, synchronisation des mesures, inclusion des copies et du décodage, puis rapporter une distribution de latences dans des conditions de charge représentatives. Vérifier la qualité avec les mêmes seuils, surtout pour tailles et classes critiques. Les paramètres de top-k ou de score peuvent réduire le coût du posttraitement tout en changeant le rappel : ils font partie de la configuration. Une comparaison utile au produit porte sur les mêmes sorties, la même cible matérielle et la même exigence de décision. Un FPS isolé d'un article ne démontre ni cette comparabilité ni le respect d'un budget caméra→décision.

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

**Rôle de cette décision** : le site ne reçoit pas une boîte simplement parce qu'elle existe dans l'image ; il doit être admissible dans la géométrie et le niveau concernés. La sélection résout les conflits de supervision avant la loss. La NMS ne remplit pas ce rôle, puisqu'elle traite des prédictions lors de la sélection finale.

**Exemple construit** : deux objets superposés peuvent contenir le même site, mais la règle de taille et d'aire choisit la cible décrite par cette formulation. Changer l'assigner change alors les exemples positifs et les régressions apprises. Pour diagnostiquer des objets manqués, visualiser les sites réellement supervisés plutôt que se limiter à la courbe de loss globale.

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

**Interprétation géométrique** : chaque valeur est une longueur depuis le site jusqu'à une face dans le même repère. La somme gauche+droit donne la largeur de la boîte, et haut+bas sa hauteur. Le site n'est pas nécessairement le centre : les distances peuvent donc être asymétriques.

**Contrôle proposé** : encoder une boîte connue, la décoder, puis appliquer l'inverse du resize/padding pour retrouver l'annotation d'origine. Tester aussi un site près d'un bord. Si une normalisation par stride existe dans une autre implémentation, la déclarer et l'inverser exactement une fois. Un réseau peut apprendre des valeurs numériques tout en produisant des boîtes fausses si ces conventions sont mélangées à l'interface.

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

**Sens de la modulation** : pour un négatif correctement classé comme fond, la probabilité du label correct peut être proche de un. Sa perte réduite empêche de nombreux cas faciles d'écraser l'apprentissage des exemples plus difficiles. La pondération de classe agit sur une autre dimension du déséquilibre.

**Limite de diagnostic** : un exemple difficile peut être informatif ou mal annoté. Lui donner davantage d'importance relative ne garantit donc pas une meilleure supervision. Dans une ablation construite, conserver assignation et données, comparer les distributions de contributions et les erreurs par taille et classe. La formule décrit une modification de l'objectif, pas une promesse de rappel supérieur sur toute configuration de détecteur.

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

**Pourquoi le terme supplémentaire aide** : les positions relatives influencent l'espace vide du rectangle englobant même lorsque l'intersection ne change pas. La loss dispose ainsi d'une variation géométrique absente du seul recouvrement dans ce cas. Cela ne signifie pas que toute direction de déplacement soit parfaitement renseignée.

**Validation proposée** : vérifier le calcul sur des boîtes simples, puis distinguer signal de localisation et classement des scores. Une meilleure loss sur des paires de boîtes n'implique pas une meilleure AP si assignation, scores ou annotations posent problème. Comparer les variantes avec mêmes données et recette autant que possible, en examinant les erreurs concrètes de localisation sur des observations réservées.

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

**Différence entre calcul et observation** : interpoler une carte profonde augmente son nombre de positions mais ne recrée pas les détails qu'elle ne représente plus. Les connexions latérales apportent au contraire des features issues de résolutions plus fines de la chaîne. Leur fusion vise à combiner localisation et information sémantique.

**Contrôle construit** : comparer petits objets et grands objets à résolution d'entrée fixée, en changeant seulement l'accès aux niveaux fins. Examiner rappel, localisation et coût. Si le petit objet ne couvre déjà presque aucun pixel dans l'entrée, une FPN ne restaure pas l'information physique détruite par l'acquisition ou le resize. La pyramide de features est une brique du système, pas un substitut à un contrat d'image adapté.

**Erreurs bloquantes** : Attribuer de nouveaux détails observés à l'interpolation seule, ou confondre FPN et pyramide d'images.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; [FPN, version 2, §3 et figure 3](https://arxiv.org/html/1612.03144v2).
Tags: cv::pilote cv::d08 famille::comprehension cv_id::CV-DETECTEURS-010 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-011

Objectif : distinguer des erreurs de classe, de localisation et de doublon. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-DETECTEURS-011
Question: Trois cas indépendants ont chacun une seule GT « voiture », sans ignore/crowd. Avec les seuils TIDE $t_b=0{,}1$, $t_f=0{,}5$, quelle erreur décrit chaque FP : (a) « camion », IoU $0{,}8$ ; (b) « voiture », IoU $0{,}3$ ; (c) « voiture », IoU $0{,}8$, mais la GT est déjà associée à une boîte de score supérieur ?
Reponse: **Noyau attendu** : (a) Classification : localisation suffisante, mauvaise classe. (b) Localisation : bonne classe, recouvrement intermédiaire. (c) Doublon : classe et localisation suffisantes, mais la GT a déjà une détection associée.

**Approfondissement** : TIDE distingue aussi l'erreur combinée classe/localisation, le fond et les GT manquées non déjà expliquées par classification/localisation. Orienter les vérifications vers labels/classes, géométrie ou posttraitement selon le cas, sans en déduire automatiquement une cause. Le nombre de FP seul ne mesure pas la perte d'AP : leur classement par score compte aussi.

**Utilité du classement** : il indique où chercher une explication, sans identifier automatiquement la cause. Une mauvaise classe peut venir d'une taxonomie ambiguë ou d'un modèle ; une mauvaise localisation peut venir du réseau ou d'une transformation de coordonnées ; un doublon peut refléter le posttraitement.

**Protocole proposé** : sélectionner des exemples de chaque famille, conserver image, annotations et étapes de sortie, puis tester une hypothèse à la fois. Le rang des erreurs par score compte pour l'AP : corriger plusieurs erreurs de faible score n'a pas forcément le même effet qu'une erreur très confiante. Une correction oracle est un outil de diagnostic du protocole, pas la prédiction du gain d'un réentraînement réel.

**Erreurs bloquantes** : Compter (c) comme un second TP, ou attribuer (a) à une mauvaise localisation.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; [TIDE, version 2, §2.2 : types et pondération des erreurs](https://arxiv.org/html/2008.08115v2) ; cas construits du projet.
Tags: cv::pilote cv::d08 famille::diagnostic cv_id::CV-DETECTEURS-011 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-012

Objectif : diagnostiquer un faux positif pouvant provenir d'une annotation manquante. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-DETECTEURS-012
Question: Un détecteur produit une boîte très confiante sans GT associée ; l'image semble pourtant montrer un objet de la classe visée. Que vérifier avant de conclure à une confusion avec le fond ?
Reponse: **Noyau attendu** : Confronter l'image à la politique d'annotation : présence et classe réelles, conventions de boîte, exclusions et règles crowd/ignore. Si l'objet aurait dû être annoté mais a été omis, une détection non ignorée est comptée FP malgré sa pertinence visuelle. La confiance du modèle ne suffit pas à prouver l'omission.

**Approfondissement** : Le projet propose de faire arbitrer les cas ambigus, versionner les corrections et réévaluer tous les modèles sur la même GT corrigée, en conservant l'ancien bilan. TIDE documente des objets manquants et des flags crowd erronés ; cela ne rend pas tous les FP suspects ni toutes les annotations exhaustives.

**Arbitrage proposé** : faire vérifier le cas selon une règle d'annotation commune à tous les modèles, avec accès à l'image et au contexte utile. Conserver les objets exclus intentionnellement distincts des omissions accidentelles. Documenter version et motifs des corrections.

**Limite de la conclusion** : un modèle peut être très confiant et faux ; l'apparence de plausibilité ne suffit donc pas à créer une nouvelle vérité terrain. Réévaluer l'ensemble des systèmes sur la même version corrigée évite de favoriser celui dont les sorties ont déclenché la revue. L'enquête porte sur la qualité du benchmark autant que sur celle du détecteur, et son résultat doit rester traçable.

**Erreurs bloquantes** : Supprimer les FP gênants d'un seul modèle, ou transformer automatiquement toute détection confiante en annotation.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; [TIDE, version 2, §3.4 et annexes D–E : annotations ambiguës/manquantes et détections ignorées](https://arxiv.org/html/2008.08115v2) ; protocole de correction proposé par le projet.
Tags: cv::pilote cv::d08 famille::diagnostic cv_id::CV-DETECTEURS-012 provenance::agent pole::A pole::C pole::E
END

## CV-DETECTEURS-013

Objectif : distinguer instances, classes et étiquettes par instance. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-DETECTEURS-013
Question: Une tâche demande de localiser trois voitures et deux vélos, avec un seul label par objet. Est-ce nécessairement une classification multi-étiquette par boîte ? Distinguer nombre d'instances, classes présentes et labels par instance.
Reponse: **Noyau attendu** : Non : il y a cinq instances, deux classes présentes, mais un label par instance dans ce contrat. La détection peut produire plusieurs instances d'une même classe. Multi-étiquette signifie que plusieurs labels sont valides pour une même instance, selon la taxonomie.

**Approfondissement** : Des labels hiérarchiques comme « véhicule » et « voiture » peuvent coexister si les annotations l'autorisent ; deux classes exclusives proposées sur le même objet restent une ambiguïté. YOLOv3 utilise des classifieurs logistiques indépendants, mais les labels effectivement rendus dépendent aussi des seuils et du posttraitement. Une NMS par classe ne garantit ni un label unique par instance ni une seule boîte par classe.

**Exemple de contrat** : cinq objets distincts de deux catégories demandent cinq décisions de localisation et de classe, sans imposer plusieurs labels sur chacune. Une taxonomie hiérarchique peut ajouter une autre règle, mais il faut alors la définir dans les annotations et les sorties attendues.

**Conséquence pour le pipeline** : des boîtes proches peuvent représenter doublons, catégories concurrentes ou objets distincts. NMS ne connaît pas directement cette sémantique. Examiner labels par instance et couverture des annotations avant de transformer une sortie multiclasse en une règle de suppression. Cette distinction relie supervision, posttraitement et évaluation, au lieu de déduire le contrat du seul nombre de labels présents dans l'image.

**Erreurs bloquantes** : Confondre plusieurs objets dans une image avec plusieurs labels pour un objet, ou limiter la sortie à une boîte par catégorie.
Source: [[80-detection-pose/references/82-detection-fasterrcnn-yolo-detr|Fiche complète]] ; [YOLOv3, version 1, §§2.2–2.3](https://arxiv.org/html/1804.02767v1) ; [Torchvision 0.29, batched_nms : séparation des catégories](https://docs.pytorch.org/vision/0.29/generated/torchvision.ops.batched_nms.html) ; exemples de contrats du projet.
Tags: cv::pilote cv::d08 famille::comprehension cv_id::CV-DETECTEURS-013 provenance::agent pole::A pole::C pole::E
END
