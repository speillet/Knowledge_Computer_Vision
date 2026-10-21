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

**Erreurs bloquantes** : Présenter une évaluation offline comme performance temps réel sans latence.
Source: [[90-segmentation/references/94-sam-sam2|Fiche complète]] ; Conséquence du protocole temporel et d’interaction proposé par le projet ; [SAM 2, §§3–4 : tâche et modèle](https://arxiv.org/abs/2408.00714).
Tags: cv::pilote cv::d09 famille::evaluation cv_id::CV-SAM-003 provenance::agent pole::A pole::D
END
