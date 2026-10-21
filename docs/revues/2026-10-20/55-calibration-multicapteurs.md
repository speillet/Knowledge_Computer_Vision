# Revue — Calibration multicapteurs, hand-eye et temps — 2026-10-20

## Synthèse

3 cartes auditées. 0 bloquant ; 2 importants (convention et source).
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

3 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 2 importante, 0 mineure, 1 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-MULTICALIB-001 | Confirmé mais fiche ne donnait aucune convention complète | interpréter hand-eye. | 51 mots à l’entrée ; objectif de convention | Fiche et format contrôlés | Important | Chaîne définie |
| CV-MULTICALIB-002 | Confirmé : axes non parallèles ; test de stabilité déduit | évaluer des mouvements informatifs. | 44 mots à l’entrée ; cause et action | Fiche et format contrôlés | Aucune | Source ciblée |
| CV-MULTICALIB-003 | Non soutenu par hand-eye seul ; LOAM confirme le deskew | séparer intrinsèques extrinsèques et temps. | 44 mots à l’entrée ; trois responsabilités liées | Fiche et format contrôlés | Important | Source LOAM |

### Affirmations de la fiche et des cartes

Chaîne eye-in-hand et axes informatifs confrontés à OpenCV ; déformation du scan confrontée à LOAM. Le choix de trajectoires réservées et le diagnostic en mouvement sont des propositions du projet. Aucune calibration temporelle automatiquement produite par calibrateHandEye n’est revendiquée.

## Corrections appliquées

Fiche révision 2 : repères explicités ; sources des trois cartes ciblées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Diagnostiquer offset et dérive d’horloge séparément | Un offset fixe ne modélise pas toute désynchronisation | Diagnostic | Une carte ; durée à mesurer | Kalibr, calibration temporelle |

Familles absentes : algorithme, comprehension, conception, evaluation, pratique. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [OpenCV 4.13.0, calibrateHandEye, équations eye-in-hand et note sur les axes](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html)
- [Zhang–Singh 2014, LOAM, §§II, IV et V-B](https://www.roboticsproceedings.org/rss10/p07.pdf) : PDF téléchargé, interpolations temporelles des points §V-B.

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
