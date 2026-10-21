# Revue — Cartes pilotes — ORB — 2026-10-18

## Synthèse

6 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 1 mineure, 5 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

Auto-revue : Agent Codex (`revue-cartes`). Le statut éditorial reste `redige`.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ORB-001 | Confirmé : FAST/Harris/centroïde/rBRIEF | reconstruire le mécanisme d'ORB. | Noyau fini ; 97 mots | Accord fiche et format | Aucune | Conserver |
| CV-ORB-002 | Confirmé par définition et exemple binaire | relier représentation et distance. | Noyau fini ; 106 mots | Accord fiche et format | Aucune | Conserver |
| CV-ORB-003 | Confirmé : WTA_K et defaultNorm | choisir la norme après changement de variante. | Noyau fini ; 103 mots | Accord fiche et format | Aucune | Conserver |
| CV-ORB-004 | Confirmé : réciprocité vs ratio | distinguer deux filtres de correspondances. | Noyau fini ; 96 mots | Accord fiche et format | Aucune | Conserver |
| CV-ORB-005 | Confirmé : limites de couverture en échelle | diagnostiquer une perte de répétabilité. | Noyau fini ; 104 mots | Accord fiche et format | Aucune | Conserver |
| CV-ORB-006 | Conception explicitement proposée | articuler contrainte de calcul et réussite de tâche. | Noyau fini ; 111 mots | Accord fiche et format | Mineur | Passages applicatifs ajoutés |

### Affirmations de la fiche et des cartes

Confirmés : score Harris de sélection, moments centrés, tests orientés, choix hors ligne, 256 bits, couverture discrète d’échelle ; normes selon WTA_K et réciprocité. Exemple recalculé : un bit changé, écart numérique 128. Les diagnostics et la baseline embarquée sont des propositions, pas des performances publiées. Extraits API non exécutés.

## Corrections appliquées

Fiche révision 3 et source CV-ORB-006 précisée ; contenu scientifique et objectifs conservés.

## Enrichissements proposés (en attente d’accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Réutiliser le protocole CV-SIFT-007 | L’évaluation comparative existe déjà ; éviter un doublon ORB | Navigation, aucune carte | Aucun rappel supplémentaire | Rublee §§4.4 et 6.1 |

## Sources

- [Rublee et al., copie du papier](https://sites.cc.gatech.edu/classes/AY2024/cs4475_summer/images/ORB_an_efficient_alternative_to_SIFT_or_SURF.pdf), §§3–4, 6 et conclusion.
- [OpenCV ORB 4.13.0](https://docs.opencv.org/4.13.0/db/d95/classcv_1_1ORB.html), create/WTA_K.
- [Code officiel tag 4.13.0, ORB_Impl::defaultNorm](https://github.com/opencv/opencv/blob/4.13.0/modules/features2d/src/orb.cpp), corps de fonction consulté directement.
- [Matching OpenCV 4.13.0](https://docs.opencv.org/4.13.0/dc/dc3/tutorial_py_matcher.html), Basics of Brute-Force Matcher.

## Contrôles et limites

Contrôles de référence : 52 fiches, 224 cartes, 34 tests réussis. Les contrôles après modification et la conservation des identifiants sont consignés dans le [bilan commun](../2026-10-20/00-bilan.md). Context7 indisponible : accès direct aux documentations officielles quand nécessaire.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l’apprenant et validation scientifique indépendante non vérifiés. Les scénarios et recommandations de diagnostic sont des raisonnements du projet, sauf résultat explicitement attribué. Les familles absentes ne justifient pas à elles seules de nouvelles cartes.
