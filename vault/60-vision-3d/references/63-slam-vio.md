---
id: CV-VIO
type: methode
domaine: d06
poles: [B, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
prerequis: ["CV-SE3", "CV-FUSION", "CV-FACTEURS", "CV-EPIPOLAIRE"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d06]
---
# SLAM, VIO, préintégration IMU et bouclage

## Problème, données et hypothèses

Estimer une trajectoire et éventuellement une carte en exploitant vision, IMU et contraintes de lieux. Sorties : poses, état/biais et incertitudes dans un repère défini. Odométrie locale, relocalisation et SLAM avec boucle ne répondent pas exactement au même contrat.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md) ; [CV-FUSION](../../10-mathematiques-estimation/references/13-kalman-ekf-eskf.md) ; [CV-FACTEURS](../../10-mathematiques-estimation/references/14-graphes-facteurs.md) ; [CV-EPIPOLAIRE](../../50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Suivre/associer observations, estimer mouvement, gérer keyframes, optimiser ou filtrer, détecter puis vérifier les boucles. La préintégration condense les mesures IMU entre keyframes avec covariance et correction de biais. MSCKF, VINS-Mono et OKVIS sont des conceptions différentes ; une mention n'implémente pas leurs variantes.

## Mathématiques, conventions et unités

Avec R corps→monde, $\Delta v_{ij}=R_i^T(v_j-v_i-g\Delta t)$ et $\Delta p_{ij}=R_i^T(p_j-p_i-v_i\Delta t-\tfrac12g\Delta t^2)$, en m/s et m. L'accéléromètre mesure une force spécifique dans son repère. Un VIO sans références globales conserve translation et yaw globaux non observables ; l'échelle métrique demande excitation et calibration suffisantes.

## Paramètres et propriétés

Intrinsèques/extrinsèques, timestamps, biais, initialisation, fenêtre et politique de boucle. DBoW2/NetVLAD proposent des candidats de lieu ; une vérification géométrique reste nécessaire.

## Coût et implémentation

Nombre d'états/landmarks, taille de fenêtre, suivi et boucle pèsent sur mémoire/latence. Aucun système VIO exécuté ; aucune dérive chiffrée ni temps réel garanti.

## Évaluation et variation contrôlée

Variation proposée : supprimer la texture puis réduire l'excitation inertielle séparément. Analyser pertes de suivi, échelle et biais ; ne pas assimiler échec d'observation locale et jauge globale. Évaluer avec timestamps et groupe d'alignement annoncés.

## Échecs et diagnostic

Couloir répétitif : vérifier parallaxe, gradients, timing, biais et fausses boucles. Un alignement Sim(3) peut masquer une mauvaise échelle d'un système censé être métrique.

## Alternatives et usages

Vision seule, stéréo/RGB-D, VIO, LiDAR-odométrie ou fusion selon texture, excitation et référence. Le contrôle de trajectoire reste hors périmètre.

## Sources et cartes

- [Forster, préintégration §§IV–VI](https://dellaert.github.io/files/Forster16tro.pdf).
- [Zhang–Scaramuzza, alignement §III et Table I](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf).
- [GTSAM, SLAM et facteurs](https://gtsam.org/tutorials/intro.html).
- [Cartes associées](../63-slam-vio.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
