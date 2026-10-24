# Otsu, distance transform et watershed — cartes

Fiche : [[90-segmentation/references/91-otsu-distance-watershed|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::90-segmentation

## CV-WATERSHED-001

Objectif : interpréter l’objectif Otsu. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-WATERSHED-001
Question: Pourquoi un seuil Otsu optimal sur l’histogramme peut-il être mauvais pour segmenter les défauts ?
Reponse: **Noyau attendu** : L’objectif sépare des intensités selon une variance, pas des catégories métier ; éclairage, déséquilibre et bruit peuvent dominer.

**Approfondissement** : Tester un masque annoté et la taille des défauts ; comparer seuillage local ou une autre représentation si l’hypothèse échoue.

**Lecture de l'objectif** : Otsu choisit une coupure selon les poids et moyennes des groupes d'intensité. Une partition qui sépare bien deux niveaux de luminosité peut surtout distinguer ombre et zone éclairée, alors que le défaut traverse les deux. L'optimum appartient au critère statistique retenu, pas à une connaissance des pièces.

**Exemple construit** : un défaut très petit et peu contrasté pèse peu dans l'histogramme global d'une grande image. Une coupure adaptée au fond majoritaire peut donc le manquer. Comparer le masque aux annotations de défauts, en stratifiant tailles et éclairage. Tester une correction d'acquisition ou un seuillage local si elle correspond à l'hypothèse observée, sans supposer que tout seuil automatique est robuste à toute scène. Pour du comptage, il faudra encore séparer les objets : une partition binaire correcte ne fournit pas leurs identités d'instance.

**Erreurs bloquantes** : Déduire l’optimalité sémantique de l’optimum d’un critère d’intensité.
Source: [[90-segmentation/references/91-otsu-distance-watershed|Fiche complète]] ; [OpenCV Otsu, théorie](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html) ; [OpenCV watershed, marqueurs et API](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html).
Tags: cv::pilote cv::d09 famille::raisonnement cv_id::CV-WATERSHED-001 provenance::agent pole::A pole::E
END

## CV-WATERSHED-002

Objectif : reconstruire le pipeline à marqueurs. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-WATERSHED-002
Question: Comment distance transform et watershed peuvent-ils séparer des objets qui se touchent ?
Reponse: **Noyau attendu** : Construire un masque, estimer des centres/marqueurs depuis les distances, identifier fond/inconnu puis propager les labels.

**Approfondissement** : Un même masque peut produire des séparations différentes selon les marqueurs ; valider chaque étape.

**Rôles successifs** : la distance au fond traduit l'épaisseur locale du premier plan. Des maxima peuvent indiquer des intérieurs de régions, mais ne deviennent des marqueurs d'objets qu'avec une règle de sélection. Le watershed utilise ensuite ces germes et une topographie pour répartir les zones encore inconnues.

**Exemple construit** : deux disques en contact peuvent former une seule composante binaire, tout en conservant deux intérieurs assez distincts pour fournir deux marqueurs. Si les maxima sont fusionnés ou si le bruit en crée beaucoup, la partition peut être sous-segmentée ou fragmentée. Visualiser masque, distances, marqueurs et labels dans cet ordre pour localiser l'étape responsable. La métrique de distance et la résolution changent aussi l'échelle des valeurs. Le succès sur des formes simples ne prouve pas que chaque objet irrégulier ou partiellement occulté produira naturellement un seul maximum utile.

**Erreurs bloquantes** : Présenter la distance transform comme une segmentation d’instances autonome.
Source: [[90-segmentation/references/91-otsu-distance-watershed|Fiche complète]] ; [OpenCV Otsu, théorie](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html) ; [OpenCV watershed, marqueurs et API](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html).
Tags: cv::pilote cv::d09 famille::algorithme cv_id::CV-WATERSHED-002 provenance::agent pole::A pole::E
END

## CV-WATERSHED-003

Objectif : distinguer fond et inconnu. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-WATERSHED-003
Question: Dans les marqueurs watershed OpenCV documentés, pourquoi ne pas coder tout le fond connu et l’inconnu à zéro ?
Reponse: **Noyau attendu** : Zéro représente une zone à attribuer ; le fond déjà déterminé doit avoir un label positif comme les autres marqueurs connus.

**Approfondissement** : Les frontières produites valent −1 ; conserver type, forme et modification sur place selon l’API.

**Pourquoi la distinction importe** : un marqueur représente une région dont l'identité est déjà fixée pour la propagation ; l'inconnu désigne une région que l'algorithme doit attribuer. Coder un fond connu comme inconnu retire donc une information de l'initialisation au lieu de lui donner un label de fond.

**Contrôle construit** : créer une petite scène avec un objet et une zone de fond certaine, afficher les marqueurs avant l'appel puis les labels après. Vérifier que les identifiants positifs correspondent aux régions prévues et réserver la valeur spéciale de frontière à son sens final. Conserver une copie si l'on doit comparer l'entrée, puisque le tableau concerné est modifié. Ces détails sont propres au contrat OpenCV documenté ; ils ne définissent pas toutes les implémentations de watershed. Une sortie du bon type ne prouve pas encore que les marqueurs décrivent les bons objets physiques.

**Erreurs bloquantes** : Assimiler valeur 0 à un fond définitivement classé.
Source: [[90-segmentation/references/91-otsu-distance-watershed|Fiche complète]] ; [OpenCV Otsu, théorie](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html) ; [OpenCV watershed, marqueurs et API](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html).
Tags: cv::pilote cv::d09 famille::pratique cv_id::CV-WATERSHED-003 provenance::agent pole::A pole::E
END

## CV-WATERSHED-004

Objectif : localiser une sous-segmentation. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-WATERSHED-004
Question: Deux objets restent dans un bassin malgré un masque qui les couvre bien. Quelle vérification est discriminante ?
Reponse: **Noyau attendu** : Visualiser les marqueurs : s’il n’existe qu’un germe commun, revoir séparation des maxima et hypothèses de forme.

**Approfondissement** : Comparer à des marqueurs manuels sur une copie pour isoler le rôle des germes ; augmenter des seuils au hasard n’identifie pas la cause.

**Ablation sur les germes** : conserver image, masque et paramètres, puis remplacer uniquement les marqueurs automatiques par deux germes manuels cohérents sur une copie. Si la séparation s'améliore, cela soutient un problème de construction des marqueurs. Si elle reste mauvaise, examiner aussi topographie, masque et géométrie des objets.

**Lecture du résultat** : une bonne couverture binaire indique seulement que le premier plan est présent. Le nombre de régions et leur frontière dépendent d'autres décisions. Un objet irrégulier peut avoir plusieurs maxima de distance sans représenter plusieurs instances ; deux objets très joints peuvent au contraire n'offrir qu'une concentration. Choisir une règle de maxima selon des tailles et formes justifiées, puis mesurer erreurs de fusion et de séparation sur d'autres images. Le diagnostic doit distinguer absence d'information, mauvaise initialisation et mauvaise règle, au lieu de multiplier les seuils sans contrôle.

**Erreurs bloquantes** : Valider des instances sur la seule qualité du masque binaire.
Source: [[90-segmentation/references/91-otsu-distance-watershed|Fiche complète]] ; [OpenCV Otsu, théorie](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html) ; [OpenCV watershed, marqueurs et API](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html).
Tags: cv::pilote cv::d09 famille::diagnostic cv_id::CV-WATERSHED-004 provenance::agent pole::A pole::E
END

## CV-WATERSHED-005

Objectif : choisir une métrique d’instances classique. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-WATERSHED-005
Question: Pourquoi une IoU binaire élevée peut-elle masquer l’échec d’un pipeline de comptage watershed ?
Reponse: **Noyau attendu** : La fusion de plusieurs objets peut conserver presque toute la région de premier plan mais perdre le nombre et l’identité des instances.

**Approfondissement** : Mesurer fusions/séparations et protocole d’appariement des objets, en plus du masque global.

**Exemple analytique** : deux objets adjacents dont l'union est exactement prédite peuvent donner un masque de premier plan parfait. Si la sortie ne possède qu'un label pour cette union, le recouvrement binaire vaut pourtant un alors que le comptage de deux objets échoue. La métrique ne contredit pas l'échec : elle mesure une autre sortie.

**Évaluation proposée** : définir une association entre instances prédites et réelles, puis compter objets retrouvés, fusions, fragments et faux objets. Conserver le masque global comme mesure complémentaire, en annonçant seuils et traitement des contacts. Vérifier plusieurs densités et tailles, car les erreurs de séparation peuvent augmenter dans les zones où la région binaire reste bonne. Le contrat du produit, par exemple compter des pièces, doit donc guider les annotations et les mesures avant le choix du pipeline de segmentation.

**Erreurs bloquantes** : Confondre recouvrement sémantique et comptage correct.
Source: [[90-segmentation/references/91-otsu-distance-watershed|Fiche complète]] ; [OpenCV Otsu, théorie](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html) ; [OpenCV watershed, marqueurs et API](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html).
Tags: cv::pilote cv::d09 famille::evaluation cv_id::CV-WATERSHED-005 provenance::agent pole::A pole::E
END
