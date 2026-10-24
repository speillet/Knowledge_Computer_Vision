---
id: CV-FISHEYE
type: methode
domaine: d05
poles: ["B", "C", "E"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 2
prerequis: ["CV-ZHANG", "CV-SE3"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d05]
---
# Calibration fisheye — projection angulaire et validation hors centre

## Prérequis et compétences

**Prérequis obligatoires** : [CV-ZHANG](52-calibration-zhang.md), [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md).
**Compétences visées** : distinguer projection fisheye et pinhole; concevoir des vues de calibration grand angle; localiser un défaut de modèle de caméra; propager le contrat après rectification; interpréter le paramètre de champ rectifié.
Les notions connexes restent des alternatives, pas des dépendances implicites.

## Problème et contrat des données

Calibrer une caméra grand angle lorsque le modèle de projection retenu doit représenter une forte déformation périphérique. Entrées : correspondances 3D/2D de mire, dimensions physiques, résolution et modèle optique ; sorties : intrinsics, coefficients de distorsion et poses. Conserver la distinction entre image brute fisheye et image rectifiée. Un grand angle n’impose pas automatiquement un modèle particulier : comparer les modèles sur observations réservées.

## Mécanisme et mathématiques

Dans le modèle OpenCV fisheye 4.13, pour un point caméra $(X,Y,Z)$ avec $Z>0$, poser $a=X/Z$, $b=Y/Z$, $r=\sqrt{a^2+b^2}$ et $\theta=\arctan r$. L’angle distordu est $\theta_d=\theta(1+k_1\theta^2+k_2\theta^4+k_3\theta^6+k_4\theta^8)$. Les coordonnées normalisées sont $x_d=(\theta_d/r)a$, $y_d=(\theta_d/r)b$, avec limite continue au centre. Les angles sont en radians, les coordonnées normalisées et coefficients sans unité ; $u=f_x(x_d+\alpha y_d)+c_x$, $v=f_yy_d+c_y$, avec focales et centre en pixels et skew $\alpha$ sans unité. Même si les $k_i$ sont nuls, la projection reste angulaire : $r_d=\theta$, pas $r_d=\tan\theta$.

## Acquisition, paramètres et limites

Calibrer en variant inclinaison, distance et couverture du champ, notamment les bords. Des vues proches du centre contraignent mal la distorsion périphérique. Fixer ou estimer certains paramètres n’est pas anodin : un coefficient libre peut absorber un défaut de mire, un flou ou une pose peu contrainte. Les quatre coefficients fisheye ne sont pas les quatre premiers coefficients Brown–Conrady du modèle pinhole. Conserver unités de mire, sens des poses, résolution et stabilité mécanique.

## Coût et rectification

L’optimisation dépend des vues, points et paramètres. Pour la vidéo, on peut calculer une map de rectification puis l’appliquer aux frames ; elle doit être recalculée si la géométrie ou la résolution change. Le paramètre `balance` de la nouvelle matrice OpenCV échange champ conservé et bordures, sans améliorer les paramètres physiques déjà estimés. Utiliser la matrice de projection de l’image rectifiée pour les calculs qui suivent, et tenir compte des pixels invalides et de l’interpolation. API vérifiée avec Context7 ; pas de calibration de caméra réelle exécutée.

## Évaluation et variation contrôlée

Baseline proposée : modèle pinhole avec distorsion et même jeu d’apprentissage. Variation : modèle fisheye, à contraintes comparables. Évaluer résidus par rayon et pose sur des vues tenues à l’écart ; vérifier une mesure géométrique utile, pas seulement un RMS global. Exemple analytique, sans distorsion supplémentaire : à $\theta=60°$, une focale de 300 px donne un rayon angulaire de 314,16 px contre 519,62 px en pinhole. Ce calcul explique pourquoi annuler les coefficients ne convertit pas l’un en l’autre.

## Diagnostic et alternatives

Un RMS moyen faible avec de grands résidus aux bords appelle une carte spatiale des erreurs, une inspection des corners et de nouvelles vues périphériques. Une image « redressée » visuellement ne prouve pas la justesse métrique. Pour un dispositif omnidirectionnel ou non central, comparer un autre modèle de caméra plutôt que multiplier arbitrairement les coefficients. Le contrat de projection et la région observée limitent les conclusions.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent couverture angulaire et compatibilité du modèle de projection. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-FISHEYE-001

**Question de travail** : Dans OpenCV fisheye, mettre les quatre coefficients de distorsion à zéro redonne-t-il la projection pinhole ? Expliquer avec un rayon hors axe.

**Réponse de référence** : Non : le rayon normalisé vaut alors $r_d=\theta$, tandis que le pinhole donne $r=\tan\theta$, avec $\theta$ l’angle au centre optique en radians. Les projections ne coïncident qu’approximativement près de l’axe.

**Pourquoi le centre trompe** : près de zéro, $\tan\theta$ est proche de $\theta$. Les deux modèles peuvent donc sembler semblables sur une petite région centrale. L'écart grandit hors axe ; des coefficients nuls ne signifient pas « aucune différence avec le pinhole », mais aucune correction supplémentaire au modèle angulaire choisi.

**Contrôle proposé** : projeter quelques rayons connus, dont un suffisamment oblique, avec les deux modèles dans les mêmes conventions et unités. Comparer ensuite aux observations réservées de la caméra réelle. Une image visuellement plausible ne départage pas les modèles sur leur précision périphérique. Les coefficients et la matrice de chaque modèle doivent rester associés à l'image et à la fonction de projection qui les interprètent.

### Cas lié à CV-FISHEYE-005

**Question de travail** : Une modification du paramètre balance d’OpenCV montre davantage de scène mais ajoute des bordures. La caméra est-elle mieux calibrée ?

**Réponse de référence** : Non : `balance` modifie le choix de la projection de sortie et le compromis de champ, pas les paramètres physiques déjà estimés. Comparer champ utile, résolution locale et pixels valides avec la même calibration.

**Interprétation du compromis** : une projection de sortie peut privilégier un cadrage qui remplit le rectangle ou un champ plus large avec des zones invalides. Ces choix changent la quantité d'information disponible et sa résolution locale, sans modifier les observations ayant servi à estimer la caméra.

**Évaluation proposée** : comparer les sorties sur la même calibration en reportant masque valide, champ utile et erreur de la tâche. Pour une mesure près d'une bordure, l'interpolation et la faible densité d'observations peuvent compter davantage que le nombre total de pixels affichés. La géométrie de sortie doit être propagée aux algorithmes suivants. Un changement de présentation peut donc aider un produit sans constituer une amélioration de calibration physique.

**Repère documentaire de cette passe** : [OpenCV 4.13, Fisheye camera model](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html), équations en theta, coefficients et fonctions de calibration. Les autres développements figurent dans les [cartes associées](../56-calibration-fisheye.md).

## Sources et cartes

- [OpenCV 4.13, fisheye, Detailed Description et estimateNewCameraMatrixForUndistortRectify](https://docs.opencv.org/4.13.0/db/d58/group__calib3d__fisheye.html).
- [OpenCV 4.13, calibration, modèle pinhole et distorsion](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
- [Cartes associées](../56-calibration-fisheye.md) : CV-FISHEYE-001 à 005.

Rédaction : Agent Codex, 2026-10-24. Sources primaires consultées et API OpenCV 4.13 vérifiées avec Context7. Calculs analytiques et protocoles proposés sont distingués des expériences ; aucun export réel, benchmark vidéo ni validation scientifique indépendante annoncé.
