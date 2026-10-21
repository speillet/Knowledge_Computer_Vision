# Revue — Capteurs, rolling shutter et synchronisation — 2026-10-18

## Synthèse

4 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 3 importante, 1 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

Auto-revue : Agent Codex (`revue-cartes`). Le statut éditorial reste `redige`.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CAPTEURS-001 | Confirmé : instants par ligne | séparer exposition et lecture rolling shutter. | Noyau fini ; 47 mots | Accord fiche et format | Mineur | Version Basler explicitée |
| CV-CAPTEURS-002 | Confirmé par calcul : 0,10 m | estimer un décalage temporel spatial. | Noyau fini ; 42 mots | Accord fiche et format | Important (attribution) | Calcul du projet |
| CV-CAPTEURS-003 | Diagnostic conditionnel ; deskew corroboré | départager calibration et temps. | Noyau fini ; 87 mots | Accord fiche et format | Important (source) | Source LOAM |
| CV-CAPTEURS-004 | Confirmé : vitesse radiale relative | interpréter les sorties de capteurs. | Noyau fini ; 49 mots | Accord fiche et format | Important (source) | Source radar dédiée |

### Affirmations de la fiche et des cartes

Confirmés : rolling shutter ≠ durée d’exposition ; vitesse radiale distincte du vecteur 3D ; mouvement pendant un scan. Calcul exécuté : 2×0,050=0,10 m. Le diagnostic extrinsèques/temps et la transformation des covariances sont des déductions du modèle de mesure, sans benchmark de capteurs.

## Corrections appliquées

Fiche révision 2 ; sources ciblées des quatre cartes ; aucune modification des objectifs ou des IDs.

## Enrichissements proposés (en attente d’accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Construire un budget d’erreur temporelle | Lier précision visée, vitesse et dérive des horloges | Conception ; une carte | 3 critères ; durée à mesurer | LOAM §§III–V, Basler shutter ; calcul du projet |

## Sources

- [Basler, Electronic Shutter Types, Rolling Shutter (v136, 2026-10-01)](https://docs.baslerweb.com/electronic-shutter-types#rolling-shutter).
- [Zhang et Singh 2014, LOAM, §§II et V, correction de distorsion de mouvement](https://www.roboticsproceedings.org/rss10/p07.pdf) : distorsion des scans et compensation par le mouvement ; lecture du PDF.
- [Texas Instruments, TIDUF01 (2021), §2.4.9](https://www.ti.com/lit/ug/tiduf01/tiduf01.pdf) : vitesse radiale et mouvement ego.
- [Forster, préintégration](https://dellaert.github.io/files/Forster16tro.pdf) ouvert ; ne justifie pas les affirmations radar.

## Contrôles et limites

Contrôles de référence : 52 fiches, 224 cartes, 34 tests réussis. Les contrôles après modification et la conservation des identifiants sont consignés dans le [bilan commun](../2026-10-20/00-bilan.md). Context7 indisponible : accès direct aux documentations officielles quand nécessaire.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l’apprenant et validation scientifique indépendante non vérifiés. Les scénarios et recommandations de diagnostic sont des raisonnements du projet, sauf résultat explicitement attribué. Les familles absentes ne justifient pas à elles seules de nouvelles cartes.

La carte 003 comporte 85 mots et cinq critères de cas en plus du noyau : sa charge réelle reste à mesurer ; ces critères servent le même diagnostic, sans nécessiter de nouvelle carte.
