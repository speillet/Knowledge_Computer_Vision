# Revue — NeRF, 3D Gaussian Splatting et reconstruction — 2026-10-20

## Synthèse

3 cartes auditées. Une ambiguïté importante de la fiche sur la densité NeRF levée ; sources précisées.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

3 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 3 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-RENDU3D-001 | Confirmé, source ciblée | distinguer représentation implicite et primitives. | 51 mots à l’entrée ; Objectif unique conservé | Fiche et format contrôlés | mineur | Préciser source |
| CV-RENDU3D-002 | Déduction du projet explicite | séparer rendu et géométrie. | 49 mots à l’entrée ; Protocole fini, sans promesse de résultat | Fiche et format contrôlés | mineur | Attribuer le cas |
| CV-RENDU3D-003 | Déduction du projet explicite | vérifier une scène peu observée. | 40 mots à l’entrée ; Protocole fini, sans promesse de résultat | Fiche et format contrôlés | mineur | Attribuer le cas |

### Affirmations de la fiche et des cartes

- Confirmé puis précisé : dans NeRF original, densité positionnelle et couleur directionnelle, avec intégration le long des rayons. La phrase de la fiche pouvait faire croire que la densité était directionnelle.
- Confirmé : 3DGS optimise des gaussiennes avec covariance anisotrope et contrôle de densité, puis rend par splatting.
- Déduction : PSNR compare des images, ne mesure pas une longueur physique. L'échelle et une référence géométrique sont nécessaires pour une assertion métrologique.
- Les contrôles de couverture/poses sont des diagnostics proposés, pas une évaluation sur données du projet.
- DUSt3R/MASt3R, MVS et TSDF ne sont que des renvois vers d'autres contrats ; aucune comparaison détaillée de ces méthodes n'est validée ici.

## Corrections appliquées

Fiche révisée et références directes ajoutées ; objectifs des trois cartes inchangés.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Aucune addition prioritaire | Les objectifs existants suffisent au périmètre annoncé | — | Aucun rappel ajouté | Sources ci-dessous |

Familles absentes : algorithme, comprehension, conception, pratique, raisonnement. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [NeRF, page des auteurs](https://www.matthewtancik.com/nerf) et [papier §§3–4, protocole §6](https://arxiv.org/abs/2003.08934).
- [3DGS, résumé et présentation des auteurs](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/) ; [papier](https://arxiv.org/abs/2308.04079).

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
