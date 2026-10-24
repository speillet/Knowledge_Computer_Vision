# Revue — PTQ, QAT, INT8/FP8 et runtimes — 2026-10-24

## Synthèse

5 cartes examinées pour leur pertinence et leur développement ; 5 réponses enrichies sur accord explicite de l’apprenant. Axe travaillé : échelle, saturation et exécution réelle du runtime. Aucun nouvel objectif ni ID. Les questions restent des rappels de mécanisme, de choix ou de diagnostic utiles en projet. Aucun doublon d’objectif justifiant un retrait dans ce sujet.

Constat éditorial : mécanisme ou mise à l’épreuve trop peu développé dans les réponses modifiées, gravité mineure. Aucun nouveau contresens bloquant établi par la confrontation ciblée ; cela ne certifie pas toutes les affirmations du noyau antérieur.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-QUANT-001 | Protocole proposé sous hypothèses ; noyau antérieur conservé | comparaison : distinguer PTQ et QAT | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 52 → 199 mots lexicaux |
| CV-QUANT-002 | Déduction ou exemple construit sous hypothèses ; noyau antérieur conservé | raisonnement : interpréter échelle et saturation | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 44 → 192 mots lexicaux |
| CV-QUANT-003 | Protocole proposé sous hypothèses ; noyau antérieur conservé | pratique : vérifier le support d’un runtime | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 38 → 183 mots lexicaux |
| CV-QUANT-004 | Protocole proposé sous hypothèses ; noyau antérieur conservé | diagnostic : diagnostiquer une absence de gain INT8 | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 80 → 209 mots lexicaux |
| CV-QUANT-005 | Protocole proposé sous hypothèses ; noyau antérieur conservé | evaluation : contrôler qualité et performance ensemble | Noyau fini et erreurs bloquantes conservés | Fiche r3, unités/hypothèses explicites | Mineure | Développer : 54 → 194 mots lexicaux |

## Corrections appliquées

- [Réponses](../../../vault/140-ingenierie-systemes/142-quantification-runtimes.md) : explications, exemples et vérifications développés, sans changer questions, objectifs, Source, tags ni identités. L’approfondissement reste facultatif pour réussir le rappel.
- [Fiche](../../../vault/140-ingenierie-systemes/references/142-quantification-runtimes.md) : révision 3, deux cas guidés repris des cartes pour relier compréhension et contrôle ; statut `redige` conservé.
- Date de consultation TensorRT actualisée dans la fiche : Quantization Workflows a été accessible depuis la navigation officielle après un premier échec d’extraction. Son URL et les champs Source des cartes sont conservés.

## Enrichissements proposés (en attente d’accord)

Aucun ajout en attente pour cette passe : le développement des réponses existantes est explicitement demandé. Aucune nouvelle carte créée. Les approfondissements APP encore ouverts restent dans l’inventaire ; ils ne sont pas déclarés couverts ici.

## Sources

- [ONNX, QuantizeLinear-21](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html#quantizelinear-21) : Summary, échelle, zero-point et arrondi, passage consulté le 2026-10-24. Il soutient le mécanisme de référence ; il ne fournit pas les résultats des scénarios construits du projet.
- Les pages TensorRT Working with Quantized Types et Quantization Workflows ont été ouvertes ; les passages PTQ/QAT, données représentatives et Q/DQ sont confirmés. Le lien workflows a fonctionné via la navigation après un premier échec d’extraction. Le support réel d’un moteur n’a pas été testé.
- Vérifications de bibliothèques : OpenCV 4.13 via Context7 pour filtres/pyramides, features/matching, fisheye/hand-eye ; documentation primaire en complément. Les autres sujets utilisent les sources primaires précisées ci-dessus, sans prétendre à une couverture intégrale de Context7.

## Contrôles et limites

Voir les [preuves globales](00-bilan.md) pour les commandes exécutées et leurs résultats. La comparaison à `8c428b4` conserve IDs, objectifs, questions, Source et tags ; le contrôle de longueur utilise `re.findall(r"\w+", Reponse)`. Le nombre de mots est un garde-fou éditorial, sans garantie de mémorisation.

Confrontation documentaire ciblée et auto-revue pédagogique par agent Codex : les affirmations antérieures ne font pas toutes l’objet d’une nouvelle confirmation ligne à ligne. Les exemples analytiques sont déduits, les essais de diagnostic sont proposés ; aucune expérimentation image/vidéo ou validation indépendante n’est revendiquée. Rendu Obsidian/AnkiDroid et maîtrise de l’apprenant non vérifiés.
