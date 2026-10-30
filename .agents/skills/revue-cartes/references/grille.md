# Grille de revue des cartes

Critères détaillés de l'étape 2 du skill. Ils reprennent le contrat
pédagogique (`specs/001-cv-knowledge-base/learning-design.md`) et les
exigences FR-007 à FR-016, FR-031, FR-032 et FR-036 de la spec.

1. [Exactitude](#exactitude)
2. [Pertinence pour un profil senior](#pertinence-pour-un-profil-senior)
3. [Corrigibilité](#corrigibilité)
4. [Développement](#développement)
5. [Cohérence](#cohérence)
6. [Signaux d'alerte](#signaux-dalerte)
7. [Gravité](#gravité)

## Exactitude

- Chaque affirmation centrale est-elle soutenue par **le passage cité**, et
  pas seulement par le document en général ?
- Les propriétés générales (article) et les particularités d'implémentation
  (documentation ou code, avec version ou commit) ont-elles chacune leur
  source (FR-036) ?
- Garantie, approximation, hypothèse et résultat empirique sont-ils
  distingués (FR-011) ?
- Un seuil, un score ou un coût est-il accompagné de son protocole, de sa
  variante ou de son matériel (FR-013) ?
- Chaque équation définit-elle ses symboles, ses conventions, ses conditions
  de validité et ses unités (FR-007) ?
- Le contrat des données est-il explicite : repère, origine des coordonnées,
  normalisation, effet d'un resize, d'un crop ou d'un padding (FR-031) ?
- Le statut du code est-il clair : illustratif, ou exécuté avec son
  environnement et son résultat (FR-008, FR-009) ?

Pour vérifier :

- **Article** : ouvrir la section citée et relire la phrase ou l'équation
  exacte. WebFetch ne lit pas le texte des PDF arXiv ; utiliser la version
  HTML `https://ar5iv.labs.arxiv.org/html/<identifiant>`. Le pseudocode y est
  souvent une image : le corroborer avec le code officiel. Une contradiction
  entre l'article et une implémentation, même sur une frontière comme `>`
  contre `≥`, est consignée avec les deux contextes, pas tranchée en silence.
- **Section citée** : une affirmation vraie mais attribuée à la mauvaise
  section reste « non soutenue » tant que la référence n'est pas corrigée.
- **Code** : consulter le fichier au commit cité, avec les numéros de ligne.
- **Documentation** : consulter la version citée (par exemple OpenCV 4.13).
- **Calcul numérique** : le refaire. `examples/pilot_math.py` contient déjà
  des calculs du pilote ; un nouveau calcul se fait dans un fichier
  temporaire hors du dépôt.

| Verdict | Sens | Suite |
| --- | --- | --- |
| Confirmé | Le passage dit la même chose, dans les mêmes conditions | Rien |
| Imprécis | Vrai sous une condition non dite, ou formulation trop forte | Corriger la nuance |
| Faux | Le passage ou un calcul contredit l'affirmation | Corriger fiche puis cartes |
| Non soutenu | Peut-être vrai, mais la source citée ne le dit pas | Trouver le bon passage ou retirer l'affirmation |
| Non vérifiable | Source inaccessible ou payante | Le dire dans le rapport ; ne pas confirmer |

## Pertinence pour un profil senior

L'apprenant a cinq ans d'expérience en CV, maîtrise le ML/DL et la
segmentation sémantique, et cherche à combler ses lacunes : méthodes
classiques, matching, calibration et recalage, tracking, détection.

- La carte entraîne-t-elle un mécanisme, un raisonnement, un choix, un
  diagnostic ou une évaluation utile en projet ?
- Un senior doit-il savoir y répondre sans chercher ? Une valeur qu'on
  consulte dans la documentation n'a pas sa place dans une carte, sauf si elle
  sert un raisonnement (128 = 4×4×8 explique la structure du descripteur SIFT)
  ou prévient une erreur fréquente (norme de Hamming pour ORB).
- L'objectif est-il unique et la famille correspond-elle à la question ?
- Une autre carte du sujet teste-t-elle déjà le même noyau ?
- La carte rappelle-t-elle un cours général de DL au lieu de la spécificité
  vision (FR-001) ?
- Le cas industriel est-il plausible et présenté comme un raisonnement du
  projet, et non comme un résultat publié ?

## Corrigibilité

- La question se comprend-elle sans ouvrir la fiche ?
- Le recto évite-t-il le terme clé, le titre ou l'extrait de source qui donne
  la réponse ?
- Le **noyau attendu** est-il un ensemble fini de points vérifiables ? Un
  détail de l'**approfondissement** ne doit pas être nécessaire pour réussir.
- Les **erreurs bloquantes** sont-elles des contresens plausibles (confusion
  de tâche, de repère ou d'hypothèse), et non des absurdités que personne ne
  commettrait ?
- Une comparaison forme-t-elle un seul objectif cohérent, plutôt que deux
  questions juxtaposées ?
- La réponse atteint-elle le plancher du contrat (180 mots lexicaux, contrôlé
  par `scripts/learning_path.py` et l'inventaire) ? Il n'y a pas de plafond.
  Le plancher repère les réponses trop brèves ; il ne mesure pas la qualité.
- Le noyau reste-t-il assez court pour être noté sans hésiter, même quand le
  verso est long ? Un noyau trop composite justifie une proposition de carte
  complémentaire, pas un noyau plus vague.

## Développement

Le contrat demande des réponses développées. Un bon développement aide à
retrouver la réponse et à vérifier qu'elle s'applique :

- il explique le **mécanisme** plutôt que d'énoncer une conclusion ;
- il suit un **exemple interprété** ou un **calcul construit**, avec ses
  hypothèses et ses unités ;
- il nomme les **hypothèses** et les **limites** utiles à l'objectif ;
- il donne un **contrôle discriminant** quand la carte porte sur un choix ou un
  diagnostic.

À éviter : paraphraser le noyau, répéter un paragraphe de diagnostic d'une autre
carte, empiler des faits sans lien avec la question, présenter un calcul ou un
protocole du projet comme un résultat publié.

## Cohérence

- La carte s'accorde-t-elle avec la fiche, et la fiche avec les autres
  sujets ? Chercher les notions partagées par `grep` (IoU, résidu, seuil,
  repère…).
- Les notations, les unités et les noms de variables sont-ils ceux de la
  fiche ?
- Le tag `famille::` correspond-il à la famille de la ligne d'en-tête ?
  L'inventaire signale les écarts.
- Le champ `Source` contient-il le wikilink vers la fiche et une source HTTPS
  avec sa section, sa ligne ou son commit ?
- Les affirmations qui dépendent d'une version ou d'une date sont-elles datées ?
- Le format respecte-t-il le [modèle de carte](format-carte.md) ?

## Signaux d'alerte

| Signal | Pourquoi c'est suspect | Que vérifier |
| --- | --- | --- |
| « garantit », « invariant », « toujours », « optimal » | Une garantie est rare en vision | Conditions exactes dans la source |
| Seuil présenté comme universel (0,5, 0,7, 0,8…) | Un seuil dépend du jeu de données et du protocole | Origine du seuil et validation |
| Chiffre sans protocole, variante ni matériel | Il n'est pas comparable | Conditions de mesure (FR-013) |
| Code présenté comme exécuté | Résultat peut-être inventé | Environnement et sortie réelle |
| Recto contenant le mot clé de la réponse | La révision devient de la reconnaissance | Reformuler le contexte |
| Deux questions dans une carte | Notation ambiguë | Scinder ou unifier l'objectif |
| Noyau qui exige un détail facultatif | Échecs injustes | Déplacer le détail en approfondissement |
| Source sans section, ligne ni commit | Affirmation invérifiable | Préciser le passage |
| Approximation présentée comme égalité | Contresens appris | Distinguer « approxime » et « égale » |
| Repère, unité ou origine des coordonnées implicites | Erreur de calcul en projet | Contrat des données (FR-031) |
| Défaut d'une bibliothèque présenté comme propriété de la méthode | Confusion méthode/implémentation | Source scientifique distincte (FR-036) |
| Lien vers la fiche absent ou différent du dossier | Carte orpheline ou mal rangée | Wikilink et domaine |
| Titre, tableau, citation ou `$` hors formule dans un champ | Le paquet Anki refuse la carte | Anomalie de conversion de l'inventaire |
| Réponse allongée par paraphrase ou répétition | Charge de révision sans gain | Ce que chaque paragraphe ajoute à l'objectif |
| Calcul ou ablation sans mention « construit » ou « proposé » | Confusion avec un résultat mesuré | Origine du chiffre et preuve d'exécution |

## Gravité

- **Bloquant** : erreur scientifique ou numérique ; réponse impossible à noter
  sans ambiguïté ; réponse révélée au recto ; contradiction avec la fiche.
- **Important** : formulation trop forte ou nuance manquante qui induit en
  erreur ; source qui ne soutient pas l'affirmation ; objectif double ;
  doublon ; contrat des données implicite là où il compte ; réponse sous le
  plancher ou refusée par la conversion du paquet.
- **Mineur** : style, notation incohérente sans conséquence, référence trop
  vague mais exacte, lien améliorable.
