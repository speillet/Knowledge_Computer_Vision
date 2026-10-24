---
id: CV-WATERSHED
type: pipeline
domaine: d09
poles: [A, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 2
prerequis: ["CV-MORPHO"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d09]
---
# Otsu, distance transform et watershed

## Problème, données et hypothèses

Séparer des objets au contact à partir d'un modèle classique d'intensité et de marqueurs. Entrées : image, masque et polarité ; sorties successives : partition binaire, distances puis labels d'instances. Ce sont des étapes différentes, pas trois noms d'un même algorithme.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-MORPHO](../../30-traitement-image/references/33-morphologie-composantes.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Otsu choisit un seuil selon les distributions d'intensité. La distance transform mesure la distance d'un pixel du masque au fond. Ses maxima peuvent fournir des marqueurs ; watershed propage des bassins selon une topographie/implémentation. De bons marqueurs importent autant que le seuillage.

## Mathématiques, conventions et unités

Otsu maximise $\omega_0\omega_1(\mu_0-\mu_1)^2$ pour un seuil, poids de classes et moyennes, équivalent à minimiser la variance intra-classe pondérée. La distance $D(p)=\min_{q\in fond}\|p-q\|$ dépend de la métrique et de la résolution. Elle ne mesure pas directement une identité ou classe d'objet.

## Paramètres et propriétés

Seuil, éclairage, morphologie, maxima et connectivité. Dans watershed OpenCV documenté, image 8 bits 3 canaux et marqueurs int32 : inconnu 0, labels positifs, frontières finales −1 ; le tableau de marqueurs est modifié. Le fond connu est distinct de l'inconnu.

## Coût et implémentation

Coût de segmentation et de propagation lié à l'image/marqueurs. Aucun appel OpenCV exécuté ; un calcul Otsu sur histogramme jouet est proposé dans les exemples arithmétiques, pas une validation image.

## Évaluation et variation contrôlée

Baseline : objets disjoints puis contact contrôlé ; comparer composantes seules et watershed à marqueurs. Prédire qu'un marqueur fusionné peut maintenir la sous-segmentation. Mesurer erreurs d'instances, pas seulement recouvrement du masque global.

## Échecs et diagnostic

Deux grains restent fusionnés : inspecter marqueurs et topographie. Trop de fragments : inspecter bruit et maxima parasites. Un bon histogramme bimodal ne prouve pas une bonne séparation sémantique.

## Alternatives et usages

Seuillage local pour éclairage variable, GrabCut pour interaction, modèle d'instances si variations dépassent les hypothèses simples.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent histogramme, distance et rôle des marqueurs. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-WATERSHED-001

**Question de travail** : Pourquoi un seuil Otsu optimal sur l’histogramme peut-il être mauvais pour segmenter les défauts ?

**Réponse de référence** : L’objectif sépare des intensités selon une variance, pas des catégories métier ; éclairage, déséquilibre et bruit peuvent dominer.

**Lecture de l'objectif** : Otsu choisit une coupure selon les poids et moyennes des groupes d'intensité. Une partition qui sépare bien deux niveaux de luminosité peut surtout distinguer ombre et zone éclairée, alors que le défaut traverse les deux. L'optimum appartient au critère statistique retenu, pas à une connaissance des pièces.

**Exemple construit** : un défaut très petit et peu contrasté pèse peu dans l'histogramme global d'une grande image. Une coupure adaptée au fond majoritaire peut donc le manquer. Comparer le masque aux annotations de défauts, en stratifiant tailles et éclairage. Tester une correction d'acquisition ou un seuillage local si elle correspond à l'hypothèse observée, sans supposer que tout seuil automatique est robuste à toute scène. Pour du comptage, il faudra encore séparer les objets : une partition binaire correcte ne fournit pas leurs identités d'instance.

### Cas lié à CV-WATERSHED-005

**Question de travail** : Pourquoi une IoU binaire élevée peut-elle masquer l’échec d’un pipeline de comptage watershed ?

**Réponse de référence** : La fusion de plusieurs objets peut conserver presque toute la région de premier plan mais perdre le nombre et l’identité des instances.

**Exemple analytique** : deux objets adjacents dont l'union est exactement prédite peuvent donner un masque de premier plan parfait. Si la sortie ne possède qu'un label pour cette union, le recouvrement binaire vaut pourtant un alors que le comptage de deux objets échoue. La métrique ne contredit pas l'échec : elle mesure une autre sortie.

**Évaluation proposée** : définir une association entre instances prédites et réelles, puis compter objets retrouvés, fusions, fragments et faux objets. Conserver le masque global comme mesure complémentaire, en annonçant seuils et traitement des contacts. Vérifier plusieurs densités et tailles, car les erreurs de séparation peuvent augmenter dans les zones où la région binaire reste bonne. Le contrat du produit, par exemple compter des pièces, doit donc guider les annotations et les mesures avant le choix du pipeline de segmentation.

**Repère documentaire de cette passe** : [OpenCV 4.13, Watershed](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html), marqueurs, transformée de distance et frontières. Les autres développements figurent dans les [cartes associées](../91-otsu-distance-watershed.md).

## Sources et cartes

- [OpenCV Otsu, théorie](https://docs.opencv.org/4.13.0/d7/d4d/tutorial_py_thresholding.html).
- [OpenCV watershed, marqueurs et API](https://docs.opencv.org/4.13.0/d3/db4/tutorial_py_watershed.html).
- [Cartes associées](../91-otsu-distance-watershed.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
