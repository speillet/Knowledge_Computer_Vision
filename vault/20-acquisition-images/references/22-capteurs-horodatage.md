---
id: CV-CAPTEURS
type: methode
domaine: d02
poles: [B, C, E, F]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
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

## Sources et cartes

- [Basler, electronic shutter types](https://docs.baslerweb.com/electronic-shutter-types).
- [Forster, IMU preintegration §§IV–VI](https://dellaert.github.io/files/Forster16tro.pdf).
- [Cartes associées](../22-capteurs-horodatage.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
