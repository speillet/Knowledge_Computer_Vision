# Revue — NMS : instances, classes et inclusion — 2026-10-21

## Synthèse

Trois cartes auditées : NMS-003 et NMS-005 enrichies, NMS-006 ajoutée pour
répondre à la demande explicite de cas multiples, multiclasses et de tailles
différentes. Deux constats mineurs d'illustration traités ; aucun défaut
bloquant ou important relevé. Fiche révision 4 ; IDs et objectifs existants
conservés. Les autres cartes NMS restent inchangées, avec leur
[audit antérieur](../2026-10-20/81-nms.md).

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-NMS-003 | Séparation par catégorie confirmée dans Torchvision 0.29 ; sorties déduites des seuils | Choisir le périmètre de suppression | 101 → 136 mots ; sorties finies puis compromis sous contrat | Classes exclusives et objets distincts séparés ; plusieurs instances restent possibles | Mineur : comparaison abstraite | Ajouter IoU, scores et contre-exemples |
| CV-NMS-005 | Perte de voisine documentée par Soft-NMS ; effet sur rappel conditionné à la couverture GT | Localiser une disparition | 110 → 139 mots ; contrôle avant/après inchangé dans son objectif | Même classe ne signifie pas même instance ; doublon supprimé distinct d'une GT perdue | Mineur : cas de même classe implicite | Préciser deux personnes et couverture par GT |
| CV-NMS-006 | Définition IoU confirmée ; résultat 0,04 recalculé | Éviter la fausse règle « inclusion ⇒ suppression » | 98 mots ; une décision justifiée par intersection/union | Coordonnées continues, scores et classe explicites | Aucun défaut relevé | Ajouter |

Les versos des cartes 003 et 005 sont plus longs ; les exemples supplémentaires
sont dans l'approfondissement. La durée réelle de rappel reste à observer.

## Corrections appliquées

[Fiche NMS](../../../vault/80-detection-pose/references/81-nms.md) complétée
avant les [cartes](../../../vault/80-detection-pose/81-nms.md) : tableau de cinq
situations, différence globale/par classe, exemple d'inclusion 100×100/20×20,
distinction IoU et intersection divisée par la petite aire. Le résultat ne
présume pas l'identité des objets à partir de leurs boîtes.

Documentation `batched_nms` épinglée à 0.29 avec date de consultation ; ancienne
date de consultation de `nms` conservée séparément. Journal : une ligne par
carte affectée. Comptes et navigation mis à jour avec le passage suivant sur
[classes et tailles](82-detecteurs-classes-tailles.md).

## Enrichissements proposés (en attente d'accord)

Aucune proposition supplémentaire en attente. Les cas explicitement demandés
sont implémentés, avec une nouvelle carte ciblée sur l'inclusion et deux
objectifs existants précisés. Pas de multiplication de cartes pour remplir
les familles absentes.

## Sources

Passages réellement consultés le 2026-10-21 :

- [Soft-NMS, §§1, 3 et 4](https://arxiv.org/html/1704.04503) : suppression de vrais voisins, traitement par classe, score et recouvrement. Aucun gain de performance de l'article n'est attribué aux cas du projet.
- [Torchvision 0.29, batched_nms, description et paramètres](https://docs.pytorch.org/vision/0.29/generated/torchvision.ops.batched_nms.html) : absence de suppression entre catégories différentes et seuil strict. Context7 indisponible dans cette session ; recours direct à la documentation officielle, sans exécution de l'API.
- [GIoU v2, §3, équation 1](https://arxiv.org/html/1902.09630v2) : définition d'IoU dont le rapport d'aires en inclusion est une dérivation du projet.

Aucune source centrale inaccessible. Les identités d'objets et politiques de
labels des scénarios sont des hypothèses explicites, pas des observations.

## Contrôles et limites

Contrôles communs aux deux passages de ce complément :

- `python3 scripts/check_vault.py` : OK, 125 Markdown, 52 fiches, 233 cartes.
- `python3 -m unittest discover -s tests` : 34 tests réussis.
- `python3 scripts/sync_catalog.py --check` : 18 documents à jour.
- Inventaire comparé aux 231 cartes initiales : seuls CV-NMS-006 et CV-DETECTEURS-013 sont ajoutés ; aucun ID disparu, objectif ni identité Anki existant modifié. Les cartes antérieures sont intactes sauf NMS-003 et NMS-005, enrichies sous leurs objectifs initiaux.
- Calculs temporaires en Python, fractions exactes : inclusion 1/25 ; translations 1/3, 19/21, 19/21, 1/3. Aucun réseau ni appel Torchvision exécuté.
- Comptes courants, liens locaux et ancres ajoutées, tableaux, caractères de contrôle et diff vérifiés. Preuves datées conservées. Les anciens totaux restants sont historiques ou des références de comparaison.

Auto-revue par Agent Codex (`revue-cartes`) ; statut `redige`. Export réel,
rendu Obsidian/AnkiDroid, benchmark, validation scientifique indépendante,
maîtrise et charge de rappel non vérifiés. Les scénarios et recommandations
de diagnostic sont des raisonnements du projet.
