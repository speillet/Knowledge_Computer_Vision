---
id: CV-REPRESENTATIONS
type: comparaison
domaine: d07
poles: [A, D, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 2
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d07]
---
# Représentations visuelles, ViT, Swin, ConvNeXt et DINOv2

## Problème, données et hypothèses

Choisir une représentation pour classification, retrieval ou tâche dense. Entrées : images prétraitées et éventuelle supervision ; sorties : features, pas nécessairement des classes adaptées au produit. La fiche compare les familles ; elle n'approfondit pas chaque architecture citée.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

HOG encode des gradients ; CNN/ResNet/ConvNeXt exploitent une structure convolutionnelle. ViT traite des tokens de patches ; Swin organise attention locale et hiérarchie. DINOv2 apprend des features transférables par autosupervision ; une tête et un protocole adaptés restent nécessaires.

## Mathématiques, conventions et unités

Pour H,W multiples du côté de patch P, un ViT a $N=HW/P^2$ tokens image. L'attention globale dense a un terme quadratique en N ; à P fixe, doubler les deux dimensions multiplie N par quatre et ce terme par seize. Une similarité cosinus compare des vecteurs normalisés ; ce n'est pas automatiquement une probabilité.

## Paramètres et propriétés

Résolution, prétraitement, tokens globaux/denses, couche choisie, normalisation et stratégie d'adaptation. Linear probing, fine-tuning complet et LoRA/adapters changent les paramètres appris et les besoins de données. MAE préentraîne par reconstruction masquée, pas par une tête de segmentation finale.

## Coût et implémentation

Comparer mémoire, pré/posttraitements et coût de la tête ; un backbone gelé peut rester coûteux en inférence. Aucun entraînement/checkpoint exécuté ni classement universel CNN/transformer annoncé.

## Évaluation et variation contrôlée

Baseline : features gelées et petite tête, puis adaptation contrôlée. Utiliser mêmes splits, labels et budget ; mesurer par classe, taille et domaine. Varier résolution séparément de la recette d'entraînement.

## Échecs et diagnostic

Bons résultats sur validation aléatoire mais mauvais nouveau site : inspecter fuite de scène, prétraitement et domaine. DINOv2 et DINO détecteur ne sont pas la même méthode.

## Alternatives et usages

Choisir robustesse et coût utiles au produit, pas seulement popularité du backbone. Les features autosupervisées peuvent être réutilisées par segmentation ou anomalies.

## Sources et cartes

- [Hu et al., LoRA, résumé et principe des paramètres gelés](https://arxiv.org/abs/2106.09685)
- [Houlsby et al., adapters, résumé](https://arxiv.org/abs/1902.00751)
- [He et al., MAE, résumé](https://arxiv.org/abs/2111.06377)
- [Dalal–Triggs, HOG, résumé](https://lear.inrialpes.fr/people/triggs/pubs/Dalal-cvpr05.pdf)

- [ViT, §§3–4](https://arxiv.org/abs/2010.11929).
- [Swin, §3](https://arxiv.org/abs/2103.14030).
- [ConvNeXt, §2](https://arxiv.org/abs/2201.03545).
- [DINOv2, méthode et transfert](https://arxiv.org/abs/2304.07193).
- [Cartes associées](../71-representations-transfert.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
