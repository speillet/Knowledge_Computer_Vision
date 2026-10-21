# Revue — Détecteurs : diagnostic et petits objets — 2026-10-21

## Synthèse

Trois cartes auditées : deux ajouts acceptés (CV-DETECTEURS-011 et 012) et
l'enrichissement de CV-DETECTEURS-004. Un constat mineur de cas trop abstrait
traité ; aucun défaut bloquant ou important relevé. Objectif, ID et tags de
004 conservés. Fiche en révision 4, statut `redige`.

Ce passage termine les sept ajouts approuvés, après les cinq cartes du
[premier passage](82-detecteurs-apprentissage.md). Le sujet comporte 12 cartes,
le vault 231. La fiche décrit aussi une expérience contrôlée sur la résolution,
explicitement non exécutée. Aucune couverture exhaustive de la détection
ni validation indépendante annoncée.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-DETECTEURS-004 | Géométrie recalculée ; mécanisme de suppression confirmé dans Soft-NMS §4 | Objectif de diagnostic après resize conservé | 82 mots avant, 180 après ; trois contrôles au noyau, valeurs et cas NMS en approfondissement | Repère, ratio, padding et étapes explicites ; aucune généralisation causale | Mineur : cas initial abstrait | Préciser scénario et vérifications |
| CV-DETECTEURS-011 | Trois catégories confirmées par TIDE §2.2 | Départager des FP qui appellent des contrôles différents | 100 mots ; trois cas indépendants, une GT chacun, aucun cas frontière | Seuils donnés, ignore/crowd exclus ; six familles développées dans la fiche | Aucun défaut relevé | Ajouter |
| CV-DETECTEURS-012 | Omission et ambiguïtés documentées par TIDE §3.4 et annexes D–E | Éviter d'attribuer toute erreur au modèle | 124 mots ; vérifier politique et image puis conclure conditionnellement | Score élevé distinct d'une preuve ; protocole de correction attribué au projet | Aucun défaut relevé | Ajouter |

004 a le verso le plus long du sujet ; les calculs restent facultatifs pour
réussir le rappel du diagnostic. La charge réelle est à observer avec
l'apprenant, sans imposer un plafond arbitraire. Les neuf autres cartes du
sujet sont inchangées et ne font pas l'objet d'une nouvelle auto-revue ici.

## Corrections appliquées

- [Fiche](../../../vault/80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md) enrichie avant les cartes : six familles TIDE, effets des scores et limites des oracles ; annotations manquantes, ambiguës ou ignorées ; cas resize/padding/NMS ; expérience à facteur contrôlé avec baseline, prédiction, mesures et limites.
- [Cartes](../../../vault/80-detection-pose/82-detection-fasterrcnn-yolo-detr.md) : ajouter 011–012 et préciser 004 sans changer son objectif. Aucune identité de synchronisation inventée.
- Les pistes de diagnostic, le protocole de correction des annotations et l'expérience proposée sont des décisions du projet, séparées des résultats des articles.
- Comptes et navigation mis à jour : 52 fiches et 231 cartes. Journal : deux ajouts, un cas enrichi et un protocole, chacun tracé ; preuves datées préservées.
- Cohérence vérifiée avec les fiches NMS et IoU/AP : seuil de score, seuil NMS et seuil d'évaluation distincts ; matching et règles crowd/ignore du protocole conservés. Le tableau TIDE ne remplace pas l'évaluateur COCO.

## Enrichissements proposés (en attente d'accord)

Aucune proposition supplémentaire en attente. Les sept cartes acceptées,
le cas des petits objets et le protocole de mise en pratique sont rédigés.
L'exécution de ce protocole sur un checkpoint et des images annotées reste
une activité d'apprentissage à réaliser, sans résultat fabriqué.

## Sources

Passages réellement consultés le 2026-10-21 :

- [TIDE v2, §2.2](https://arxiv.org/html/2008.08115v2) : six catégories, seuils, doublons et importance du rang par score.
- Même article, §2.3 et annexe A.1 : oracles depuis la même baseline et non-additivité générale ; ces interventions idéalisées ne garantissent pas l'effet d'une modification de modèle.
- Même article, §3.4 et annexes D–E : erreurs et ambiguïtés d'annotations, flags crowd, effet des détections ignorées sur le diagnostic. Les pourcentages de leur étude ne sont pas généralisés au jeu du projet.
- [Soft-NMS, §4](https://arxiv.org/html/1704.04503) : une boîte mieux localisée peut être supprimée par une boîte mieux scorée ; les calculs du cas sont ceux du projet. Les égalités aux seuils sont évitées, conformément à la distinction documentée dans la fiche NMS.
- [FPN v2, §3](https://arxiv.org/html/1612.03144v2), consulté au premier passage du même jour : rôles des features fines et profondes, sans garantie de rappel.

Aucun passage central inaccessible. Aucune nouvelle API de bibliothèque ni
exécution de TIDE introduite ; il s'agit des mécanismes décrits dans les articles.

## Contrôles et limites

- `python3 scripts/check_vault.py` : OK, 125 Markdown, 52 fiches et 231 cartes.
- `python3 -m unittest discover -s tests` : 34 tests réussis.
- `python3 scripts/sync_catalog.py --check` : 18 documents à jour.
- Inventaire comparé avant/après ce passage : seuls 011 et 012 ajoutés. Comparaison globale à la référence de 224 cartes : sept ajouts acceptés, aucun ID supprimé ni identité Anki modifiée ; objectifs et tags existants conservés.
- Calculs avec fractions exactes en Python temporaire : facteur 1/3, padding 140, boîte transformée (300,290,304,293), aller-retour exact, taille 4×3. IoU(P,Q) = IoU(Q,G) = 5/11, supérieur à 0,4 et inférieur à 0,5 ; rappel 1→0 dans le seul cas construit.
- Diff complet, liens locaux, tableaux, caractères de contrôle et comptes vérifiés ; sections de preuves antérieures, y compris celles du premier passage, conservées. Les anciens totaux qui subsistent sont historiques ou servent de référence de comparaison.

Auto-revue par Agent Codex (`revue-cartes`). Export Anki réel, rendu
Obsidian/AnkiDroid, entraînement ou benchmark, maîtrise, charge de rappel
et validation scientifique indépendante non réalisés. Les calculs analytiques
ne valent pas une expérimentation sur images.
