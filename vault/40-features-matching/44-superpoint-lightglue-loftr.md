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

**Contrats successifs** : les coordonnées indiquent où les observations se trouvent, les descripteurs représentent leurs voisinages, et le matcher utilise les deux ensembles pour décider quelles paires sont compatibles. L'information contextuelle du matcher peut aider à départager des ressemblances locales, mais elle reste une prédiction apprise sur une distribution de données.

**Exemple de pipeline construit** : extraire les features compatibles avec le checkpoint, convertir les positions dans les repères déclarés, obtenir les candidats, puis estimer une homographie si l'objet observé est plan. Contrôler erreur et couverture sur la région utile. Si la scène présente de la parallaxe, un grand nombre de matches n'autorise pas automatiquement un warp global. Comparer à une baseline SIFT ou ORB sur les mêmes paires. Le remplacement du matcher change la proposition de correspondances ; il ne fournit pas à lui seul la calibration ni la validation finale du système.

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

**Lecture de l'architecture** : la recherche à niveau grossier construit des hypothèses de correspondance à partir du contexte des deux images ; l'étape fine précise certaines positions retenues. « Sans détecteur » désigne l'absence du détecteur sparse classique comme point d'entrée obligatoire, pas l'assurance que chaque point de la scène aura un correspondant visible.

**Exemple de limite** : une région occultée dans la deuxième vue n'a pas de correspondance physique observable, même si un modèle retourne un score ou une position candidate. Une trajectoire demanderait en outre d'associer les observations à travers plusieurs instants et de gérer disparition et retour. Déclarer la représentation, les masques de validité et les critères de rejet, puis évaluer les positions avec une géométrie ou des annotations indépendantes. La confiance du réseau est une donnée de décision à vérifier sur le domaine cible, et non un certificat de trajectoire correcte.

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

**Pourquoi la dimension ne suffit pas** : deux vecteurs de même longueur peuvent coder des propriétés différentes, avec d'autres distributions de normes, d'orientations et de scores. Les couches du matcher apprennent à exploiter ces conventions. Brancher une représentation inconnue respecte éventuellement les formes des tenseurs tout en rompant le contrat statistique du modèle.

**Contrôle proposé** : reproduire d'abord l'extracteur et le checkpoint indiqués par les auteurs, sur une paire témoin dont la transformation est connue. Conserver explicitement les transformations de coordonnées. Remplacer ensuite un composant à la fois et mesurer correspondances, couverture et erreur géométrique. Si une autre représentation est envisagée, rechercher des poids compatibles ou une adaptation réellement évaluée. Une exécution sans exception ne démontre ni cette compatibilité ni un gain de matching. Ce raisonnement porte sur l'interface apprise ; il ne condamne pas les changements de représentation lorsqu'ils sont accompagnés d'une validation appropriée.

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

**Définir le gain utile** : fixer d'abord la tâche finale, par exemple recaler une pièce avec une erreur admissible dans une région donnée. Un matcher peut produire davantage de paires mais les concentrer sur une zone peu utile, ou augmenter le coût de vérification. Les comptes intermédiaires n'indiquent donc pas seuls un progrès produit.

**Comparaison construite** : utiliser des paires réservées couvrant texture, flou, éclairage et changement de point de vue. Conserver les règles d'acceptation géométrique et séparer réglage des seuils et test final. Rapporter succès, erreurs d'acceptation, refus, mémoire et latence de bout en bout sur le même matériel. Si une méthode utilise une résolution supérieure ou un autre prétraitement, le déclarer comme différence du pipeline. La comparaison reste valable pour ce protocole ; sa généralisation à une nouvelle caméra ou à une autre usine demande encore des observations représentatives.

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

**Exemple analytique** : si le réseau reçoit $x'=sx+p_x$ et $y'=sy+p_y$, où $s$ est le facteur de resize et $(p_x,p_y)$ le padding en pixels réseau, le retour vaut $x=(x'-p_x)/s$, $y=(y'-p_y)/s$. Chaque image peut avoir ses propres paramètres. Soustraire seulement le padding sans remettre l'échelle laisse une erreur systématique.

**Vérification proposée** : suivre trois points connus, notamment un point proche de l'origine et un point éloigné, à travers le prétraitement et son inverse. Contrôler ensuite que le seuil de reprojection est exprimé dans le même repère que les résidus. Une superposition visuelle sur l'image paddée peut sembler juste alors que l'estimateur reçoit des coordonnées de deux espaces différents. Le problème se situe alors dans le contrat des données, et changer le checkpoint ou le seuil du matcher risque de le masquer sans le résoudre.

**Erreurs bloquantes** : Mélanger coordonnées normalisées et pixels dans une même estimation.
Source: [[40-features-matching/references/44-superpoint-lightglue-loftr|Fiche complète]] ; [LightGlue, README, Usage et Advanced configuration, consulté le 2026-10-20](https://github.com/cvg/LightGlue) ; diagnostic de changement de repère déduit par le projet.
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-MATCH-APPRIS-005 provenance::agent pole::B
END
