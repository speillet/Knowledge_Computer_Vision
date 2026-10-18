---
id: CV-MULTICALIB
type: methode
domaine: d05
poles: [B, C, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
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

Une convention possible est $A_iX=XB_i$ pour mouvements relatifs nommés et extrinsèque X. L'équation n'a de sens qu'après définition des repères et sens. Rotations sur un seul axe et translations peu variées peuvent rendre des composantes mal observables. Les translations suivent la même unité de longueur.

## Paramètres et propriétés

Définir outil→base, caméra→mire et ordre de composition. Consigner horloges, temps de pose, levier, incertitudes et mouvement. Ne pas annoncer un minimum universel indépendant du solveur et des trajectoires.

## Coût et implémentation

La collecte et la diversité des mouvements dominent souvent la qualité. Aucun robot ou capteur n'est commandé ici ; les procédures sont des propositions de validation.

## Évaluation et variation contrôlée

Variation proposée : comparer mouvements quasi parallèles à des rotations/positions diversifiées, à qualité de mesure comparable. Évaluer stabilité des extrinsèques et résidus sur mouvements réservés.

## Échecs et diagnostic

Bonne calibration immobile, erreur en mouvement : mesurer timing et deskew. Transformations inversées : suivre un point à travers chaque repère avant d'optimiser davantage.

## Alternatives et usages

Cible commune, méthodes targetless et optimisation conjointe temporelle selon équipement et observabilité. La sécurité de commande robotique reste hors de cette fiche.

## Sources et cartes

- [OpenCV calib3d, calibrateHandEye et robot-world hand-eye](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).
- [Cartes associées](../55-calibration-multicapteurs.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
