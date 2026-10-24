---
id: CV-ECC
type: methode
domaine: d04
poles: [B, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
prerequis: ["CV-HOMOGRAPHIE"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d04]
---
# Recalage par intensités et ECC

## Problème, données et hypothèses

Aligner des images en optimisant un critère photométrique sous un modèle de mouvement. Entrées : images compatibles, masque éventuel et initialisation ; sortie : paramètres de warp. Ce n'est pas un matcher de descripteurs locaux.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-HOMOGRAPHIE](../../50-calibration-geometrie/references/51-ransac-homographie.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

L'optimiseur déforme une image pour améliorer la corrélation avec l'autre. Le centrage et la normalisation rendent la corrélation inchangée sous un gain positif et un offset globaux sur un support fixé, de variance non nulle (déduction algébrique). Cela ne garantit pas une convergence du recalage ECC. Une pyramide peut améliorer l'initialisation sans garantir un optimum global.

## Mathématiques, conventions et unités

Un warp $W(x;\theta)$ transforme les coordonnées selon le modèle choisi. Une corrélation normalisée compare des intensités centrées/normées sur la zone commune ; $\theta$ n'a pas les mêmes dimensions pour translation, affine et homographie. Préciser le sens du warp et l'usage de sa réciproque à l'affichage.

## Paramètres et propriétés

Modèle, critère d'arrêt, masque et échelle doivent correspondre au mouvement. Texture, recouvrement et initialisation sont essentiels. Robustesse à un gain simple ne couvre pas ombres, occultations ou géométrie 3D arbitraire.

## Coût et implémentation

Chaque itération évalue et dérive le critère sur des pixels ; résolution et pyramide comptent. Aucun appel `findTransformECC` exécuté ; ne pas transformer convergence en garantie de recalage.

## Évaluation et variation contrôlée

Variation proposée : translation connue puis initialisation de plus en plus éloignée. Mesurer erreur de warp sur points réservés et taux de convergence ; un score photométrique seul peut favoriser un motif répétitif.

## Échecs et diagnostic

Échec malgré des images proches : vérifier plage/type, sens de transformation, recouvrement et perturbation photométrique réelle.

## Alternatives et usages

Features + RANSAC pour grandes transformations avec points distinctifs ; recalage par intensités pour raffinement approprié. Comparer sur précision et bassin utile.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent critère photométrique, bassin de convergence et masques. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-ECC-001

**Question de travail** : Quel contrat distingue ECC d’un pipeline SIFT + RANSAC ?

**Réponse de référence** : ECC optimise un critère d’intensité sur un warp initialisé ; SIFT propose des paires puis une géométrie robuste.

**Mécanisme interprété** : ECC cherche des paramètres de transformation en comparant directement les intensités sur une zone commune. Les correspondances ne sont pas d'abord exprimées comme une liste de patches détectés. SIFT et RANSAC peuvent proposer une transformation à partir de points distinctifs ; un raffinement photométrique peut ensuite être essayé si le modèle et le recouvrement s'y prêtent.

**Exemple construit** : pour deux vues proches d'une étiquette, une initialisation convenable peut rendre utile l'optimisation des intensités. Pour un grand déplacement avec faible recouvrement, la même procédure peut atteindre un mauvais optimum ou échouer. Vérifier séparément initialisation, masque, variations photométriques et modèle de mouvement. Une corrélation normalisée peut tolérer un gain positif et un offset globaux sur un support fixé non constant ; cette propriété algébrique ne couvre pas une ombre locale, une occultation ou une convergence globale du recalage.

### Cas lié à CV-ECC-003

**Question de travail** : Pourquoi ne pas choisir systématiquement une homographie dans un recalage ECC ?

**Réponse de référence** : Plus de paramètres peuvent surajuster ou réduire la stabilité alors qu’une translation ou un affine suffit au besoin.

**Raisonnement sur les degrés de liberté** : un modèle de translation impose que tous les points partagent deux déplacements ; une homographie autorise une déformation projective plus générale. Cette souplesse peut expliquer de vraies variations de vue sur un plan, mais aussi absorber du bruit ou une perturbation photométrique lorsque les données contraignent mal ses paramètres.

**Comparaison construite** : sur une installation où le mouvement prévu est une petite translation, ajuster d'abord ce modèle, puis un modèle plus riche avec les mêmes images et zone utile. Comparer erreurs sur des points réservés, stabilité des paramètres et extrapolation près des bords. Un meilleur score sur les pixels d'ajustement ne suffit pas. Inversement, conserver une translation si la perspective change réellement introduit un biais. Le choix relie donc la géométrie de capture, la richesse des observations et l'erreur admise, plutôt qu'un principe de simplicité ou de flexibilité appliqué aveuglément.

**Repère documentaire de cette passe** : [OpenCV 4.13, Video Tracking](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html), findTransformECC et paramètres du warp. Les autres développements figurent dans les [cartes associées](../45-recalage-ecc.md).

## Sources et cartes

- [OpenCV findTransformECC, motion and criteria](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html).
- [Cartes associées](../45-recalage-ecc.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
