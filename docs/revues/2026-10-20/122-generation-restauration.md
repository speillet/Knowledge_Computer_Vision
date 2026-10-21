# Revue — VAE, GAN et diffusion pour génération/restauration — 2026-10-20

## Synthèse

3 cartes auditées. Une imprécision importante de la formule forward corrigée ; bibliographie complétée.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

3 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 3 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-DIFFUSION-001 | Confirmé, source ciblée | séparer apprentissage et sampling. | 63 mots à l’entrée ; Objectif unique conservé | Fiche et format contrôlés | mineur | Préciser source |
| CV-DIFFUSION-002 | Confirmé, source ciblée | situer la diffusion latente. | 48 mots à l’entrée ; Objectif unique conservé | Fiche et format contrôlés | mineur | Préciser source |
| CV-DIFFUSION-003 | Déduction du projet explicite | protéger une observation industrielle. | 50 mots à l’entrée ; Protocole fini, sans promesse de résultat | Fiche et format contrôlés | mineur | Attribuer le cas |

### Affirmations de la fiche et des cartes

- Confirmé dans les résumés originaux : VAE modélise des variables latentes avec inférence approchée ; GAN oppose générateur et discriminateur.
- Imprécis puis corrigé : la formule de bruit est un échantillon du marginal q(x_t|x_0), pas la transition depuis x_{t−1}. DDPM équation 4 et algorithmes 1/2 distinguent entraînement et échantillonnage.
- Confirmé : LDM §3.1 entraîne un autoencodeur perceptuel, §3.2 opère la diffusion en latent ; fig. 1 compare des reconstructions à différents niveaux de compression.
- Cas de fissure : déduction sur la différence entre fidélité de mesure et objectif perceptuel. Aucun défaut industriel effectivement effacé n'a été observé dans cette revue.
- Niveau repérage respecté : aucune dérivation ELBO ou loss adversariale ajoutée aux cartes.

## Corrections appliquées

Fiche révisée avec marginal/alpha-bar explicites ; sources des trois cartes ciblées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Aucune addition prioritaire | Les objectifs existants suffisent au périmètre annoncé | — | Aucun rappel ajouté | Sources ci-dessous |

Familles absentes : algorithme, conception, evaluation, pratique, raisonnement. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [VAE, résumé](https://arxiv.org/abs/1312.6114).
- [GAN, résumé](https://arxiv.org/abs/1406.2661).
- [DDPM, équation 4 et algorithmes 1–2](https://arxiv.org/abs/2006.11239), PDF complet.
- [LDM, §§3.1–3.2 et fig. 1](https://arxiv.org/abs/2112.10752).

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
