# Revue — OCR et compréhension documentaire — 2026-10-20

## Synthèse

3 cartes auditées. 0 bloquant ; 1 important (variante du protocole cité).
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

3 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 1 importante, 0 mineure, 2 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-OCR-001 | Confirmé : sorties distinctes ; choix métier déduit | séparer reconnaissance et structure. | 49 mots à l’entrée ; un besoin d’évaluation | Fiche et format contrôlés | Aucune | Source ciblée |
| CV-OCR-002 | Confirmé pour CER classique ; divergence OCR-D explicitée | interpréter CER. | 51 mots à l’entrée ; conditions du score | Fiche et format contrôlés | Important | Convention précisée |
| CV-OCR-003 | Diagnostic déduit de la chaîne de traitement | localiser un défaut d’ordre de lecture. | 44 mots à l’entrée ; localisation d’un composant | Fiche et format contrôlés | Aucune | Conserver |

### Affirmations de la fiche et des cartes

CRNN : extraction/séquence/CTC ; TrOCR : encoder-decoder transformer ; LayoutLM : texte et positions ; Donut : génération structurée sans OCR séparé, confirmés au niveau de repérage par les textes primaires. OCR-D distingue plusieurs CER ; exemple propre : référence « a », prédiction « abc » donne 2/1=200 % avec la convention classique. En revanche, sa CER normalisée reste bornée. Les caractères et mots doivent être définis par protocole.

## Corrections appliquées

Fiche révision 2 ; distinction classique/normalisée et sources des trois cartes.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Agréger CER par micro/macro moyenne | Éviter de comparer des documents de longueurs différentes sans protocole | Évaluation | Une carte, un exemple ; durée à mesurer | OCR-D CER Granularity |

Familles absentes : algorithme, comprehension, conception, evaluation, pratique. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [OCR-D, Text Evaluation, CER and WER, consulté le 2026-10-20](https://ocr-d.de/en/spec/ocrd_eval.html) : sections Characters, Levenshtein, CER and WER lues.
- [CRNN §2](https://arxiv.org/abs/1507.05717), [TrOCR résumé](https://arxiv.org/abs/2109.10282), [LayoutLM résumé/§2](https://arxiv.org/abs/1912.13318), [Donut résumé et figure 1](https://arxiv.org/abs/2111.15664) : PDFs extraits.

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
