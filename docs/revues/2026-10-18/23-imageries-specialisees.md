# Revue — Line-scan, télédétection et volumes médicaux — 2026-10-18

## Synthèse

3 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 1 importante, 2 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

Auto-revue : Agent Codex (`revue-cartes`). Le statut éditorial reste `redige`.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-IMAGERIES-001 | Confirmé : distances physiques et axes | propager les unités d’un volume. | Noyau fini ; 58 mots | Accord fiche et format | Mineur | Source DICOM ciblée |
| CV-IMAGERIES-002 | Confirmé : trigger par déplacement | contrôler une acquisition line-scan. | Noyau fini ; 48 mots | Accord fiche et format | Important | Source line-scan ajoutée |
| CV-IMAGERIES-003 | Risque déduit ; pas une garantie universelle | éviter une fuite géographique. | Noyau fini ; 46 mots | Accord fiche et format | Mineur | Attribution et URL corrigées |

### Affirmations de la fiche et des cartes

Confirmés : métadonnées physiques DICOM/NIfTI ; dépendance de l’échelle line-scan au déplacement ; télécentricité sur sa plage d’usage. Déductions du projet : risque de fuite géographique, choix des splits, tests de raccord et absence de garantie clinique. HD95 n’est pas défini par DICOM : la carte vérifie uniquement son contrat d’unités, pas toutes ses variantes.

## Corrections appliquées

Fiche révision 2 ; références des cartes remplacées selon leur objet. Les domaines spécialisés restent au niveau repérage.

## Enrichissements proposés (en attente d’accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Distinguer espacement des coupes et épaisseur | Éviter une distance 3D fausse malgré des métadonnées présentes | Pratique ; une carte | 2 critères et un contre-exemple ; durée à mesurer | DICOM C.7-10 |

## Sources

- [DICOM PS3.3, C.7.6.2.1.1, orientation/position et espacement (consulté le 2026-10-18)](https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.6.2.html) : table C.7-10 et équation de coordonnées.
- [NIfTI-1.1, innovations du format](https://nifti.nimh.nih.gov/nifti-1/) : indices vers position par affine.
- [Basler, GigE Line Scan Use Cases, Use Case 1 b (v136, 2026-10-01)](https://docs.baslerweb.com/line-scan-gige-use-cases).
- [SpaceNet7, The Problem et The Data (consulté le 2026-10-18)](https://www.spacenet.ai/sn7-challenge/) : description des séries temporelles ; ancienne URL 404.
- [Edmund Optics, The Advantages of Telecentricity](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/advantages-of-telecentricity/) : grandissement et distance.

## Contrôles et limites

Contrôles de référence : 52 fiches, 224 cartes, 34 tests réussis. Les contrôles après modification et la conservation des identifiants sont consignés dans le [bilan commun](../2026-10-20/00-bilan.md). Context7 indisponible : accès direct aux documentations officielles quand nécessaire.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l’apprenant et validation scientifique indépendante non vérifiés. Les scénarios et recommandations de diagnostic sont des raisonnements du projet, sauf résultat explicitement attribué. Les familles absentes ne justifient pas à elles seules de nouvelles cartes.
