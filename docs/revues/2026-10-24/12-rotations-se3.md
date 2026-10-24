# Revue — CV-SE3 — 2026-10-24

## Synthèse

Correction ciblée avant fusion de la PR existante. Matrice 3×3 composée avec poses homogènes 4×4 (FR-007). Définir M pour les vecteurs 3D et M_h pour les poses homogènes ; dimensions et côtés de composition explicites.
Pas de carte ajoutée ni d’ID modifié ; fiche révision 5, statut `redige`.
Les autres cartes du sujet ne font pas l’objet d’un nouvel audit exhaustif.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-SE3-006 | Point signalé vérifié avec les sources ci-dessous | Objectif existant conservé | Noyau et limites explicités | Fiche et carte accordées | Important | Corrigé |

## Corrections appliquées

`vault/10-mathematiques-estimation/references/12-rotations-se3.md` et `vault/10-mathematiques-estimation/12-rotations-se3.md` : Définir M pour les vecteurs 3D et M_h pour les poses homogènes ; dimensions et côtés de composition explicites. Journal complété sans réécrire
les preuves datées du passage précédent. Les identités pédagogiques et Anki
restent stables.

## Enrichissements proposés (en attente d’accord)

Aucun ajout proposé dans ce correctif. Les nouveaux sujets prioritaires feront
l’objet d’un lot distinct autorisé par l’apprenant le 2026-10-24.

## Sources

[Solà et al., micro Lie theory, annexe D-A, équations 170–171](https://arxiv.org/html/1812.01537v9#A4.SS1) ; [REP 103, axes caméra](https://www.ros.org/reps/rep-0103.html). La correction dimensionnelle est une déduction algébrique du projet.

## Contrôles et limites

Contrôleur, tests de la bibliothèque standard et comparaison d’inventaire
exécutés avant publication. Aucun export réel, rendu AnkiDroid, mesure matérielle
ou validation scientifique indépendante n’est déduit de cette auto-revue.
