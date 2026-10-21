# Revue — SO(3), SE(3) et conventions de transformation — 2026-10-18

## Synthèse

4 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 2 importante, 2 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

Auto-revue : Agent Codex (`revue-cartes`). Le statut éditorial reste `redige`.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SE3-001 | Confirmé : composition Eq.171 | composer avec des repères nommés. | Noyau fini ; 40 mots | Accord fiche et format | Important (source) | Source SE(3) |
| CV-SE3-002 | Confirmé : inverse Eq.170 | inverser une pose rigide. | Noyau fini ; 44 mots | Accord fiche et format | Important (source) | Source SE(3) |
| CV-SE3-003 | Confirmé sous convention local→global | distinguer perturbations locale et globale. | Noyau fini ; 48 mots | Accord fiche et format | Mineur | Sections II-E–II-H |
| CV-SE3-004 | Confirmé : quatre choix de convention | contrôler un quaternion. | Noyau fini ; 46 mots | Accord fiche et format | Mineur | Section 3.1 |

### Affirmations de la fiche et des cartes

Confirmés : orthogonalité, déterminant positif, composition et inverse ; perturbations droite/gauche dans la convention énoncée ; dépendance des Jacobiennes au repère ; conventions quaternion. Le centre caméra est déduit en posant son point image 3D dans le repère caméra à zéro. Les tests de points connus et de composition sont des propositions du projet.

## Corrections appliquées

Fiche révision 2 : préciser « orientation de la base ». Cartes 001–002 : remplacer la source sur les quaternions par les équations SE(3) appropriées ; 003–004 : cibler les passages. Questions, objectifs et identifiants conservés.

## Enrichissements proposés (en attente d’accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Transporter une covariance par l’adjoint | Éviter un mélange de repères d’incertitude | Raisonnement ; une carte | 3 critères ; durée à mesurer | Solà et al., §II-H |

## Sources

- [Solà et al., A micro Lie theory, annexe D-A, équations 170–171](https://arxiv.org/html/1812.01537v9#A4.SS1).
- [Solà et al., A micro Lie theory, §§II-E–II-H](https://arxiv.org/html/1812.01537v9#S2.SS5).
- [Solà, Quaternion kinematics, §3.1, équations 140–143](https://arxiv.org/pdf/1711.02508). Version HTML 1711.02508v6 inaccessible (404), PDF consulté.

## Contrôles et limites

Contrôles de référence : 52 fiches, 224 cartes, 34 tests réussis. Les contrôles après modification et la conservation des identifiants sont consignés dans le [bilan commun](../2026-10-20/00-bilan.md). Context7 indisponible : accès direct aux documentations officielles quand nécessaire.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l’apprenant et validation scientifique indépendante non vérifiés. Les scénarios et recommandations de diagnostic sont des raisonnements du projet, sauf résultat explicitement attribué. Les familles absentes ne justifient pas à elles seules de nouvelles cartes.
