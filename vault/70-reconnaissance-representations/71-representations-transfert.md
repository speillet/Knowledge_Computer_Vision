# Représentations visuelles, ViT, Swin, ConvNeXt et DINOv2 — cartes

Fiche : [[70-reconnaissance-representations/references/71-representations-transfert|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::70-reconnaissance-representations

## CV-REPRESENTATIONS-001

Objectif : estimer le coût des tokens. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-REPRESENTATIONS-001
Question: Dans un ViT à patch fixe et attention globale dense, doubler largeur et hauteur change comment le nombre de tokens et le terme quadratique d’attention ?
Reponse: **Noyau attendu** : Tokens ×4 ; terme quadratique ×16, dans ce modèle de coût.

**Approfondissement** : Ce n’est pas une prédiction exacte du temps total : kernels, mémoire et autres blocs comptent.

**Erreurs bloquantes** : Annoncer une latence ×16 garantie pour tout transformer.
Source: [[70-reconnaissance-representations/references/71-representations-transfert|Fiche complète]] ; [ViT, §§3–4](https://arxiv.org/abs/2010.11929) ; [Swin, §3](https://arxiv.org/abs/2103.14030) ; [ConvNeXt, §2](https://arxiv.org/abs/2201.03545) ; [DINOv2, méthode et transfert](https://arxiv.org/abs/2304.07193).
Tags: cv::pilote cv::d07 famille::raisonnement cv_id::CV-REPRESENTATIONS-001 provenance::agent pole::A pole::D pole::E
END

## CV-REPRESENTATIONS-002

Objectif : situer Swin et ConvNeXt. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-REPRESENTATIONS-002
Question: Swin et ConvNeXt remplacent-ils les CNN par la même attention globale ?
Reponse: **Noyau attendu** : Non : Swin utilise une hiérarchie à fenêtres locales décalées ; ConvNeXt reste un ConvNet modernisé.

**Approfondissement** : Séparer structure et recette d’entraînement, puis comparer sur le même protocole cible.

**Erreurs bloquantes** : Qualifier ConvNeXt de transformer ou chaque couche Swin d’attention globale.
Source: [[70-reconnaissance-representations/references/71-representations-transfert|Fiche complète]] ; [ViT, §§3–4](https://arxiv.org/abs/2010.11929) ; [Swin, §3](https://arxiv.org/abs/2103.14030) ; [ConvNeXt, §2](https://arxiv.org/abs/2201.03545) ; [DINOv2, méthode et transfert](https://arxiv.org/abs/2304.07193).
Tags: cv::pilote cv::d07 famille::comparaison cv_id::CV-REPRESENTATIONS-002 provenance::agent pole::A pole::D pole::E
END

## CV-REPRESENTATIONS-003

Objectif : utiliser des features autosupervisées. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-REPRESENTATIONS-003
Question: Que manque-t-il entre des features DINOv2 et un détecteur industriel de défauts prêt à évaluer ?
Reponse: **Noyau attendu** : Définir sorties, tête ou stratégie de décision, données, seuils et protocole de validation du produit.

**Approfondissement** : Des features transférables ne sont pas automatiquement une taxonomie sémantique ou un score calibré sur le nouveau domaine.

**Erreurs bloquantes** : Présenter l’extraction seule comme une solution supervisée complète.
Source: [[70-reconnaissance-representations/references/71-representations-transfert|Fiche complète]] ; [ViT, §§3–4](https://arxiv.org/abs/2010.11929) ; [Swin, §3](https://arxiv.org/abs/2103.14030) ; [ConvNeXt, §2](https://arxiv.org/abs/2201.03545) ; [DINOv2, méthode et transfert](https://arxiv.org/abs/2304.07193).
Tags: cv::pilote cv::d07 famille::comprehension cv_id::CV-REPRESENTATIONS-003 provenance::agent pole::A pole::D pole::E
END

## CV-REPRESENTATIONS-004

Objectif : choisir une adaptation. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-REPRESENTATIONS-004
Question: Quel compromis distingue linear probing, fine-tuning complet et LoRA/adapters en transfert visuel ?
Reponse: **Noyau attendu** : Ils entraînent respectivement une tête, tout le modèle ou une partie paramétrée plus réduite ; coût d’apprentissage et flexibilité diffèrent.

**Approfondissement** : Mesurer généralisation, données nécessaires et coût final ; peu de paramètres appris ne garantit pas une inférence plus rapide.

**Erreurs bloquantes** : Assimiler faible nombre de paramètres entraînés et faible latence.
Source: [[70-reconnaissance-representations/references/71-representations-transfert|Fiche complète]] ; [ViT, §§3–4](https://arxiv.org/abs/2010.11929) ; [Swin, §3](https://arxiv.org/abs/2103.14030) ; [ConvNeXt, §2](https://arxiv.org/abs/2201.03545) ; [DINOv2, méthode et transfert](https://arxiv.org/abs/2304.07193).
Tags: cv::pilote cv::d07 famille::comparaison cv_id::CV-REPRESENTATIONS-004 provenance::agent pole::A pole::D pole::E
END

## CV-REPRESENTATIONS-005

Objectif : contrôler le prétraitement d’un backbone. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-REPRESENTATIONS-005
Question: Un backbone préentraîné se dégrade après remplacement du chargeur d’images. Que vérifier avant un nouveau fine-tuning ?
Reponse: **Noyau attendu** : Ordre couleur, normalisation, plage, interpolation, crop et résolution réellement reçus.

**Approfondissement** : Comparer une image identique dans les deux chaînes avant d’attribuer l’écart aux données ou à l’architecture.

**Erreurs bloquantes** : Changer l’entraînement sans contrôler le contrat d’entrée.
Source: [[70-reconnaissance-representations/references/71-representations-transfert|Fiche complète]] ; [ViT, §§3–4](https://arxiv.org/abs/2010.11929) ; [Swin, §3](https://arxiv.org/abs/2103.14030) ; [ConvNeXt, §2](https://arxiv.org/abs/2201.03545) ; [DINOv2, méthode et transfert](https://arxiv.org/abs/2304.07193).
Tags: cv::pilote cv::d07 famille::diagnostic cv_id::CV-REPRESENTATIONS-005 provenance::agent pole::A pole::D pole::E
END
