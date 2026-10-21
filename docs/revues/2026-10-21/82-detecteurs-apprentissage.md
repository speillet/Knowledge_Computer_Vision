# Revue — Détecteurs : apprentissage et FPN — 2026-10-21

## Synthèse

Cinq nouvelles cartes auditées et ajoutées après accord explicite de l'apprenant :
CV-DETECTEURS-006 à 010. Aucun défaut bloquant, important ou mineur restant relevé
sur ces ajouts. La fiche passe de la révision 2 à 3, statut `redige` conservé.
Les cinq cartes antérieures sont inchangées ; leur audit reste dans le
[rapport précédent](../2026-10-20/82-detection-fasterrcnn-yolo-detr.md).

La conclusion antérieure « Aucune addition prioritaire » était trop limitée
pour l'objectif senior : assignation, cibles, losses et fusion multiéchelle
méritent un rappel propre. Cette nouvelle décision complète le rapport daté
sans le réécrire. Les deux cartes de diagnostic également acceptées seront
traitées dans le passage suivant. Aucune affirmation d'exhaustivité.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-DETECTEURS-006 | Confirmé : FCOS §§3.1–3.2 | Reconstruire l'assignation sans anchors | 105 mots au verso ; admissibilité, arbitrage et cible ; détails de variante facultatifs | Plages de distances, pas seulement aire ; version précisée | Aucun défaut restant relevé | Ajouter |
| CV-DETECTEURS-007 | Équation 1 confirmée ; calcul refait | Appliquer un encodage de boîte | 84 mots ; quatre valeurs attendues, décodage facultatif | Coordonnées continues et pixels d'entrée explicites | Aucun défaut restant relevé | Ajouter |
| CV-DETECTEURS-008 | Équation 5 et rôle des paramètres confirmés | Expliquer le déséquilibre en détection dense | 117 mots ; facteur et effet suffisent, formule complète facultative | Probabilité du label correct, y compris pour un négatif | Aucun défaut restant relevé | Ajouter |
| CV-DETECTEURS-009 | Plateau IoU et pénalité confirmés ; calcul refait | Relier géométrie et signal de régression | 131 mots ; mécanisme au noyau, exemple numérique facultatif | Rectangle englobant aligné sur les axes ; aucune garantie universelle | Aucun défaut restant relevé | Ajouter |
| CV-DETECTEURS-010 | §3 et figure 3 confirmés | Comprendre les features utiles aux petits objets | 103 mots ; deux apports à distinguer, détails de convolutions facultatifs | Ne confond pas pyramide de features et d'images | Aucun défaut restant relevé | Ajouter |

Les versos sont plus développés que les 40 à 82 mots des cartes précédentes.
Le calcul de GIoU reste dans l'approfondissement : il n'est pas requis pour
réussir le rappel du mécanisme. Charge et durée de révision non mesurées.
La famille conception reste absente : aucune carte artificielle ajoutée
pour remplir cette catégorie.

## Corrections appliquées

- [Fiche](../../../vault/80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md) : assignation FCOS, convention de coordonnées, Focal Loss, GIoU et FPN développés avant l'écriture des cartes. Les cas numériques sont attribués au projet.
- [Cartes](../../../vault/80-detection-pose/82-detection-fasterrcnn-yolo-detr.md) : cinq objectifs nouveaux, IDs 006 à 010, aucun identifiant de synchronisation inventé.
- Comptes courants, index et navigation par pôles recalculés : 52 fiches, 229 cartes. Journal : une ligne par ajout accepté, export « Non synchronisé ».
- Recherche transversale FCOS/Focal/GIoU/FPN/anchor-free dans le vault : aucun noyau contradictoire ou doublon de ces cinq objectifs repéré.

## Enrichissements proposés (en attente d'accord)

Aucune nouvelle proposition en attente d'accord. Les sept cartes proposées
ont été acceptées ; cette livraison réalise les cinq cartes sur l'apprentissage.
La décomposition des erreurs, les annotations et le cas des petits objets
restent à réaliser dans le second passage déjà autorisé.

## Sources

Passages primaires réellement consultés le 2026-10-21 :

- [FCOS v5, §§3.1–3.3](https://arxiv.org/html/1904.01355v5) : équation 1, choix de la boîte de plus petite aire après filtrage du niveau, distinction avec les variantes de center sampling.
- [Focal Loss v2, §2 et §§3.1–3.2](https://arxiv.org/html/1708.02002v2) : difficulté contre pondération de classe, équations 3–5 ; ce n'est pas une loss robuste aux cas aberrants.
- [GIoU v2, §3.1 et algorithmes 1–2](https://arxiv.org/html/1902.09630v2) : enveloppe rectangulaire, plateau sans recouvrement. La carte n'étend pas la propriété à une garantie de convergence.
- [FPN v2, §3 et figure 3](https://arxiv.org/html/1612.03144v2) : apport sémantique descendant et localisation latérale.

Les articles ont été consultés sur arXiv en versions épinglées ; aucun passage
central inaccessible. Aucune API de bibliothèque introduite ni exécutée.
Les exemples chiffrés sont des dérivations synthétiques, pas des mesures publiées.

## Contrôles et limites

- `python3 scripts/check_vault.py` : OK, 125 Markdown, 52 fiches et 229 cartes.
- `python3 -m unittest discover -s tests` : 34 tests réussis.
- `python3 scripts/sync_catalog.py --check` : 18 documents à jour.
- Inventaire complet comparé à celui d'avant enrichissement : cinq ajouts attendus, aucun ID disparu ni identité Anki modifiée ; objectifs et tags des 224 cartes conservés. Le comparateur signale les ajouts, qui sont attendus.
- Calculs Python temporaires avec fractions exactes : distances (20,20,50,40), décodage exact ; facteurs 1/100 et 81/100 ; losses GIoU 6/5 puis 10/9. Aucun réseau exécuté.
- Diff, liens locaux, caractères de contrôle et conservation des sections de preuves datées vérifiés. Les occurrences de 224 restantes décrivent l'historique ou la référence de comparaison.

Auto-revue par Agent Codex (`revue-cartes`). Export Anki réel, rendu
Obsidian/AnkiDroid, validation scientifique indépendante et maîtrise de
l'apprenant restent non vérifiés. Les anciens essais de parseur ne constituent
pas une validation d'export des nouvelles cartes.
