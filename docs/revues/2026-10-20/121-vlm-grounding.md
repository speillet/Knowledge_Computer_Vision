# Revue — VLM, grounding et frontière vision–action — 2026-10-20

## Synthèse

4 cartes auditées. Une imprécision importante de la fiche sur entraînement/décodage corrigée ; bibliographie complétée.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

4 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 4 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-VLM-001 | Confirmé, source ciblée | situer encodeur VLM et VLA. | 57 mots à l’entrée ; Objectif unique conservé | Fiche et format contrôlés | mineur | Préciser source |
| CV-VLM-002 | Confirmé, source ciblée | situer un connecteur visuel. | 57 mots à l’entrée ; Objectif unique conservé | Fiche et format contrôlés | mineur | Préciser source |
| CV-VLM-003 | Déduction du projet explicite | concevoir un index vidéo. | 85 mots à l’entrée ; Protocole fini, sans promesse de résultat | Fiche et format contrôlés | mineur | Attribuer le cas |
| CV-VLM-004 | Déduction du projet explicite | départager hallucination et observation insuffisante. | 93 mots à l’entrée ; Protocole fini, sans promesse de résultat | Fiche et format contrôlés | mineur | Attribuer le cas |

### Affirmations de la fiche et des cartes

- Confirmé : BLIP-2 §3.1 relie encodeur et LLM gelés via un Q-Former produisant un nombre fixe de features ; LLaVA original utilise une projection et un instruction tuning (§4) ; Flamingo §2 accepte images/vidéos entrelacées avec texte.
- Corrigé dans la fiche : l'objectif d'entraînement sur tokens n'est pas identique au décodage, qui peut rechercher ou échantillonner une sortie.
- Confirmé : OpenVLA prédit des actions tokenisées décodées en actions continues. RT-2 et π0 sont seulement situés comme interfaces d'action ; sources de leurs résumés ajoutées. Aucun protocole robotique n'est validé ici.
- Florence-2 : caractère multitâche confirmé dans le résumé ; fonctionnement détaillé hors périmètre.
- Les deux cas d'indexation/hallucination proposent une enquête expérimentale ; ils ne démontrent pas une correction universelle par prompt.

## Corrections appliquées

Fiche révisée, comparaison 001 contextualisée et sources des quatre cartes ciblées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Aucune addition prioritaire | Les objectifs existants suffisent au périmètre annoncé | — | Aucun rappel ajouté | Sources ci-dessous |

Familles absentes : algorithme, evaluation, pratique, raisonnement. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [BLIP-2, §§3.1–3.3](https://arxiv.org/abs/2301.12597).
- [LLaVA original, §§4.1–4.2](https://arxiv.org/abs/2304.08485).
- [Flamingo, introduction et §2.2](https://arxiv.org/abs/2204.14198).
- [OpenVLA, architecture](https://openvla.github.io/), consultée le 20 octobre 2026.
- [Florence-2, résumé](https://arxiv.org/abs/2311.06242) ; [RT-2, résumé/fig. 1](https://arxiv.org/abs/2307.15818) ; [π0, résumé](https://arxiv.org/abs/2410.24164).
- [CLIP, §2.3](https://arxiv.org/abs/2103.00020), passage contrôlé dans la revue 72.

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
