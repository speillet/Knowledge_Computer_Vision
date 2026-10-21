# Revue — Kalman, EKF, UKF et ESKF pour la fusion — 2026-10-18

## Synthèse

4 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 2 importante, 2 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

Auto-revue : Agent Codex (`revue-cartes`). Le statut éditorial reste `redige`.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FUSION-001 | EKF/ESKF confirmé et précisé ; UKF non vérifiable | distinguer variantes de filtre. | Noyau fini ; 77 mots | Accord fiche et format | Important | Recouvrement explicité, source UKF séparée |
| CV-FUSION-002 | Confirmé : NIS Eq.7 | interpréter une innovation normalisée. | Noyau fini ; 55 mots | Accord fiche et format | Important | Symboles et source ajoutés |
| CV-FUSION-003 | Confirmé : reset covariance Eq.286 | préserver la covariance ESKF. | Noyau fini ; 50 mots | Accord fiche et format | Mineur | Section précisée |
| CV-FUSION-004 | Confirmé : propagation en Δt ; diagnostic déduit | traiter temps et données manquantes. | Noyau fini ; 53 mots | Accord fiche et format | Mineur | Passages précisés |

### Affirmations de la fiche et des cartes

Confirmés : étapes ESKF, reset de covariance, propagation avec pas temporel ; covariance d’innovation et pondération. Imprécis corrigé : ESKF n’est pas exclusif d’EKF. Non vérifiable dans le texte primaire consultable : détail des sigma-points UKF. Les diagnostics délais/biais/corrélations sont des raisonnements du projet. La variation de R doit être comprise dans un modèle fixé, pas comme un ordre universel composante par composante.

## Corrections appliquées

Fiche révision 2, cartes 001–004 : sources ciblées ; 001 distingue les axes de comparaison ; 002 définit les symboles et corrige « dinnovation ». Aucun objectif ni ID changé.

## Enrichissements proposés (en attente d’accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Contrôler cohérence NIS et résidus biaisés | Évaluer une covariance, au-delà du faible résidu | Évaluation ; une carte | 3 critères ; durée à mesurer | Gamse et al., §§2.2.2 et 3.4 |

## Sources

- [Solà, §§5.2 et 6.1–6.3](https://arxiv.org/pdf/1711.02508) : état nominal/erreur, correction et reset. §5.4/annexe E : discrétisation.
- [Gamse et al. 2014, §2.2.2, équations 5–7](https://pmc.ncbi.nlm.nih.gov/articles/PMC4239867/) : innovation et score sans unité.
- [Julier et Uhlmann 2004, Unscented Filtering and Nonlinear Estimation (texte intégral à vérifier)](https://doi.org/10.1109/JPROC.2003.823141) : seul résumé disponible ; accès IEEE bloqué et copies PDF 1997/2004 indisponibles. Ne pas considérer le mécanisme UKF comme confirmé par Solà.

## Contrôles et limites

Contrôles de référence : 52 fiches, 224 cartes, 34 tests réussis. Les contrôles après modification et la conservation des identifiants sont consignés dans le [bilan commun](../2026-10-20/00-bilan.md). Context7 indisponible : accès direct aux documentations officielles quand nécessaire.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l’apprenant et validation scientifique indépendante non vérifiés. Les scénarios et recommandations de diagnostic sont des raisonnements du projet, sauf résultat explicitement attribué. Les familles absentes ne justifient pas à elles seules de nouvelles cartes.
