# Segmentation sémantique, instances et panoptique — cartes

Fiche : [[90-segmentation/references/93-semantique-instances-panoptique|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::90-segmentation

## CV-SEGMENTATION-001

Objectif : choisir la sortie de segmentation. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-SEGMENTATION-001
Question: Quelle différence sépare segmentation sémantique, d’instances et panoptique ?
Reponse: **Noyau attendu** : Sémantique : classe par pixel ; instances : séparer objets comptables ; panoptique : partition sans recouvrement, avec classe et instance pour things, classe pour stuff.

**Approfondissement** : Le masque d’un objet sans classe ne remplit pas automatiquement le contrat panoptique.

**Exemple de contrat** : deux personnes qui se touchent partagent le label sémantique personne mais doivent avoir des IDs d'instance différents si l'on veut les compter. Une région de ciel relève du stuff dans le contrat panoptique usuel et ne demande pas la même séparation en objets comptables.

**Conséquence pour les données** : un masque de classe ne contient pas forcément la frontière entre deux instances de même classe. Un modèle entraîné sur ces seuls labels ne reçoit donc pas explicitement cette information. Les identifiants d'instances peuvent être renumérotés sans changer la partition ; leur valeur numérique n'exprime pas une quantité à interpoler. Définir aussi pixels ignorés et politique de recouvrement avant l'évaluation. Un score de recouvrement par classe, un score d'instances et PQ testent des aspects différents : choisir celui qui correspond au livrable demandé, avec des mesures complémentaires si plusieurs propriétés comptent.

**Erreurs bloquantes** : Assimiler classe identique et identité d’instance identique.
Source: [[90-segmentation/references/93-semantique-instances-panoptique|Fiche complète]] ; [Panoptic Segmentation, §3 : format, stuff/things et absence de recouvrement](https://arxiv.org/abs/1801.00868).
Tags: cv::pilote cv::d09 famille::comparaison cv_id::CV-SEGMENTATION-001 provenance::agent pole::A pole::E
END

## CV-SEGMENTATION-002

Objectif : détecter une mauvaise définition de tâche. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-SEGMENTATION-002
Question: Un modèle sémantique segmente très bien un tas de pièces mais ne permet pas leur comptage. Est-ce nécessairement un échec de réseau ?
Reponse: **Noyau attendu** : Non : la sortie peut ne pas séparer les instances. Vérifier tâche, labels et métrique avant la capacité du réseau.

**Approfondissement** : Ajouter un pipeline d’instances ou des marqueurs selon acquisition, puis évaluer fusions/séparations.

**Pourquoi la sortie peut être correcte** : si les labels d'apprentissage décrivent toute la matière d'une classe, fusionner des pièces en contact peut respecter la supervision. Le réseau n'a pas nécessairement été entraîné à placer une frontière entre ces instances. Un défaut d'interface de tâche peut donc précéder tout problème de capacité.

**Enquête proposée** : vérifier annotations et sortie attendue, puis examiner si l'image contient des indices de séparation. Comparer composantes seules, marqueurs et méthode d'instances sur les mêmes scènes, en comptant fusions et fragments. Des pièces parfaitement superposées peuvent aussi rester ambiguës dans une seule vue. Une amélioration de mIoU ne règle pas automatiquement le comptage : elle peut provenir de meilleurs pixels de fond ou de régions déjà faciles. Relier la mesure au nombre et aux positions des objets utiles évite de poursuivre un indicateur qui ne représente pas le besoin.

**Erreurs bloquantes** : Déduire le nombre d’objets d’une bonne mIoU.
Source: [[90-segmentation/references/93-semantique-instances-panoptique|Fiche complète]] ; [Reinke et al., P1 et fig. 1/3 : métrique et catégorie de problème](https://www.nature.com/articles/s41592-023-02150-0) ; application au comptage : raisonnement du projet.
Tags: cv::pilote cv::d09 famille::diagnostic cv_id::CV-SEGMENTATION-002 provenance::agent pole::A pole::E
END

## CV-SEGMENTATION-003

Objectif : propager une augmentation dense. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-SEGMENTATION-003
Question: Pourquoi une augmentation géométrique d’image doit-elle être appliquée différemment mais de façon cohérente au masque de classes ?
Reponse: **Noyau attendu** : La géométrie doit rester alignée ; l’interpolation du masque doit préserver les labels discrets selon le contrat.

**Approfondissement** : Contrôler aussi void, crops/padding et reconstruction de l’image complète. Une interpolation continue peut créer des labels artificiels.

**Deux types de valeurs** : une intensité peut représenter une mesure continue que l'on interpole ; un ID de classe représente une catégorie. Une moyenne entre labels 1 et 3 ne signifie pas automatiquement la classe 2. La transformation spatiale doit toutefois placer la classe au même endroit que le contenu correspondant dans l'image.

**Contrôle construit** : transformer une image et un masque simples dont la frontière est connue, afficher leur superposition et examiner les valeurs uniques du masque obtenu. Vérifier pixels ignorés et valeur de padding. Distinguer cette opération sur labels discrets d'une interpolation éventuelle de logits ou probabilités avant décision, qui concerne une autre représentation. Pour le tuilage, contrôler aussi restitution du crop dans l'image complète. Une erreur d'alignement peut dégrader l'apprentissage même si chaque fichier semble visuellement plausible pris séparément ; la cohérence doit donc être testée sur la paire image–annotation.

**Erreurs bloquantes** : Transformer l’image seule ou lisser les IDs de classe comme des intensités.
Source: [[90-segmentation/references/93-semantique-instances-panoptique|Fiche complète]] ; Conséquence du contrat de labels discrets de la fiche ; [Panoptic Segmentation, §3 : classes et IDs](https://arxiv.org/abs/1801.00868).
Tags: cv::pilote cv::d09 famille::pratique cv_id::CV-SEGMENTATION-003 provenance::agent pole::A pole::E
END

## CV-SEGMENTATION-004

Objectif : évaluer une segmentation médicale. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-SEGMENTATION-004
Question: Pourquoi une bonne Dice moyenne ne suffit-elle pas pour conclure à l’utilité d’une segmentation médicale ?
Reponse: **Noyau attendu** : Elle mesure un recouvrement selon protocole ; validation externe, frontières, cas rares, unités physiques et usage visé apportent d’autres preuves.

**Approfondissement** : Séparer patients/sites et rapporter cas vides ou échecs ; aucun score seul ne démontre une décision clinique utile.

**Pourquoi le recouvrement est partiel** : une région volumineuse peut conserver une forte Dice malgré une erreur localisée sur une frontière importante. Une petite structure manquée peut également peser peu dans certaines agrégations. Le score doit donc être interprété dans ses unités, son niveau d'agrégation et ses conventions de vides.

**Évaluation technique proposée** : séparer patients et sites, mesurer frontières dans la géométrie physique appropriée et conserver les cas rares ou absents. Définir la sortie effectivement utile et une référence indépendante, puis examiner les échecs individuellement. Une amélioration sur une validation interne peut dépendre de l'acquisition et ne pas se transférer à un autre site. Ces contrôles décrivent la validité technique du modèle ; ils ne constituent pas un avis médical ni une preuve d'utilité clinique. Le raisonnement senior garde distincts performance de segmentation, reproductibilité du protocole et conséquence dans l'usage envisagé.

**Erreurs bloquantes** : Déduire une utilité clinique du seul benchmark interne.
Source: [[90-segmentation/references/93-semantique-instances-panoptique|Fiche complète]] ; [Reinke et al., P2.1–P2.3, P3.2 et discussion](https://www.nature.com/articles/s41592-023-02150-0) ; protocole externe/patients/sites proposé par le projet.
Tags: cv::pilote cv::d09 famille::evaluation cv_id::CV-SEGMENTATION-004 provenance::agent pole::A pole::E
END
