# Revue — Recalage par intensités et ECC — 2026-10-20

## Synthèse

3 cartes auditées. 0 bloquant ; 1 important dans la fiche (hypothèses photométriques) ; 1 mineur partagé (attribution).
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

3 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 3 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ECC-001 | Confirmé : intensités, warp initial et appariement sparse | choisir matching ou optimisation photométrique. | 44 mots à l’entrée ; comparaison cohérente | Fiche et format contrôlés | Mineur | Source précisée |
| CV-ECC-002 | Déduit : motifs périodiques et maxima concurrents | interpréter une convergence ECC. | 35 mots à l’entrée ; contrôles réservés évaluables | Fiche et format contrôlés | Mineur | Déduction identifiée |
| CV-ECC-003 | Modèles confirmés ; compromis déduit | choisir un modèle de mouvement. | 43 mots à l’entrée ; une décision | Fiche et format contrôlés | Mineur | Déduction identifiée |

### Affirmations de la fiche et des cartes

Confirmés dans la documentation : optimisation par intensités, transformation initiale nécessaire pour déplacements importants, paramètres translation/rigide/affine/homographie, sens inverse pour affichage. Imprécision importante de la fiche corrigée : les conditions du raisonnement gain/offset sont désormais explicites. Les coûts par pixels/itérations et le surajustement sont des raisonnements ; aucun benchmark. Article ECC primaire non accessible lors de ce passage : son détail de dérivation reste non vérifiable ici.

## Corrections appliquées

Fiche révision 2 : conditions photométriques précisées. Sources des trois cartes ciblées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Écrire la convention du warp retourné | Risque pratique présent seulement en approfondissement | Pratique | Une carte, un point test ; durée à mesurer | OpenCV 4.13, findTransformECC |

Familles absentes : algorithme, comprehension, conception, evaluation, raisonnement. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [OpenCV 4.13.0, findTransformECC, modèle, initialisation et inverse warping](https://docs.opencv.org/4.13.0/dc/d6b/group__video__track.html) : section findTransformECC, paramètres et paragraphes après la formule.
- [Evangelidis–Psarakis 2008, résumé primaire via PubMed](https://pubmed.ncbi.nlm.nih.gov/18703836/) ; texte intégral auteur inaccessible, ne confirme pas la dérivation détaillée.

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
