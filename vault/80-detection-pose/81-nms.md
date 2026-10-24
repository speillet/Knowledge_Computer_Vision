# Cartes pilotes — NMS

Fiche : [[80-detection-pose/references/81-nms|NMS]]. Provenance : agent.

TARGET DECK: CV::Pilote::80-detection-pose

## CV-NMS-001

Objectif : dérouler hard NMS. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-NMS-001
Question: Trois boîtes continues $A=(0,0,10,10)$, $B=(2,0,12,10)$ et $C=(20,0,30,10)$ ont les scores $0,9;0,8;0,7$. Quelles boîtes garde une hard NMS qui supprime pour IoU supérieure à 0,5 ?
Reponse: **Noyau attendu** : sélectionner $A$, supprimer $B$ car leur intersection vaut 80, l'union 120 et l'IoU $2/3>0,5$ ; conserver ensuite $C$, disjointe. La sortie est donc $A,C$.

**Approfondissement** : le calcul utilise `xyxy` continu sans `+1`. La sélection est gloutonne et suit les scores, sans fusion des boîtes. À seuil 0,7, cet exemple garderait les trois : le seuil contrôle la redondance, pas directement la justesse sémantique. Résultat exécuté dans l'exemple arithmétique du dépôt.

**Raisonnement sur les instances** : le recouvrement est utilisé comme indice de redondance entre prédictions, sans connaître l'identité réelle des objets. Si A et B représentent deux personnes proches, supprimer B peut retirer une vraie instance ; si elles représentent la même pièce, la suppression peut au contraire être utile.

**Contrôle proposé** : conserver les sorties avant et après l'opération et vérifier quelles annotations restent couvertes. Le seuil règle donc un compromis dépendant de la scène. Une boîte éloignée reste candidate même avec un score plus faible, tant qu'elle passe les autres filtres du pipeline. Cette lecture évite de transformer la sélection gloutonne en règle « une boîte par image » ou « une boîte par classe ».

**Erreurs bloquantes** : supprimer $C$ au seul motif de son score inférieur, ou traiter la sortie comme une moyenne de $A$ et $B$.
Source: [[80-detection-pose/references/81-nms|Fiche NMS]] ; [Soft-NMS, §4](https://arxiv.org/abs/1704.04503) ; [convention hard NMS](https://docs.pytorch.org/vision/stable/generated/torchvision.ops.nms.html).
Tags: cv::pilote cv::d08 famille::algorithme cv_id::CV-NMS-001 provenance::agent pole::A pole::C pole::E
END

## CV-NMS-002

Objectif : distinguer trois seuils. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-NMS-002
Question: En détection, quelle différence sépare seuil de score, seuil IoU de NMS et seuil IoU d'évaluation ?
Reponse: **Noyau attendu** : le seuil de score filtre les prédictions selon leur confiance ; le seuil NMS compare deux prédictions pour réduire les doublons ; le seuil IoU d'évaluation compare une prédiction à une annotation selon le protocole.

**Approfondissement** : un même nombre numérique ne leur donne pas le même sens. La NMS ne consulte pas la GT au moment de l'inférence. Modifier un seuil de score peut changer rappel et coût avant NMS ; modifier NMS affecte les doublons et les voisins conservés ; modifier le seuil d'évaluation change l'exigence de localisation. Consigner les trois séparément.

**Exemple de distinction** : une prédiction peut passer le seuil de score, être supprimée pour son recouvrement avec une autre prédiction et ne jamais atteindre l'évaluation. À l'inverse, deux boîtes conservées peuvent correspondre à un seul objet et l'une devenir un doublon dans le protocole de mesure.

**Enquête proposée** : journaliser les étapes et leurs paramètres séparément, puis calculer la couverture des mêmes annotations à chaque stade. Modifier l'exigence IoU de l'évaluation ne change pas les boîtes que le système a produites ; modifier le seuil NMS peut les changer. Régler les paramètres sur validation, puis figer le protocole. Une valeur numérique identique, par exemple 0,5, ne rapproche pas les responsabilités de ces trois décisions.

**Erreurs bloquantes** : utiliser le seuil AP50 pour décider directement quelles prédictions se suppriment entre elles, ou dire que NMS requiert la GT.
Source: [[80-detection-pose/references/81-nms|Fiche NMS]] ; [NMS](https://docs.pytorch.org/vision/stable/generated/torchvision.ops.nms.html) ; [COCO](https://cocodataset.org/#detection-eval).
Tags: cv::pilote cv::d08 famille::comprehension cv_id::CV-NMS-002 provenance::agent pole::A pole::C pole::E
END

## CV-NMS-003

Objectif : choisir le périmètre d'une suppression. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-NMS-003
Question: Deux candidates de classes différentes, de scores $0{,}9$ et $0{,}8$, ont une IoU de $0{,}8$. Avec un seuil NMS de $0{,}5$, quel compromis distingue suppression globale et suppression par classe ?
Reponse: **Noyau attendu** : La NMS globale conserve seulement la candidate de score $0{,}9$ ; la NMS par classe conserve les deux. Cela protège deux objets de classes différentes, mais laisse aussi deux labels concurrents sur une même instance. Choisir selon que les annotations autorisent ces deux détections ou imposent une classe exclusive.

**Approfondissement** : Personne et vélo peuvent être deux objets légitimes qui se recouvrent. Deux catégories exclusives d'une même pièce demandent une décision de classe ; prendre le score maximal ne garantit pas le bon label. Une NMS par classe conserve aussi plusieurs instances disjointes de cette classe : elle n'impose pas une boîte par catégorie. Les scores, repères et règles de sortie doivent être comparables.

**Cas construit** : une personne et son vélo peuvent fournir deux catégories valides qui se recouvrent. Deux types de pièce exclusifs sur la même instance posent une autre question : il faut décider du label, pas seulement empêcher des boîtes de se supprimer.

**Validation proposée** : annoter clairement instances et taxonomie, puis examiner les conflits interclasses et les voisins de même classe. Une NMS par classe protège les catégories différentes mais pas deux personnes très proches l'une de l'autre. Le bon choix se mesure sur les erreurs utiles au produit, avec scores et seuils consignés, sans déduire une identité physique du seul recouvrement.

**Erreurs bloquantes** : Croire que NMS par classe résout les confusions interclasses, ou que NMS globale connaît l'identité réelle des objets.
Source: [[80-detection-pose/references/81-nms|Fiche NMS]] ; [Torchvision 0.29, batched_nms : description et seuil](https://docs.pytorch.org/vision/0.29/generated/torchvision.ops.batched_nms.html), consulté le 2026-10-21 ; cas construit du projet.
Tags: cv::pilote cv::d08 famille::comparaison cv_id::CV-NMS-003 provenance::agent pole::A pole::C pole::E
END

## CV-NMS-004

Objectif : expliquer l'effet de Soft-NMS. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-NMS-004
Question: Que change Soft-NMS gaussienne par rapport à hard NMS, et pourquoi faut-il revoir l'ordre des candidats après une pénalisation ?
Reponse: **Noyau attendu** : au lieu d'une suppression immédiate au-delà d'un recouvrement, elle réduit le score de chaque candidate selon son recouvrement avec la boîte retenue $M$ : $s_i\leftarrow s_i\exp(-\operatorname{IoU}(M,b_i)^2/\sigma)$, avec $\sigma>0$. Les scores modifiés changent le prochain maximum, donc l'ordre doit être recalculé.

**Approfondissement** : la pénalité gaussienne agit sur les recouvrements sans même seuil discontinu que hard NMS. Un seuil de score final peut éliminer les boîtes devenues trop faibles : Soft-NMS ne garantit pas de tout conserver ni de résoudre toutes les occultations. Préciser variante et convention d'aire avant une comparaison.

**Interprétation de l'ordre** : après pénalisation, une candidate initialement deuxième peut devenir moins prioritaire qu'une autre candidate peu recouvrante. Reprendre le maximum actuel fait partie de la logique gloutonne. Parcourir une fois l'ancien classement correspondrait à une autre procédure.

**Exemple de contrôle** : enregistrer à chaque étape boîte retenue et scores restants sur un petit ensemble connu. Comparer ensuite hard et soft à seuils de score annoncés, en comptant doublons et vrais voisins supprimés. La modification des scores n'ajoute aucune observation à la scène et ne résout pas nécessairement des instances très superposées. Une amélioration doit être mesurée sur validation avant d'être attribuée à la méthode.

**Erreurs bloquantes** : garder l'ancien ordre malgré les nouveaux scores ou dire que Soft-NMS ne peut jamais retirer de boîte.
Source: [[80-detection-pose/references/81-nms|Fiche NMS]] ; [Bodla et al., §4 pénalités, §5 seuil final](https://arxiv.org/abs/1704.04503) ; [code original](https://github.com/bharatsingh430/soft-nms/blob/b8e69bdf8df2ad53025c9d198ded909b50471d4f/lib/nms/cpu_nms.pyx).
Tags: cv::pilote cv::d08 famille::raisonnement cv_id::CV-NMS-004 provenance::agent pole::A pole::C pole::E
END

## CV-NMS-005

Objectif : localiser la cause d'une disparition. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-NMS-005
Question: Un objet disparaît des sorties finales dans une zone dense. Comment déterminer si la NMS est en cause et choisir une intervention vérifiable ?
Reponse: **Noyau attendu** : comparer boîtes, scores et classes avant/après NMS avec l'annotation ; vérifier quelle GT cesse d'être couverte, si une proposition correcte existait et par quelle boîte elle a été supprimée. Si elle n'existait pas, changer NMS ne la recréera pas.

**Approfondissement** : deux personnes distinctes restent en concurrence dans une NMS par classe : partager le label ne signifie pas partager l'identité. Si une vraie voisine est supprimée, tester seuil ou Soft-NMS sur validation et mesurer rappel, doublons, AP et effets sur le tracker. Vérifier les coordonnées et le top-k amont ; une suppression de doublon qui laisse la GT couverte ne diminue pas son rappel. Le résultat attendu est une cause étayée et un compromis mesuré.

**Pourquoi l'amont doit être conservé** : si une vraie boîte est absente dès les prédictions décodées, NMS n'a jamais eu l'occasion de la garder. Si elle existe puis disparaît, retrouver sa concurrente et le calcul de recouvrement permet de tester une cause de sélection concrète.

**Ablation proposée** : faire varier uniquement le posttraitement sur les mêmes sorties de réseau, avec mêmes annotations et limites de détections. Mesurer objets manqués et doublons ensemble, puis observer les pistes temporelles affectées. Une amélioration locale dans une foule peut introduire davantage de doublons ailleurs. La correction doit donc répondre au diagnostic et rester vérifiée sur un ensemble réservé, pas seulement faire réapparaître une boîte dans une image choisie.

**Erreurs bloquantes** : modifier directement le seuil sur le jeu de test ou confondre erreur de proposition et suppression.
Source: [[80-detection-pose/references/81-nms|Fiche NMS]] ; [Soft-NMS, §§1 et 4](https://arxiv.org/abs/1704.04503).
Tags: cv::pilote cv::d08 famille::diagnostic cv_id::CV-NMS-005 provenance::agent pole::A pole::C pole::E
END

## CV-NMS-006

Objectif : interpréter l'inclusion de boîtes dans une suppression par IoU. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-NMS-006
Question: Deux boîtes continues de même classe, $A=(0,0,100,100)$ et $B=(40,40,60,60)$, ont les scores $0{,}9$ et $0{,}8$. L'inclusion de B dans A entraîne-t-elle sa suppression par une hard NMS à IoU $>0{,}5$ ? Justifier.
Reponse: **Noyau attendu** : Non. L'intersection a l'aire de B, 400, et l'union celle de A, 10000 : IoU $=0{,}04$. A est sélectionnée, puis B reste puisque le seuil n'est pas dépassé.

**Approfondissement** : Pour $B\subset A$, IoU $=|B|/|A|$, et non intersection divisée par aire de B. Ce dernier rapport vaudrait 1. La géométrie seule ne tranche pas entre objet imbriqué, partie d'objet et deux localisations d'une même instance. Exemple analytique du projet.

**Lecture géométrique** : une petite boîte entièrement contenue dans une grande a une intersection égale à sa propre aire, mais une union égale à la grande aire. Le recouvrement relatif à la petite boîte et l'IoU répondent donc à deux questions différentes. Remplacer l'un par l'autre changerait la règle de suppression.

**Conséquence de diagnostic** : deux boîtes survivantes ne prouvent pas deux instances : elles peuvent être deux localisations très différentes de la même pièce. À l'inverse, objet et partie d'objet peuvent être tous deux légitimes si la taxonomie le prévoit. Vérifier les annotations, les scores et le contrat de sortie avant de modifier la mesure de recouvrement. Ce cas analytique montre une limite du slogan « les grandes boîtes éliminent les petites ».

**Erreurs bloquantes** : Donner une IoU de 1 dès qu'il y a inclusion, ou supprimer automatiquement toute boîte plus petite.
Source: [[80-detection-pose/references/81-nms|Fiche NMS]] ; [GIoU, version 2, §3, équation 1](https://arxiv.org/html/1902.09630v2) ; [Soft-NMS, §4 : hard NMS](https://arxiv.org/html/1704.04503) ; calcul du projet.
Tags: cv::pilote cv::d08 famille::raisonnement cv_id::CV-NMS-006 provenance::agent pole::A pole::C pole::E
END
