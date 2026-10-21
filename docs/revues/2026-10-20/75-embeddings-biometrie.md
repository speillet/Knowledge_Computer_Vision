# Revue — Reconnaissance biométrique, ArcFace et PAD — 2026-10-20

## Synthèse

2 cartes auditées. 0 bloquant ; 1 important (source PAD absente) ; 1 mineur.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

2 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 1 importante, 1 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-BIOMETRIE-001 | Confirmé : objectifs identité/PAD distincts | distinguer identité et présentation. | 45 mots à l’entrée ; un contraste évaluable | Fiche et format contrôlés | Important | Source PAD ajoutée |
| CV-BIOMETRIE-002 | Confirmé : FNMR mesurée à FMR fixé ; EER distinct par définition | choisir un point d’exploitation. | 47 mots à l’entrée ; un point d’exploitation | Fiche et format contrôlés | Mineur | Source datée |

### Affirmations de la fiche et des cartes

Marge angulaire d’ArcFace et erreurs de comparaison FRTE vérifiées ; PAD confronté au résumé primaire du NIST. L’EER n’est pas une mesure universelle à tous les seuils : déduction du protocole de courbe. La fiche reste au repérage ; FAR/FRR système et échecs d’acquisition exigent une spécification propre pour une étude détaillée. Aucune conformité ni certification évaluée.

## Corrections appliquées

Fiche révision 2 ; source PAD et champs Source corrigés.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Définir une évaluation 1:N avec galerie ouverte | Contrat d’identification seulement évoqué | Évaluation | Une carte, trois critères ; durée à mesurer | NIST FRTE 1:N |

Familles absentes : algorithme, comprehension, conception, diagnostic, pratique, raisonnement. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [Deng et al., ArcFace, objectif de marge angulaire](https://arxiv.org/abs/1801.07698) : PDF résumé et objectif.
- [NIST FRTE 1:1, définitions FMR/FNMR, consulté le 2026-10-20](https://pages.nist.gov/frvt/html/frvt11.html) : paragraphes Accuracy, seuil fixé.
- [Ngan et al. 2023, NISTIR 8491, résumé PAD](https://www.nist.gov/publications/face-analysis-technology-evaluation-fate-part-10-performance-passive-software-based)

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
