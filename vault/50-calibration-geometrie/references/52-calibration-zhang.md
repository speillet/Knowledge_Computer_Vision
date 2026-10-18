---
id: CV-ZHANG
type: methode
domaine: d05
poles: [B, C, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
prerequis: ["CV-HOMOGRAPHIE"]
revision: 2
tags: [cv/d05, calibration, zhang]
---
# Calibration caméra sur mire — méthode de Zhang

## Problème et contrat

La calibration estime les paramètres de formation de l'image à partir de
points de mire connus et observés. Elle se distingue de la pose d'une caméra
déjà calibrée et d'un recalage entre images. Elle ne calibre pas les scores
probabilistes d'un détecteur. [Zhang, §§2–3][zhang]

Entrées : coordonnées 3D des coins d'une mire plane, coordonnées 2D associées
dans plusieurs vues, résolution et modèle optique choisis. La taille du carré
fixe l'unité des translations : millimètres si les points sont en millimètres.
Sorties : intrinsèques $K$, distorsion et une pose de mire par image.
Garder identifiants des coins, dimensions du damier et ordre des correspondances.

**Prérequis obligatoires** : [projection et repères](../../01-Parcours/Pre-requis.md),
[homographie](51-ransac-homographie.md) pour l'initialisation.
**Compétences** : expliquer l'identifiabilité, concevoir la capture et valider.

## Intuition et équations

Le même plan connu est observé sous différentes orientations. Chaque vue donne
une homographie ; l'orthogonalité des axes de la mire contraint les mêmes
intrinsèques à travers les vues. Une optimisation affine ensuite les paramètres.

$$
X_c=RX_w+t,\qquad
s\tilde x=K[R\mid t]\tilde X_w,\qquad
K=\begin{bmatrix}f_x&\gamma&c_x\\0&f_y&c_y\\0&0&1\end{bmatrix}.
$$

$X_w,X_c\in\mathbb R^3$ sont le point dans les repères mire et caméra ;
$R\in SO(3)$ transforme monde vers caméra ; $t\in\mathbb R^3$ est en
unités de mire ; $\tilde X_w$ est homogène. $f_x,f_y$ et le point principal
$(c_x,c_y)$ sont en pixels ; $\gamma$ est le skew en unités pixel.
$s$ est le facteur homogène. La projection écrite est idéale, avant distorsion.

Sur $Z_w=0$, $H\sim K[r_1\ r_2\ t]$, où $r_1,r_2$ sont les deux premières
colonnes de $R$. En notant $B=K^{-T}K^{-1}$ et $h_i$ les colonnes de $H$ :

$$
h_1^TBh_2=0,\qquad h_1^TBh_1=h_2^TBh_2.
$$

Ces deux contraintes par vue viennent de l'orthogonalité et de l'égalité de
norme des axes de rotation. Avec cinq intrinsèques libres, trois vues
indépendantes sont nécessaires en général à l'initialisation linéaire ;
deux peuvent suffire en imposant un skew nul. Ce minimum algébrique ne donne
pas une garantie de précision. Des translations seules n'apportent pas de
nouvelles contraintes d'orientation. [Zhang, §§3.1 et 4][zhang]

## Déroulement, distorsion et acquisition

1. Définir le modèle, la taille réelle des carrés et l'ordre des coins.
2. Capturer des vues nettes, orientées et réparties dans l'image.
3. Détecter et affiner les coins, inspecter les associations.
4. Initialiser homographies, intrinsèques et poses ; estimer la distorsion.
5. Raffiner les paramètres avec une erreur de reprojection non linéaire.
6. Valider sur d'autres observations et avec une mesure liée à l'usage.

Le modèle radial du papier et les modèles OpenCV à coefficients supplémentaires
ne sont pas interchangeables sans le préciser. Par exemple, en coordonnées
normalisées sans unité $(x_n,y_n)$, $r^2=x_n^2+y_n^2$ et
$x_d=x_n(1+k_1r^2+k_2r^4)$ décrivent la composante radiale simple ;
la relation analogue s'applique à $y_n$. Les paramètres tangentiels, fisheye
ou modèles rationnels nécessitent leur propre définition. [Zhang, §3.3][zhang]

Hypothèses : mire suffisamment plane et rigide, paramètres optiques stables,
projection adaptée au capteur, observations exploitables. Focus/zoom variables,
rolling shutter avec mouvement et mire déformée peuvent violer ces hypothèses.
Leur présence exige un diagnostic, pas seulement plus de coefficients.

## Résidu, paramètres et coût

Pour $M$ observations valides, une convention de RMS géométrique est

$$
E=\sqrt{\frac1M\sum_{j,i}\|x_{ij}-\hat x(K,d,R_j,t_j,X_i)\|_2^2}.
$$

$x_{ij}$ est le coin observé, $\hat x$ sa projection prédite en pixels,
$d$ les coefficients de distorsion et $j$ la vue. $M$ compte les points,
pas deux fois les coordonnées ; d'autres conventions peuvent utiliser $2M$.
Le RMS est ici en pixels. Il mesure l'ajustement aux observations, pas
directement la précision métrique ni l'absence de biais. [OpenCV calibration][opencv]

Paramètres à consigner : modèle de distorsion, contraintes sur intrinsèques,
résolution, estimation des coins, critère de convergence et vues exclues.
Trop de paramètres peuvent surajuster une capture peu informative.
Le coût augmente avec le nombre de vues/coins et les itérations ; il s'agit
souvent d'une étape hors ligne, distincte du coût d'undistortion en production.

Pseudocode **non exécuté** : détecter → vérifier → calibrer → analyser les
résidus par vue et position → valider sur captures réservées. Aucun résultat
de calibration réel n'est annoncé dans ce lot.

## Validation et variation contrôlée

**Protocole proposé par le projet**, pas une prescription du papier : garder
$K,d$ fixes sur des captures réservées ; estimer la pose avec une partie des
coins et mesurer les autres. Ajouter une mesure indépendante adaptée au produit,
par exemple une dimension connue à différentes positions et distances.
Les seuils d'acceptation viennent du besoin métier, pas d'une valeur RMS universelle.

**Variation non exécutée** : comparer un jeu presque frontal à un jeu avec
orientations diverses, à nombres de vues et qualité de coins comparables.
Prédiction : la diversité améliore l'observabilité ; le RMS d'entraînement
peut rester faible dans les deux cas. Examiner stabilité et validation externe.

| Symptôme | Causes possibles | Vérification discriminante |
| --- | --- | --- |
| Faible RMS, résultats métriques faux | Taille des carrés, biais de mire, modèle mal identifié | Mesure indépendante et vérification des unités |
| Forts résidus en périphérie | Couverture insuffisante, distorsion inadaptée | Carte vectorielle des résidus, nouvelles vues périphériques |
| Intrinsèques instables selon le sous-ensemble | Poses redondantes, flou, paramètres libres excessifs | Sous-échantillons, diversité angulaire et modèle contraint justifié |

Après resize par facteurs $a_x,a_y$, appliquer la transformation pixel aux
intrinsèques ; crop/padding déplacent aussi le point principal. Si le modèle
physique reste valable, ce changement de repère n'exige pas forcément une
nouvelle calibration. Un changement de focus ou de zoom est une autre situation.

## Alternatives, sources et cartes

Pour grand angle, évaluer un modèle fisheye ; pour plusieurs capteurs, distinguer
intrinsèques individuels et extrinsèques entre capteurs ; pour une pose seule,
partir d'une calibration déjà connue avec PnP.

- [Zhang, rapport complet associé à TPAMI 2000][zhang] : §§2–4.
- [OpenCV 4.13 `calibrateCamera`][opencv] : flags, modèles et données attendues.
- [Cartes calibration](../52-calibration-zhang.md).

[zhang]: https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf
[opencv]: https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html
