---
id: CV-METRIQUES-APPLIQUEES
type: metrique-protocole
domaine: d13
poles: [A, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
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

## Raisonnement guidé et contrôles proposés

Ces cas construits développent topologie, surfaces physiques et références incertaines. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-METRIQUES-APPLIQUEES-001

**Question de travail** : Pourquoi Dice et HD95 peuvent-ils raconter des choses différentes sur un même masque ?

**Réponse de référence** : Dice mesure un recouvrement ; HD95 une distance de surface selon un percentile/protocole, avec unité physique si les coordonnées sont calibrées.

**Exemple de divergence** : un grand masque peut conserver presque tout son volume alors qu'une petite partie de surface est éloignée. Le recouvrement et une distance de surface pondèrent cet écart différemment. Un percentile écarte aussi une partie des distances extrêmes selon la définition retenue ; ce n'est pas nécessairement la distance maximale.

**Protocole proposé** : annoncer définition des surfaces, distances dirigées ou symétrisées, percentile, espacement et unité. Conserver le traitement des vides et le niveau d'agrégation par cas ou pixel. Examiner les exemples où les métriques divergent pour identifier l'erreur qu'elles révèlent, plutôt que choisir automatiquement le score favorable. Une distance en millimètres nécessite une géométrie physique cohérente. Ces mesures peuvent être complémentaires si l'usage dépend à la fois de couverture et de frontière ; aucune valeur isolée ne démontre toute la qualité du masque ou son utilité dans un autre processus.

### Cas lié à CV-METRIQUES-APPLIQUEES-004

**Question de travail** : Que faut-il annoncer lorsqu’une métrique de segmentation rencontre référence ou prédiction vide ?

**Réponse de référence** : La convention choisie et son effet sur le score/agrégation ; ne pas laisser une division indéfinie devenir un résultat implicite.

**Distinguer les situations** : deux masques vides, une référence vide avec faux positif et une prédiction vide sur un objet présent n'ont pas le même sens. Une distance de surface peut être indéfinie lorsqu'une surface manque, tandis qu'un recouvrement peut nécessiter une convention particulière pour un dénominateur nul.

**Choix de protocole proposé** : définir ces cas avant les résultats et les conserver dans un tableau de comptage séparé si la métrique principale ne peut pas les résumer. Annoncer valeurs conventionnelles, exclusions éventuelles et poids dans l'agrégation. Retirer silencieusement les cas négatifs peut cacher des faux positifs ; retirer les prédictions vides peut cacher les objets entièrement manqués. Tester quelques exemples synthétiques connus dans l'outil d'évaluation et conserver sa version. La convention n'est pas une astuce numérique : elle détermine quelles erreurs le score final représente et lesquelles doivent être rapportées autrement.

**Repère documentaire de cette passe** : [Reinke et al., Understanding metric-related pitfalls](https://arxiv.org/html/2302.01790v4), P2.2–P2.4 : tailles, formes, références/prédictions vides. Les autres développements figurent dans les [cartes associées](../134-metriques-applications.md).

## Sources et cartes

- [Reinke et al., P2.1–P2.4 et P3.2](https://www.nature.com/articles/s41592-023-02150-0) : frontières, vides et agrégation.

- [Metrics Reloaded](https://doi.org/10.1038/s41592-023-02151-z).
- [NIST, Gauge R&R](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc4.htm).
- [MVTec AD2, PRO et protocole](https://arxiv.org/abs/2503.21622v1).
- [Cartes associées](../134-metriques-applications.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
