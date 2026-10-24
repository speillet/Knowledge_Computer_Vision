# Plan d’implémentation : pilote du vault

**Branche** : `feat/obsidian-pilot` · **Date** : 2026-10-18
**Entrée** : [spec.md](spec.md), [contrat pédagogique](learning-design.md).

## Résumé

Créer un vault autonome dans `vault/`, avec les sept sujets initiaux du pilote,
des fiches canoniques et des cartes détaillées à objectif unique. Les trois
extensions et la production du catalogue restent des étapes suivantes.
Le client de révision confirmé est **AnkiDroid sur Android**.

## Contexte technique

- Markdown UTF-8, front matter YAML simple, liens relatifs et MathJax.
- Obsidian pour lire et éditer ; Obsidian_to_Anki 3.6.0 comme candidat d’export
  **pilote**, modèle explicite à quatre champs, une carte par note.
- Anki Desktop + AnkiConnect pour l’export ; AnkiWeb pour rejoindre AnkiDroid.
  Aucune application personnelle ni configuration de compte modifiée.
- Python 3.9+ et bibliothèque standard pour les contrôles et expériences
  arithmétiques : aucune dépendance nécessaire pour lire ou vérifier le vault.
- Pas de synchroniseur, entraînement ou service ajouté. Le lot du 2026-10-24
  ajoute le générateur `.apkg` décrit ci-dessous.
- Aucun objectif de latence du système pédagogique ; les performances des
  méthodes sont discutées avec leurs conditions, sans promesse matérielle.

## Contrôle des principes

La constitution est toujours un modèle non ratifié : ses exemples ne sont pas
des obligations. Les règles applicables proviennent d’AGENTS.md, du contrat et
de la demande utilisateur. Avant et après conception : français, sources primaires,
IDs stables, réponses évaluables, états séparés et absence de généralisation
du format comme validé avant l’essai réel sont respectés. Aucun hook d’extension présent.

## Phase 0 — Recherche

Conserver la recherche précédente ; lui ajouter les décisions de pilote.
Vérifier les articles SIFT, ORB, RANSAC, Zhang, SORT et le code COCO officiel.
Utiliser Context7 pour les API OpenCV et le format du plugin, puis confronter
ces résultats aux sources officielles. Documenter les divergences de protocole.

Le choix provisoire du plugin permet de préparer les fichiers du pilote ;
il ne valide pas leur synchronisation. Anki Desktop n’étant pas installé,
la validation réelle est une dépendance externe identifiée, avec un protocole
exécutable par l’apprenant ; elle n’empêche pas la préparation éditoriale.

## Phase 1 — Conception

- [Modèle de données](data-model.md) : sujets, fiches, cartes et preuves séparés.
- [Contrat Markdown–Anki](contracts/obsidian-anki.md) : format et identité.
- [Guide de validation](quickstart.md) : contrôles locaux et essai applicatif.
- `vault/01-Parcours/Inventaire.md` garde visibles les quatorze domaines et
  les lacunes ; seules les entrées avec artefacts sont rédigées.

## Structure retenue

```text
vault/
  .obsidian/app.json
  00-Accueil.md
  01-Parcours/             # inventaire, guide et journal des essais
  40-features-matching/   # cartes SIFT et ORB, index, références complètes
  50-calibration-geometrie/
  80-detection-pose/
  110-tracking-association/
  130-evaluation-fiabilite/
  ...                     # 14 thèmes, état « à rédiger » pour les autres
  99-Ressources/           # schéma original
anki/                     # gabarits du modèle, hors vault scanné
examples/                 # expériences sans dépendance externe
scripts/check_vault.py    # contrôle documentaire, pas un exporteur
scripts/vault_sections.json # correspondance domaines / dossiers / titres
tests/                    # cas d’erreur du contrôleur et calculs
```

## Livraison et limites

Une première livraison comprend les sept références, les cartes et les contrôles
locaux. Les états restent « rédigé / auto-revu », sans validation indépendante
ni maîtrise présumée. Les sessions de rappel sont laissées à remplir.
Les douze cas de transfert couvrant les six familles, les extensions, les tests
Anki et la mesure pédagogique restent visibles dans [tasks.md](tasks.md).
La préparation éditoriale élargie est autorisée par la demande actuelle ;
le pilote technique et pédagogique reste à réussir avant adoption du format.

## Organisation demandée après le premier lot

La demande du 2026-10-18 retient un répertoire par thématique, inspiré de
Knowledge_AI_Engineering. Les cartes se trouvent directement dans le thème ;
les fiches complètes sont regroupées dans son sous-dossier `references/`.
Le sous-deck reprend le nom du thème, les IDs restent stables, et l'accueil
relie les quatorze index. Liens, médias, contrôleur et test du parseur sont
adaptés à cette structure avant toute nouvelle publication.

## Lot de couverture thématique — révision 6

La nouvelle demande étend la préparation éditoriale aux quatorze thèmes et
aux six pôles ; les essais applicatifs et de rappel restent ouverts. Les
fiches canoniques sont enrichies de `poles`, les cartes exportent `pole::A`
à `pole::F`. Les sujets partagés restent dans un seul domaine et un seul fichier.

Recherche : vérifier les références primaires par grandes familles, Context7
pour les bibliothèques. Les corrections de cadrage portent sur priorités V0,
observabilité et jauges VIO, occupation/surfaces implicites, frontière VLA/action,
quantification conditionnée au backend et distinction thème/variante traitée.

Conception : conserver le modèle à quatre champs et les identités existantes.
Ajouter des fiches structurées et cartes évaluables dans les répertoires existants,
un inventaire d'entrées individuelles, une vue des pôles et des cas de transfert.
La navigation et les comptes seront calculés depuis le contenu pour éviter
les totaux périmés. Les tests vérifient pôles, parents et états ; ils ne certifient
pas les textes scientifiques. Aucun hook d'extension n'est présent.

## Export direct — lot du 2026-10-24

Publier l'exporteur local préparé sur `feat/apkg-export`, avec genanki 0.13.1
isolé par uv. Le vault et le modèle à quatre champs restent canoniques ;
`modelId` reprend celui du paquet local existant (1153189853). Le GUID dépend
du nom du modèle et de l'ID pédagogique. Cette chaîne alimente une collection
distincte de celle du plugin historique.

Critères : [contrat d'export direct](../../docs/export-apkg.md).
`build_apkg.py` construit et relit ZIP/SQLite, compare les manifestes et embarque
les médias ; `simulate_anki_import.py` teste dans une collection jetable le
contenu, le style, les identités et l'historique avec anki 26.9.3 et Python 3.12.
Le rendu AnkiDroid et les cas applicatifs de T010 restent ouverts. Une fusion
publie les sources ; les paquets dans `dist/` ne sont pas versionnés et une
release demande une action distincte.
