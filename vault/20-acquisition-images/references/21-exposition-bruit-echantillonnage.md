---
id: CV-ACQUISITION
type: methode
domaine: d02
poles: [A, B, C, E, F]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 5
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

Modèle simplifié : flou $b_{px}\approx v_{px}t_e$, vitesse image en px/s et exposition en s. Le bruit photonique idéal a variance égale au nombre moyen de photoélectrons ; il ne résume pas tout le bruit du capteur. EMVA 1288 (§2.4, équations 13–14) ajoute une variance de bruit de lecture $\sigma_d^2$ en e⁻² (son écart-type $\sigma_d$ est en e⁻), et un bruit de quantification $\sigma_q^2=1/12$ DN². $\eta$ est le rendement quantique, $\mu_p$ le nombre moyen de photons reçus par pixel pendant l’exposition ; $\eta\mu_p$ est le nombre moyen de photoélectrons. $K$ est le gain système en DN/e⁻, et $\sigma_q^2$ la variance de quantification en DN². Le modèle suppose une réponse linéaire non saturée à un point de fonctionnement fixé. Le SNR s'écrit $\eta\mu_p/\sqrt{\sigma_d^2+\sigma_q^2/K^2+\eta\mu_p}$ (§2.6, équation 21). Hors quantification, le gain système $K$ s'y annule : augmenter le gain ne change pas le SNR, alors que doubler les photons le multiplie par $\sqrt2$ en régime photonique et jusqu'à 2 en régime de bruit de lecture (équation 22). Un gain plus fort atteint la valeur numérique maximale avec moins d'électrons, d'où une capacité de saturation réduite (§2.7). Exemple du projet, $\sigma_d=5$ e⁻ : SNR 8,9 à 100 e⁻, 13,3 à 200 e⁻, inchangé si l'on double $K$. Nyquist demande une fréquence inférieure à la moitié de l'échantillonnage pour un signal limité en bande, sans garantir la détection de tout défaut à deux pixels. Réduire une image sans préfiltre adapté au facteur de réduction replie les hautes fréquences dans le résultat. Parmar et al. (2022, §§2 et 3.2) le rappellent, et observent de l’aliasing dans les configurations OpenCV, TensorFlow et PyTorch étudiées en 2022, face aux filtres adaptatifs de PIL (§1, §6.3). Ce résultat n’est pas une propriété intemporelle d’une bibliothèque : vérifier API, version, interpolation et antialiasing. Par exemple, `torchvision.transforms.Resize` 0.24 active `antialias=True`, valeur par défaut introduite en 0.17.

## Paramètres et propriétés

Vérifier plage, profondeur de bits, gamma, BGR/RGB, balance des blancs et saturation. Le gain numérique ne crée pas de photons. Rolling shutter et temps d'exposition sont deux dimensions temporelles distinctes. Pour éclaircir une image, renforcer l'éclairage double le signal sans allonger le flou, au contraire d'une exposition plus longue.

## Coût et implémentation

Résolution et débit capteur imposent transferts et calcul ; mesurer le coût complet. Aucune capture matérielle exécutée ; les équations sont des modèles annoncés, pas des propriétés universelles de caméra.

## Évaluation et variation contrôlée

Variation analytique : doubler l'exposition à vitesse image constante double le flou prévu. Sur images réservées, comparer netteté et saturation avant/après, à éclairage contrôlé. Une meilleure moyenne d'intensité peut masquer une perte de résolution utile.

## Échecs et diagnostic

Échec sur pièces rapides : mesurer flou, saturation et contraste aux endroits critiques avant de réentraîner. Un motif changeant après resize peut indiquer aliasing et non dérive sémantique.

## Alternatives et usages

Éclairage synchronisé, exposition plus courte, optique adaptée ou cadence différente : arbitrer signal, flou, chaleur, coût et contraintes de ligne.

## Sources et cartes

- [OpenCV 4.13.0, Image Pyramids, Gaussian Pyramid](https://docs.opencv.org/4.13.0/d4/d1f/tutorial_pyramids.html). Le tutoriel décrit le flou gaussien avant décimation, pas l'aliasing.
- [Parmar, Zhang et Zhu 2022, On Aliased Resizing and Surprising Subtleties in GAN Evaluation, CVPR, §§1–3.2 et 6.3](https://arxiv.org/abs/2104.11222) : critère de Nyquist, préfiltre et conventions de resize selon la bibliothèque.
- [sRGB, §§A.7–A.8 et B.1, conversion linéaire et fonction de transfert](https://www.w3.org/Graphics/Color/srgb).

Le calcul $b_{px}=v_{px}t_e$ est une déduction cinématique du projet pour une vitesse image constante ; EMVA documente le capteur, pas cette formule de flou. Le contrôle de cohérence entraînement/inférence est une démarche du projet.

- [EMVA1288 Linear 4.0, 16 juin 2021, §2.4, équations 13–15, §2.6, équations 20–23, §2.7](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf) : modèle de bruit, SNR et saturation.
- [Edmund Optics, resolution](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/resolution/). Page inaccessible aux outils automatisés le 2026-10-23 : non revérifiée.
- [torchvision 0.24, Resize, paramètre antialias et changement de défaut en 0.17 (consulté le 2026-10-24)](https://docs.pytorch.org/vision/0.24/generated/torchvision.transforms.Resize.html).
- [Cartes associées](../21-exposition-bruit-echantillonnage.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet. Révisions 3 et 4 : auto-revue `revue-cartes` par Agent Claude Code le 2026-10-23, correction puis enrichissement accepté par l'apprenant, sans validation indépendante.
