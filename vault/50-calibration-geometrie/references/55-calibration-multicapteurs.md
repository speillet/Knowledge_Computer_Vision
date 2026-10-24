---
id: CV-MULTICALIB
type: methode
domaine: d05
poles: [B, C, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
prerequis: ["CV-ZHANG", "CV-SE3", "CV-CAPTEURS"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d05]
---
# Calibration multicapteurs, hand-eye et temps

## Problème, données et hypothèses

Estimer les transformations entre capteurs ou robot/caméra avec observations cohérentes dans le temps. Entrées : poses ou mesures avec repères, synchronisation et unités ; sortie : extrinsèques et éventuellement offset temporel selon le modèle. La calibration intrinsèque de chaque caméra est un problème distinct.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-ZHANG](52-calibration-zhang.md) ; [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md) ; [CV-CAPTEURS](../../20-acquisition-images/references/22-capteurs-horodatage.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Associer observations communes et mouvements informatifs ; résoudre une initialisation puis raffiner et valider sur d'autres mouvements. Hand-eye relie des mouvements relatifs ; calibrer une pose fixe ne remplace pas un modèle de synchronisation.

## Mathématiques, conventions et unités

Pour une caméra portée par l'outil et une mire fixe dans la base, noter $G_i={}^bT_{g_i}$ (outil→base), $C_i={} ^{c_i}T_t$ (mire→caméra) et $X={}^gT_c$ (caméra→outil). L'égalité $G_iXC_i=G_jXC_j$ donne $A_{ij}X=XB_{ij}$ avec $A_{ij}=G_j^{-1}G_i$ et $B_{ij}=C_jC_i^{-1}$. Cette convention correspond au cas eye-in-hand ; changer le montage impose de redéfinir la chaîne. Rotations sur un seul axe et translations peu variées peuvent rendre des composantes mal observables. Les translations suivent la même unité de longueur.

## Paramètres et propriétés

Définir outil→base, mire→caméra et ordre de composition pour la convention ci-dessus. Consigner horloges, temps de pose, levier, incertitudes et mouvement. Ne pas annoncer un minimum universel indépendant du solveur et des trajectoires.

## Coût et implémentation

La collecte et la diversité des mouvements dominent souvent la qualité. Aucun robot ou capteur n'est commandé ici ; les procédures sont des propositions de validation.

## Évaluation et variation contrôlée

Variation proposée : comparer mouvements quasi parallèles à des rotations/positions diversifiées, à qualité de mesure comparable. Évaluer stabilité des extrinsèques et résidus sur mouvements réservés.

## Échecs et diagnostic

Bonne calibration immobile, erreur en mouvement : mesurer timing et deskew. Transformations inversées : suivre un point à travers chaque repère avant d'optimiser davantage.

## Alternatives et usages

Cible commune, méthodes targetless et optimisation conjointe temporelle selon équipement et observabilité. La sécurité de commande robotique reste hors de cette fiche.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent séparer transformations spatiales et désynchronisation. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-MULTICALIB-001

**Question de travail** : Pourquoi écrire $AX=XB$ ne suffit-il pas à appliquer une calibration hand-eye ?

**Réponse de référence** : Il faut définir les repères, les mouvements relatifs A/B, leur sens et la transformation inconnue X.

**Dérivation par chaîne** : en eye-in-hand avec une mire fixe, la composition outil→base, caméra→outil puis mire→caméra doit donner la même pose mire→base pour chaque acquisition. L'égalité de ces compositions conduit à des mouvements relatifs de part et d'autre de l'extrinsèque inconnue. Le sens des produits n'est pas libre : il découle des repères adjacents.

**Test construit** : prendre une pose connue, transformer un point de mire jusqu'à la base, puis vérifier l'inverse de la chaîne. Répéter avec une rotation non triviale et des translations non nulles dans des unités communes. Un test identité peut laisser des inversions invisibles. Cette validation d'interface précède le réglage du solveur ; si elle échoue, ajouter des données ou changer la méthode d'optimisation traite un autre problème que l'erreur de convention.

### Cas lié à CV-MULTICALIB-003

**Question de travail** : Pourquoi une faible reprojection intrinsèque ne valide-t-elle pas une fusion caméra–LiDAR en mouvement ?

**Réponse de référence** : Elle ne teste pas à elle seule l’extrinsèque entre capteurs, leur offset temporel ou la déformation du scan.

**Séparer les contrats** : l'intrinsèque relie rayons et pixels d'une caméra. L'extrinsèque relie les axes des capteurs. Le temps détermine quelles positions de la scène et du porteur sont comparées. Une fusion peut respecter le premier contrat et violer les deux autres, particulièrement pendant une rotation.

**Enquête construite** : commencer par des observations immobiles pour contrôler une partie de la géométrie, puis comparer translation et rotation en inspectant temps par point du LiDAR et instant de capture caméra. Corriger séparément les offsets, le deskew et les transformations pour mesurer leur effet. Une translation ajustée pour une seule vitesse peut masquer un retard sans généraliser. Réserver une séquence avec d'autres mouvements pour la validation finale. Une bonne reprojection caméra reste utile, mais elle ne teste ni la simultanéité des mesures ni toute la projection d'un nuage vers l'image.

**Repère documentaire de cette passe** : [OpenCV 4.13, Camera Calibration and 3D Reconstruction](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), modèles de projection et composition des extrinsèques. Les autres développements figurent dans les [cartes associées](../55-calibration-multicapteurs.md).

## Sources et cartes

- [Zhang–Singh 2014, LOAM, §§II, IV et V-B](https://www.roboticsproceedings.org/rss10/p07.pdf)

- [OpenCV calib3d, calibrateHandEye et robot-world hand-eye](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
- [Cartes associées](../55-calibration-multicapteurs.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
