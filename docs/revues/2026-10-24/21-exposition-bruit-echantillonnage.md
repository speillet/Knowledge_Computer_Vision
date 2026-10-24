# Revue — CV-ACQUISITION — 2026-10-24

## Synthèse

Correction ciblée avant fusion de la PR existante. Comparaison de resize 2022 généralisée au présent ; symboles et unités SNR absents. Limiter l’observation à Parmar 2022 ; définir QE, photons, gain et variances, préciser modèle linéaire.
Pas de carte ajoutée ni d’ID modifié ; fiche révision 5, statut `redige`.
Les autres cartes du sujet ne font pas l’objet d’un nouvel audit exhaustif.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ACQUISITION-002 | Point signalé vérifié avec les sources ci-dessous | Objectif existant conservé | Noyau et limites explicités | Fiche et carte accordées | Important | Corrigé |
| CV-ACQUISITION-003 | Point signalé vérifié avec les sources ci-dessous | Objectif existant conservé | Noyau et limites explicités | Fiche et carte accordées | Important | Corrigé |

## Corrections appliquées

`vault/20-acquisition-images/references/21-exposition-bruit-echantillonnage.md` et `vault/20-acquisition-images/21-exposition-bruit-echantillonnage.md` : Limiter l’observation à Parmar 2022 ; définir QE, photons, gain et variances, préciser modèle linéaire. Journal complété sans réécrire
les preuves datées du passage précédent. Les identités pédagogiques et Anki
restent stables.

## Enrichissements proposés (en attente d’accord)

Aucun ajout proposé dans ce correctif. Les nouveaux sujets prioritaires feront
l’objet d’un lot distinct autorisé par l’apprenant le 2026-10-24.

## Sources

[Parmar et al. 2022, §§3.2 et 6.3](https://arxiv.org/html/2104.11222v3) ; [torchvision 0.24 Resize, antialias](https://docs.pytorch.org/vision/0.24/generated/torchvision.transforms.Resize.html) ; [EMVA 1288 Linear 4.0, §§2.4–2.7](https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf).

## Contrôles et limites

Contrôleur, tests de la bibliothèque standard et comparaison d’inventaire
exécutés avant publication. Aucun export réel, rendu AnkiDroid, mesure matérielle
ou validation scientifique indépendante n’est déduit de cette auto-revue.
