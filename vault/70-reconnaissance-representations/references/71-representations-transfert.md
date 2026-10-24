---
id: CV-REPRESENTATIONS
type: comparaison
domaine: d07
poles: [A, D, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
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

## Raisonnement guidé et contrôles proposés

Ces cas construits développent biais d’architecture, échelle et protocole de transfert. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-REPRESENTATIONS-001

**Question de travail** : Dans un ViT à patch fixe et attention globale dense, doubler largeur et hauteur change comment le nombre de tokens image (hors token de classe) et le terme quadratique associé ?

**Réponse de référence** : Tokens ×4 ; terme quadratique ×16, dans ce modèle de coût.

**Dérivation du coût** : avec des patches de côté $P$ fixé et des dimensions compatibles, $N=HW/P^2$. Doubler $H$ et $W$ multiplie le nombre de patches par quatre. Une matrice d'interactions globale entre tokens a alors seize fois plus de couples. Ce comptage concerne le terme d'attention considéré, pas toutes les opérations du réseau.

**Conséquence pratique proposée** : avant d'augmenter la résolution pour de petits défauts, estimer mémoire des activations et tester la latence complète. Les projections, convolutions éventuelles, kernels et contraintes de bande passante ne suivent pas nécessairement ce même facteur. Une réduction de batch ou une autre représentation peut modifier le compromis. Vérifier aussi si l'information du défaut existe dans l'acquisition initiale : agrandir une image sans détail supplémentaire n'apporte pas les mêmes observations qu'une capture réellement mieux résolue. Les mesures sur le matériel cible complètent donc le modèle de coût.

### Cas lié à CV-REPRESENTATIONS-005

**Question de travail** : Un backbone préentraîné se dégrade après remplacement du chargeur d’images. Que vérifier avant un nouveau fine-tuning ?

**Réponse de référence** : Ordre couleur, normalisation, plage, interpolation, crop et résolution réellement reçus.

**Piège d'interface** : deux chargeurs peuvent produire des images visuellement semblables tout en différant dans l'ordre des canaux ou le traitement des centres de pixels. Une normalisation répétée ou omise peut également modifier fortement le tenseur reçu. Le backbone ne voit que ces valeurs, pas l'intention du pipeline.

**Enquête reproductible proposée** : utiliser un fichier témoin identique, enregistrer formes, types, plages et pixels connus après chaque étape, puis comparer les tenseurs d'entrée. Refaire l'extraction avec les mêmes poids et paramètres. Si les features changent avant toute variation de scène, rechercher d'abord cette différence déterministe. Une fois le contrat restauré, évaluer le nouveau domaine sur un ensemble réservé. Un fine-tuning lancé trop tôt peut absorber partiellement un bug de prétraitement, rendre la régression moins visible et compliquer la reproductibilité sans avoir traité sa cause.

**Repère documentaire de cette passe** : [ViT](https://arxiv.org/html/2010.11929v2), §3, représentation par patches. Les autres développements figurent dans les [cartes associées](../71-representations-transfert.md).

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
