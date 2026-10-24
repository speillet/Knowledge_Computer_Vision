# FAST et BRIEF — détecter un coin puis décrire son voisinage — cartes

Fiche : [[40-features-matching/references/47-fast-brief|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::40-features-matching

## CV-FAST-BRIEF-001

Objectif : expliquer le test FAST. Famille : algorithme. Provenance : agent.

START
CV-Pilote
ID: CV-FAST-BRIEF-001
Question: Quel motif d’intensité fait accepter un candidat par le segment test FAST, et que produisent les étapes suivantes ?
Reponse: **Noyau attendu** : Un arc contigu de voisins du cercle doit être entièrement plus clair que le centre plus un seuil, ou plus sombre que le centre moins ce seuil. La variante fixe longueur de l’arc et cercle ; la suppression des maxima sélectionne les réponses voisines.

**Approfondissement** : L’arbre de décision réduit le nombre moyen de comparaisons. La sortie reste une position de keypoint : un descripteur et une vérification géométrique sont des étapes distinctes. Un nombre arbitraire de voisins dispersés ne satisfait pas le test d’arc.

**Exemple logique** : dans une variante donnée, plusieurs voisins très clairs répartis sur tout le cercle ne remplacent pas un arc contigu assez long. Le motif accepté décrit une organisation spatiale du contraste autour du centre, et non un simple histogramme des valeurs voisines.

**Choix d'implémentation** : conserver seuil, variante et unité d'intensité dans le protocole. Un seuil plus faible augmente potentiellement les candidats, y compris les réponses instables sous bruit ; la suppression des maxima contrôle ensuite la redondance locale. Pour diagnostiquer une chute de matches, observer d'abord si les mêmes positions sont détectées. Une extraction rapide de candidats ne donne encore ni orientation stable, ni signature distinctive, ni transformation entre images. Ces responsabilités appartiennent aux composants suivants de la chaîne.

**Erreurs bloquantes** : Compter des voisins dispersés ; attribuer un descripteur binaire à FAST seul.
Source: [[40-features-matching/references/47-fast-brief|Fiche complète]] ; [Rosten et Drummond 2006, §§2–3, segment test et apprentissage](https://www.edwardrosten.com/work/rosten_2006_machine.pdf).
Tags: cv::pilote cv::d04 famille::algorithme cv_id::CV-FAST-BRIEF-001 provenance::agent pole::B pole::C pole::E
END

## CV-FAST-BRIEF-002

Objectif : calculer une distance binaire. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-FAST-BRIEF-002
Question: Deux descripteurs BRIEF jouets sont 101101 et 100001. Quelle distance utiliser et quelle valeur obtient-on ?
Reponse: **Noyau attendu** : La distance de Hamming : XOR = 001100, donc deux bits différents et $d_H=2$. Ne pas soustraire les entiers représentés par ces chaînes.

**Approfondissement** : Chaque bit code un test de différence d’intensité sur un patch lissé. Le motif doit être le même pour comparer les descripteurs. Convertir simplement les octets en flottants ne préserve pas leur géométrie de Hamming.

**Sens de la mesure** : chaque position de la chaîne représente la réponse à un même test local dans les deux patches. Le XOR vaut un exactement lorsque les réponses diffèrent ; compter ces positions mesure donc le désaccord des tests. Le poids binaire utilisé pour stocker un bit dans un octet n'a aucun rôle géométrique dans ce comptage.

**Exemple et limite** : déplacer ou faire tourner un patch sans adapter le motif peut changer les tests tout en conservant le même objet physique. Une petite distance favorise alors une ressemblance dans la représentation choisie ; elle ne garantit pas l'identité du point. Vérifier aussi que les patches ont utilisé le même motif, les mêmes conventions et un lissage compatible. Le matching et sa vérification géométrique sont deux contrôles complémentaires.

**Erreurs bloquantes** : Utiliser une distance L2 entre entiers codant les chaînes.
Source: [[40-features-matching/references/47-fast-brief|Fiche complète]] ; [Calonder et al. 2010, §2, tests BRIEF et lissage](https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf).
Tags: cv::pilote cv::d04 famille::raisonnement cv_id::CV-FAST-BRIEF-002 provenance::agent pole::B pole::C pole::E
END

## CV-FAST-BRIEF-003

Objectif : séparer FAST BRIEF et ORB. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-FAST-BRIEF-003
Question: Pourquoi « FAST + BRIEF » et ORB ne sont-ils pas des synonymes ?
Reponse: **Noyau attendu** : FAST détecte les positions ; BRIEF décrit des patches par tests binaires ; ORB construit une chaîne comportant notamment pyramide, orientation et tests binaires orientés/sélectionnés. Ces ajouts changent les propriétés du pipeline.

**Approfondissement** : Un détecteur peut rester stable alors que son descripteur échoue sous rotation. Évaluer les étapes séparément évite d’attribuer une propriété de l’assemblage à chaque composant. Les variantes d’implémentation doivent être nommées.

**Chaîne à reconstruire** : demander pour chaque étape ce qui entre, ce qui sort et quelle variation elle cherche à traiter. FAST répond à la localisation de candidats ; BRIEF à la description par relations binaires ; l'orientation et les échelles organisent le repère dans lequel ces relations sont comparées.

**Ablation proposée** : sur la même scène transformée, conserver le détecteur et changer la normalisation d'orientation du descripteur, puis conserver la description et modifier la sélection de points. Cela permet d'attribuer une amélioration au composant réellement changé. Le nom d'un assemblage n'autorise pas à transférer toutes ses propriétés à chaque brique. Même un pipeline orienté et multiéchelle reste limité par les détails visibles, le flou et les déformations de perspective.

**Erreurs bloquantes** : Attribuer orientation ou invariance d’échelle universelle à FAST seul.
Source: [[40-features-matching/references/47-fast-brief|Fiche complète]] ; [OpenCV 4.13, ORB, orientation et rBRIEF](https://docs.opencv.org/4.13.0/d1/d89/tutorial_py_orb.html).
Tags: cv::pilote cv::d04 famille::comparaison cv_id::CV-FAST-BRIEF-003 provenance::agent pole::B pole::C pole::E
END

## CV-FAST-BRIEF-004

Objectif : isoler un échec sous rotation. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-FAST-BRIEF-004
Question: Après rotation de l’image, les points FAST restent bien localisés mais les matches BRIEF chutent. Quel mécanisme tester en premier ?
Reponse: **Noyau attendu** : Le motif de tests BRIEF fixe ne suit pas nécessairement l’orientation locale : les paires comparent d’autres structures après rotation. Contrôler l’orientation/normalisation des patches à détecteur constant.

**Approfondissement** : Comparer des patches remis dans le même repère, puis un descripteur orienté comme ORB. Éliminer séparément les points non redétectés, les bords de patch et le flou d’interpolation. Ce protocole sert à isoler une cause, sans garantir un résultat sur toute scène.

**Exemple de changement de repère** : un test qui compare un pixel à gauche du centre et un pixel au-dessus ne compare plus les mêmes structures physiques après rotation si les positions du test restent fixes dans l'image. Le résultat binaire peut changer alors que le keypoint central est toujours correct.

**Vérification construite** : utiliser une transformation connue, comparer les mêmes patches avant et après remise dans un repère commun, puis examiner les distances avec et sans compensation d'orientation. Contrôler l'interpolation et exclure les voisinages sortis de l'image. Si le défaut persiste, tester contraste, lissage et stabilité de la localisation. La compensation d'orientation est une hypothèse utile pour isoler cette cause, pas une garantie d'invariance à toute déformation ni à la disparition de texture.

**Erreurs bloquantes** : Conclure que FAST est forcément en faute alors que ses points sont stables.
Source: [[40-features-matching/references/47-fast-brief|Fiche complète]] ; [Calonder et al. 2010, §2, tests BRIEF et lissage](https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf).
Tags: cv::pilote cv::d04 famille::diagnostic cv_id::CV-FAST-BRIEF-004 provenance::agent pole::B pole::C pole::E
END

## CV-FAST-BRIEF-005

Objectif : mesurer le compromis calcul répétabilité. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-FAST-BRIEF-005
Question: Pour une caméra embarquée, quels résultats comparer avant de remplacer SIFT par FAST/BRIEF ?
Reponse: **Noyau attendu** : Comparer répétabilité, qualité des matches validés, couverture, latence extraction+matching et mémoire, à résolution et budget de points comparables. Inclure rotations, échelles et bruit représentatifs.

**Approfondissement** : Le coût d’un segment test ne suffit pas à prédire le coût complet. Une extraction rapide peut créer davantage de matches ambigus et augmenter la vérification géométrique. Les chiffres historiques d’un article ne donnent pas la latence du matériel cible.

**Comparer des systèmes complets** : un gain sur la détection peut être perdu si davantage de points peu distinctifs multiplient les comparaisons et les échantillons d'estimation robuste. Inversement, une description plus coûteuse peut réduire le nombre de mauvaises hypothèses à traiter. Le coût aval dépend donc aussi de la qualité et de la répartition des features.

**Critère proposé** : fixer une tolérance de recalage et mesurer les cas acceptés à tort, refusés et correctement localisés, avec les mêmes transformations de référence. Chronométrer construction éventuelle d'index, extraction, matching et géométrie sur le CPU cible. Conserver des cas de faible texture et de rotation forte. Ce protocole transforme une promesse de rapidité historique en une décision vérifiable pour la caméra et le produit actuels.

**Erreurs bloquantes** : Choisir sur un FPS publié sans protocole ; ignorer le coût après détection.
Source: [[40-features-matching/references/47-fast-brief|Fiche complète]] ; [Rosten et Drummond 2006, §§2–3, segment test et apprentissage](https://www.edwardrosten.com/work/rosten_2006_machine.pdf).
Tags: cv::pilote cv::d04 famille::evaluation cv_id::CV-FAST-BRIEF-005 provenance::agent pole::B pole::C pole::E
END
