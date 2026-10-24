---
id: CV-VIO
type: methode
domaine: d06
poles: [B, C]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
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

Avec $R_i$ corps→monde, $p_i,v_i$ position et vitesse dans le monde, $g$ gravité dans ce même repère et $\Delta t=t_j-t_i$ en secondes, $\Delta v_{ij}=R_i^T(v_j-v_i-g\Delta t)$ et $\Delta p_{ij}=R_i^T(p_j-p_i-v_i\Delta t-\tfrac12g\Delta t^2)$, en m/s et m. L'accéléromètre mesure une force spécifique dans son repère. Un VIO sans références globales conserve translation et yaw globaux non observables ; l'échelle métrique demande excitation et calibration suffisantes.

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

## Raisonnement guidé et contrôles proposés

Ces cas construits développent fusion inertielle, jauges et évaluation sans masquer les erreurs. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-VIO-001

**Question de travail** : La préintégration IMU constitue-t-elle à elle seule un système VIO ?

**Réponse de référence** : Non : elle résume des mesures entre keyframes en contraintes avec bruit et biais ; le système doit aussi associer la vision, initialiser et estimer les états.

**Contrat de la préintégration** : entre deux keyframes, les nombreuses observations inertielles sont condensées dans des contraintes de mouvement avec leur incertitude et leur dépendance aux biais. Ces contraintes doivent être combinées aux observations visuelles, à un état initial et à la gravité dans des repères cohérents.

**Exemple de limite** : intégrer une accélération mesurée dans le repère IMU comme si elle était directement une accélération monde confond orientation, force spécifique et gravité. Une très bonne vision ne répare pas automatiquement cette incohérence de modèle. Un système complet doit aussi gérer horodatages, extrinsèques, biais, keyframes et pertes d'observation. La préintégration évite de reprendre naïvement toute la séquence brute à chaque calcul ; elle ne fournit pas une pose absolue ni une référence globale absente des capteurs. Valider le système demande donc trajectoire, incertitude, disponibilité et latence sur des mouvements représentatifs.

### Cas lié à CV-VIO-005

**Question de travail** : Cas B — diagnostic : un VIO dérive en échelle et lacet dans un couloir peu texturé. Quels contrôles départagent les causes ?

**Réponse de référence** : Inspecter texture/parallaxe, excitation, biais et synchronisation ; vérifier fausses boucles et groupe d’alignement utilisé.

**Enquête par signatures** : une faible texture dégrade les contraintes visuelles ; une excitation insuffisante limite certaines estimations inertielles ; un retard ou un biais peut produire une erreur dépendant du mouvement. Comparer la chronologie des résidus et des pertes de suivi, plutôt que seulement la trajectoire finale.

**Ablations proposées** : contrôler les timestamps sur des mouvements instrumentés, inspecter les features et la parallaxe, puis examiner les contraintes de boucle une par une. Réserver des séquences où un seul facteur change pour distinguer les hypothèses. Un alignement avec échelle libre peut rendre la superposition visuelle convaincante tout en cachant l'erreur métrique. Rapporter donc l'erreur avant et après l'alignement permis, avec sa justification. Aucun contrôle isolé ne prouve une cause unique lorsque plusieurs défauts de capteurs et d'estimation coexistent.

**Repère documentaire de cette passe** : [Forster et al. 2016](https://dellaert.github.io/files/Forster16tro.pdf), §§IV–VI, préintégration et estimation. Les autres développements figurent dans les [cartes associées](../63-slam-vio.md).

## Sources et cartes

- [Forster, préintégration §§IV–VI](https://dellaert.github.io/files/Forster16tro.pdf).
- [Zhang–Scaramuzza, alignement §III et Table I](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf).
- [GTSAM, SLAM et facteurs](https://gtsam.org/tutorials/intro.html).
- [Cartes associées](../63-slam-vio.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
