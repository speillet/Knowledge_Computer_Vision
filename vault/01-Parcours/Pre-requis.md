# Conventions et rappels utiles

**Provenance** : agent. Ces rappels soutiennent le pilote ; ils ne remplacent
pas les futures fiches canoniques d'estimation et de géométrie.

## Lire une carte

Masquer le verso, produire une réponse, puis comparer au **noyau attendu**.
Une réponse est satisfaisante si elle couvre ce noyau sans **erreur bloquante**.
L'approfondissement explique davantage sans imposer une récitation intégrale.
Rédaction, export et maîtrise personnelle sont suivis séparément.

## Images et coordonnées

Une image en niveaux de gris se note $I[y,x]$, avec hauteur $H$ et largeur $W$.
Les coordonnées géométriques sont $(x,y)$ ; l'indexation d'un tableau est
habituellement `[y, x]`. L'origine est en haut à gauche et $y$ descend dans
les exemples du pilote. Une image couleur n'est pas automatiquement RGB :
les tableaux chargés par OpenCV sont généralement BGR.

Les boîtes sont continues, en pixels, sous la forme
$(x_1,y_1,x_2,y_2)$, avec $x_2>x_1$ et $y_2>y_1$. Leur aire vaut
$(x_2-x_1)(y_2-y_1)$, sans `+1`. Une annotation COCO `xywh` fournit au contraire
$(x,y,w,h)$. Une boîte normalisée doit être remise dans le même repère avant IoU.
Après resize/crop/padding, transformer aussi les points, boîtes et intrinsèques
concernés. Une mesure dans une autre résolution ne garde pas automatiquement
le même seuil en pixels.

## Points homogènes et projection

Un point image $(x,y)$ peut être représenté par
$\tilde x=[x,y,1]^T$. Deux vecteurs homogènes qui ne diffèrent que par un
facteur non nul représentent le même point. Pour $c\ne0$,
$\pi([a,b,c]^T)=[a/c,b/c]^T$. Le symbole $\sim$ signifie cette égalité à
un facteur près ; il ne signifie pas une égalité de coordonnées euclidiennes.

Une projection perspective idéale s'écrit
$s\tilde x=K[R\mid t]\tilde X_w$, avec $X_c=RX_w+t$.
$R$ va du monde à la caméra, $t$ est exprimé dans le repère caméra et dans
l'unité choisie pour la scène. $K$ transforme les coordonnées caméra
normalisées en pixels ; la distorsion est une étape supplémentaire.
Référence : [Zhang, §2](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf).

## Distance, correspondance et estimation

Un détecteur localise des points ; un descripteur représente leur voisinage ;
un matcher propose des paires ; une vérification géométrique teste leur cohérence.
Un plus proche voisin n'est pas nécessairement la même structure physique.
La distance doit correspondre à la représentation : euclidienne pour le SIFT
classique, Hamming pour ORB avec tests binaires à deux points.
Voir [SIFT](../40-features-matching/references/41-sift.md), [ORB](../40-features-matching/references/42-orb.md).

Un estimateur minimise un résidu choisi. Une estimation robuste tolère une
partie d'observations incompatibles ; elle ne répare pas un modèle physique faux.
Voir [RANSAC](../50-calibration-geometrie/references/51-ransac-homographie.md).

## Kalman et affectation

Un filtre de Kalman linéaire représente l'état estimé et sa covariance. Il
prédit avec un modèle de mouvement, puis corrige avec une mesure et son bruit.
Le gain traduit leur incertitude relative ; il ne choisit pas l'identité de
l'objet mesuré. L'affectation est le problème séparé qui associe mesures et
pistes, avec des observations non associées possibles.

Dans le cas scalaire, $K=P^-/(P^-+R)$,
$u^+=u^-+K(z-u^-)$ et $P^+=(1-K)P^-$.
$u^-,z,u^+$ sont ici des positions en pixels ; $P^-,R,P^+$ sont des variances
en pixels carrés ; $K$ est sans unité. Ces relations supposent un modèle
linéaire et les hypothèses de bruit appropriées. Elles illustrent la correction,
pas tout le tracker [SORT](../110-tracking-association/references/111-sort.md).
Référence : [SORT, §3.2](https://arxiv.org/abs/1602.00763).

## Prérequis et liens thématiques

Un prérequis est nécessaire pour comprendre le raisonnement principal.
Un lien thématique donne une connexion utile sans imposer un ordre de lecture.
Le parcours proposé est SIFT → ORB → homographie → calibration, et
IoU/AP → NMS → SORT pour les notions de détection et d'association.
Il n'implique pas qu'il faut maîtriser toute la métrique AP pour comprendre Kalman.
