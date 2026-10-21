# Revue — SLAM, VIO, préintégration IMU et bouclage — 2026-10-20

## Synthèse

5 cartes auditées. 0 bloquant, 0 important ; 1 mineur partagé (définitions et références).
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

5 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 0 mineure, 5 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-VIO-001 | Confirmé : contraintes relatives et biais | situer la préintégration. | 52 mots à l’entrée ; rôle unique | Fiche et format contrôlés | Aucune | Conserver ; source ciblée |
| CV-VIO-002 | Confirmé : facteur de revisite ; risque déduit | distinguer odométrie et boucle. | 54 mots à l’entrée ; fonction et limite | Fiche et format contrôlés | Aucune | Conserver ; source ciblée |
| CV-VIO-003 | Confirmé : jauge 4 DoF distincte de l’échelle | identifier les jauges VIO. | 64 mots à l’entrée ; deux ambiguïtés distinguées | Fiche et format contrôlés | Aucune | Conserver ; source ciblée |
| CV-VIO-004 | Cas de conception proposé | concevoir un VIO pour réalité augmentée. | 82 mots à l’entrée ; noyau large mais cohérent ; durée à mesurer | Fiche et format contrôlés | Aucune | Conserver ; source ciblée |
| CV-VIO-005 | Diagnostic proposé | diagnostiquer une dérive en couloir. | 86 mots à l’entrée ; causes à départager ; pas de solution unique forcée | Fiche et format contrôlés | Aucune | Conserver ; source ciblée |

### Affirmations de la fiche et des cartes

Définitions de Δv/Δp conformes aux états dans le monde et à R corps→monde ; unités ajoutées. Forster traite covariance et correction du biais, pas un système complet obtenu par une seule intégration. Zhang–Scaramuzza confirme le groupe à quatre degrés de liberté du cas inertiel. MSCKF/VINS-Mono/OKVIS sont seulement cités : leurs variantes ne sont pas auditées ici. DBoW2/NetVLAD ne sont pas détaillés ; leur rôle de proposition de lieux reste à documenter par leurs articles si approfondi.

## Corrections appliquées

Fiche révision 2 ; symboles et sources des cinq cartes précisés.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Distinguer biais corrigé au premier ordre et réintégration | Limite pratique de la préintégration | Raisonnement | Une carte, trois critères ; durée à mesurer | Forster, VI-C et annexe B |

Familles absentes : algorithme, evaluation, pratique. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [Forster et al., §§V–VI, équations 31–34 et VI-C](https://dellaert.github.io/files/Forster16tro.pdf)
- [Zhang–Scaramuzza 2018, §III et table I](https://rpg.ifi.uzh.ch/docs/IROS18_Zhang.pdf)
- [GTSAM, §4.1 Loop Closure Constraints, consulté le 2026-10-20](https://gtsam.org/tutorials/intro.html)

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
