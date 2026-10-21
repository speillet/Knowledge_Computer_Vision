# Revue — RANSAC appliqué à une homographie — 2026-10-20

## Synthèse

7 cartes auditées. 0 bloquant, 0 important ; 1 mineur partagé (statut des cas).
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

7 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 1 mineure, 6 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-HOMOGRAPHIE-001 | Confirmé : plan/rotation pure, parallaxe | choisir un modèle géométrique. | 103 mots à l’entrée ; noyau distinct de l’approfondissement | Fiche et format contrôlés | Aucune | Conserver |
| CV-HOMOGRAPHIE-002 | Confirmé : huit degrés et rang minimal | relier degrés de liberté et dégénérescence. | 93 mots à l’entrée ; noyau distinct de l’approfondissement | Fiche et format contrôlés | Aucune | Conserver |
| CV-HOMOGRAPHIE-003 | Confirmé : hypothèse, consensus, réestimation | reconstruire une itération robuste. | 111 mots à l’entrée ; noyau distinct de l’approfondissement | Fiche et format contrôlés | Aucune | Conserver |
| CV-HOMOGRAPHIE-004 | Confirmé par §II et calcul : 72/9 | interpréter le budget nominal de RANSAC. | 122 mots à l’entrée ; noyau distinct de l’approfondissement | Fiche et format contrôlés | Aucune | Conserver la justification demandée |
| CV-HOMOGRAPHIE-005 | Confirmé : résidu destination ; resize déduit | interpréter l'unité d'un seuil de résidu. | 117 mots à l’entrée ; noyau distinct de l’approfondissement | Fiche et format contrôlés | Aucune | Conserver |
| CV-HOMOGRAPHIE-006 | Diagnostic algébrique du projet | diagnostiquer un modèle extrapolé. | 95 mots à l’entrée ; noyau distinct de l’approfondissement | Fiche et format contrôlés | Mineur | Attribution explicite |
| CV-HOMOGRAPHIE-007 | Confirmé : incompatibilité de modèle | expliquer une incompatibilité de modèle. | 100 mots à l’entrée ; noyau distinct de l’approfondissement | Fiche et format contrôlés | Aucune | Conserver |

### Affirmations de la fiche et des cartes

Confirmés : modèle homogène, cas plan/rotation, calcul de résidu, quatre correspondances non dégénérées, budget sous hypothèse indépendante. La normalisation ne rétablit pas un rang absent : déduction algébrique. Les diagnostics spatiaux ne sont pas des résultats d’expérience. Les deux diagnostics 006/007 ont des causes différentes (conditionnement et modèle). La carte 004 donne le résultat numérique mais demande sa dérivation et son interprétation : pas de réponse révélée.

## Corrections appliquées

Fiche révision 3 et source de 006. Calculs de examples/pilot_math.py exécutés : 72 et 9.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Résidu symétrique et incertitude dans les deux images | Limite du seul transfert destination | Raisonnement | Une carte, trois critères ; durée à mesurer | Hartley–Zisserman, estimation optimale d’homographie |

Familles absentes : comprehension, conception, evaluation. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [Fischler–Bolles 1981, §II, procédure et probabilité p.383](https://www.sri.com/wp-content/uploads/2021/12/ransac-publication.pdf), PDF extrait ; formule et interprétation consultées.
- [OpenCV 4.13, homographie, Basic theory et Demo 5](https://docs.opencv.org/4.13.0/d9/dab/tutorial_homography.html).
- [OpenCV 4.13, findHomography, paramètres et algorithme](https://docs.opencv.org/4.13.0/d9/d0c/group__calib3d.html).

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
