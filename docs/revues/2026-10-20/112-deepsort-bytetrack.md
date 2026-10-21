# Revue — DeepSORT, ByteTrack et association multiobjet — 2026-10-20

## Synthèse

4 cartes auditées. Mécanismes confirmés ; attribution et sources précisées.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

4 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 4 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-ASSOCIATION-001 | Confirmé ; source précisée | identifier l’ajout de DeepSORT. | 44 mots à l’entrée ; Objectif conservé | Fiche et format contrôlés | mineur | Cibler source |
| CV-ASSOCIATION-002 | Confirmé ; source précisée | comprendre l’usage des faibles scores ByteTrack. | 62 mots à l’entrée ; Objectif conservé | Fiche et format contrôlés | mineur | Cibler source |
| CV-ASSOCIATION-003 | Déduction conditionnelle du projet | contrôler le transfert ReID. | 48 mots à l’entrée ; Contrôle de domaine précis | Fiche et format contrôlés | mineur | Attribuer diagnostic |
| CV-ASSOCIATION-004 | Protocole du projet | séparer détecteur et association. | 49 mots à l’entrée ; Variables à fixer finies | Fiche et format contrôlés | mineur | Citer effet détecteur |

### Affirmations de la fiche et des cartes

- Confirmé : DeepSORT utilise distance de mouvement, gating Mahalanobis, plus petite distance cosinus à la mémoire et cascade privilégiant les pistes vues récemment. La fiche ne prétend pas que toutes ces distances sont des probabilités.
- Confirmé : ByteTrack Algorithm 1 associe d'abord les détections fortes, puis les faibles aux pistes restantes ; les nouvelles pistes viennent des fortes non associées.
- Confirmé : AB3DMOT associe détections 3D, Kalman 3D et Hungarian (résumé/introduction) ; le besoin de conventions 3D en découle.
- Le transfert aux pièces industrielles est une hypothèse à tester, pas une mesure du papier. L'impossibilité de distinguer des objets par une apparence identique est conditionnée à cette seule information.
- SORT tableau 1 démontre que changer le détecteur change le résultat du tracker ; le protocole contrôlé proposé est cohérent.

## Corrections appliquées

Fiche révisée, bibliographie complétée pour l’effet du détecteur ; sources des quatre cartes ciblées.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Expliquer la priorité de la cascade DeepSORT | La carte 001 nomme la cascade sans rappeler son mécanisme | algorithme | 1 carte ; priorité aux pistes récemment observées | DeepSORT §2.2 Listing 1 |

Familles absentes : comprehension, conception, pratique, raisonnement. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [DeepSORT, §§2.1–2.3, équation 3 et Listing 1](https://arxiv.org/abs/1703.07402).
- [ByteTrack, §3 Algorithm 1 et paragraphe de création](https://arxiv.org/abs/2110.06864).
- [AB3DMOT, résumé et introduction](https://arxiv.org/abs/2008.08063).
- [SORT, §3.1 et tableau 1](https://arxiv.org/abs/1602.00763).

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
