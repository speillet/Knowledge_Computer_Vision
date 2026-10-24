# Représentations visuelles, ViT, Swin, ConvNeXt et DINOv2 — cartes

Fiche : [[70-reconnaissance-representations/references/71-representations-transfert|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::70-reconnaissance-representations

## CV-REPRESENTATIONS-001

Objectif : estimer le coût des tokens. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-REPRESENTATIONS-001
Question: Dans un ViT à patch fixe et attention globale dense, doubler largeur et hauteur change comment le nombre de tokens image (hors token de classe) et le terme quadratique associé ?
Reponse: **Noyau attendu** : Tokens ×4 ; terme quadratique ×16, dans ce modèle de coût.

**Approfondissement** : Ce n’est pas une prédiction exacte du temps total : kernels, mémoire et autres blocs comptent.

**Dérivation du coût** : avec des patches de côté $P$ fixé et des dimensions compatibles, $N=HW/P^2$. Doubler $H$ et $W$ multiplie le nombre de patches par quatre. Une matrice d'interactions globale entre tokens a alors seize fois plus de couples. Ce comptage concerne le terme d'attention considéré, pas toutes les opérations du réseau.

**Conséquence pratique proposée** : avant d'augmenter la résolution pour de petits défauts, estimer mémoire des activations et tester la latence complète. Les projections, convolutions éventuelles, kernels et contraintes de bande passante ne suivent pas nécessairement ce même facteur. Une réduction de batch ou une autre représentation peut modifier le compromis. Vérifier aussi si l'information du défaut existe dans l'acquisition initiale : agrandir une image sans détail supplémentaire n'apporte pas les mêmes observations qu'une capture réellement mieux résolue. Les mesures sur le matériel cible complètent donc le modèle de coût.

**Erreurs bloquantes** : Annoncer une latence ×16 garantie pour tout transformer.
Source: [[70-reconnaissance-representations/references/71-representations-transfert|Fiche complète]] ; [ViT, §3.1](https://arxiv.org/abs/2010.11929) ; comptage analytique du projet.
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

**Ce que l'on compare** : une architecture décrit les opérations et leurs connexions ; une recette d'entraînement décrit données, objectifs et réglages utilisés pour les apprendre. Une amélioration observée en changeant les deux ne se rapporte pas automatiquement à un seul mécanisme architectural.

**Exemple de comparaison construite** : pour une tâche dense, examiner résolution des features, hiérarchie et coût de la tête, puis comparer les mêmes splits et contraintes d'inférence. Une attention par fenêtres limite certaines interactions locales à un niveau, tandis que décalages et hiérarchie organisent l'échange d'information. Un ConvNet peut moderniser sa conception sans devenir une attention globale. Le bon raisonnement consiste à relier champ d'information, échelle, mémoire et protocole à la tâche, et pas à classer toutes les méthodes sous une étiquette supposée supérieure. Les méthodes nommées sont ici repérées ; chacune demanderait une fiche dédiée pour sa maîtrise complète.

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

**Passage de représentation à décision** : une feature décrit l'image selon le préentraînement ; le produit doit encore définir défaut, localisation et comportement quand aucun exemple connu ne convient. Une tête supervisée, une comparaison au nominal ou une recherche de voisins posent des problèmes et des besoins de données différents.

**Baseline proposée** : fixer extraction et prétraitement, choisir une règle simple, puis mesurer défauts manqués et faux rejets par type de pièce. Comparer ensuite une adaptation contrôlée avec les mêmes données réservées. Un excellent transfert moyen sur un benchmark n'établit pas la séparabilité des petits défauts de la nouvelle caméra. Examiner échelle des features, couverture du nominal et seuils avant de complexifier le système. La représentation est une ressource utile ; l'évaluation doit porter sur les sorties effectivement consommées par l'inspection, avec une politique pour les cas incertains.

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

**Raisonnement sur les ressources** : geler le backbone réduit le nombre de gradients et de paramètres modifiés, mais le calcul de ses features reste nécessaire pour chaque nouvelle image. Des modules d'adaptation peuvent réduire le coût d'apprentissage ou de stockage des variantes sans supprimer le backbone de l'inférence.

**Comparaison proposée** : conserver données et sortie cible, puis comparer une tête seule, une adaptation partielle et un ajustement complet sur généralisation, mémoire d'entraînement et coût final. Rapporter aussi le coût des activations et la façon dont les paramètres adaptés sont intégrés au modèle déployé. Un faible nombre de paramètres entraînés peut être utile pour plusieurs variantes produit ; il ne prouve pas une meilleure précision avec peu de données ni une accélération sur chaque runtime. Le choix dépend donc de la capacité nécessaire au changement de domaine et des ressources réellement contraintes.

**Erreurs bloquantes** : Assimiler faible nombre de paramètres entraînés et faible latence.
Source: [[70-reconnaissance-representations/references/71-representations-transfert|Fiche complète]] ; [ViT, §3.1](https://arxiv.org/abs/2010.11929) ; [Hu et al., LoRA, résumé et principe des paramètres gelés](https://arxiv.org/abs/2106.09685) ; [Houlsby et al., adapters, résumé](https://arxiv.org/abs/1902.00751) ; principe d’adaptation transposé à la vision, sans reprendre les gains NLP.
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

**Piège d'interface** : deux chargeurs peuvent produire des images visuellement semblables tout en différant dans l'ordre des canaux ou le traitement des centres de pixels. Une normalisation répétée ou omise peut également modifier fortement le tenseur reçu. Le backbone ne voit que ces valeurs, pas l'intention du pipeline.

**Enquête reproductible proposée** : utiliser un fichier témoin identique, enregistrer formes, types, plages et pixels connus après chaque étape, puis comparer les tenseurs d'entrée. Refaire l'extraction avec les mêmes poids et paramètres. Si les features changent avant toute variation de scène, rechercher d'abord cette différence déterministe. Une fois le contrat restauré, évaluer le nouveau domaine sur un ensemble réservé. Un fine-tuning lancé trop tôt peut absorber partiellement un bug de prétraitement, rendre la régression moins visible et compliquer la reproductibilité sans avoir traité sa cause.

**Erreurs bloquantes** : Changer l’entraînement sans contrôler le contrat d’entrée.
Source: [[70-reconnaissance-representations/references/71-representations-transfert|Fiche complète]] ; [DINOv2, résumé et évaluation par transfert](https://arxiv.org/abs/2304.07193) ; contrôle du prétraitement proposé par le projet.
Tags: cv::pilote cv::d07 famille::diagnostic cv_id::CV-REPRESENTATIONS-005 provenance::agent pole::A pole::D pole::E
END
