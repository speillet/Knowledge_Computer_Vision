# Revue — Métriques de segmentation, inspection et applications — 2026-10-20

## Synthèse

4 cartes auditées. Sources ciblées et lien primaire de remplacement ajouté ; réponses conservées.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

4 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 4 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-METRIQUES-APPLIQUEES-001 | Confirmé ; source ciblée | distinguer recouvrement et frontière. | 51 mots à l’entrée ; Objectif fini et autonome | Fiche et format contrôlés | mineur | Préciser la source |
| CV-METRIQUES-APPLIQUEES-002 | Confirmé ; source ciblée | mesurer les petits défauts. | 53 mots à l’entrée ; Objectif fini et autonome | Fiche et format contrôlés | mineur | Préciser la source |
| CV-METRIQUES-APPLIQUEES-003 | Confirmé ; source ciblée | séparer calibration et métrologie. | 44 mots à l’entrée ; Objectif fini et autonome | Fiche et format contrôlés | mineur | Préciser la source |
| CV-METRIQUES-APPLIQUEES-004 | Confirmé ; source ciblée | traiter les masques vides. | 48 mots à l’entrée ; Objectif fini et autonome | Fiche et format contrôlés | mineur | Préciser la source |

### Affirmations de la fiche et des cartes

- Confirmé : Dice est un recouvrement ; HD95 caractérise les distances de frontière avec conventions à définir. Reinke fig. 4a montre que le même Dice peut masquer des frontières différentes ; fig. 5c explicite le percentile robuste HD95.
- Confirmé : MVTec AD2 v1, fig. 4, pondère chaque région dans PRO, contrairement à une agrégation dominée par les grands défauts. Le domaine FPR d'intégration doit rester explicite ; aucune valeur unique n'est imposée aux cartes.
- Confirmé : NIST sépare répétabilité, reproductibilité, stabilité et biais ; le RMS d'un ajustement caméra ne résume pas ces composantes physiques.
- Confirmé : les cas vides peuvent rendre les métriques indéfinies et modifier une moyenne ; Reinke P2.3/P2.4/P3.2 demande de traiter ces propriétés.
- Les exemples de petits défauts et de métrologie sont des raisonnements construits. Les définitions détaillées biométriques/OCR restent dans leurs fiches 75/74 ; aucune équivalence de tous ces taux n'est affirmée.

## Corrections appliquées

Fiche révisée, lien AD2 remplacé par la même version primaire v1 ; quatre sources de cartes ciblées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Aucune addition prioritaire | Les objectifs existants suffisent au périmètre annoncé | — | Aucun rappel ajouté | Sources ci-dessous |

Familles absentes : algorithme, comprehension, conception, raisonnement. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [Metrics Reloaded, Semantic segmentation et métriques complémentaires](https://doi.org/10.1038/s41592-023-02151-z).
- [Reinke et al., fig. 4a/5c et P2.3/P2.4/P3.2](https://www.nature.com/articles/s41592-023-02150-0).
- [MVTec AD2 v1, fig. 4 et protocole PRO](https://arxiv.org/abs/2503.21622v1) ; PDF fournisseur initial inaccessible.
- [NIST, répétabilité](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc441.htm), [reproductibilité](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc442.htm), [stabilité](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc443.htm), [biais](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc45.htm).

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
