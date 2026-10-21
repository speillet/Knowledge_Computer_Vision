# Revue — GrabCut, régions et modèles d’apparence — 2026-10-20

## Synthèse

3 cartes auditées. Aucun défaut nécessitant correction. Trois objectifs distincts et corrigibles.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

3 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 0 mineure, 3 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-GRABCUT-001 | Confirmé | expliquer l’alternance GrabCut. | 51 mots à l’entrée ; Noyau fini et autonome | Fiche et format contrôlés | — | Conserver |
| CV-GRABCUT-002 | Raisonnement explicite du projet | contrôler une contrainte d’initialisation. | 50 mots à l’entrée ; Vérifications finies, sans promesse de résultat | Fiche et format contrôlés | — | Conserver |
| CV-GRABCUT-003 | Raisonnement explicite du projet | choisir une interaction. | 52 mots à l’entrée ; Vérifications finies, sans promesse de résultat | Fiche et format contrôlés | — | Conserver |

### Affirmations de la fiche et des cartes

- Confirmé : modèles GMM fond/objet, alternance estimation et coupe de graphe ; l'énergie de la fiche est expressément schématique, pas la transcription complète de l'article.
- Confirmé : l'extérieur du rectangle est du fond sûr et les contraintes certaines ne sont pas révoquées par une simple itération. Les labels probables ont un autre rôle.
- Déduction : des couleurs ambiguës peuvent nécessiter une intervention ; le coût d'annotation et la qualité doivent compléter le temps d'optimisation. Cette proposition n'est pas un benchmark.
- Region growing et contours actifs sont seulement cités comme alternatives ; aucun fonctionnement détaillé ni comparaison quantitative à valider.

## Corrections appliquées

Aucune correction nécessaire.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Aucune addition prioritaire | Les objectifs existants suffisent au périmètre annoncé | — | Aucun rappel ajouté | Sources ci-dessous |

Familles absentes : comprehension, conception, evaluation, pratique, raisonnement. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [OpenCV 4.13.0, GrabCut, Theory (hard-labelling, GMM, mincut) et Demo (labels)](https://docs.opencv.org/4.13.0/d8/d83/tutorial_py_grabcut.html).

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API. L'article original n'a pas été confronté intégralement ; le niveau d'affirmation contrôlé correspond au tutoriel officiel et à l'énergie explicitement schématique.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
