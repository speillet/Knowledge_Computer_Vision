# Revue — SAM, SAM 2 et segmentation guidée en vidéo — 2026-10-20

## Synthèse

3 cartes auditées. Noyaux confirmés ; sources et attribution du protocole précisées.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

3 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 3 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SAM-001 | Confirmé, référence précisée | définir la sortie SAM. | 51 mots à l’entrée ; Objectif conservé | Fiche et format contrôlés | mineur | Cibler source |
| CV-SAM-002 | Confirmé, référence précisée | situer SAM 2 en vidéo. | 47 mots à l’entrée ; Objectif conservé | Fiche et format contrôlés | mineur | Cibler source |
| CV-SAM-003 | Déduction de protocole explicite | contrôler le futur dans l’évaluation. | 42 mots à l’entrée ; Information disponible et budget finis | Fiche et format contrôlés | mineur | Attribuer au projet |

### Affirmations de la fiche et des cartes

- Confirmé : SAM fournit des masques conditionnés par prompts ; plusieurs masques peuvent représenter l'ambiguïté. §7.5 est explicitement une preuve de concept text-to-mask, distincte du modèle des expériences précédentes.
- Confirmé : SAM 2 §4 ajoute une mémoire et conditionne les frames courantes sur les mémoires/prompts pour produire des masklets ; une sortie par objet guidé ne définit pas un MOT autonome à taxonomie complète.
- Confirmé : encodage image réutilisable et décodeur conditionné dans SAM §3 ; aucun temps d'exécution n'est transféré aux machines du projet.
- L'objection à la comparaison offline/causale est une déduction sur l'information disponible, pas un résultat chiffré du papier.

## Corrections appliquées

Sources des trois cartes ciblées, fiche révisée.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Aucune addition prioritaire | Les objectifs existants suffisent au périmètre annoncé | — | Aucun rappel ajouté | Sources ci-dessous |

Familles absentes : algorithme, conception, diagnostic, pratique, raisonnement. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [SAM, §3, §7.5](https://arxiv.org/abs/2304.02643).
- [SAM 2 v2, §§3–4, Memory attention et memory bank](https://arxiv.org/abs/2408.00714).

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
