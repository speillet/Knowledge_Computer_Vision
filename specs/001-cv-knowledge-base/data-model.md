# Modèle de données du pilote

## Fiche canonique

Front matter : `id`, `type`, `domaine`, `poles`, `priorite`, `profondeur`, `statut`,
`provenance`, `revision`, `tags`. L'ID est stable et indépendant du chemin.
Les prérequis, compétences, notions connexes, sources et cartes sont des liens
dans le corps, lisibles sans plugin. `provenance: agent` décrit la rédaction.

États distincts : inventorié → rédigé → relu. La relecture nomme son responsable
et sa portée ; l'auto-revue ne signifie pas validation indépendante.
L'export et la maîtrise personnelle ne sont pas des états de rédaction.

## Carte

Une note `CV-Pilote` comprend quatre champs ordonnés : `ID`, `Question`,
`Reponse`, `Source`. Un seul gabarit produit une seule carte, sans inverse.
Le champ `ID` est un identifiant pédagogique tel que `CV-SIFT-001` ; il reste
inchangé lors d'une correction. `Source` relie la fiche et le passage primaire.
Au-dessus du bloc, les métadonnées donnent objectif, famille et provenance.
Les tags de domaine, famille et ID sont également exportés.
Le champ `poles` est une liste non vide de lettres uniques A à F ; les cartes
portent les mêmes rattachements en tags `pole::A` à `pole::F`. Ces pôles décrivent
un parcours, pas une aptitude certifiée. Le contrôleur refuse lettres inconnues,
doublons et désaccords entre la fiche et ses cartes. Les cas métiers portent
en plus `cas_pole::<lettre>::conception` ou `cas_pole::<lettre>::diagnostic`.

Le commentaire numérique ajouté par le plugin identifie une note Anki : il est
distinct de l'ID pédagogique, absent avant la première synchronisation, conservé
lors d'un déplacement et retiré seulement lors de la création d'une nouvelle note.

## Couverture et preuves

L'inventaire affiche par entrée domaine, type, priorité, profondeur, prérequis,
compétences, fiche/cartes et lacunes. Il ne déduit pas la maîtrise de la présence
d'une carte. Les preuves dans le journal du pilote précisent environnement,
date, responsable, observation et limites ; une ligne vide signifie « non testé ».

## Intégrité

- Un ID de fiche et un ID de carte sont uniques dans leur catégorie.
- Une carte possède une fiche existante et une source primaire explicite.
- Chaque réponse contient noyau attendu, approfondissement et erreurs bloquantes.
- Un lien relatif pointe vers un fichier existant à l'intérieur du vault.
- Un export vérifié n'est déclaré qu'après création, répétition, mise à jour,
  conservation de l'historique et contrôle du rendu sur AnkiDroid.
