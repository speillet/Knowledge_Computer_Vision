---
id: CV-CAPTEURS
type: methode
domaine: d02
poles: [B, C, E, F]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
prerequis: ["CV-SE3"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d02]
---
# Capteurs, rolling shutter et synchronisation

## Problème, données et hypothèses

Relier images, mesures IMU, LiDAR, radar ou ToF à un même temps et à des repères explicites. Une frame, un scan LiDAR et une mesure inertielle ne sont pas des observations instantanées de même durée.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-SE3](../../10-mathematiques-estimation/references/12-rotations-se3.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Distinguer instant de capture, durée d'intégration, lecture et arrivée du paquet. Le rolling shutter décale les lignes ; un scan tournant échantillonne des directions à des temps distincts. Trigger matériel et synchronisation d'horloges doivent être mesurés, pas supposés.

## Mathématiques, conventions et unités

Avec vitesse $v$ en m/s et retard $\Delta t$ en s, un décalage apparent de l'ordre de $v\Delta t$ apparaît en translation uniforme. La rotation ajoute un effet dépendant du bras de levier et de la profondeur. LiDAR/ToF infèrent une distance de propagation ; radar Doppler renseigne une vitesse radiale, pas directement le vecteur vitesse 3D complet.

## Paramètres et propriétés

Consigner origine d'horloge, offset, dérive, latence, fréquence et temps par point/ligne. Une pose extrinsèque fixe ne corrige pas toujours un retard temporel. Une exposition courte ne supprime pas à elle seule le rolling shutter.

## Coût et implémentation

Deskew et interpolation requièrent mouvement et timestamps ; leur précision dépend de ces modèles. Aucun ROS 2 ni driver n'est exécuté ; vérifier formats et QoS avant un exemple réel.

## Évaluation et variation contrôlée

Cas analytique : à 2 m/s et 50 ms d'écart, prévoir 0,10 m de décalage de translation. Contrôler séparément temps et extrinsèques sur séquences immobiles puis en mouvement.

## Échecs et diagnostic

Des obstacles se dédoublent surtout dans les virages : comparer données au même temps, deskew, extrinsèques et sens des transformations. L'immobilité peut masquer un offset.

## Alternatives et usages

Global shutter, capteurs déclenchés, correction temporelle ou modèle rolling shutter selon cadence et mouvement ; aucun capteur n'est idéal pour toutes conditions.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent séparer temps d’exposition, lecture et synchronisation. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-CAPTEURS-001

**Question de travail** : Une exposition très courte suffit-elle à supprimer toute déformation rolling shutter ?

**Réponse de référence** : Non : elle réduit le flou par ligne, mais les lignes peuvent encore représenter des instants différents.

**Décomposition du phénomène** : l'exposition décrit la durée pendant laquelle une ligne accumule la lumière ; le temps de lecture détermine le décalage entre lignes. Une scène mobile peut donc produire des lignes individuellement nettes mais prises à des positions différentes. Dans un exemple construit, une mire verticale qui se déplace horizontalement peut apparaître inclinée, sans flou marqué sur ses bords.

**Vérification proposée** : comparer immobilité, translation et rotation, puis faire varier séparément exposition et durée de lecture lorsque le matériel le permet. Si le raccourcissement de l'exposition améliore la netteté sans supprimer l'inclinaison, les deux effets ont bien été distingués. Un global shutter modifie la simultanéité de capture ; il ne garantit pas une exposition assez courte ni une bonne synchronisation avec un autre capteur. Le modèle de projection utilisé pour la calibration doit rester compatible avec l'acquisition réelle.

### Cas lié à CV-CAPTEURS-004

**Question de travail** : Pourquoi une mesure Doppler radar ne se substitue-t-elle pas directement à une vitesse cartésienne 3D ?

**Réponse de référence** : Elle contraint la composante radiale relativement au capteur selon son modèle de mesure.

**Modèle de mesure** : si $\hat r$ est le vecteur unitaire du capteur vers la cible et $v_{rel}$ sa vitesse relative dans le même repère, la mesure idéale contraint $v_r=\hat r^Tv_{rel}$, avec une convention de signe à annoncer. C'est une projection scalaire. Toute composante orthogonale à $\hat r$ peut changer sans modifier cette mesure instantanée.

**Exemple construit** : une cible qui traverse latéralement le champ peut avoir une vitesse importante et une composante radiale faible à un instant donné. Conclure qu'elle est immobile serait donc injustifié. Pour retrouver davantage de composantes, exploiter d'autres directions, plusieurs instants ou d'autres capteurs avec un modèle dynamique explicite. Si le porteur bouge, son propre mouvement contribue à la vitesse relative. Une fusion doit traiter cette contribution et l'incertitude de la mesure, plutôt que recopier le scalaire Doppler dans trois axes.

**Repère documentaire de cette passe** : [Basler, Electronic Shutter Types](https://docs.baslerweb.com/electronic-shutter-types), global et rolling shutter. Les autres développements figurent dans les [cartes associées](../22-capteurs-horodatage.md).

## Sources et cartes

- [Zhang et Singh 2014, LOAM, §§II et V, correction de distorsion de mouvement](https://www.roboticsproceedings.org/rss10/p07.pdf).
- [Texas Instruments, TIDUF01 (2021), §2.4.9](https://www.ti.com/lit/ug/tiduf01/tiduf01.pdf).

Le calcul de décalage est cinématique et le cas caméra–LiDAR est construit par le projet ; Forster étaye la préintégration inertielle, pas la mesure Doppler.

- [Basler, electronic shutter types](https://docs.baslerweb.com/electronic-shutter-types).
- [Forster, IMU preintegration §§IV–VI](https://dellaert.github.io/files/Forster16tro.pdf).
- [Cartes associées](../22-capteurs-horodatage.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
