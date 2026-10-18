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

**Erreurs bloquantes** : accepter le système sur sa seule moyenne ou régler le seuil après observation des résultats du test final.
Source: [[130-evaluation-fiabilite/references/131-iou-ap-coco|Fiche IoU/AP]] ; [COCO, agrégations par catégorie et taille](https://cocodataset.org/#detection-eval).
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-IOU-AP-007 provenance::agent pole::A pole::C pole::E
END
