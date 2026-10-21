# Revue — Segmentation sémantique, instances et panoptique — 2026-10-20

## Synthèse

4 cartes auditées. Définition panoptique et justification des métriques précisées.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

4 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 1 importante, 3 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SEGMENTATION-001 | Confirmé après précision | choisir la sortie de segmentation. | 44 mots à l’entrée ; Trois sorties distinctes | Fiche et format contrôlés | important | Préciser partition |
| CV-SEGMENTATION-002 | Confirmé, référence précisée | détecter une mauvaise définition de tâche. | 47 mots à l’entrée ; Objectif conservé | Fiche et format contrôlés | mineur | Cibler source |
| CV-SEGMENTATION-003 | Déduction de labels discrets | propager une augmentation dense. | 54 mots à l’entrée ; Un seul objectif de cohérence | Fiche et format contrôlés | mineur | Attribuer le raisonnement |
| CV-SEGMENTATION-004 | Confirmé, référence précisée | évaluer une segmentation médicale. | 51 mots à l’entrée ; Objectif conservé | Fiche et format contrôlés | mineur | Cibler source |

### Affirmations de la fiche et des cartes

- Confirmé : U-Net encodeur/décodeur avec concaténations (§2), DeepLabv3+ contexte atrous (résumé), Mask R-CNN branche de masque et détection (résumé), nnU-Net configuration de tout un pipeline (résumé Nature).
- Imprécis puis corrigé : le noyau panoptique omettait l'absence de recouvrement ; §3 établit une affectation par pixel.
- Confirmé : PQ sépare qualité de segmentation et reconnaissance (§4). Formules IoU/Dice cohérentes sous dénominateur non nul ; la fiche exige une convention des vides.
- Discrétion des labels : déduction, pas prescription d'une API. Interpoler les nombres des classes comme des intensités peut créer une classe sans sens.
- Sources complétées : Reinke P1/P2/P3 justifie les limites du recouvrement, les frontières, petites structures et agrégations. Les modalités de validation externe restent une proposition du projet.

## Corrections appliquées

Fiche et noyau 001 précisent la partition ; sources 002–004 adaptées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Calculer PQ sur un mini-appariement | La fiche cite PQ sans rappel opératoire | evaluation | 1 carte ; TP/FP/FN et IoU moyenne | Panoptic Segmentation §4 |

Familles absentes : algorithme, comprehension, conception, raisonnement. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [U-Net, §2 et overlap-tile](https://arxiv.org/abs/1505.04597).
- [DeepLabv3+, résumé](https://arxiv.org/abs/1802.02611) ; [Mask R-CNN, résumé et introduction](https://arxiv.org/abs/1703.06870).
- [Panoptic Segmentation, §§3–4](https://arxiv.org/abs/1801.00868).
- [nnU-Net, résumé](https://doi.org/10.1038/s41592-020-01008-z).
- [Reinke et al., P1, P2.1–P2.4, P3.2 et discussion](https://www.nature.com/articles/s41592-023-02150-0).

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
