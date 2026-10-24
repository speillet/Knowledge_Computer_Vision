# Spécification : base de connaissances de computer vision senior

**Branche de travail** : `feat/obsidian-pilot`
**Création** : 2026-10-18
**Révision éditoriale** : 6, revue des pôles et couverture thématique le 2026-10-18
**Statut** : cadrage en implémentation ; validation éditoriale et applicative suivie séparément
**Périmètre Spec Kit** : `specs/001-cv-knowledge-base`

**Demande** : constituer un vault Obsidian et des flashcards exportables vers
Anki, couvrant largement la computer vision classique et moderne, pour progresser
vers un profil senior généraliste en industrie.

**Public confirmé** : ingénieur CV depuis cinq ans, à l'aise en ML/DL,
expérimenté en segmentation sémantique. Lacunes prioritaires : méthodes classiques,
spécificités des techniques de vision, matching, calibration/recalage, tracking
et détection.

**Choix confirmés** : fiches complètes reliées à plusieurs cartes détaillées ;
prose en français, termes techniques anglais et noms originaux conservés ;
équations expliquées, pseudocode, code et illustrations utiles à la compréhension.
Les priorités détaillées et le pilote restent des propositions éditoriales.

**Décisions de démarrage, 2026-10-18** : l'utilisateur demande de commencer
l'implémentation. Le premier lot suit les sept sujets initiaux proposés ;
le client de révision confirmé est **AnkiDroid sur Android**. Le format d'export
reste expérimental pendant ce lot, sans validation technique ou pédagogique
anticipée. Les cartes initiales sont rédigées par un agent, provenance affichée.

**Organisation confirmée** : un répertoire par thématique, inspiré du dépôt
Knowledge_AI_Engineering indiqué par l'utilisateur. Les cartes et leurs fiches
de référence sont regroupées dans ce thème ; la navigation et les sous-decks
Anki suivent cette organisation.

**Pôles métiers, 2026-10-18** : l'utilisateur demande de couvrir six pôles
liés à des familles de métiers, de A (Image Understanding) à F (Vision Systems
& Deployment), décrits dans la [cartographie](curriculum.md). Décisions : les
pôles forment une surcouche des domaines existants, qui restent l'organisation
du vault ; la vague V0 reste consacrée aux lacunes exprimées (socle d'abord) ;
les specs sont enrichies d'abord et le report dans le vault suit par tâches.

La [revue de pertinence](review.md) décrit les lacunes de la première version,
les corrections et les décisions encore ouvertes. La largeur du catalogue,
la qualité des explications et le transfert en situation sont évalués séparément.

## Scénarios utilisateur et validation

### Parcours 1 — Comprendre une méthode (priorité P1)

Je veux partir du problème résolu pour comprendre fonctionnement, hypothèses,
paramètres et limites, puis retrouver les sources permettant d'approfondir.

**Justification** : combler les lacunes propres à la vision, en s'appuyant
sur les bases ML/DL acquises.

**Validation indépendante** : relire une fiche du pilote avec ses cartes selon
le [contrat pédagogique](learning-design.md), sans attendre le catalogue complet.

**Scénarios d'acceptation** :

1. En ouvrant une fiche, je retrouve problème, entrées/sorties, hypothèses,
   étapes, paramètres, limites, alternatives et sources primaires.
2. Pour chaque équation, les symboles, conventions et conditions de validité
   sont définis, avec les dimensions et unités pertinentes.
3. Pour un extrait de code, je sais s'il est illustratif ou exécuté et quelle
   explication algorithmique il matérialise.

### Parcours 2 — Choisir et diagnostiquer (priorité P1)

Je veux comparer les approches et raisonner sur les échecs d'un pipeline dans
des conditions industrielles : données imparfaites, occlusions, mouvement,
contraintes de ressources et exigences de mesure.

**Justification** : développer un jugement technique applicable aux projets.

**Validation indépendante** : traiter un cas de comparaison et un cas de
diagnostic, indépendamment de l'export Anki.

**Scénarios d'acceptation** :

1. Pour deux méthodes répondant au même besoin, je retrouve hypothèses,
   compromis, critères de choix et conditions d'évaluation.
2. Face à un symptôme, la réponse distingue causes possibles, observations
   à recueillir, vérifications discriminantes et limites du diagnostic.
3. Une métrique est expliquée avec son protocole et les défauts qu'elle peut masquer.
4. Face à un contexte différent des exemples corrigés, je peux proposer une
   méthode ou un diagnostic à partir des hypothèses et d'observations pertinentes.

### Parcours 3 — Réviser dans Obsidian et Anki (priorité P1)

Je veux réviser des questions contextualisées aux réponses développées, puis
revenir à la fiche de référence pour approfondir ou corriger le contenu.

**Justification** : associer richesse pédagogique et pratique du rappel.

**Validation indépendante** : exporter un ensemble représentatif dans un deck
d'essai, puis modifier et exporter à nouveau cet ensemble.

**Scénarios d'acceptation** :

1. Dans Anki, la question est compréhensible sans ouvrir la fiche et les critères
   de correction permettent d'évaluer ma réponse.
2. Paragraphes, listes, formules, image et code restent lisibles après export,
   sans disparition d'information essentielle.
3. À modèle de note inchangé, modifier une réponse met à jour la note attendue,
   sans doublon ni perte de l'historique de révision associé.
4. Un export sans modification conserve les nombres de notes et cartes attendus.
5. Le noyau attendu et les erreurs bloquantes permettent de corriger mon rappel,
   même si le verso comporte des approfondissements facultatifs.
6. La durée de révision et la charge quotidienne projetée sont connues avant
   de généraliser le format des cartes.

### Parcours 4 — Naviguer et suivre la couverture (priorité P2)

Je veux retrouver une notion par problème, méthode, domaine ou prérequis,
et identifier les sujets absents ou incomplets.

**Justification** : rendre visibles les lacunes et les compétences effectivement couvertes.

**Validation indépendante** : examiner la cartographie avant la rédaction
de l'ensemble des fiches.

**Scénarios d'acceptation** :

1. Chaque domaine présente un inventaire dont les états éditoriaux sont visibles.
2. Une méthode transverse possède une fiche canonique reliée depuis les domaines concernés.
3. Un prérequis ML/DL est lié ou rappelé lorsqu'il sert une spécificité de vision.

### Parcours 5 — Corriger et enrichir (priorité P2)

Je veux ajouter une variante, corriger une formule et actualiser une source
en conservant la cohérence des fiches et des cartes existantes.

**Justification** : éviter qu'une correction scientifique laisse des cartes contradictoires.

**Validation indépendante** : simuler une correction sur un sujet du pilote.

**Scénarios d'acceptation** :

1. Une correction permet d'identifier les cartes concernées.
2. Les affirmations dépendant d'une expérience ou d'une version conservent leur contexte.
3. Un changement de format ou d'export est vérifié sur le pilote avant généralisation.

### Parcours 6 — Se préparer à un pôle métier (priorité P2)

Je veux voir, pour une famille de métiers visée, les domaines et sujets à
travailler, leur profondeur cible et leur état, puis m'entraîner sur des cas
propres à ce métier.

**Justification** : relier la couverture générale aux attentes des postes
visés, sans dupliquer les fiches.

**Validation indépendante** : examiner le cadrage d'un pôle dans la cartographie
avant la rédaction de ses fiches.

**Scénarios d'acceptation** :

1. Pour un pôle, je retrouve périmètre, métiers indicatifs, domaines mobilisés,
   entrées clés et approfondissements, chacun avec son domaine d'accueil.
2. Un sujet servant plusieurs pôles, comme CLIP pour A et D, n'a qu'une fiche
   canonique, reliée depuis chacun d'eux.
3. L'avancement d'un pôle distingue entrées inventoriées, rédigées et relues,
   sans en déduire ma maîtrise ni mon aptitude à un poste.
4. Chaque pôle propose un cas de conception et un cas de diagnostic propres à
   ses métiers, corrigibles avec des critères explicites.

### Cas limites

- Repère, unité, transformation ou convention de coordonnées ambiguë.
- Méthode valable dans un cas particulier ou soumise à une dégénérescence.
- Score publié sans protocole ou variante clairement identifiés.
- Sources contradictoires, indisponibles ou devenues obsolètes.
- Carte mêlant plusieurs questions indépendantes et difficile à corriger.
- Formule ou média fonctionnant dans le vault mais pas dans le deck exporté.
- Modèle de note ou noms de champs différents selon l'installation d'Anki.
- Copie d'une carte conservant accidentellement l'identifiant d'une autre note.
- Note déplacée côté source ou supprimée côté destination.
- Plugin pressenti indisponible dans le catalogue courant.
- Suppression ou modification dans Anki non répercutée dans la source.
- Connaissance récitée correctement mais non transférée à un problème nouveau.
- Confusion entre calibration caméra et calibration des scores d'un modèle.
- Transformation d'image non répercutée sur les boîtes, masques ou paramètres caméra.
- Comparaison utilisant des données futures, des seuils réglés sur le test ou
  des coûts de pré/posttraitement non comptés.
- Fiche déclarée relue malgré une divergence centrale entre sources non résolue.
- Source citée qui ne soutient pas réellement l'affirmation, notamment après
  une rédaction assistée par un agent.
- Rendu correct sur Anki Desktop mais dégradé sur le client utilisé pour réviser.
- Sujet servant plusieurs pôles, rédigé deux fois de façon divergente.
- Intitulé de métier dont le contenu varie selon l'entreprise ou le secteur.
- Modèles et outils à évolution rapide (VLM, VLA, runtimes d'inférence) cités
  sans date ni version.

## Exigences

### Exigences fonctionnelles

- **FR-001** : la base DOIT cibler le profil confirmé ; les connaissances
  générales ML/DL servent de prérequis acquis et de rappels contextualisés.
- **FR-002** : la prose pédagogique DOIT être en français ; termes techniques
  anglais, acronymes et noms originaux sont conservés lorsqu'ils sont utiles.
- **FR-003** : la couverture DOIT inclure tous les domaines de la
  [cartographie](curriculum.md), avec des états explicites et un inventaire extensible.
- **FR-004** : l'inventaire DOIT distinguer problème, famille, méthode,
  variante et protocole d'évaluation.
- **FR-005** : chaque sujet DOIT indiquer les prérequis et notions connexes
  nécessaires, en distinguant dépendances obligatoires et liens thématiques,
  avec des liens permettant de combler un manque.
- **FR-006** : une fiche validée DOIT respecter le [contrat pédagogique](learning-design.md),
  avec justification des rubriques non applicables.
- **FR-007** : chaque équation DOIT expliquer symboles, conventions,
  conditions d'application et dimensions/unités pertinentes.
- **FR-008** : code et pseudocode DOIVENT servir une explication identifiée
  et être distingués ; un appel de bibliothèque seul ne suffit pas à expliquer la méthode.
- **FR-009** : tout exemple annoncé exécutable DOIT préciser dépendances,
  entrées et résultat attendu, et avoir été exécuté dans l'environnement indiqué.
  Un exemple non exécuté doit être signalé.
- **FR-010** : les visuels DOIVENT avoir une fonction explicative, une légende
  et une provenance ; les conditions de réutilisation doivent être conservées.
- **FR-011** : les propriétés d'une méthode DOIVENT distinguer garantie,
  approximation, hypothèse et résultat empirique, avec leurs limitations.
- **FR-012** : chaque fiche validée DOIT citer au moins une source primaire
  pertinente ; les affirmations centrales doivent être traçables jusqu'à leur source.
- **FR-013** : scores et coûts dépendant d'un protocole, matériel ou variante
  DOIVENT préciser ces conditions ; les informations susceptibles d'évoluer
  doivent avoir une date de vérification et une version si pertinente.
- **FR-014** : les cartes DOIVENT couvrir les familles pertinentes définies dans
  la section « Familles de cartes » du [contrat pédagogique](learning-design.md).
  Une famille non applicable doit être justifiée lors de la revue.
- **FR-015** : chaque carte DOIT définir un objectif de rappel et des critères
  de correction distinguant noyau attendu, approfondissement facultatif et
  erreurs bloquantes ; sa réponse reste développée sans plafond de longueur.
  Depuis la demande du 2026-10-24, tous les versos doivent être longs et
  explicatifs : mécanisme, exemple ou raisonnement suivi et limites utiles.
  Le seuil éditorial de repérage est décrit dans le contrat pédagogique ;
  le noyau attendu reste la règle de correction du rappel.
- **FR-016** : chaque carte DOIT être reliée à une fiche canonique et rester
  compréhensible dans son contexte de révision autonome.
- **FR-017** : fiche de référence et cartes DOIVENT avoir des rôles distincts ;
  aucun nombre uniforme de cartes par méthode n'est imposé.
- **FR-018** : les domaines prioritaires DOIVENT inclure des cas de choix ou
  de diagnostic sous contraintes industrielles, avec une justification évaluable.
- **FR-019** : les métriques DOIVENT être reliées à leur tâche et protocole ;
  les comparaisons doivent expliquer leurs limites de comparabilité.
- **FR-020** : les identifiants pédagogiques DOIVENT être stables et distincts
  des identités de synchronisation ; les relations fiche/carte/export sont traçables.
- **FR-021** : l'export DOIT préserver prose développée, formules, médias
  utiles et extraits de code lisibles.
- **FR-022** : création, mise à jour et export répété DOIVENT être vérifiés
  sans doublon ni perte d'historique à modèle de note inchangé.
- **FR-023** : suppression, déplacement, renommage et conflits source/destination
  DOIVENT avoir un comportement documenté et testé avant généralisation.
- **FR-024** : les fichiers source DOIVENT rester consultables et versionnables
  indépendamment de l'export ; le vault est la source pédagogique canonique.
- **FR-025** : la navigation DOIT permettre une recherche par domaine,
  problème, méthode et prérequis, au-delà de l'organisation en decks.
- **FR-026** : les états éditoriaux DOIVENT distinguer sujet inventorié, fiche
  rédigée, fiche relue, cartes rédigées et export vérifié ; ils sont distincts
  du niveau de maîtrise personnel de l'apprenant. Pour permettre ce suivi séparé,
  les cartes exportées DOIVENT porter leur domaine et leur famille.
- **FR-027** : les distinctions calibration/pose/recalage,
  flot/tracking/réidentification et détecteur/descripteur/matcher/validation
  géométrique DOIVENT être explicites dans les sujets concernés.
- **FR-028** : la production à grande échelle DOIT être précédée d'un pilote
  validant le contrat pédagogique, ses cas contrastés et les capacités d'export.
  Les travaux éditoriaux préparatoires restent possibles pendant le choix du plugin.
- **FR-029** : le catalogue DOIT rendre visibles périmètre, lacunes et procédure
  d'enrichissement ; sa couverture ne peut pas être déclarée exhaustive par défaut.
- **FR-030** : chaque méthode retenue DOIT avoir une entrée d'inventaire avec
  profondeur cible, compétences visées, dépendances et artefacts associés.
  Priorité, profondeur, état éditorial et maîtrise personnelle sont distincts.
- **FR-031** : les sujets concernés DOIVENT préciser le contrat des données :
  formes/types/plages, couleur, repères, unités, normalisation et propagation
  des changements de résolution, crop, padding ou coordonnées.
- **FR-032** : les fiches pertinentes DOIVENT relier hypothèses et échecs aux
  conditions d'acquisition, de cadence, de causalité temporelle et aux contraintes
  industrielles ; une hypothèse non applicable est explicitement écartée.
- **FR-033** : chaque famille du pilote DOIT proposer une baseline ou référence
  simple et une variation contrôlée, avec prédiction, résultat attendu ou observé
  et analyse. Une expérience analytique ou non exécutée doit être identifiée.
- **FR-034** : le pilote DOIT inclure deux cas distincts des exemples corrigés
  pour chacune de ses six familles : matching, calibration/géométrie, tracking,
  détection, segmentation classique et recalage 3D. Un cas porte sur le choix,
  l'autre sur le diagnostic, avec des critères de correction explicites.
- **FR-035** : l'essai pédagogique DOIT consigner une première tentative et
  un rappel lors d'une autre session aux dates choisies par l'apprenant,
  les ambiguïtés et corrections nécessaires, sans présupposer un taux de rétention.
  L'échantillon doit couvrir les six familles du pilote et chaque type de carte
  réellement produit ; sa sélection est consignée avant d'observer les résultats.
  L'essai mesure aussi la durée de révision par carte et estime la charge
  quotidienne du premier lot de production, sans plafond fixé a priori.
- **FR-036** : les propriétés générales et les particularités d'implémentation
  DOIVENT être sourcées séparément. Une divergence centrale non résolue empêche
  de valider l'affirmation et la fiche concernées.
- **FR-037** : une validation éditoriale DOIT conserver date, responsable,
  preuves et limites. Une auto-revue doit être identifiée ; les erreurs
  bloquantes ou ambiguïtés de correction doivent être résolues avant publication.
- **FR-038** : chaque fiche et chaque carte DOIT indiquer sa provenance de
  rédaction : apprenant, agent ou mixte. Une affirmation centrale rédigée par
  un agent n'est validée qu'après confrontation au passage de la source citée ;
  la présence d'une référence ne suffit pas.
- **FR-039** : le vault DOIT être organisé par répertoire thématique numéroté,
  avec index de section et sommaire central. Les cartes d'un thème et leurs
  références canoniques DOIVENT être regroupées dans son répertoire ; le deck
  cible suit la thématique. Le déplacement DOIT préserver les identifiants et
  mettre à jour liens, médias et contrôles. Une section sans contenu rédigé
  DOIT afficher son état, sans être comptée comme couverture acquise.
- **FR-040** : la [cartographie](curriculum.md) DOIT définir six pôles métiers,
  de A à F, chacun avec périmètre, métiers indicatifs, domaines mobilisés,
  entrées clés et approfondissements. Les pôles ne remplacent pas les domaines :
  chaque entrée propre à un pôle a un seul domaine d'accueil, et un sujet
  partagé entre pôles garde une seule fiche canonique.
- **FR-041** : chaque entrée d'inventaire DOIT indiquer les pôles qu'elle sert ;
  fiches et cartes exportées portent ces pôles en étiquettes, afin de suivre
  l'avancement par pôle séparément de la maîtrise personnelle.
- **FR-042** : chaque pôle DOIT proposer au moins un cas de conception de
  système et un cas de diagnostic propres à ses métiers, avec réponse de
  référence et critères de correction selon le contrat pédagogique.
- **FR-043** : les priorités DOIVENT suivre le principe « socle d'abord » :
  la vague V0 reste consacrée aux lacunes exprimées ; les entrées clés d'un pôle
  nouvellement introduites visent V1 et l'usage opérationnel, les autres V2.
  Une entrée déjà priorisée V0 conserve cette priorité même si plusieurs pôles
  la réutilisent. La couverture d'un pôle se
  mesure par ses artefacts et NE DOIT PAS être présentée comme une aptitude
  à un poste.

### Entités principales

- **Domaine / problème** : besoin visuel, entrées/sorties, contraintes,
  familles de méthodes et protocoles associés.
- **Méthode / variante** : approche identifiée, hypothèses, paramètres,
  prérequis, propriétés et références.
- **Fiche** : explication canonique d'un sujet, cartes liées, état éditorial
  et provenance de rédaction.
- **Carte pédagogique** : identifiant, question, objectif, réponse,
  critères de correction, références, fiche parente, domaine, famille,
  pôles et provenance de rédaction.
- **Note / carte Anki** : objets de destination ; une note peut générer
  plusieurs cartes selon le modèle. Leurs identités et nombres sont distincts.
- **Source** : référence primaire, localisation et contexte de version si nécessaire.
- **Cas industriel** : scénario, contraintes, hypothèses, alternatives,
  observations et critères d'une réponse satisfaisante.
- **Entrée de couverture** : sujet, domaine d'accueil, pôles servis, priorité,
  prérequis, états éditoriaux et lacunes.
- **Pôle métier** : périmètre, métiers indicatifs, domaines mobilisés, entrées
  clés et approfondissements avec leur domaine d'accueil, cas propres et
  avancement éditorial.
- **Compétence / profondeur cible** : résultat observable attendu pour un sujet,
  relié à ses artefacts et distinct de sa priorité ou de sa maîtrise personnelle.
- **Preuve de revue ou d'essai** : version de contenu, date, responsable,
  critères appliqués, résultat, limites et corrections éventuelles.

Une fiche « validée » a fait l'objet d'une revue argumentée selon le contrat
pédagogique, sans erreur bloquante ni divergence centrale non résolue.
Ce statut ne signifie ni export validé, ni maîtrise personnelle acquise.

## Critères de réussite

### Résultats mesurables

- **SC-001** : tous les domaines de la cartographie ont un inventaire initial ; chaque entrée
  de méthode retenue affiche profondeur, compétences, prérequis, états et liens
  vers ses artefacts existants. Une ligne générale de domaine ne suffit pas.
- **SC-002** : 100 % des fiches déclarées validées respectent le contrat
  pédagogique et possèdent une source primaire ; toute rubrique non applicable est justifiée.
- **SC-003** : 100 % des cartes publiées possèdent un identifiant distinct,
  une fiche parente, un objectif et un noyau de correction sans ambiguïté,
  avec approfondissements et erreurs bloquantes identifiés.
- **SC-004** : le pilote proposé couvre les sujets initiaux puis les extensions
  de `curriculum.md`, dont au moins une fiche de type métrique/protocole, et
  tous les contenus attendus : prose, liste, formule inline/en bloc, image,
  pseudocode et code.
- **SC-005** : tous les scénarios du [pilote d'export](research.md) ont un résultat
  consigné ; création, mise à jour et répétition passent sans doublon ni perte
  d'historique. Un échec de rendu essentiel empêche la validation de la solution.
- **SC-006** : les six familles définies dans FR-034 ont chacune un cas de choix
  et un cas de diagnostic inédits, soit douze cas. Leur correction précise
  adéquation à la tâche, hypothèses/conventions, justification, vérification
  discriminante et limites ; tous les critères applicables doivent être satisfaits
  pour déclarer un cas réussi. Les échecs de l'apprenant restent consignés.
- **SC-007** : une correction de fiche du pilote permet d'identifier et de
  mettre à jour les cartes concernées ; aucune carte ne reste orpheline.
- **SC-008** : les cartes retenues pour l'essai pédagogique ont un compte rendu
  de première tentative et de rappel différé, avec résultats, limites et
  corrections ; leur couverture des familles et types est explicitée, sans
  exclusion a posteriori des échecs. Aucune carte publiée ne conserve un défaut bloquant identifié.
  La durée de révision par carte et la charge quotidienne projetée sont
  consignées, avec la décision de conserver ou d'ajuster le format des cartes.
- **SC-009** : chaque famille du pilote dispose d'une référence et d'une
  variation contrôlée documentées ; les preuves distinguent prédiction,
  résultat observé, résultat analytique et exemple non exécuté.
- **SC-010** : 100 % des fiches et cartes publiées indiquent leur provenance
  de rédaction ; pour un contenu rédigé par un agent, la revue consigne les
  affirmations centrales confrontées à leur source.
- **SC-011** : chacun des six pôles a, dans la cartographie, son périmètre,
  ses métiers indicatifs, ses domaines mobilisés, ses entrées clés et
  approfondissements avec un domaine d'accueil unique, ainsi qu'un cas de
  conception et un cas de diagnostic avec réponses de référence, hypothèses,
  vérifications discriminantes et critères de correction ; les seuls énoncés
  ne suffisent pas à satisfaire ce critère.
- **SC-012** : aucun sujet partagé entre pôles n'a deux fiches canoniques ;
  l'avancement éditorial de chaque pôle est consultable dans le vault,
  distinct de la maîtrise personnelle.
- **SC-013** : chacun des quatorze domaines comporte des fiches et cartes
  effectives pour les entrées retenues dans le lot de couverture. La matrice
  distingue cette couverture thématique, le traitement détaillé de chaque
  algorithme, les variantes seulement introduites et les sujets restant à rédiger.
  Aucun de ces états ne vaut validation d'export ou compétence professionnelle.

## Hypothèses et décisions ouvertes

- Les domaines de la cartographie traduisent l'ambition de couverture large ; les
  spécialisations et variantes seront enrichies par inventaire.
- Les six pôles et leurs intitulés de métiers proviennent de la demande de
  l'utilisateur du 2026-10-18. Les intitulés sont indicatifs : leur contenu
  varie selon les entreprises.
- Pour le pôle C, la planification de trajectoire et le contrôle sont hors
  périmètre ; seule la perception qui les alimente est couverte.
- Le pilote technique reste un échantillon de validation. La demande actuelle
  autorise la préparation éditoriale des quatorze domaines et des six pôles
  avant son achèvement ; les contenus gardent leur statut rédigé et leur format
  d'export provisoire. L'adoption et la diffusion automatisée à grande échelle
  restent conditionnées aux essais, notamment à l'historique et au rendu mobile.
- Priorités, niveaux de profondeur, pilote en deux étages et protocole de
  transfert sont proposés à partir des lacunes exprimées ; ils ne réduisent
  pas la couverture finale et restent ajustables après relecture.
- Aucun volume total de cartes, calendrier ou temps quotidien de révision
  n'a été imposé par l'utilisateur. Le pilote mesure la charge au lieu de la borner.
- La répartition de la rédaction entre l'apprenant et un agent n'est pas fixée.
  Proposition : l'agent rédige, l'apprenant confronte les affirmations centrales
  aux sources et reformule au moins l'objectif et le noyau de chaque carte.
  FR-038 impose seulement la traçabilité de ce choix.
- Proposition de périmètre : 001 couvre le cadre, le contrat et le pilote.
  La production du catalogue se ferait ensuite par lots, avec leur propre spec
  ou un suivi de couverture dans le vault ; ce découpage reste à décider.
- Le nom du plugin oublié reste incertain. Le candidat et ses limites sont
  décrits dans [la recherche d'interopérabilité](research.md).
- Plugin, syntaxe finale, modèles de notes et politique de suppression
  seront fixés pendant la conception après un pilote dans un deck d'essai.
- La constitution Spec Kit est encore un modèle non ratifié ; ses exemples
  ne deviennent pas des règles du projet par ce brouillon. Principes candidats
  à y déplacer après ratification : langue (FR-002), statut des propriétés et
  traçabilité des sources (FR-011, FR-012, FR-036), vault canonique (FR-024),
  séparation des états éditoriaux et de la maîtrise (FR-026).
- La destination de `to-spec` n'est pas choisie. Ce brouillon local utilise
  Spec Kit et ne publie aucune issue.
- Cette phase inclut la rédaction des contenus manquants par thème, à la demande
  de l'utilisateur. Elle exclut l'installation dans les applications personnelles,
  un synchroniseur sur mesure et un nouveau cursus général ML/DL.
  Le plan B `.apkg` est implémenté dans le lot du 2026-10-24 pour l'import direct
  sur Android, conformément au [contrat d'export](../../docs/export-apkg.md).
  Les preuves du moteur Anki restent distinctes de la validation mobile.
- Les cartes soutiennent les compétences visées ; un nombre de cartes ou leur
  mémorisation ne peut pas certifier à lui seul le statut de senior.
