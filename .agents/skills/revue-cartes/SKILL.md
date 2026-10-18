---
name: revue-cartes
description: "Audite la pertinence, l'exactitude et la corrigibilité des fiches et cartes Anki existantes du vault de computer vision (vault/), corrige les défauts en préservant IDs et identités Anki, puis propose des enrichissements à valider. Utiliser dès que l'utilisateur demande de vérifier, relire, auditer, corriger, améliorer, compléter ou enrichir des cartes, flashcards, notes Anki, fiches de référence, un deck ou un thème du vault (par exemple « relis les cartes SIFT », « vérifie le deck NMS », « enrichis la calibration »), même sans nommer ce skill. Ne pas l'utiliser pour créer un sujet encore absent du vault."
---

# Revue des cartes du vault

Les fiches et cartes du vault ont été rédigées par un agent et n'ont eu qu'une
auto-revue documentaire. Elles servent un ingénieur CV expérimenté qui vise un
niveau senior : une erreur affirmée avec assurance, une réponse impossible à
noter ou une carte anecdotique coûte du temps de révision chaque jour et peut
ancrer une idée fausse. Ce skill fait donc une revue lente et sourcée, pas une
relecture de style.

Il audite, applique les corrections, propose des enrichissements, met à jour
les comptes et produit un rapport. Il ne valide ni l'export Anki, ni le rendu
AnkiDroid, ni la maîtrise de l'apprenant, et ne déclare jamais une fiche
« relue » : l'auto-revue d'un agent n'est pas une relecture (FR-037).

## 0. Délimiter le passage

L'argument peut être un fichier de cartes ou sa fiche
(`vault/80-detection-pose/81-nms.md`), un ID de fiche (`CV-NMS`) ou de carte
(`CV-NMS-003`), un dossier thématique (`vault/50-calibration-geometrie/`) ou
`tout`. Sans argument, demander le périmètre.

Traiter un sujet, c'est-à-dire une fiche et ses cartes, par passage :
confronter chaque affirmation à son passage source prend du temps. Pour un
dossier ou `tout`, enchaîner les sujets un par un, produire un rapport par
sujet et proposer de s'arrêter entre deux sujets.

## 1. Préparer

1. Lancer `git status --short` et noter les fichiers déjà modifiés : un autre
   agent travaille parfois sur ce dépôt en parallèle.
2. Établir la référence :

   ```sh
   python3 scripts/check_vault.py
   python3 -m unittest discover -s tests
   ```

   Si l'un échoue, le signaler avant tout et ne pas mélanger une réparation de
   format avec la revue.
3. Inventorier le périmètre, puis garder un inventaire complet hors du dépôt
   (scratchpad ou répertoire temporaire) pour la comparaison finale :

   ```sh
   python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py <fichier-ou-dossier>
   python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault --json > <tmp>/avant.json
   ```

   L'inventaire donne, par carte, famille, objectif, longueur, sources et
   identité Anki, ainsi que les familles absentes et le prochain ID libre.
4. Lire, dans cet ordre :
   - le fichier de cartes et sa fiche dans `references/` ;
   - [la grille de revue](references/grille.md) : critères et signaux d'alerte ;
   - dans `specs/001-cv-knowledge-base/learning-design.md`, les sections
     « Contrat d'une carte », « Noyau attendu et approfondissement »,
     « Familles de cartes » et « Sources, revue et corrections » ;
   - l'auto-revue et le journal de correction de
     `vault/01-Parcours/Suivi-pilote.md`, pour ne pas refaire ni contredire
     une correction antérieure.

## 2. Auditer

Commencer par la fiche : une carte ne peut pas être plus juste qu'elle. Puis
évaluer chaque carte sur quatre axes, détaillés dans la grille.

- **Exactitude.** Relever les affirmations centrales du noyau et de
  l'approfondissement, puis ouvrir le passage précis cité : section d'article,
  ligne de code à un commit, page de documentation versionnée. WebFetch sert
  pour les articles et les pages. Pour une API ou un paramètre de bibliothèque,
  passer par Context7 (`resolve-library-id`, puis `query-docs`), puis par la
  documentation officielle, comme le demande `AGENTS.md`. Donner un verdict
  par affirmation : confirmé, imprécis, faux, non soutenu par la source citée,
  non vérifiable. Ne jamais conclure « confirmé » de mémoire : la valeur de la
  revue tient à la confrontation réelle. Une source inaccessible laisse
  l'affirmation « non vérifiable », et le rapport le dit.
- **Pertinence.** La carte entraîne-t-elle un mécanisme, un choix, un
  diagnostic ou une évaluation dont un senior a besoin en projet ? Objectif
  unique, famille cohérente avec la question, pas de doublon dans le sujet.
- **Corrigibilité.** La question se comprend sans la fiche ; le recto ne livre
  pas la réponse ; le noyau est un ensemble fini de points vérifiables ; les
  erreurs bloquantes sont de vrais contresens ; l'approfondissement n'est pas
  nécessaire pour réussir. Signaler une réponse longue (nombre de mots de
  l'inventaire) sans imposer de plafond : la spec mesure la charge au lieu de
  la borner.
- **Cohérence.** Accord avec la fiche et les autres cartes, notations,
  repères et unités, affirmations dépendant d'une version datées, format
  conforme au [modèle de carte](references/format-carte.md).

Attribuer une gravité à chaque constat :

- **bloquant** : erreur scientifique, réponse impossible à noter, réponse
  révélée au recto ;
- **important** : imprécision qui peut induire en erreur, source qui ne
  soutient pas l'affirmation, objectif double, doublon ;
- **mineur** : formulation, notation, référence de source trop vague.

## 3. Corriger

Appliquer directement les corrections bloquantes et importantes, ainsi que les
mineures sans risque. Les règles suivantes protègent l'historique de révision
et la traçabilité.

- Relire le fichier juste avant de l'éditer. S'il a changé depuis la lecture,
  s'arrêter et le signaler plutôt que d'écraser le travail d'un autre agent.
- Corriger d'abord la fiche, puis chercher par `grep` dans tout le vault les
  cartes qui reprennent l'affirmation, y compris dans d'autres thèmes : aucune
  carte contradictoire ne doit rester active (SC-007).
- Garder `ID:` et le titre `## ID` inchangés : l'ID pédagogique est stable par
  contrat. Laisser intact le commentaire `<!--ID: …-->` du plugin, juste avant
  `END`, et ne jamais en écrire un : il relie la carte à sa note Anki et à son
  historique.
- Si la correction change l'objectif même de la carte, ne pas la réécrire sous
  le même ID. Proposer une nouvelle carte et le sort de l'ancienne : la
  suppression d'une note Anki n'a pas encore été testée.
- Un contenu rédigé par l'apprenant (provenance `apprenant` ou `mixte`) reçoit
  une proposition, pas une modification. Si l'apprenant l'accepte, la
  provenance devient `mixte`.
- Dans la fiche, incrémenter `revision` et laisser `statut: redige`.
- Garder la forme du vault : prose française, termes techniques et noms
  originaux, maths en `$…$` ou `$$…$$`, aucun espace en fin de ligne.
- Consigner chaque correction dans la section « Suite et corrections » de
  `vault/01-Parcours/Suivi-pilote.md`, dans un tableau « Journal de
  correction » (le créer s'il n'existe pas) avec ces colonnes : date, fiche
  et sa nouvelle révision, cartes affectées, erreur et source, correction,
  responsable (« Agent <Codex ou Claude Code>, auto-revue (`revue-cartes`) »),
  contrôles, statut d'export. Une ligne par erreur distincte. Une carte qui a
  une identité Anki est « à resynchroniser », sinon « non synchronisé ». Ne pas
  modifier les sections de preuves datées : elles décrivent ce qui a été testé
  à une date.

## 4. Proposer l'enrichissement

Chercher ce qui manquerait à un senior sur ce sujet, pas des cases à remplir :

- une famille de cartes absente (voir l'inventaire) qui a un vrai objet ici ;
  une famille sans objet se justifie au lieu de se remplir ;
- une notion centrale de la fiche qu'aucune carte n'interroge ;
- un mode d'échec, un cas industriel ou une décision sous contrainte manquant ;
- dans la fiche : une rubrique du contrat absente ou creuse, la baseline et la
  variation contrôlée (FR-033), la distinction entre source scientifique et
  source d'implémentation (FR-036), une affirmation non datée qui dépend
  d'une version ;
- les pôles métiers A–F, seulement si le champ `poles` existe déjà dans
  `specs/001-cv-knowledge-base/data-model.md` (tâche T017) ; sinon, noter la
  proposition sans l'appliquer.

Présenter les propositions sans rien écrire :

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |

Chaque carte ajoutée se révise pendant des mois : privilégier peu de cartes à
forte valeur et indiquer leur coût.

Après accord explicite de l'utilisateur :

1. Rédiger selon le [modèle de carte](references/format-carte.md), avec le
   prochain ID libre de l'inventaire et `Provenance : agent`. Vérifier chaque
   affirmation comme à l'étape 2.
2. Relier la fiche à ses nouvelles cartes et compléter la fiche si besoin, en
   incrémentant `revision`.
3. Mettre à jour les comptes qui décrivent l'état courant, d'après les
   totaux de l'inventaire : `vault/00-Accueil.md`, le `00-index.md` du thème,
   `vault/01-Parcours/Inventaire.md`, `README.md`, `docs/vault-layout.md`,
   `vault/01-Parcours/Guide-Anki.md`,
   `specs/001-cv-knowledge-base/contracts/obsidian-anki.md` et l'en-tête
   « Lot » de `Suivi-pilote.md`. Ne pas toucher aux résultats d'essais datés,
   comme « 47 notes reconnues ».
4. Consigner l'ajout dans le journal, comme une correction.

## 5. Vérifier

```sh
python3 scripts/check_vault.py
python3 -m unittest discover -s tests
python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault --comparer <tmp>/avant.json
```

- Le contrôleur et les tests passent ; les totaux de l'inventaire égalent ceux
  du contrôleur.
- La comparaison ne montre ni ID disparu ni identité Anki modifiée ; seuls
  apparaissent les IDs ajoutés après accord.
- Un `grep` sur l'ancien total ne trouve plus de compte d'état courant oublié.
- Relire le diff complet du périmètre.

## 6. Rapporter

Toujours utiliser ce modèle :

```markdown
# Revue — <sujet> — <date>

## Synthèse
<cartes auditées ; constats par gravité ; corrections appliquées ; propositions en attente>

## Constats par carte
| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |

## Corrections appliquées
<fichier, changement et raison, source consultée>

## Enrichissements proposés (en attente d'accord)
<tableau de l'étape 4>

## Sources
<passages réellement consultés ; sources non vérifiables et pourquoi>

## Contrôles et limites
<commandes et résultats ; reste non vérifié : export Anki, rendu AnkiDroid,
maîtrise de l'apprenant, validation indépendante>
```
