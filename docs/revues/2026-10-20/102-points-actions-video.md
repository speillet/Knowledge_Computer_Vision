# Revue — Suivi de points, actions et compréhension vidéo — 2026-10-20

## Synthèse

4 cartes auditées. Bibliographie incomplète de la fiche corrigée ; provenance des cas précisée.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

4 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 1 importante, 3 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-VIDEO-001 | Confirmé avec source ciblée | choisir la bonne sortie vidéo. | 52 mots à l’entrée ; Objectif conservé | Fiche et format contrôlés | mineur | Préciser source |
| CV-VIDEO-002 | Contre-exemple mathématique | tester la perte d’événements courts. | 45 mots à l’entrée ; Question autonome, un point | Fiche et format contrôlés | mineur | Attribuer au projet |
| CV-VIDEO-003 | Confirmé avec source complémentaire | contrôler causalité et délai. | 40 mots à l’entrée ; Contrat temporel fini | Fiche et format contrôlés | important | Ajouter CoTracker3 |
| CV-VIDEO-004 | Confirmé avec source ciblée | vérifier l’utilisation de l’ordre temporel. | 49 mots à l’entrée ; Objectif conservé | Fiche et format contrôlés | mineur | Préciser source |

### Affirmations de la fiche et des cartes

- Confirmé : CoTracker exploite les interactions entre trajectoires et estime leur visibilité ; fenêtres chevauchantes et récurrence inter-fenêtres décrites dans §3.
- Confirmé : TimeSformer sépare notamment attention spatiale et temporelle ; ViViT traite des tokens spatio-temporels. VideoMAE utilise le masquage en tubes pour une reconstruction de préentraînement ; son ratio 90–95 % ne devient pas une prescription générale.
- Sources manquantes ajoutées pour ViViT et les variantes CoTracker3 online/offline.
- Déductions vérifiées : un événement de 100 ms peut tenir entre t=0 et t=1 s ; L timestamps réguliers couvrent (L−1)/f. Ce sont des arguments d'échantillonnage, pas des performances de réseau.
- La permutation des frames est une intervention proposée ; elle n'établit pas à elle seule ce que le modèle a appris.

## Corrections appliquées

Ajout des sources manquantes dans la fiche ; sources des quatre cartes adaptées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Aucune addition prioritaire | Les objectifs existants suffisent au périmètre annoncé | — | Aucun rappel ajouté | Sources ci-dessous |

Familles absentes : algorithme, comprehension, conception, pratique. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [CoTracker, introduction et §3](https://arxiv.org/abs/2307.07635).
- [TimeSformer, résumé et divided attention](https://arxiv.org/abs/2102.05095).
- [ViViT, résumé](https://arxiv.org/abs/2103.15691).
- [VideoMAE, résumé](https://arxiv.org/abs/2203.12602).
- [CoTracker3, résumé et introduction](https://arxiv.org/abs/2410.11831).

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
