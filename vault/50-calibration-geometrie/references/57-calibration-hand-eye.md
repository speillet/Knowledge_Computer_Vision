---
id: CV-HANDEYE
type: methode
domaine: d05
poles: ["B", "C", "E"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
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

## Sources et cartes

- [OpenCV 4.13, calibrateHandEye, repères, équations et minimum de mouvements](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
- [Solà et al., micro Lie theory, annexe D-A, composition SE(3)](https://arxiv.org/html/1812.01537v9#A4.SS1).
- [Cartes associées](../57-calibration-hand-eye.md) : CV-HANDEYE-001 à 005.

Rédaction : Agent Codex, 2026-10-24. Sources primaires consultées et API OpenCV 4.13 vérifiées avec Context7. Calculs analytiques et protocoles proposés sont distingués des expériences ; aucun export réel, benchmark vidéo ni validation scientifique indépendante annoncé.
