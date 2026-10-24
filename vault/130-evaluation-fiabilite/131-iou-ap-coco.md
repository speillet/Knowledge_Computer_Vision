# Cartes pilotes — IoU et AP COCO

Fiche : [[130-evaluation-fiabilite/references/131-iou-ap-coco|IoU/AP]]. Provenance : agent.

TARGET DECK: CV::Pilote::130-evaluation-fiabilite

## CV-IOU-AP-001

Objectif : calculer un recouvrement dans le bon contrat. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-IOU-AP-001
Question: Que faut-il fixer avant de calculer l'IoU de deux boîtes, et pourquoi un mélange `xyxy`/`xywh` peut-il rendre le résultat trompeur ?
Reponse: **Noyau attendu** : fixer format, repère, unité, validité et convention continue/inclusive. En `xyxy`, les deux derniers nombres sont un coin ; en `xywh`, ce sont largeur et hauteur. Convertir explicitement avant intersection et union.

**Approfondissement** : l'IoU vaut $|A\cap B|/(|A|+|B|-|A\cap B|)$, sans unité. Pour les boîtes continues du pilote, aire $(x_2-x_1)(y_2-y_1)$ sans `+1`. Ramener aussi boîtes normalisées, crop et padding dans le même repère. Une boîte dégénérée est une erreur de contrat à traiter, pas une raison d'ajouter silencieusement un epsilon.

**Exemple de contrat** : les nombres `(10,20,30,40)` décrivent soit deux coins, soit une origine et deux dimensions. Les régions obtenues ont alors des aires et positions différentes. Une formule d'intersection correcte ne peut pas compenser cette ambiguïté d'entrée.

**Contrôle proposé** : convertir une boîte connue vers le format de l'évaluateur, revenir au format initial et comparer ses coins. Répéter après resize et padding. Si prédiction et annotation subissent la même mise à l'échelle géométrique cohérente, leur IoU reste identique dans le cas idéal ; si une seule chaîne est convertie, le score change artificiellement. L'absence d'unité du ratio ne signifie donc pas absence de convention sur ses entrées.

**Erreurs bloquantes** : calculer directement entre conventions ou repères différents.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|Fiche IoU/AP]] ; [COCO, format des résultats](https://cocodataset.org/#format-results).
Tags: cv::pilote cv::d13 famille::pratique cv_id::CV-IOU-AP-001 provenance::agent pole::A pole::C pole::E
END

## CV-IOU-AP-002

Objectif : distinguer mesure locale et protocole agrégé. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-IOU-AP-002
Question: Quelle différence sépare l'IoU d'une paire, AP50, AP75 et l'AP principale COCO ?
Reponse: **Noyau attendu** : l'IoU mesure un recouvrement de régions. AP50 et AP75 évaluent le classement précision/rappel avec un seuil de recouvrement fixé à 0,50 ou 0,75. L'AP principale COCO moyenne dix seuils de 0,50 à 0,95 par pas de 0,05, ainsi que les catégories valides et les niveaux de rappel du protocole.

**Approfondissement** : un score AP n'est pas une moyenne des IoU ni une précision à un seuil de score unique. Toujours préciser bbox/segm, sous-ensemble de tailles et nombre maximal de prédictions. AP75 demande une localisation plus stricte qu'AP50, sans isoler à elle seule toutes les causes d'erreur.

**Lecture d'un résultat** : AP50 peut rester élevée lorsque les boîtes sont suffisamment proches pour un critère permissif mais manquent la précision exigée à 0,75. Cette différence est informative pour la localisation, sans prouver que le réseau soit la cause : repères ou annotations peuvent aussi intervenir.

**Décision proposée** : consulter les courbes et erreurs par classe et taille, puis choisir le point d'exploitation sur validation. Un seuil de score utilisé en production sélectionne un sous-ensemble de la liste ; l'AP résume un protocole de classement plus large. Une même AP peut donc accompagner des compromis métier différents. Conserver les conventions de l'évaluateur et le nombre de prédictions retenues avant de comparer des versions.

**Erreurs bloquantes** : interpréter AP50 comme 50 % de précision ou comme la moyenne des recouvrements.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|Fiche IoU/AP]] ; [protocole officiel COCO](https://cocodataset.org/#detection-eval).
Tags: cv::pilote cv::d13 famille::comprehension cv_id::CV-IOU-AP-002 provenance::agent pole::A pole::C pole::E
END

## CV-IOU-AP-003

Objectif : expliquer la pénalité d'un doublon. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-IOU-AP-003
Question: Deux prédictions bien localisées couvrent la même GT ordinaire. Pourquoi peuvent-elles donner un TP puis un FP dans une évaluation de détection ?
Reponse: **Noyau attendu** : l'appariement suit le protocole et l'ordre des scores ; une GT ordinaire ne peut justifier qu'un seul TP. La seconde prédiction est un doublon même si son recouvrement est élevé.

**Approfondissement** : une NMS vise notamment cette redondance mais peut supprimer de vrais voisins. Les crowds et GT ignorées ont des règles spécifiques : ne pas généraliser la règle ordinaire à toutes les annotations COCO. Le classement des doublons influence la courbe précision/rappel et donc l'AP.

**Pourquoi le doublon coûte** : après le premier TP, la seconde boîte augmente le nombre de prédictions positives sans ajouter d'objet retrouvé. La précision peut donc baisser alors que le rappel ne progresse pas. Son influence sur l'AP dépend notamment de son rang par rapport aux détections suivantes.

**Contrôle construit** : garder les boîtes et permuter seulement les scores du doublon et d'une autre détection. Observer la courbe de précision/rappel sous le même protocole. Ne pas conclure qu'un faux positif tardif est sans coût dans le produit : il peut encore être émis au seuil d'exploitation. L'évaluation et le posttraitement ont donc des rôles complémentaires, avec une exception explicite pour les annotations auxquelles s'appliquent des règles crowd ou ignore.

**Erreurs bloquantes** : compter chaque prédiction recouvrant suffisamment la même GT comme un nouveau TP.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|Fiche IoU/AP]] ; [cocoeval.py, evaluateImg L235](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py#L235).
Tags: cv::pilote cv::d13 famille::algorithme cv_id::CV-IOU-AP-003 provenance::agent pole::A pole::C pole::E
END

## CV-IOU-AP-004

Objectif : reconstruire une AP interpolée simple. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-IOU-AP-004
Question: Pour deux GT valides, une seule catégorie, un seuil IoU fixé et aucune crowd/ignore, les prédictions ordonnées sont TP, FP doublon, TP. Comment obtenir l'AP interpolée aux 101 rappels ?
Reponse: **Noyau attendu** : rappels $0,5;0,5;1$, précisions $1;0,5;2/3$. L'enveloppe maximale vers la droite vaut 1 jusqu'au rappel 0,5 inclus, puis $2/3$. Donc $AP=(51+50\times2/3)/101\approx0,834983$.

**Approfondissement** : les 101 niveaux sont $0;0,01;\ldots;1$, donc 51 niveaux sont au plus 0,5. Les rappels inatteignables reçoivent zéro ; une seule GT détectée sur deux donnerait $51/101$, malgré une précision de 1 pour la seule détection. Exemple exécuté ; ce calcul simplifié n'implémente pas tout COCO.

**Raisonnement de classement** : la deuxième prédiction ne retrouve aucune nouvelle GT et fait passer la précision courante à un demi. La troisième atteint le rappel maximal avec une précision de deux tiers ; l'enveloppe reprend ce meilleur niveau pour les rappels intermédiaires accessibles.

**Variation interprétée** : placer le doublon après les deux TP peut conserver une enveloppe d'AP parfaite dans ce petit cas, alors que le système produit toujours un doublon. Le score résume donc un classement sous une convention précise et pas toutes les conséquences métier de la liste. Examiner aussi les sorties au seuil d'exploitation, puis ne généraliser ce calcul jouet ni aux crowds ni aux autres détails de l'évaluateur complet.

**Erreurs bloquantes** : moyenner seulement les trois précisions brutes ou remplacer les 101 rappels par un unique point d'exploitation.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|Fiche IoU/AP]] ; [cocoeval.py, accumulate L353](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py#L353).
Tags: cv::pilote cv::d13 famille::raisonnement cv_id::CV-IOU-AP-004 provenance::agent pole::A pole::C pole::E
END

## CV-IOU-AP-005

Objectif : comparer des évaluateurs avec prudence. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-IOU-AP-005
Question: Deux outils annoncent une AP COCO différente pour les mêmes sorties. Quels éléments faut-il aligner avant de conclure à une erreur du modèle ?
Reponse: **Noyau attendu** : aligner split/GT, catégories, bbox ou masque, conversions de coordonnées, filtres de score/NMS/top-k, maxDets, ignore/crowd, tailles, version de l'évaluateur et interpolation. Comparer le même fichier de résultats et les paramètres effectifs.

**Approfondissement** : dans le code pycocotools épinglé avec `useCats=1`, maxDets est appliqué par image et catégorie ; la page descriptive évoque un top-100 global et certains wrappers peuvent le faire en amont. Décrire la chaîne réellement exécutée plutôt qu'une règle universelle. Les catégories sans GT valide sont exclues, pas comptées comme AP zéro.

**Reproduction proposée** : archiver un seul fichier de prédictions et une seule version de GT, puis faire varier uniquement l'évaluateur ou son paramètre suspect. Comparer d'abord le nombre d'images, de catégories, de GT valides et de détections effectivement retenues avant le score final.

**Pourquoi ces contrôles précèdent le modèle** : une différence de maxDets ou de catégorie ignorée change les objets admis dans le calcul sans modifier les poids ni les boîtes du détecteur. Chercher une régression d'inférence alors que l'écart vient du protocole ferait perdre du temps. Une attribution correcte exige la trace de la chaîne complète et les règles réellement exécutées par le wrapper, pas seulement le nom COCO affiché.

**Erreurs bloquantes** : appeler tout calcul maison « COCO » sans règles d'appariement, ou comparer des ensembles de catégories différents sans le signaler.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|Fiche IoU/AP]] ; [cocoeval.py épinglé](https://github.com/cocodataset/cocoapi/blob/8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9/PythonAPI/pycocotools/cocoeval.py).
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-IOU-AP-005 provenance::agent pole::A pole::C pole::E
END

## CV-IOU-AP-006

Objectif : diagnostiquer un écart selon l'exigence de localisation. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-IOU-AP-006
Question: AP50 reste élevée alors qu'AP75 baisse fortement après un nouveau prétraitement. Que vérifier sans attribuer immédiatement le problème au réseau ?
Reponse: **Noyau attendu** : vérifier la précision de localisation et la propagation des coordonnées à travers resize/crop/padding. Comparer prédictions et GT dans le même repère, puis analyser les résultats par taille et classe.

**Approfondissement** : une petite translation peut laisser l'IoU au-dessus de 0,50 et sous 0,75, surtout sur de petits objets. Vérifier aussi arrondis, format de boîte et posttraitement. L'écart suggère une sensibilité au critère de recouvrement, mais ne démontre pas à lui seul une cause unique.

**Exemple de signature** : une translation de deux pixels peut être faible pour une grande boîte et représenter une fraction importante d'un petit défaut. Une erreur constante de padding ou d'arrondi peut donc affecter différemment les tailles et les seuils de recouvrement.

**Enquête proposée** : tester quelques boîtes connues à travers le nouveau prétraitement et son inverse, puis comparer les prédictions avant et après posttraitement sur les mêmes images. Examiner les vecteurs d'erreur et non uniquement les moyennes d'AP. Si le contrat de coordonnées est correct, poursuivre vers acquisition, résolution effective ou qualité de régression. Cette démarche transforme une signature de métriques en hypothèses testables, sans attribuer automatiquement la baisse à un bug précis.

**Erreurs bloquantes** : prendre AP75 pour une métrique de classification indépendante de la géométrie, ou conclure à un bug précis sans inspection.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|Fiche IoU/AP]] ; [COCO, définition des métriques](https://cocodataset.org/#detection-eval).
Tags: cv::pilote cv::d13 famille::diagnostic cv_id::CV-IOU-AP-006 provenance::agent pole::A pole::C pole::E
END

## CV-IOU-AP-007

Objectif : relier moyenne benchmark et décision métier. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-IOU-AP-007
Question: Un détecteur a une bonne AP moyenne mais rate les défauts les plus coûteux sur de petites pièces. Comment compléter l'évaluation pour décider de sa mise en service ?
Reponse: **Noyau attendu** : examiner rappel et faux positifs au seuil d'exploitation, les classes/tailles critiques et les conditions d'acquisition réelles, avec les coûts métier. Une moyenne sur classes et seuils peut masquer une erreur rare mais grave.

**Approfondissement** : fixer les seuils sur validation, conserver un test représentatif, analyser incertitude et cas hors distribution selon le besoin. Mesurer aussi latence et comportement aval. L'AP reste utile pour comparer le classement et la localisation sous protocole fixé, sans certifier la fiabilité du produit.

**Contrat de décision** : définir les défauts dont l'absence de détection est coûteuse, la charge acceptable de faux rejets et le comportement des cas incertains. Une AP moyenne pondère des catégories selon son protocole ; elle ne connaît pas automatiquement cette hiérarchie des conséquences.

**Validation proposée** : conserver des lots indépendants incluant petites tailles et conditions difficiles, puis mesurer les erreurs au seuil figé et les performances des sous-groupes critiques. Examiner aussi le délai utile et les erreurs introduites par les étapes aval. Un gain d'AP peut être intéressant sans suffire à autoriser la mise en service. La conclusion doit dire quel usage a été validé, sur quelles données et avec quelles limites, plutôt que convertir un score agrégé en garantie de fiabilité.

**Erreurs bloquantes** : accepter le système sur sa seule moyenne ou régler le seuil après observation des résultats du test final.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|Fiche IoU/AP]] ; [COCO, agrégations par catégorie et taille](https://cocodataset.org/#detection-eval).
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-IOU-AP-007 provenance::agent pole::A pole::C pole::E
END
