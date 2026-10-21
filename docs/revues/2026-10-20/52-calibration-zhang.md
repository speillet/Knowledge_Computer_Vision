# Revue — Calibration caméra sur mire — méthode de Zhang — 2026-10-20

## Synthèse

7 cartes auditées. 0 bloquant ; 1 important (passage de source erroné) ; 1 mineur (repère bibliographique).
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

7 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 1 importante, 1 mineure, 5 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ZHANG-001 | Confirmé : sorties distinctes | distinguer trois objectifs géométriques. | 104 mots à l’entrée ; comparaison unique | Fiche et format contrôlés | Aucune | Conserver |
| CV-ZHANG-002 | Confirmé au §2.1 ; ancienne référence imprécise | interpréter les conventions de projection. | 124 mots à l’entrée ; conventions évaluables ; skew facultatif explicite | Fiche et format contrôlés | Important | Passage corrigé |
| CV-ZHANG-003 | Confirmé : deux contraintes et vues indépendantes | expliquer les contraintes multi-vues. | 109 mots à l’entrée ; mécanisme et limite liés | Fiche et format contrôlés | Mineur | §2.3 ajouté |
| CV-ZHANG-004 | Confirmé : ajustement pixel ; validation proposée | interpréter un RMS sans conclusion abusive. | 111 mots à l’entrée ; pas de seuil universel | Fiche et format contrôlés | Aucune | Conserver |
| CV-ZHANG-005 | Confirmé par composition K′=AK | propager une transformation pixel. | 105 mots à l’entrée ; convention pixel de l’outil à vérifier | Fiche et format contrôlés | Aucune | Conserver |
| CV-ZHANG-006 | Confirmé : orientations dégénérées ; diagnostic déduit | diagnostiquer l'observabilité. | 107 mots à l’entrée ; hypothèse et test cohérents | Fiche et format contrôlés | Aucune | Conserver |
| CV-ZHANG-007 | Protocole du projet cohérent avec la capture Zhang | construire une collecte et une validation cohérentes. | 102 mots à l’entrée ; carte de conception ; charge à mesurer | Fiche et format contrôlés | Aucune | Conserver |

### Affirmations de la fiche et des cartes

Confirmés : projection monde→caméra, K, orthogonalité des colonnes, trois vues pour cinq paramètres, deux sous skew nul, dégénérescence par orientations identiques, modèle radial et minimisation de reprojection. Le §4 mentionne une exception sous translation connue (annexe D) : elle ne contredit pas le cas sans mouvement métrique connu du vault. Le resize/crop est une dérivation de repère et non une calibration refaite. Les recommandations industrielles sont déjà distinguées des résultats du papier.

## Corrections appliquées

Fiche révision 3 ; sources de 002–003 corrigées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Identifier le cas de translation métrique connue | Éviter de généraliser la dégénérescence à toute calibration | Approfondissement de fiche | Pas de carte prioritaire | Zhang, annexe D |

Familles absentes : algorithme, comparaison. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [Zhang, rapport TR98-71, §§2.1–2.3, 3.1–3.3, 4 et annexe D](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr98-71.pdf), texte intégral téléchargé.
- [OpenCV 4.13, modèle caméra et calibrateCamera](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html), paramètres, RMS et changement de résolution.

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
