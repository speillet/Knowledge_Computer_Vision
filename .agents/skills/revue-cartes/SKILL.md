---
name: revue-cartes
description: "Audite la pertinence, l'exactitude et la corrigibilité des fiches et cartes Anki existantes du vault de computer vision (vault/), corrige les défauts en préservant les IDs, approfondit les réponses (mode par défaut) et gère les propositions de nouvelles cartes jusqu'à la décision de l'apprenant. Utiliser dès que l'utilisateur demande de vérifier, relire, auditer, corriger, approfondir, développer, compléter ou enrichir des cartes, flashcards, notes Anki, fiches de référence, un deck, un thème ou tout le vault (par exemple « relis les cartes SIFT », « vérifie le deck NMS », « approfondis les réponses de calibration », « fais une revue complète »), même sans nommer ce skill. Ne pas l'utiliser pour créer un sujet encore absent du vault, ni pour construire ou publier le paquet Anki (skill paquet-anki)."
---

# Revue des cartes du vault

Les fiches et cartes du vault sont rédigées par un agent et ne reçoivent que
des auto-revues. Elles servent un ingénieur CV expérimenté qui vise un niveau
senior : une erreur affirmée avec assurance, une réponse impossible à noter ou
une carte anecdotique coûte du temps de révision chaque jour et peut ancrer une
idée fausse. Ce skill fait donc une revue lente et sourcée, pas une relecture
de style.

Il ne valide ni le rendu sur AnkiDroid, ni la maîtrise de l'apprenant, et ne
déclare jamais une fiche « relue » : l'auto-revue d'un agent n'est pas une
relecture (FR-037).

## Choisir le mode

Le mode fixe ce que le passage a le droit de changer. Par défaut, le skill
travaille en mode `approfondir`, à la demande de l'apprenant (2026-10-30) :
l'invoquer vaut autorisation de développer les réponses. Il commence toujours
par l'audit, car on ne développe pas une réponse avant d'en avoir vérifié
l'exactitude.

| | `approfondir` (défaut) | `audit` | `ajouter` |
| --- | --- | --- | --- |
| Déclencheur | toute demande de revue, sauf mention contraire | « audit seulement », « vérifie sans développer » | accord sur une proposition du registre |
| ID, question, objectif, famille, tags | inchangés | inchangés | nouveaux IDs |
| Noyau attendu | inchangé, sauf correction sourcée | corrigé si une source contredit | rédigé |
| Approfondissement | corrigé puis développé | corrigé | rédigé |
| Fiche canonique | corrigée et alignée d'abord | corrigée d'abord | complétée |
| Nouvelles cartes | proposées seulement | proposées seulement | rédigées |

Le mode `approfondir` enchaîne les étapes 1 à 4 ; le mode `audit` saute l'étape 4.
Les deux finissent par les étapes 5 à 7.

## 0. Délimiter le passage

L'argument peut être un fichier de cartes ou sa fiche
(`vault/80-detection-pose/81-nms.md`), un ID de fiche (`CV-NMS`) ou de carte
(`CV-NMS-003`), un dossier thématique (`vault/50-calibration-geometrie/`) ou
`tout`. Sans argument, demander le périmètre.

L'unité de travail est un sujet : une fiche et ses cartes. Confronter chaque
affirmation à sa source prend du temps. Pour plusieurs sujets, écrire
d'abord un cadrage, traiter les sujets un par un avec un rapport chacun, puis
un bilan ([conventions des rapports](references/rapports.md)). Proposer une
pause entre deux sujets, sauf si l'apprenant demande d'enchaîner.

## 1. Préparer

1. Lancer `git status --short` et `git branch --show-current`. Un autre agent
   travaille parfois dans ce dépôt : ne pas mêler son travail au passage. Une
   passe de revue se fait sur sa propre branche (voir `CONTRIBUTING.md`).
2. Établir la référence ; si un contrôle échoue déjà, le signaler avant tout :

   ```sh
   python3 scripts/check_vault.py
   python3 scripts/sync_catalog.py --check
   python3 scripts/learning_path.py
   python3 -m unittest discover -s tests
   ```

3. Inventorier le périmètre, puis garder l'inventaire complet hors du dépôt
   (scratchpad ou répertoire temporaire) pour la comparaison finale :

   ```sh
   python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py <fichier-ou-dossier>
   python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault --json > <tmp>/avant.json
   ```

   Pour chaque carte : famille, objectif, pôles, longueur de la réponse et
   plancher du contrat, GUID de la note Anki, sources. L'inventaire signale
   aussi les syntaxes que le paquet Anki refuse, les familles absentes et le
   prochain ID libre.
4. Lire, sans tout relire à chaque fois :
   - le fichier de cartes et sa fiche dans `references/` ;
   - [la grille de revue](references/grille.md) ;
   - le dernier rapport du sujet : `ls docs/revues/*/<fichier>.md`. Ne pas
     refaire une vérification consignée sans raison, et ne pas la contredire
     sans source ;
   - les lignes du journal qui concernent la fiche :
     `grep -n "<ID-fiche>" vault/01-Parcours/Suivi-pilote.md`. Le journal est
     long : ne pas le lire en entier ;
   - les propositions du sujet dans `docs/revues/propositions.md` ;
   - au besoin, les sections « Contrat d'une carte », « Noyau attendu et
     approfondissement » et « Familles de cartes » de
     `specs/001-cv-knowledge-base/learning-design.md`.

## 2. Auditer

Commencer par la fiche : une carte ne peut pas être plus juste qu'elle. Puis
évaluer chaque carte sur les quatre axes détaillés dans la grille.

- **Exactitude.** Relever les affirmations centrales du noyau et de
  l'approfondissement, puis ouvrir le passage précis cité : section d'article,
  ligne de code à un commit, page de documentation versionnée. Pour une API,
  passer par Context7 puis la documentation officielle (`AGENTS.md`). Verdict
  par affirmation : confirmé, imprécis, faux, non soutenu par la source citée,
  non vérifiable. Ne jamais conclure « confirmé » de mémoire : une source
  inaccessible laisse l'affirmation « non vérifiable », et le rapport le dit.
- **Pertinence.** Un jugement, pas une recopie de l'objectif : la carte
  entraîne-t-elle un mécanisme, un choix, un diagnostic ou une évaluation
  dont un senior a besoin en projet ? Un seul objectif, famille cohérente,
  pas de doublon dans le sujet.
- **Corrigibilité.** La question se comprend sans la fiche ; le recto ne livre
  pas la réponse ; le noyau est un ensemble fini de points vérifiables ; les
  erreurs bloquantes sont de vrais contresens. La réponse respecte le plancher
  du contrat (180 mots lexicaux, contrôlé par `learning_path.py`). Son
  développement explique mécanisme, exemple, hypothèses ou limites, mais n'est
  jamais nécessaire pour réussir le rappel.
- **Cohérence.** Accord avec la fiche et les autres cartes, notations,
  repères et unités, affirmations dépendant d'une version datées, format
  conforme au [modèle de carte](references/format-carte.md), conversion
  acceptée par le paquet Anki.

Gravité de chaque constat :

- **bloquant** : erreur scientifique ou numérique, réponse impossible à noter,
  réponse révélée au recto, contradiction avec la fiche ;
- **important** : nuance manquante qui induit en erreur, source qui ne
  soutient pas l'affirmation, objectif double, doublon, réponse sous le plancher ;
- **mineur** : formulation, notation, référence trop vague mais exacte.

## 3. Corriger

Appliquer directement les corrections bloquantes et importantes, ainsi que les
mineures sans risque. Ces règles protègent l'historique de révision et la
traçabilité :

- Relire le fichier juste avant de l'éditer. S'il a changé depuis la lecture,
  s'arrêter et le signaler plutôt que d'écraser le travail d'un autre agent.
- Corriger d'abord la fiche, puis chercher par `grep` dans tout le vault les
  cartes qui reprennent l'affirmation, y compris dans d'autres thèmes : aucune
  carte contradictoire ne doit rester active (SC-007).
- Garder `ID:` et le titre `## ID` inchangés. Le paquet Anki dérive de l'ID le
  GUID de la note : changer l'ID créerait une autre note sur le téléphone et y
  laisserait l'ancienne, avec son historique. S'il reste un ancien commentaire
  `<!--ID: …-->` du plugin, le laisser intact et ne jamais en écrire un.
- Si la correction change l'objectif même de la carte, ne pas la réécrire sous
  le même ID : l'inscrire au registre des propositions, avec le sort prévu pour
  l'ancienne carte.
- Un contenu rédigé par l'apprenant (`apprenant` ou `mixte`) reçoit une
  proposition, pas une modification. S'il l'accepte, la provenance devient `mixte`.
- Dans la fiche, incrémenter `revision` et laisser `statut: redige`.
- Garder la forme du vault : prose française, termes techniques et noms
  originaux, maths en `$…$` ou `$$…$$`, aucun espace en fin de ligne, ni titre,
  tableau ou citation dans un champ de carte (le paquet les refuse).
- Consigner chaque correction dans le tableau « Journal de correction » de
  `vault/01-Parcours/Suivi-pilote.md`, une ligne par erreur distincte :
  - date ;
  - fiche et nouvelle révision ;
  - cartes affectées ;
  - erreur et source ;
  - correction ;
  - responsable (« Agent <Codex ou Claude Code>, auto-revue (`revue-cartes`) ») ;
  - contrôles ;
  - export : « à republier (`paquet-anki`) ».

  Ne pas modifier les sections de preuves datées.

## 4. Approfondir (mode par défaut)

Pour chaque carte, chercher ce qui manque à l'objectif de rappel, pas une
longueur :

- un mécanisme encore implicite, une dérivation commentée, un calcul construit ;
- une étape d'algorithme, un paramètre et son effet, un contre-exemple ;
- les symboles, dimensions, unités et hypothèses d'une équation.

Aligner d'abord la fiche, puis la carte. Chaque ajout apporte une information
sourcée ou explicitement construite : signaler un calcul ou un protocole du
projet comme tel, et n'annoncer une expérience exécutée qu'avec sa preuve. Ne
pas paraphraser un paragraphe déjà présent ni gonfler une réponse jusqu'au
plancher. Le noyau reste suffisant pour réussir. Une carte déjà complète est
conservée, et le rapport le dit.

## 5. Proposer, faire décider, ajouter

Repérer ce qui manquerait à un senior sur ce sujet, pas des cases à remplir :

- une famille absente (inventaire) qui a un vrai objet ici ;
- une notion centrale de la fiche qu'aucune carte n'interroge ;
- un mode d'échec, un cas industriel ou une décision sous contrainte manquant ;
- dans la fiche : une rubrique du contrat absente ou creuse, la baseline et la
  variation contrôlée (FR-033), la distinction entre source scientifique et
  source d'implémentation (FR-036).

Inscrire chaque proposition dans `docs/revues/propositions.md`, selon le
format du fichier, avec un identifiant stable. Avant d'en créer une, vérifier
qu'elle n'y figure pas déjà, et ne pas reproposer une proposition refusée
sans fait nouveau. Chaque carte ajoutée se révise pendant des mois :
privilégier peu de propositions à forte valeur, et indiquer leur coût.

Les propositions ne valent que si elles sont tranchées. À la fin du passage,
présenter à l'apprenant les propositions « à décider » du périmètre, les plus
utiles en premier, et lui demander pour chacune : accepter, refuser ou
reporter. Reporter le choix dans le registre.

Pour une proposition acceptée (mode `ajouter`) :

1. Rédiger selon le [modèle de carte](references/format-carte.md), avec le
   prochain ID libre de l'inventaire et `Provenance : agent`. Vérifier chaque
   affirmation comme à l'étape 2 et respecter le plancher de longueur.
2. Relier la fiche à ses nouvelles cartes, en incrémentant `revision`.
3. Régénérer la navigation et les comptes :
   `python3 scripts/sync_catalog.py`. Puis chercher par `grep` l'ancien total
   dans les documents non générés (`docs/`, `specs/`,
   `vault/01-Parcours/Guide-Anki.md`, en-tête « Lot » de `Suivi-pilote.md`) et
   corriger ceux qui décrivent l'état courant. Ne pas toucher aux résultats
   d'essais datés.
4. Passer la proposition à « faite » avec les IDs créés, et consigner l'ajout
   dans le journal.

## 6. Vérifier

```sh
python3 scripts/check_vault.py
python3 scripts/sync_catalog.py --check
python3 scripts/learning_path.py
python3 -m unittest discover -s tests
python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault
python3 .agents/skills/revue-cartes/scripts/inventaire_cartes.py vault --comparer <tmp>/avant.json
```

- Tous les contrôles passent. L'inventaire ne signale aucune anomalie
  (conversion, plancher, format) et ses totaux égalent ceux du contrôleur.
- La comparaison ne montre aucun ID disparu ; seuls apparaissent les IDs ajoutés
  après accord.
- Relire le diff complet du périmètre.
- Les cartes corrigées n'arrivent sur le téléphone qu'avec un nouveau paquet :
  le signaler, et renvoyer au skill `paquet-anki`.

## 7. Rapporter

Écrire un rapport par sujet dans `docs/revues/<AAAA-MM-JJ>[-<objet>]/<fichier-de-cartes>.md`,
et, pour plusieurs sujets, `00-cadrage.md` puis `00-bilan.md`, selon
[les conventions des rapports](references/rapports.md). Dans la conversation,
résumer : constats par gravité, corrections, propositions à décider, contrôles
et limites.
