---
id: CV-FILTRES
type: methode
domaine: d03
poles: [A, B, E, F]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 2
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d03]
---
# Filtres, gradients et pyramides

## Problème, données et hypothèses

Atténuer certaines perturbations sans détruire les structures nécessaires au pipeline. Entrée : image, type/plage et bruit supposé ; sortie : image filtrée ou dérivées. Les conditions aux bords et l'échelle du noyau font partie de l'algorithme.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Gaussien : moyenne pondérée spatiale linéaire. Médian : statistique d'ordre non linéaire utile pour impulsions. Bilatéral : poids de proximité et de similarité photométrique. Dériver amplifie certaines hautes fréquences ; lisser puis dériver choisit une échelle d'analyse.

## Mathématiques, conventions et unités

La convolution discrète écrit $J(p)=\sum_q K(q)I(p-q)$, avec noyau normalisé pour une moyenne. Pour une intensité scalaire, dans un bilatéral gaussien, le poids est proportionnel à $\exp(-\|p-q\|^2/(2\sigma_s^2)-|I(p)-I(q)|^2/(2\sigma_r^2))$ puis renormalisé. $\sigma_s$ est en pixels ; $\sigma_r$ dans l'unité d'intensité. Pour $I'=I/255$, conserver les poids photométriques exige $\sigma_r'=\sigma_r/255$. Le cas couleur remplace la différence scalaire par une distance dans l’espace couleur choisi.

## Paramètres et propriétés

Taille, sigma, bord et plage photométrique doivent être fixés. Un filtre préservant relativement les contours ne conserve pas tous les petits défauts. Une pyramide suppose un filtrage approprié avant décimation.

## Coût et implémentation

Le Gaussien séparable permet deux passes 1D ; un bilatéral naïf visite chaque voisin du support pour chaque pixel. Aucun benchmark ni appel OpenCV exécuté ici.

## Évaluation et variation contrôlée

Variation proposée : même image avec bruit gaussien puis impulsionnel, à protocole fixe. Comparer résidu de bruit et rappel d'un petit défaut ; optimiser la qualité du pipeline aval, pas seulement une image visuellement lisse.

## Échecs et diagnostic

Des contours disparaissent : inspecter échelle du filtre et contraste du détail. Une teinte change au bord : vérifier padding et espace couleur avant de changer le réseau.

## Alternatives et usages

Choisir le modèle de bruit et la tâche ; restauration apprise ou débruitage spécialisé peuvent aider mais doivent être comparés à une baseline simple.

## Sources et cartes

- [Tomasi et Manduchi 1998, Bilateral Filtering, §§2–3](https://users.soe.ucsc.edu/~manduchi/Papers/ICCV98.pdf).
- [OpenCV 4.13.0, Image Pyramids, Gaussian Pyramid](https://docs.opencv.org/4.13.0/d4/d1f/tutorial_pyramids.html).

Le protocole de rappel des défauts plutôt que PSNR seul est un choix d’évaluation du projet, sans résultat expérimental annoncé.

- [OpenCV, smoothing images : Theory](https://docs.opencv.org/4.12.0/dc/dd3/tutorial_gausian_median_blur_bilateral_filter.html).
- [Cartes associées](../31-filtrage-gradients.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
