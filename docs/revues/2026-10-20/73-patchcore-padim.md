# Revue — Inspection : golden template, PatchCore et PaDiM — 2026-10-20

## Synthèse

4 cartes auditées. 0 bloquant, 0 important ; 1 mineur partagé d’attribution.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

4 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 0 mineure, 4 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ANOMALIES-001 | Confirmé pour méthodes ; template défini par le projet | choisir modèle de nominal. | 49 mots à l’entrée ; comparaison cohérente | Fiche et format contrôlés | Aucune | Conserver le noyau |
| CV-ANOMALIES-002 | Confirmé : coreset et couverture/coût | expliquer le coreset. | 50 mots à l’entrée ; un mécanisme | Fiche et format contrôlés | Aucune | Conserver le noyau |
| CV-ANOMALIES-003 | Diagnostic conditionnel | détecter une dérive du nominal. | 48 mots à l’entrée ; causes et contrôle indépendant | Fiche et format contrôlés | Aucune | Conserver le noyau |
| CV-ANOMALIES-004 | Cas construit ; métriques métier pertinentes | concevoir une inspection à défauts rares. | 83 mots à l’entrée ; conception cohérente ; charge à mesurer | Fiche et format contrôlés | Aucune | Conserver le noyau |

### Affirmations de la fiche et des cartes

Banque de patches, coreset glouton et repondération du maximum confirmés. PaDiM : covariance par position, régularisation epsilon I, distance de Mahalanobis ; formule et rôle distincts des probabilités. Les effets d’acquisition et les splits par lots sont des choix de validation, pas des garanties publiées. Pas de confusion score patch/score image dans la fiche.

## Corrections appliquées

Fiche révision 2 ; attribution du template et sources des cas.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Tester la contamination de la banque nominale | Défaut présent à l’apprentissage pouvant devenir normal | Diagnostic | Une carte, deux contrôles ; durée à mesurer | PatchCore §3.1–3.3 |

Familles absentes : algorithme, comprehension, evaluation, pratique. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [Roth et al., PatchCore, §§3.1–3.3](https://arxiv.org/abs/2106.08265)
- [Defard et al., PaDiM, §III, équations 1–2](https://arxiv.org/abs/2011.08785)

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
