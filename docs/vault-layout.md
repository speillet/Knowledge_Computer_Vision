# Organisation du vault par thématique

La demande du 2026-10-18 reprend l'organisation de
[Knowledge_AI_Engineering](https://github.com/speillet/Knowledge_AI_Engineering/tree/5fdbfe259e53d01361cf6337f6c494b4663db592) :
un dossier numéroté par thème, fichiers numérotés dans le thème et navigation
centrale. Les explications complètes et les cartes gardent leurs rôles distincts.

```text
vault/
  00-Accueil.md
  01-Parcours/
  40-features-matching/
    00-index.md
    41-sift.md                 # cartes
    42-orb.md                  # cartes
    references/
      41-sift.md               # explication complète
      42-orb.md
  50-calibration-geometrie/
    00-index.md
    51-ransac-homographie.md
    52-calibration-zhang.md
    references/
      51-ransac-homographie.md
      52-calibration-zhang.md
  80-detection-pose/
  110-tracking-association/
  130-evaluation-fiabilite/
  99-Ressources/
```

Les quatorze thèmes ont chacun un index et des fiches.
Le [sommaire](../vault/00-Accueil.md) expose cet état et l'inventaire décrit
les lacunes. `scripts/vault_sections.json` associe chaque dossier à son domaine,
son titre et son introduction, et sert au contrôleur.

## Ajouter une fiche et ses cartes

1. Choisir la thématique d'après le problème, puis le fichier numéroté : par
   exemple `41-sift.md` dans `40-features-matching`. Après neuf sujets, utiliser
   un rang explicite comme `40-010-nouveau-sujet.md` pour garder le thème stable.
2. Placer la fiche complète de même nom dans `references/`. Son front matter
   conserve le domaine, la provenance, la profondeur et les états éditoriaux.
3. Placer les cartes à la racine du thème. Leur cible est
   `CV::Pilote::<nom-du-répertoire>`. Le format du pilote reste Obsidian_to_Anki,
   modèle `CV-Pilote`, quatre champs et un seul gabarit.
4. Relier fiches et cartes, actualiser l'index du thème, l'accueil et l'inventaire.
5. Exécuter le contrôleur et les tests. Les nouveautés du pilote doivent encore
   passer les essais applicatifs avant généralisation.

Les guides, index et références ne contiennent aucun marqueur de début de note
sur une ligne isolée, même dans un bloc de code : le scan du plugin n'ignore pas
nécessairement ces exemples. Garder les gabarits hors du vault, dans `anki/`.

## Déplacer un contenu existant

Préserver l'ID pédagogique, son tag et le commentaire numérique Anki s'il existe.
Corriger liens Markdown, wikilinks depuis la racine, chemins des médias et deck
cible. Le changement de chemin ne crée pas un nouveau concept ou une nouvelle
identité. Le déplacement et le changement de deck doivent encore être observés
sur une vraie note déjà révisée avant de déclarer l'historique conservé.

Les 47 cartes du lot initial ont conservé leurs identifiants et textes lors du
reclassement. Le catalogue courant compte 52 fiches et 242 cartes dans les
14 thèmes. `python3 scripts/sync_catalog.py` met à jour index, accueil, inventaire
et parcours métiers ; `--check` détecte une navigation périmée sans écrire.
