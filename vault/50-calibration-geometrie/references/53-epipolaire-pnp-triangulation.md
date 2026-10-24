---
id: CV-EPIPOLAIRE
type: methode
domaine: d05
poles: [B, C]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 3
prerequis: ["CV-SE3", "CV-ZHANG"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d05]
---
# Épipolaire, PnP et triangulation

## Problème, données et hypothèses

Distinguer contraintes entre deux vues, pose depuis points 3D connus et reconstruction de points. Les coordonnées doivent être corrigées de distorsion ou traitées par un modèle cohérent ; préciser repère et échelle des points.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md) ; [CV-ZHANG](52-calibration-zhang.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

La fondamentale relie points pixels ; l'essentielle exploite les intrinsèques. PnP estime la pose objet→caméra à partir de 3D–2D. La triangulation cherche un point 3D expliquant plusieurs rayons ; faible parallaxe et bruit peuvent rendre sa profondeur très incertaine.

## Mathématiques, conventions et unités

Pour $X_2=RX_1+t$, $E=[t]_\times R$ et $x_2^TEx_1=0$ en coordonnées normalisées. En pixels idéaux $F=K_2^{-T}EK_1^{-1}$. La direction t issue de deux vues monoculaires n'a pas d'échelle métrique. PnP renvoie t dans l'unité des points 3D ; la caméra a centre $-R^Tt$.

## Paramètres et propriétés

Minimum, ambiguïtés et raffinement dépendent de la variante. P3P peut donner plusieurs solutions ; dans OpenCV 4.13.0, `solvePnP(..., SOLVEPNP_P3P)` exige quatre points, tandis que `solveP3P` accepte trois correspondances et retourne les solutions candidates. Vérifier chiralité, parallaxe et résidus, pas le seul nombre de points.

## Coût et implémentation

RANSAC, solveur et optimisation aval ont des coûts différents. Aucun appel OpenCV exécuté ; les conventions `solvePnP` ont été vérifiées dans la documentation 4.13.

## Évaluation et variation contrôlée

Cas analytique : deux rayons presque parallèles donnent une profondeur sensible à une petite erreur angulaire. Variation proposée : modifier baseline ou distance en conservant bruit image ; rapporter incertitude et erreur 3D sur référence.

## Échecs et diagnostic

Profondeur immense avec petit résidu : examiner parallaxe, échelle, chiralité et mauvaise association. Pose inversée : contrôler monde→caméra et axes.

## Alternatives et usages

Homographie pour un plan ; PnP si carte 3D connue ; deux vues puis reconstruction si carte inconnue. Ne pas interpréter toute translation comme métrique.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent épipolarité, pose et profondeur distinguées par leur contrat. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-EPIPOLAIRE-001

**Question de travail** : Quelles coordonnées distinguent matrice essentielle et fondamentale ?

**Réponse de référence** : E agit sur coordonnées caméra normalisées idéales ; F sur pixels idéaux avec intrinsèques absorbés.

**Écriture cohérente** : pour $X_2=RX_1+t$, l'essentielle vaut $E=[t]_\times R$. La contrainte $x_2^TEx_1=0$ s'écrit avec des coordonnées normalisées idéales ; en pixels idéaux, $F=K_2^{-T}EK_1^{-1}$ absorbe les deux matrices intrinsèques. Le symbole homogène implique aussi une convention de normalisation.

**Exemple de contrôle** : si les points ont été undistordus vers des coordonnées normalisées, les réinjecter dans une fondamentale associée à d'autres matrices pixel mélange deux contrats. Vérifier un point connu et son lieu épipolaire avant d'interpréter le score. Un produit scalaire algébrique proche de zéro n'est pas directement une erreur euclidienne en pixels : le choix du résidu et de son seuil doit être explicité. La matrice choisie décrit la relation entre vues ; elle ne corrige pas implicitement toutes les distorsions ni les transformations de prétraitement appliquées ensuite.

### Cas lié à CV-EPIPOLAIRE-005

**Question de travail** : Pourquoi le slogan « P3P = appeler solvePnP avec trois points quelconques » est-il trompeur ?

**Réponse de référence** : Le problème peut avoir plusieurs solutions, les configurations peuvent être dégénérées et l’API sélectionnée peut demander un quatrième point.

**Différence entre problème et fonction** : une formulation minimale indique combien de correspondances peuvent suffire sous des hypothèses géométriques. Une fonction peut ajouter une observation pour sélectionner une solution, retourner plusieurs hypothèses ou imposer d'autres contraintes de données. Son nom ne remplace donc pas la lecture du contrat de la variante utilisée.

**Protocole proposé** : consigner méthode et version, vérifier nombre et configuration des points, puis examiner les poses candidates avec des observations supplémentaires. Contrôler résidus, visibilité et plausibilité du mouvement dans les repères annoncés. Des points dégénérés ou presque dégénérés peuvent rester peu informatifs même si le nombre demandé est satisfait. Dans une application critique pour la précision, utiliser aussi des points réservés et un raffinement approprié. Ce raisonnement évite de confondre minimum algébrique, appel d'API réussi et pose effectivement validée dans la scène réelle.

**Repère documentaire de cette passe** : [OpenCV 4.13, Camera Calibration and 3D Reconstruction](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), modèle pinhole, matrices essentielles, solvePnP et triangulation. Les autres développements figurent dans les [cartes associées](../53-epipolaire-pnp-triangulation.md).

## Sources et cartes

- [OpenCV calib3d, E/F/recoverPose/triangulatePoints](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
- [OpenCV solvePnP, conventions et variantes](https://docs.opencv.org/4.13.0/d5/d1f/calib3d_solvePnP.html).
- [Cartes associées](../53-epipolaire-pnp-triangulation.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
