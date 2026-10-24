# Revue — Graphes de facteurs et optimisation incrémentale — 2026-10-23

## Synthèse

Trois cartes auditées, plus leur fiche. Aucune affirmation fausse. Il y a un
constat important (CV-FACTEURS-001, question fermée) et deux cartes justes
mais minces. Correction appliquée : fiche en révision 3, IDs et objectifs
inchangés. Les quatre enrichissements proposés ont été acceptés et rédigés
en révision 4 : le sujet passe de 3 à 5 cartes, et 002 et 003 sont enrichies.

Auto-revue : Agent Claude Code (`revue-cartes`). Statut éditorial `redige`.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-FACTEURS-001 | Confirmé (GTSAM §§2.3–2.4, 4.1, 7 ; Kaess §2) ; GTSAM ne formule pas l'équivalence MAP gaussien–moindres carrés | Faible sous forme oui/non | Question fermée : « Non » se devine | Accord fiche | Important | Question ouverte, représentation et éléments à fournir |
| CV-FACTEURS-002 | Confirmé (Ceres, Gauge Invariance) | Forte | Noyau net | Recoupe CV-BA-003 sans la contredire | Aucun | Enrichissement proposé |
| CV-FACTEURS-003 | Diagnostic du projet, plausible | Forte | Noyau net mais sans test discriminant | Accord fiche | Mineur | Enrichissement proposé |

## Corrections appliquées

- `vault/10-mathematiques-estimation/references/14-graphes-facteurs.md`,
  révision 3 :
  - définition biparti et rôle des `Values` ;
  - prior de première pose ;
  - élimination par QR creuse, fill-in et ordre incrémental ;
  - sources précisées par section.
- `vault/10-mathematiques-estimation/14-graphes-facteurs.md` : CV-FACTEURS-001
  réécrite sans changer d'objectif.
- Journal : une ligne.

## Enrichissements acceptés et appliqués

Tous acceptés le 2026-10-23 :

- **CV-FACTEURS-002**, jauge ;
- **CV-FACTEURS-003**, test $\chi^2$ et réoptimisation sans la boucle ;
- **CV-FACTEURS-004**, back-ends robustes ;
- **CV-FACTEURS-005**, iSAM2.

La fiche reçoit la dimension de la jauge et ses traitements, le mécanisme
d'iSAM2 et une rubrique sur les fausses boucles. Le total passe de 242 à 244
cartes.

Table des propositions telle que soumise :

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| CV-FACTEURS-002 : dimension de la jauge selon les capteurs (pose graph 6, BA monoculaire 7, visuel-inertiel 4 : position et lacet) et les trois traitements (fixer, prior, laisser libre) | La carte ne dit pas combien de degrés sont libres ni comment les traiter | approfondissement seul | aucun nouveau rappel | Zhang, Gallego et Scaramuzza 2018, RA-L, résumé, §I et table I ; Ceres, Gauge Invariance |
| CV-FACTEURS-003 : test par facteur, résidu blanchi au carré comparé à un quantile du $\chi^2$ | Le diagnostic actuel n'a pas de test chiffré | approfondissement seul | aucun nouveau rappel | Agarwal et al. 2013, §III ; Gamse et al. 2014 (CV-FUSION-002) |
| CV-FACTEURS-004 : fermetures de boucle robustes : perte robuste, contraintes commutables, DCS | Le perceptual aliasing rend un front-end sans faux positifs impossible ; aucune carte sur le back-end robuste | comparaison | 1 carte ; noyau à 3 points | Agarwal et al. 2013, résumé et §III : $s=\min(1, 2\Phi/(\Phi+\chi^2))$ ; Sünderhauf et Protzel 2012, à lire |
| CV-FACTEURS-005 : ce que recalcule iSAM2 à chaque mesure : partie affectée de l'arbre de Bayes, relinéarisation fluide, mises à jour partielles | Le mot « incrémental » est cité sans mécanisme | algorithme | 1 carte ; noyau à 3 points | Kaess et al. 2012, §§3–4 |

## Sources

- [Dellaert, Factor Graphs and GTSAM](https://gtsam.org/tutorials/intro.html),
  consulté le 2026-10-23 :
  - §1, graphe biparti ;
  - §2.3, graphe et `Values` ;
  - §2.4, estimée initiale du MAP ;
  - §4.1, prior de première pose, seul lien au repère global ;
  - §7, iSAM et arbre de Bayes ;
  - fill-in et COLAMD ne sont pas mentionnés.
- [Kaess et al. 2012, iSAM2, IJRR](https://www.cs.cmu.edu/~kaess/pub/Kaess12ijrr.pdf),
  texte intégral :
  - §2, cas gaussien, moindres carrés et QR creuse ;
  - §3.4, ordre incrémental et COLAMD ;
  - §§4.1–4.2, relinéarisation fluide et mises à jour partielles.
- Pour les propositions :
  - [Zhang, Gallego et Scaramuzza 2018](https://rpg.ifi.uzh.ch/docs/RAL18_Zhang.pdf),
    prépublication des auteurs : 4 degrés de liberté non observables en
    visuel-inertiel, 7 en BA monoculaire, trois approches de précision
    similaire et covariances reliées ;
  - [Agarwal et al. 2013, DCS](https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/agarwal13icra.pdf),
    texte intégral : résumé et §III.
- Non lu : Sünderhauf et Protzel 2012. Le dépôt QUT n'a fourni que la notice ;
  seule sa reprise par Agarwal et al. a été lue.

## Contrôles et limites

`check_vault.py` OK (242 cartes) après correction, puis 244 après ajouts ;
34 tests réussis ; catalogue régénéré puis à jour ; inventaire sans ID
disparu ni identité Anki modifiée. Context7 n'est pas
disponible dans cette session. Non vérifiés : export Anki, rendu Obsidian et
AnkiDroid, maîtrise, validation indépendante.
