# Revue — Évaluer identités, trajectoires et localisation 3D — 2026-10-20

## Synthèse

5 cartes auditées. Source directe de RPE et notations ajoutées ; sources des cinq cartes ciblées.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

5 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 1 importante, 4 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-METRIQUES-TEMPS-001 | Déduction de protocole confirmée | séparer détection et identité. | 44 mots à l’entrée ; Contre-exemple précis | Fiche et format contrôlés | mineur | Cibler source |
| CV-METRIQUES-TEMPS-002 | Confirmé | respecter l’agrégation HOTA. | 49 mots à l’entrée ; Agrégation finie | Fiche et format contrôlés | mineur | Cibler HOTA |
| CV-METRIQUES-TEMPS-003 | Confirmé | choisir un alignement de trajectoire. | 55 mots à l’entrée ; Une liberté de jauge identifiée | Fiche et format contrôlés | mineur | Cibler tableau I |
| CV-METRIQUES-TEMPS-004 | Confirmé avec source ajoutée | distinguer ATE et RPE. | 45 mots à l’entrée ; Distinction des mesures finie | Fiche et format contrôlés | important | Ajouter Sturm |
| CV-METRIQUES-TEMPS-005 | Diagnostic du projet | comparer des évaluateurs temporels. | 45 mots à l’entrée ; Liste de paramètres finie | Fiche et format contrôlés | mineur | Attribuer le cas |

### Affirmations de la fiche et des cartes

- Confirmé : MOTA agrège FN/FP/IDSW ; IDF1 repose sur des correspondances d'identités (HOTA §4, équations 2/6).
- Confirmé : HOTA §5 calcule la moyenne des scores par seuil, approximant une intégrale, avec α de 0,05 à 0,95 ; la racine du produit est calculée avant cette moyenne.
- Confirmé : Zhang–Scaramuzza tableau I distingue similitude monoculaire, transformation rigide stéréo et transformation à yaw seul pour inertiel. L'alignement ne doit pas absorber un défaut observable.
- Confirmé avec source ajoutée : RPE de Sturm équation 1 correspond au produit relatif de la fiche ; ATE est évaluée après alignement. La RE par sous-trajectoires présentée par Zhang n'est pas une convention RPE universelle.
- Les unités supposent des poses métriques ; conversion d'angle et intervalle doivent être spécifiés.
- Permutation d'IDs et diagnostic d'écart entre outils : déductions du projet, aucun score de benchmark calculé.

## Corrections appliquées

Fiche révisée et bibliographie complétée ; sources des cartes adaptées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Calculer l’effet d’un ID switch sur IDF1 | La distinction de métriques reste qualitative | raisonnement | 1 carte sur une courte séquence | Définition IDF1 et HOTA §4 |

Familles absentes : algorithme, comprehension, conception, pratique. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [HOTA, §4 équations 2/6, §5 agrégation](https://arxiv.org/abs/2009.07736).
- [Zhang–Scaramuzza, §III/tableau I, §IV/tableau II](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf).
- [Sturm et al., §VII-A/B équations 1–4](https://cvg.cit.tum.de/_media/spezial/bib/sturm12iros.pdf).
- [nuScenes, Metrics](https://github.com/nutonomy/nuscenes-devkit/blob/master/python-sdk/nuscenes/eval/detection/README.md), contrôlé dans la revue 84.

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
