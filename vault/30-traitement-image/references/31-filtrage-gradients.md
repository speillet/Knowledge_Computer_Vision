---
id: CV-FILTRES
type: methode
domaine: d03
poles: [A, B, E, F]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 3
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

## Raisonnement guidé et contrôles proposés

Ces cas construits développent effet du support, unités du bilatéral et sous-échantillonnage. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-FILTRES-001

**Question de travail** : Pourquoi le médian peut-il convenir à du bruit impulsionnel sans être un remplaçant universel du Gaussien ?

**Réponse de référence** : Il rejette des valeurs extrêmes locales via l’ordre, tandis que le Gaussien moyenne ; l’effet dépend du bruit et des structures.

**Mécanisme concret** : dans un voisinage où la plupart des intensités valent environ 100 et une valeur vaut 255, une moyenne propage l'influence de cette impulsion à sa sortie, tandis qu'une médiane peut rester proche du niveau majoritaire. En revanche, une rayure réelle très fine peut elle aussi devenir minoritaire dans le voisinage et disparaître. Le filtre ne sait pas distinguer une impulsion parasite d'un défaut utile sur leur seule taille.

**Choix proposé** : comparer plusieurs supports sur un lot contenant bruit, bords et détails critiques. Garder identiques les étapes aval, puis mesurer défauts manqués et erreurs de localisation. Un support plus grand augmente l'échelle de modification de l'image. Le médian ne se décrit pas comme une convolution linéaire ; le Gaussien réalise une moyenne pondérée dont le comportement fréquentiel aide à construire des pyramides. Ces différences expliquent le choix, sans établir de classement universel.

### Cas lié à CV-FILTRES-004

**Question de travail** : Pourquoi ne suffit-il pas de prendre un pixel sur deux pour construire une pyramide de matching ?

**Réponse de référence** : La décimation sans filtrage peut replier les hautes fréquences en aliasing et changer les structures observées.

**Chaîne de raisonnement** : réduire la grille diminue la fréquence spatiale maximale représentable. Une alternance rapide d'intensités peut alors être interprétée comme un motif plus lent si l'on décime directement. Le lissage préalable atténue les composantes incompatibles avec la nouvelle grille ; la décimation réduit ensuite le nombre d'échantillons. Le préfiltre choisit donc ce qui est conservé avant la perte de résolution.

**Conséquence pour le matching** : les gradients et extrema utilisés comme features changent si la texture est repliée. Deux vues du même objet peuvent produire des descripteurs instables simplement à cause du rééchantillonnage. Dans un test construit, comparer le nombre de correspondances géométriquement vérifiées sur une mire réduite avec et sans préfiltre, à détecteur constant. Une meilleure stabilité ne constitue pas une invariance parfaite à l'échelle : un détail trop petit finit par disparaître même avec une pyramide correctement filtrée.

**Repère documentaire de cette passe** : [OpenCV 4.13, Smoothing Images](https://docs.opencv.org/4.13.0/dc/dd3/tutorial_gausian_median_blur_bilateral_filter.html), Median Blur et Bilateral Filter. Les autres développements figurent dans les [cartes associées](../31-filtrage-gradients.md).

## Sources et cartes

- [Tomasi et Manduchi 1998, Bilateral Filtering, §§2–3](https://users.soe.ucsc.edu/~manduchi/Papers/ICCV98.pdf).
- [OpenCV 4.13.0, Image Pyramids, Gaussian Pyramid](https://docs.opencv.org/4.13.0/d4/d1f/tutorial_pyramids.html).

Le protocole de rappel des défauts plutôt que PSNR seul est un choix d’évaluation du projet, sans résultat expérimental annoncé.

- [OpenCV, smoothing images : Theory](https://docs.opencv.org/4.12.0/dc/dd3/tutorial_gausian_median_blur_bilateral_filter.html).
- [Cartes associées](../31-filtrage-gradients.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
