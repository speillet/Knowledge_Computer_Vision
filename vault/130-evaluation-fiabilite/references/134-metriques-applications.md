---
id: CV-METRIQUES-APPLIQUEES
type: metrique-protocole
domaine: d13
poles: [A, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
prerequis: ["CV-IOU-AP", "CV-SEGMENTATION"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d13]
---
# Métriques de segmentation, inspection et applications

## Problème, données et hypothèses

Choisir la mesure d'après la décision à prendre et l'unité d'évaluation. Un pixel, une région défectueuse, une pièce, un patient et un document ne doivent pas être implicitement pondérés pareil. Les protocoles de masques vides, classes absentes et agrégation sont explicités.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-IOU-AP](131-iou-ap-coco.md) ; [CV-SEGMENTATION](../../90-segmentation/references/93-semantique-instances-panoptique.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Recouvrement (IoU/Dice), distance de surface (HD95), détection/localisation de défauts (AUROC/PRO), reconnaissance de texte (CER/WER), biométrie et métrologie répondent à des erreurs différentes. La fiche compare les choix ; les définitions détaillées spécialisées restent à approfondir séparément.

## Mathématiques, conventions et unités

Dice=$2TP/(2TP+FP+FN)$ sous convention définie. HD95 requiert surfaces, unité physique et définition de percentile/directions. PRO donne un poids par région selon protocole ; préciser le domaine FPR d'intégration AU-PRO. En métrologie, biais, répétabilité, reproductibilité et stabilité sont distincts ; un RMS caméra pixel n'est pas une incertitude dimensionnelle.

## Paramètres et propriétés

Unités, objets ignorés, taille, négatifs, seuils et agrégation. Un patient avec gros volume ou un défaut étendu ne doit pas masquer des cas critiques par un pooling pixel incontrôlé.

## Coût et implémentation

Certaines distances de surface coûtent plus que des comptages ; la collecte de références peut dominer. Aucun usage clinique, biométrique ou Gauge R&R réel exécuté.

## Évaluation et variation contrôlée

Variation analytique : conserver le grand objet correctement segmenté puis manquer un petit objet. Une moyenne pixel peut peu bouger ; une métrique par région/cas révèle la perte. Comparer au coût métier et au seuil d'exploitation.

## Échecs et diagnostic

Métriques contradictoires : chercher l'erreur mesurée, l'unité, les vides et le protocole ; ne pas retenir automatiquement le score le plus favorable.

## Alternatives et usages

Rapporter plusieurs vues complémentaires et leur limite. Les taux de comparaison FMR/FNMR, les décisions système FAR/FRR et PAD ne sont pas une métrique unique.

## Sources et cartes

- [Metrics Reloaded](https://doi.org/10.1038/s41592-023-02151-z).
- [NIST, Gauge R&R](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc4.htm).
- [MVTec AD2, PRO et protocole](https://www.mvtec.com/fileadmin/Redaktion/mvtec.com/company/research/datasets/MVTecAD2_arXiv_preprint_2503.21622v1.pdf).
- [Cartes associées](../134-metriques-applications.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
