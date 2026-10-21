---
id: CV-ACQUISITION
type: methode
domaine: d02
poles: [A, B, C, E, F]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 2
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d02]
---
# Exposition, bruit, couleur et échantillonnage

## Problème, données et hypothèses

Obtenir une image dont les détails utiles sont mesurables. Entrées : scène, éclairage, optique, exposition et capteur ; sortie : intensités échantillonnées avec saturation, bruit et repères connus. Un réseau ne récupère pas automatiquement une information détruite par l'acquisition.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Les photons deviennent une mesure bruitée puis numérisée. Exposition, ouverture, éclairage et gain ont des effets différents. Filtrer avant décimation limite l'aliasing ; appliquer une opération photométrique en valeurs gamma n'est pas équivalent à l'appliquer en lumière linéaire.

## Mathématiques, conventions et unités

Modèle simplifié : flou $b_{px}\approx v_{px}t_e$, vitesse image en px/s et exposition en s. Le bruit photonique idéal a variance égale au nombre moyen de photoélectrons ; il ne résume pas tout le bruit du capteur. Nyquist demande une fréquence inférieure à la moitié de l'échantillonnage pour un signal limité en bande, sans garantir la détection de tout défaut à deux pixels.

## Paramètres et propriétés

Vérifier plage, profondeur de bits, gamma, BGR/RGB, balance des blancs et saturation. Le gain numérique ne crée pas de photons. Rolling shutter et temps d'exposition sont deux dimensions temporelles distinctes.

## Coût et implémentation

Résolution et débit capteur imposent transferts et calcul ; mesurer le coût complet. Aucune capture matérielle exécutée ; les équations sont des modèles annoncés, pas des propriétés universelles de caméra.

## Évaluation et variation contrôlée

Variation analytique : doubler l'exposition à vitesse image constante double le flou prévu. Sur images réservées, comparer netteté et saturation avant/après, à éclairage contrôlé. Une meilleure moyenne d'intensité peut masquer une perte de résolution utile.

## Échecs et diagnostic

Échec sur pièces rapides : mesurer flou, saturation et contraste aux endroits critiques avant de réentraîner. Un motif changeant après resize peut indiquer aliasing et non dérive sémantique.

## Alternatives et usages

Éclairage synchronisé, exposition plus courte, optique adaptée ou cadence différente : arbitrer signal, flou, chaleur, coût et contraintes de ligne.

## Sources et cartes

- [OpenCV 4.13.0, Image Pyramids, Gaussian Pyramid](https://docs.opencv.org/4.13.0/d4/d1f/tutorial_pyramids.html).
- [sRGB, §§A.7–A.8 et B.1, conversion linéaire et fonction de transfert](https://www.w3.org/Graphics/Color/srgb).

Le calcul $b_{px}=v_{px}t_e$ est une déduction cinématique du projet pour une vitesse image constante ; EMVA documente le capteur, pas cette formule de flou. Le contrôle de cohérence entraînement/inférence est une démarche du projet.

- [EMVA1288 Linear 4.0, bruit et SNR](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf).
- [Edmund Optics, resolution](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/resolution/).
- [Cartes associées](../21-exposition-bruit-echantillonnage.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
