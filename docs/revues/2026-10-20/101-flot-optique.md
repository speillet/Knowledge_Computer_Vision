# Revue — Flot optique : Lucas–Kanade, Farnebäck et RAFT — 2026-10-20

## Synthèse

4 cartes auditées. Aucun défaut nécessitant correction dans les quatre cartes.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

4 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 0 mineure, 4 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FLOT-001 | Confirmé | interpréter la contrainte du flot. | 47 mots à l’entrée ; Objectif unique, noyau fini | Fiche et format contrôlés | — | Conserver |
| CV-FLOT-002 | Confirmé | respecter l’unité temporelle. | 51 mots à l’entrée ; Objectif unique, noyau fini | Fiche et format contrôlés | — | Conserver |
| CV-FLOT-003 | Confirmé | situer RAFT. | 51 mots à l’entrée ; Objectif unique, noyau fini | Fiche et format contrôlés | — | Conserver |
| CV-FLOT-004 | Déduction explicite du projet | traiter une occultation. | 46 mots à l’entrée ; Cas et vérifications finis | Fiche et format contrôlés | — | Conserver |

### Affirmations de la fiche et des cartes

- Confirmé : constance photométrique et mouvement local cohérent conduisent à une contrainte scalaire ; le système de Lucas–Kanade requiert un bon conditionnement spatial. La pyramide traite des déplacements plus grands sans inventer des gradients.
- Confirmé : le tutoriel définit le flot retourné comme déplacement entre images et dérive aussi la vitesse continue dx/dt. La fiche conditionne explicitement les unités au pas de dérivation. Calcul 4/0,020 = 200 px/s vérifié.
- Confirmé : RAFT §3.2 construit les corrélations entre toutes les paires de features ; §3.3 raffine le flot récurrentement. La récurrence porte sur le raffinement, pas une ReID d'objet.
- `status=1` indique un point trouvé par l'algorithme, pas une preuve physique ; le diagnostic d'occultation et la baseline sont des déductions du projet. Aucun contrôle aller-retour ne garantit seul une bonne correspondance.

## Corrections appliquées

Aucune correction nécessaire.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Distinguer EPE et validité sous occultation | Choisir explicitement les pixels évalués | evaluation | 1 carte ; norme et masque | RAFT §4 et protocole du jeu retenu |

Familles absentes : algorithme, comprehension, conception, evaluation. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [OpenCV 4.13.0, Optical Flow et Lucas–Kanade, définition, dérivation et status](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html).
- [RAFT, §§3.1–3.3](https://arxiv.org/abs/2003.12039).

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
