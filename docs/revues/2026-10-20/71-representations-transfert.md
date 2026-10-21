# Revue — Représentations visuelles, ViT, Swin, ConvNeXt et DINOv2 — 2026-10-20

## Synthèse

5 cartes auditées. 0 bloquant ; 1 important (source manquante) ; 2 mineurs.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

5 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 1 importante, 2 mineure, 2 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-REPRESENTATIONS-001 | Confirmé : N×4 et terme image×16 | estimer le coût des tokens. | 39 mots à l’entrée ; token de classe exclu | Fiche et format contrôlés | Mineur | Recto précisé |
| CV-REPRESENTATIONS-002 | Confirmé : fenêtres décalées vs convolution | situer Swin et ConvNeXt. | 43 mots à l’entrée ; comparaison unique | Fiche et format contrôlés | Aucune | Conserver |
| CV-REPRESENTATIONS-003 | Transfert confirmé ; exigences produit déduites | utiliser des features autosupervisées. | 47 mots à l’entrée ; sorties et décision évaluables | Fiche et format contrôlés | Aucune | Conserver |
| CV-REPRESENTATIONS-004 | Non soutenu initialement pour LoRA/adapters ; confirmé par sources dédiées | choisir une adaptation. | 52 mots à l’entrée ; paramètres entraînés vs inférence | Fiche et format contrôlés | Important | Sources ajoutées |
| CV-REPRESENTATIONS-005 | Checklist du projet | contrôler le prétraitement d’un backbone. | 43 mots à l’entrée ; contrat d’entrée précis | Fiche et format contrôlés | Mineur | Attribution explicite |

### Affirmations de la fiche et des cartes

ViT : patches et coût ; Swin : fenêtres hiérarchiques ; ConvNeXt : ConvNet ; DINOv2 : apprentissage autosupervisé et transfert. LoRA/adapters vérifiés au niveau du principe, sans extrapoler leurs performances NLP à la vision. MAE reconstruit des pixels masqués. HOG résumé primaire disponible dans l’index, téléchargement INRIA indisponible ; aucune dérivation HOG approfondie n’est confirmée. Le calcul exclut tokens additionnels et ne prédit pas la latence.

## Corrections appliquées

Fiche révision 2 et sources 001/004/005 ; recto 001 précisé.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Interpréter tokens denses et token global | Choisir les sorties pour une tâche localisée | Pratique | Une carte, deux critères ; durée à mesurer | DINOv2, tâches denses |

Familles absentes : algorithme, conception, evaluation, pratique. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [ViT, §3.1](https://arxiv.org/abs/2010.11929)
- [Swin, §3](https://arxiv.org/abs/2103.14030)
- [ConvNeXt, §2](https://arxiv.org/abs/2201.03545)
- [DINOv2, résumé et évaluation par transfert](https://arxiv.org/abs/2304.07193)
- [Hu et al., LoRA, résumé et principe des paramètres gelés](https://arxiv.org/abs/2106.09685)
- [Houlsby et al., adapters, résumé](https://arxiv.org/abs/1902.00751)
- [He et al., MAE, résumé](https://arxiv.org/abs/2111.06377)
- [Dalal–Triggs, HOG, résumé](https://lear.inrialpes.fr/people/triggs/pubs/Dalal-cvpr05.pdf)

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
