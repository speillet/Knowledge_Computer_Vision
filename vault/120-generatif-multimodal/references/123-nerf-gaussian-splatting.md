---
id: CV-RENDU3D
type: comparaison
domaine: d12
poles: [B, D]
priorite: V2
profondeur: reperage
statut: redige
provenance: agent
revision: 3
prerequis: ["CV-EPIPOLAIRE"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d12]
---
# NeRF, 3D Gaussian Splatting et reconstruction

## Problème, données et hypothèses

Synthétiser des vues d'une scène et distinguer qualité de rendu et précision géométrique. Entrées : images et poses/calibration selon méthode ; sorties : représentation et nouvelles vues. Les méthodes de profondeur monoculaire ou DUSt3R/MASt3R relèvent d'autres contrats de reconstruction, à approfondir séparément.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-EPIPOLAIRE](../../50-calibration-geometrie/references/53-epipolaire-pnp-triangulation.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Dans NeRF original, la densité dépend de la position 3D seule ; la couleur/radiance dépend aussi de la direction de vue. Le rendu utilise une intégration volumique. 3D Gaussian Splatting optimise des primitives anisotropes explicites, leur apparence et densification, puis effectue un rendu par splatting.

## Mathématiques, conventions et unités

L'intégration volumique pondère une couleur par densité et transmittance le long du rayon ; les coordonnées, unités et poses doivent être cohérentes. Une PSNR élevée sur vues voisines n'établit ni surface métrique exacte ni qualité sur angles non observés.

## Paramètres et propriétés

Couverture des vues, poses, fond, exposition et scène statique supposée ; nombre de primitives, régularisation et protocole d'entraînement. Les ambiguïtés de régions jamais observées restent réelles.

## Coût et implémentation

Entraînement/optimisation, stockage et rendu coûtent différemment. Les FPS des auteurs dépendent du matériel et des scènes. Aucun rendu ou entraînement exécuté.

## Évaluation et variation contrôlée

Baseline : vues et poses connues avec split d'angles réservé ; varier couverture et bruit de pose séparément. Mesurer synthèse de vues et référence géométrique distinctement si la géométrie importe.

## Échecs et diagnostic

Rendu bon mais surface flottante : vérifier vues réservées, poses, régions non contraintes et objectif. Un optimiseur peut expliquer les images avec une géométrie inadéquate à la mesure.

## Alternatives et usages

MVS/TSDF pour d'autres hypothèses et sorties ; reconstruction apprise pour une autre supervision. Aucun de ces noms ne garantit une échelle absolue sans contrat adapté.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent synthèse de vues, support d’observation et géométrie. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-RENDU3D-001

**Question de travail** : Quelle différence centrale sépare NeRF et 3D Gaussian Splatting ?

**Réponse de référence** : NeRF utilise un champ de densité/radiance avec rendu volumique ; 3DGS une représentation explicite de gaussiennes optimisées et un rendu par splatting.

**Représentation et opération** : un champ implicite est interrogé le long de rayons pour calculer une image selon son modèle volumique. Des primitives explicites portent positions, étendues et apparence, puis sont projetées par un autre mécanisme de rendu. Ces choix déplacent les coûts d'optimisation, de stockage et de synthèse.

**Comparaison construite** : utiliser les mêmes vues et poses, réserver des angles puis mesurer qualité visuelle, mémoire et temps sur le même matériel. Si la géométrie importe, ajouter une référence de surface ou de dimension indépendante. Une représentation peut expliquer des images avec des structures qui ne conviennent pas à la métrologie ; un rendu rapide ne prouve pas une surface exacte. Dans NeRF original, distinguer aussi densité dépendant de la position et radiance dépendant de la vue. Le nom d'une famille ne décrit pas toutes les variantes ni une performance universelle.

### Cas lié à CV-RENDU3D-003

**Question de travail** : Des vues d’entraînement sont plausibles mais une rotation de caméra révèle des artefacts. Que tester ?

**Réponse de référence** : Couverture angulaire, poses et hypothèse de scène statique, puis régions insuffisamment contraintes.

**Origines possibles** : les vues d'apprentissage peuvent peu contraindre certaines faces, contenir des poses biaisées ou mélanger une scène qui change dans le temps. Une représentation flexible peut expliquer ces images sans reconstruire une scène cohérente depuis toutes les directions.

**Enquête construite** : cartographier couverture des rayons et erreurs selon angle, inspecter calibration et poses, puis comparer des vues réservées à distance angulaire annoncée. Faire varier séparément nombre de vues et qualité des poses, en gardant l'autre facteur contrôlé. Une amélioration sur les vues déjà utilisées peut n'être qu'un meilleur ajustement à ces données. Si une région n'a jamais été observée, davantage d'itérations n'apporte pas son apparence vraie. Le diagnostic doit donc distinguer manque d'information, modèle de scène faux et problème d'optimisation, plutôt que considérer toute synthèse plausible à l'entraînement comme une validation complète.

**Repère documentaire de cette passe** : [NeRF](https://arxiv.org/html/2003.08934v2), §3, champ et rendu volumétrique. Les autres développements figurent dans les [cartes associées](../123-nerf-gaussian-splatting.md).

## Sources et cartes

- [NeRF, §§3–4](https://arxiv.org/abs/2003.08934) : dépendances du champ et rendu volumique.
- [3D Gaussian Splatting, §§4–6](https://arxiv.org/abs/2308.04079) : primitives anisotropes, optimisation/densification et rendu.

- [NeRF, page et papier des auteurs](https://www.matthewtancik.com/nerf).
- [3D Gaussian Splatting, auteurs](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/).
- [Cartes associées](../123-nerf-gaussian-splatting.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
