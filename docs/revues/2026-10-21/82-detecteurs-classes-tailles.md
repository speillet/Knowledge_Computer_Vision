# Revue — Détecteurs : instances, classes et tailles — 2026-10-21

## Synthèse

Une nouvelle carte auditée et ajoutée, CV-DETECTEURS-013, pour répondre à la
demande de cas de détections multiples et de multiclasse. Aucun défaut bloquant,
important ou mineur relevé sur cet ajout. Fiche révision 5 : contrat de sortie
et exemples de tailles/rapports d'aspect développés. Les douze cartes
antérieures sont inchangées ; leurs audits restent dans les rapports
[d'apprentissage](82-detecteurs-apprentissage.md) et de
[diagnostic](82-detecteurs-diagnostic.md), ainsi que le
[rapport initial](../2026-10-20/82-detection-fasterrcnn-yolo-detr.md).

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-DETECTEURS-013 | Distinction multi-étiquette confirmée par YOLOv3 §2.2 ; cas d'instances construit ; portée NMS confirmée | Séparer nombre d'objets, catégories et labels par objet | 129 mots ; cinq instances, deux classes et un label par instance dans le cas donné | Ne généralise pas YOLOv3 à toute la famille ; annotation et posttraitement explicites | Aucun défaut relevé | Ajouter |

Les choix de supervision et de sortie ne se déduisent pas du seul nombre de
classes présentes dans l'image. Le noyau est limité à cette distinction ;
les détails de tête et de NMS sont des approfondissements.

## Corrections appliquées

[Fiche](../../../vault/80-detection-pose/references/82-detection-fasterrcnn-yolo-detr.md)
complétée avant la [carte](../../../vault/80-detection-pose/82-detection-fasterrcnn-yolo-detr.md) :
plusieurs instances de même classe, plusieurs classes par image, labels
multiples ou exclusifs par instance ; renvois vers les scénarios NMS.

La rubrique géométrique calcule l'effet d'une erreur de deux pixels sur des
boîtes 4×4, 40×40 et 40×4, selon l'axe du déplacement. Elle distingue taille,
rapport d'aspect et changement commun d'échelle. Ce calcul développe le
rappel de diagnostic déjà présent dans CV-IOU-AP-006 ; aucune nouvelle carte
redondante sur ce dernier objectif n'est ajoutée.

Fiche NMS et carte NMS-006 traitent l'autre cas de tailles différentes :
inclusion sans forte IoU. Les deux fiches se renvoient l'une à l'autre. Comptes
courants : 52 fiches, 233 cartes, dont six NMS et treize détecteurs ; journal
et navigation recalculés. Aucun identifiant Anki inventé.

## Enrichissements proposés (en attente d'accord)

Aucune proposition supplémentaire en attente. Le complément demandé est rédigé.
Les scénarios ne prétendent pas couvrir toutes les architectures ou politiques
d'annotation. Leur interprétation empirique reste à éprouver sur des images.

## Sources

Passages réellement consultés le 2026-10-21 :

- [YOLOv3 v1, §§2.1–2.3](https://arxiv.org/html/1804.02767v1) : régression des dimensions, classification logistique indépendante et prédictions à plusieurs échelles. Les exemples voiture/vélo et véhicule/voiture sont ceux du projet.
- [GIoU v2, §3, équation 1 et propriété d'échelle](https://arxiv.org/html/1902.09630v2) : point de départ des calculs synthétiques. Translation fixée en pixels et redimensionnement commun des deux boîtes sont distingués.
- [Torchvision 0.29, batched_nms, description](https://docs.pytorch.org/vision/0.29/generated/torchvision.ops.batched_nms.html) : séparation des catégories, sans exclusivité des labels ni contrainte d'une boîte par classe. Context7 indisponible ; documentation officielle consultée directement.

Recherche transversale dans détection et IoU/AP : les objectifs de format de
boîte, de doublon d'évaluation et de sensibilité à la localisation sont déjà
présents et restent distincts. Aucune contradiction repérée. Aucun passage
central inaccessible ; aucun appel de bibliothèque ni réseau exécuté.

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
