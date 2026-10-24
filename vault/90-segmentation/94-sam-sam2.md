# SAM, SAM 2 et segmentation guidée en vidéo — cartes

Fiche : [[90-segmentation/references/94-sam-sam2|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::90-segmentation

## CV-SAM-001

Objectif : définir la sortie SAM. Famille : comprehension. Provenance : agent.

START
CV-Pilote
ID: CV-SAM-001
Question: SAM attribue-t-il automatiquement une classe sémantique à chaque pixel ?
Reponse: **Noyau attendu** : Non : son contrat central est le masque guidé par prompt, pas une taxonomie sémantique complète.

**Approfondissement** : Une classe peut venir d’un autre composant ou d’une annotation ; ne pas attribuer le prototype texte du papier à tout checkpoint standard.

**Lecture de la condition** : un point, une boîte ou un masque guide la région d'intérêt. La segmentation répond à ce conditionnement ; attribuer ensuite un nom de classe demande une autre information ou un autre composant. Un masque très précis peut donc être utile pour annoter sans fournir directement une taxonomie complète.

**Exemple construit** : un utilisateur désigne une pièce parmi plusieurs objets. Le masque produit délimite une région candidate, mais ne démontre pas qu'il s'agit du bon type de pièce ni qu'aucun autre objet n'a été oublié. Évaluer qualité de frontière, ambiguïtés et effort de correction avec des prompts comparables. Si une pipeline ajoute un texte ou un détecteur, préciser cette nouvelle chaîne au lieu d'attribuer ses sorties à SAM seul. Le contrat dépend du checkpoint et de l'interface réellement utilisés ; une possibilité explorée dans un papier n'est pas automatiquement une fonction disponible de chaque modèle distribué.

**Erreurs bloquantes** : Confondre masque d’objet et classe métier.
Source: [[90-segmentation/references/94-sam-sam2|Fiche complète]] ; [SAM, §3 et preuve de concept text-to-mask §7.5](https://arxiv.org/abs/2304.02643).
Tags: cv::pilote cv::d09 famille::comprehension cv_id::CV-SAM-001 provenance::agent pole::A pole::D
END

## CV-SAM-002

Objectif : situer SAM 2 en vidéo. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-SAM-002
Question: Que rajoute SAM 2 par rapport à une segmentation indépendante de chaque frame ?
Reponse: **Noyau attendu** : Mémoire et propagation de masques guidées dans le temps selon le protocole.

**Approfondissement** : Préciser prompts, corrections, causalité et version ; cela ne fournit pas seul un MOT autonome et classifié de tous objets.

**Rôle de la mémoire** : traiter chaque frame isolément oblige à réinterpréter la cible à partir des seules informations de cette frame et de son prompt. Une mémoire temporelle peut transporter des observations et interactions précédentes pour produire une séquence de masques cohérente. Cette information peut aider, mais peut aussi conserver une confusion.

**Exemple de diagnostic** : après croisement de deux objets semblables, un masque peut rester bien dessiné sur le mauvais objet. Il faut alors examiner identité, visibilité, prompts et contenu mémorisé plutôt que seulement la qualité de contour. Comparer propagation et segmentation indépendante avec le même budget de données et de correction. Le système ne crée pas automatiquement toutes les classes et toutes les naissances de pistes. Définir ce que l'utilisateur initialise et ce que le modèle doit découvrir est indispensable pour comparer à un tracker multiobjet autonome ou à un annotateur interactif.

**Erreurs bloquantes** : Assimiler propagation de masklets et système complet de suivi d’objets.
Source: [[90-segmentation/references/94-sam-sam2|Fiche complète]] ; [SAM 2, §4 : mémoire, prompts et masklets](https://arxiv.org/abs/2408.00714).
Tags: cv::pilote cv::d09 famille::comparaison cv_id::CV-SAM-002 provenance::agent pole::A pole::D
END

## CV-SAM-003

Objectif : contrôler le futur dans l’évaluation. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-SAM-003
Question: Pourquoi une annotation vidéo interactive avec corrections sur des frames futures ne se compare-t-elle pas directement à un tracker causal ?
Reponse: **Noyau attendu** : Elle dispose d’informations différentes ; budget d’interaction et accès temporel modifient la tâche.

**Approfondissement** : Rapporter délai, frames consultées et qualité finale sous même contrat avant de comparer.

**Différence d'information** : corriger un masque après avoir vu la suite peut résoudre une ambiguïté qui était réelle à l'instant de la frame. L'annotation finale profite alors d'observations et d'interventions indisponibles pour une décision immédiate. La qualité finale et la disponibilité à temps sont deux propriétés distinctes.

**Protocole proposé** : annoncer frames consultées, nombre de clics ou corrections, propagation autorisée et instant où chaque sortie devient disponible. Comparer soit à budget identique, soit comme un compromis explicitement différent. Conserver les pertes et ambiguïtés au lieu de les effacer par un reset non compté. Un outil interactif peut être excellent pour produire une vérité terrain sans être un tracker autonome déployable avec les mêmes performances. Cette distinction protège les conclusions du benchmark et relie le coût humain, le temps et la qualité au véritable usage du système.

**Erreurs bloquantes** : Présenter une évaluation offline comme performance temps réel sans latence.
Source: [[90-segmentation/references/94-sam-sam2|Fiche complète]] ; Conséquence du protocole temporel et d’interaction proposé par le projet ; [SAM 2, §§3–4 : tâche et modèle](https://arxiv.org/abs/2408.00714).
Tags: cv::pilote cv::d09 famille::evaluation cv_id::CV-SAM-003 provenance::agent pole::A pole::D
END
