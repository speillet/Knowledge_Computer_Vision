---
id: CV-HANDEYE
type: methode
domaine: d05
poles: ["B", "C", "E"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 2
prerequis: ["CV-SE3", "CV-ZHANG"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d05]
---
# Hand-eye calibration — résoudre AX = XB sans mélanger les repères

## Prérequis et compétences

**Prérequis obligatoires** : [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md), [CV-ZHANG](52-calibration-zhang.md).
**Compétences visées** : dériver les mouvements relatifs; respecter le sens des poses API; exciter les directions observables; tester la fermeture de la chaîne; distinguer eye-in-hand et eye-to-hand.
Les notions connexes restent des alternatives, pas des dépendances implicites.

## Problème et contrat des données

Estimer l’extrinsèque rigide entre caméra et gripper d’un robot en configuration eye-in-hand. Le robot bouge, la caméra est solidaire du gripper et la mire reste fixe dans la base. Convention : $T_{ab}$ envoie les coordonnées du repère $b$ vers $a$. Les poses robot et caméra doivent correspondre au même instant, avec des unités de translation communes. Ni une calibration intrinsèque ni une transformation caméra–mire isolée ne donnent cette extrinsèque.

## Chaîne de transformations et équation

Noter $G_i=T_{bg_i}$, $C_i=T_{c_it}$, $X=T_{gc}$ et $Y=T_{bt}$. La chaîne fixe impose $G_iXC_i=Y$ pour chaque pose $i$. Pour deux poses $i,j$, poser $A_{ij}=G_j^{-1}G_i$ et $B_{ij}=C_jC_i^{-1}$ : $A_{ij}X=XB_{ij}$. Toutes sont des matrices homogènes $4\times4$ ; rotations sans unité, translations en m ou en mm mais jamais mélangées. Le développement donne $R_AR_X=R_XR_B$ et $(R_A-I)t_X=R_Xt_B-t_A$. L’ordre de chaque produit découle du sens des repères.

## Mécanisme, paramètres et observabilité

Des solveurs estiment séparément rotation et translation ; d’autres les traitent ensemble, par exemple avec des quaternions duaux. Comparer les solutions avec un résidu sur poses réservées, pas par leur seul nom. Des mouvements autour d’un seul axe ou sans diversité de rotation laissent des directions mal contraintes. Dans OpenCV 4.13, `calibrateHandEye` reçoit gripper→base et target→camera et retourne camera→gripper ; sa documentation demande au moins deux mouvements aux axes de rotation non parallèles, donc trois poses, et recommande davantage de vues. Ce minimum ne remplace pas un diagnostic de conditionnement.

## Coût, synchronisation et variantes

Le coût du solveur est souvent inférieur à celui d’une acquisition propre. Former toutes les paires augmente le nombre d’équations mais les paires partageant une pose ne sont pas des observations indépendantes. Vérifier timestamps, poses robot, intrinsics et effet rolling shutter avant d’augmenter le nombre de paires. En eye-to-hand, la caméra est fixe et la chaîne d’inconnues change : on ne corrige pas le contrat d’entrée en inversant seulement la sortie. Aucun robot ni solveur hand-eye exécuté ici ; la dérivation est algébrique.

## Évaluation et variation contrôlée

Pour un $X$ candidat, calculer $Y_i=G_iXC_i$ sur des poses réservées. Mesurer dispersion des rotations et des translations séparément, dans des unités annoncées, puis une erreur de reprojection ou de position utile. Variation proposée : garder le nombre de poses mais remplacer des mouvements à axe unique par des rotations autour d’axes variés ; prédire un meilleur conditionnement. Introduire séparément un décalage temporel permet de tester la sensibilité à la synchronisation. Aucun résultat physique n’est revendiqué.

## Diagnostic et alternatives

Si $Y_i$ varie avec la pose robot, vérifier sens de $G_i$, sens de $C_i$, multiplication, unités et synchronisation. Un résultat visuellement plausible n’exclut pas une inversion. Si la mire bouge, le modèle $Y$ constant est violé. Pour calibrer simultanément une base robot et un monde de vision inconnus, le problème robot-world/hand-eye comporte d’autres inconnues ; ne pas lui appliquer aveuglément ce contrat $AX=XB$.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent conventions AX=XB, excitation et validation indépendante. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-HANDEYE-001

**Question de travail** : En eye-in-hand, $G_i$ envoie gripper→base et $C_i$ mire→caméra. Avec $X$ caméra→gripper et une mire fixe, comment obtenir $AX=XB$ ?

**Réponse de référence** : La chaîne fixe est $G_iXC_i=G_jXC_j$. En multipliant à gauche par $G_j^{-1}$ et à droite par $C_i^{-1}$, on obtient $A=G_j^{-1}G_i$ et $B=C_jC_i^{-1}$, puis $AX=XB$.

**Lecture des repères** : en suivant un point de la mire vers la caméra, puis l'outil et la base, les indices intermédiaires se raccordent. La mire fixe impose que la transformation finale soit constante. Les deux acquisitions fournissent alors deux chemins vers le même résultat, d'où l'équation sur les mouvements relatifs.

**Contrôle construit** : vérifier d'abord cette fermeture avec des transformations synthétiques cohérentes. Introduire ensuite une seule inversion de pose pour observer l'effet sur le résidu de chaîne. Cela contrôle l'algèbre sans commander un robot ni prétendre valider des captures réelles. Une équation formellement reconnue ne dispense pas de définir montage, inconnues et synchronisation dans le dispositif utilisé.

### Cas lié à CV-HANDEYE-005

**Question de travail** : Passer d’une caméra montée sur le gripper à une caméra fixe se résume-t-il à inverser la sortie du solveur ?

**Réponse de référence** : Non : les repères fixes et les inconnues de la chaîne changent. Redéfinir les transformations mesurées et inconnues, écrire la chaîne constante, puis dériver l’équation et le contrat d’entrée adaptés.

**Construction du nouveau problème** : identifier ce qui est fixé à la base, ce qui suit l'outil et où se trouve la mire. Écrire ensuite deux chemins reliant les mêmes repères, avec une transformation inconnue constante seulement là où le montage le justifie. C'est cette égalité qui détermine les inverses et mouvements relatifs nécessaires.

**Exemple de piège** : une caméra devenue fixe ne possède plus une pose caméra→gripper constante lorsque l'outil se déplace. Inverser cette ancienne inconnue ne la transforme donc pas magiquement en la nouvelle constante caméra→base. Vérifier les contrats du solveur adaptés au montage et une fermeture sur plusieurs poses. Le raisonnement reste une dérivation géométrique ; aucune commande de robot ni validation d'installation n'est effectuée ici.

**Repère documentaire de cette passe** : [OpenCV 4.13, calibrateHandEye](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), calibrateHandEye, transformations et mouvements minimums. Les autres développements figurent dans les [cartes associées](../57-calibration-hand-eye.md).

## Sources et cartes

- [OpenCV 4.13, calibrateHandEye, repères, équations et minimum de mouvements](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
- [Solà et al., micro Lie theory, annexe D-A, composition SE(3)](https://arxiv.org/html/1812.01537v9#A4.SS1).
- [Cartes associées](../57-calibration-hand-eye.md) : CV-HANDEYE-001 à 005.

Rédaction : Agent Codex, 2026-10-24. Sources primaires consultées et API OpenCV 4.13 vérifiées avec Context7. Calculs analytiques et protocoles proposés sont distingués des expériences ; aucun export réel, benchmark vidéo ni validation scientifique indépendante annoncé.
