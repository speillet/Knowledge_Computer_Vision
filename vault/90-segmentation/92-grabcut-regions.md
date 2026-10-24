# GrabCut, régions et modèles d’apparence — cartes

Fiche : [[90-segmentation/references/92-grabcut-regions|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::90-segmentation

## CV-GRABCUT-001

Objectif : expliquer l’alternance GrabCut. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-GRABCUT-001
Question: Quelles deux opérations principales GrabCut alterne-t-il ?
Reponse: **Noyau attendu** : Estimer les modèles d’apparence fond/objet puis optimiser les labels via graph cut dans l’énergie définie.

**Approfondissement** : Les contraintes sûres et probables de l’initialisation ont un rôle distinct ; le procédé n’est pas un classifieur sémantique générique.

**Intuition de l'alternance** : les labels actuels donnent des exemples de couleur pour le fond et le premier plan ; les modèles d'apparence influencent ensuite le coût de chaque attribution. Les relations entre voisins ajoutent une préférence spatiale. La nouvelle partition sert à une nouvelle estimation, dans les contraintes de l'initialisation.

**Exemple de limite** : si une partie de la cible ressemble au fond, son coût d'apparence peut favoriser la mauvaise région. Une indication utilisateur peut apporter une information que la couleur seule ne fournit pas. Le procédé ne nomme pas automatiquement un objet selon une taxonomie et un minimum d'énergie n'est pas une preuve de vérité métier. Vérifier initialisation et labels sûrs avant d'augmenter les itérations. Pour comparer à une méthode promptable apprise, compter aussi les interventions, les échecs et le coût complet, et pas seulement le temps de la dernière optimisation.

**Erreurs bloquantes** : Décrire seulement un seuil de couleur fixe.
Source: [[90-segmentation/references/92-grabcut-regions|Fiche complète]] ; [OpenCV GrabCut, théorie et masques](https://docs.opencv.org/4.13.0/d8/d83/tutorial_py_grabcut.html).
Tags: cv::pilote cv::d09 famille::algorithme cv_id::CV-GRABCUT-001 provenance::agent pole::A pole::E
END

## CV-GRABCUT-002

Objectif : contrôler une contrainte d’initialisation. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-GRABCUT-002
Question: GrabCut exclut toujours une partie d’objet malgré plus d’itérations. Que vérifier d’abord ?
Reponse: **Noyau attendu** : La zone initiale et les labels de fond sûr : une région utile peut être rendue impossible par la contrainte.

**Approfondissement** : Tester une correction manuelle des labels sur copie puis observer le masque ; distinguer initialisation et apparence insuffisante.

**Chaîne causale** : un pixel imposé comme fond sûr ne fait pas partie des labels que l'optimisation peut librement transformer en objet. Si le rectangle initial exclut une partie de la cible, la procédure peut respecter parfaitement son contrat tout en produisant un masque tronqué.

**Vérification construite** : superposer labels sûrs et probables à l'image, puis corriger uniquement la zone erronée sur une copie. Conserver les autres paramètres et mesurer l'effet. Si cette correction ne suffit pas, comparer les distributions de couleur et la frontière, car plusieurs défauts peuvent coexister. Une répétition supplémentaire de la même optimisation ne remplace pas une information initiale correcte. Cette distinction entre contrainte fausse et modèle d'apparence insuffisant aide à choisir l'intervention utile : changer le masque de départ, ajouter un indice ou envisager un autre mécanisme plutôt que supposer une panne numérique.

**Erreurs bloquantes** : Supposer que la convergence doit annuler toute contrainte erronée.
Source: [[90-segmentation/references/92-grabcut-regions|Fiche complète]] ; [OpenCV GrabCut, théorie et masques](https://docs.opencv.org/4.13.0/d8/d83/tutorial_py_grabcut.html).
Tags: cv::pilote cv::d09 famille::diagnostic cv_id::CV-GRABCUT-002 provenance::agent pole::A pole::E
END

## CV-GRABCUT-003

Objectif : choisir une interaction. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-GRABCUT-003
Question: Pour extraire un objet avec couleurs proches du fond, pourquoi comparer coût d’interaction et hypothèses plutôt que seulement temps d’optimisation ?
Reponse: **Noyau attendu** : Les labels ajoutés par l’utilisateur peuvent fournir l’information manquante ; une solution rapide peut demander beaucoup de corrections.

**Approfondissement** : Évaluer masque, nombre de corrections et robustesse sur images réservées ; un optimum d’énergie ne suffit pas.

**Coût réellement payé** : un algorithme rapide peut demander plusieurs retouches si son modèle de couleur sépare mal cible et fond. Une méthode plus coûteuse par appel peut réduire l'interaction ; l'inverse est aussi possible. Les temps doivent inclure la procédure nécessaire pour atteindre une qualité définie.

**Protocole proposé** : fixer des images réservées, une règle d'initialisation et un budget de correction, puis mesurer qualité de masque, nombre d'interventions, temps total et taux d'échec. Ajouter séparément un fond plus proche de la cible pour tester l'hypothèse d'apparence. Conserver les cas non résolus dans le bilan. Un optimum de l'énergie indique que la procédure a satisfait son modèle ; il ne dit pas que ce modèle possède assez d'information pour distinguer l'objet utile. La comparaison doit donc relier hypothèses de la méthode et effort humain, sans choisir seulement sur la durée du solveur.

**Erreurs bloquantes** : Présenter un temps de calcul faible comme performance complète du processus.
Source: [[90-segmentation/references/92-grabcut-regions|Fiche complète]] ; [OpenCV GrabCut, théorie et masques](https://docs.opencv.org/4.13.0/d8/d83/tutorial_py_grabcut.html).
Tags: cv::pilote cv::d09 famille::comparaison cv_id::CV-GRABCUT-003 provenance::agent pole::A pole::E
END
