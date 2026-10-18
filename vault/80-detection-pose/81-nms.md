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

**Erreurs bloquantes** : utiliser le seuil AP50 pour décider directement quelles prédictions se suppriment entre elles, ou dire que NMS requiert la GT.
Source: [[80-detection-pose/references/81-nms|Fiche NMS]] ; [NMS](https://docs.pytorch.org/vision/stable/generated/torchvision.ops.nms.html) ; [COCO](https://cocodataset.org/#detection-eval).
Tags: cv::pilote cv::d08 famille::comprehension cv_id::CV-NMS-002 provenance::agent pole::A pole::C pole::E
END

## CV-NMS-003

Objectif : choisir le périmètre d'une suppression. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-NMS-003
Question: Deux catégories peuvent se recouvrir dans l'image. Quel compromis distingue une NMS globale d'une NMS par classe ?
Reponse: **Noyau attendu** : une NMS globale peut supprimer une boîte d'une autre classe ; une NMS par classe évite cette suppression mais peut conserver plusieurs classes sur le même objet. Choisir selon la sémantique des labels et l'évaluation.

**Approfondissement** : un casque et une personne peuvent légitimement se recouvrir ; deux catégories exclusives d'une même pièce peuvent exiger un autre traitement. Vérifier aussi scores comparables et conventions de coordonnées. La séparation par classe n'est pas une garantie universelle de bonne décision.

**Erreurs bloquantes** : annoncer que la NMS standard connaît automatiquement les classes ou qu'une stratégie gagne dans toutes les tâches.
Source: [[80-detection-pose/references/81-nms|Fiche NMS]] ; [Torchvision batched_nms](https://docs.pytorch.org/vision/stable/generated/torchvision.ops.batched_nms.html).
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
Reponse: **Noyau attendu** : comparer boîtes, scores et classes avant/après NMS avec l'annotation ; vérifier si une proposition correcte existait et par quelle boîte elle a été supprimée. Si elle n'existait pas, changer NMS ne la recréera pas.

**Approfondissement** : si une vraie voisine est supprimée, tester seuil ou Soft-NMS sur validation et mesurer rappel, doublons, AP et effets sur le tracker. Vérifier les coordonnées et le top-k amont avant d'accuser l'algorithme. Le résultat attendu est une cause étayée et un compromis mesuré, pas une hausse automatique du seuil.

**Erreurs bloquantes** : modifier directement le seuil sur le jeu de test ou confondre erreur de proposition et suppression.
Source: [[80-detection-pose/references/81-nms|Fiche NMS]] ; [Soft-NMS, §§1 et 4](https://arxiv.org/abs/1704.04503).
Tags: cv::pilote cv::d08 famille::diagnostic cv_id::CV-NMS-005 provenance::agent pole::A pole::C pole::E
END
