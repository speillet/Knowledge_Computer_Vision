# Détection open-vocabulary et grounding — cartes

Fiche : [[80-detection-pose/references/83-detection-open-vocabulary|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::80-detection-pose

## CV-OPENVOC-001

Objectif : séparer les sorties multimodales. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-OPENVOC-001
Question: Pourquoi un classement CLIP d’une image ne remplace-t-il pas directement un détecteur open-vocabulary ?
Reponse: **Noyau attendu** : Le classement image porte sur l’image globale ; la détection doit aussi localiser les instances avec un protocole de sortie adapté.

**Approfondissement** : Une image peut contenir plusieurs objets et candidats ; grounding, classification et génération ne partagent pas toutes les mêmes métriques.

**Décomposition de la sortie** : une similarité globale image–texte peut indiquer qu'un contenu est compatible avec une description. Un détecteur doit en plus proposer des positions et distinguer plusieurs occurrences, avec leurs classes ou relations au texte. Un score sur l'image entière ne détermine ni ces boîtes ni leur nombre.

**Exemple construit** : une scène avec deux tasses et une assiette peut bien correspondre au texte « tasse » sans fournir la localisation de chaque tasse. L'évaluation de détection doit vérifier instances, coordonnées et objets manqués, y compris lorsque le prompt est absent de l'image. Un grounding référentiel peut demander encore une autre sortie, comme « la tasse à gauche de l'assiette ». Définir annotations, négatifs, seuils et métriques selon ce contrat. Le langage élargit l'interface des candidats ; il ne dispense pas de vérifier la précision spatiale et les confusions du domaine.

**Erreurs bloquantes** : Prendre un score image–texte pour une boîte correctement localisée.
Source: [[80-detection-pose/references/83-detection-open-vocabulary|Fiche complète]] ; [OWL-ViT, §3.1 : adaptation à la localisation](https://arxiv.org/abs/2205.06230) ; [Grounding DINO, §§3.2–3.3](https://arxiv.org/abs/2303.05499).
Tags: cv::pilote cv::d08 famille::comparaison cv_id::CV-OPENVOC-001 provenance::agent pole::A pole::D
END

## CV-OPENVOC-002

Objectif : choisir un système à catalogue évolutif. Famille : conception. Provenance : agent.

START
CV-Pilote
ID: CV-OPENVOC-002
Question: Cas A — conception : un catalogue de produits change chaque mois. Comment choisir détecteur fermé réentraîné ou open-vocabulary ?
Reponse: **Noyau attendu** : Définir nouveautés, erreurs acceptables et budget d’annotation ; comparer les deux sur anciens/nouveaux produits avec négatifs, seuils figés et coût de maintenance.

**Approfondissement** : Mesurer localisation, rejet et latence ; une approche hybride peut être justifiée. Le prompt seul ne garantit pas la reconnaissance d’une nouveauté.

**Décision proposée** : comparer coût des annotations et du réentraînement à celui du réglage des formulations, de l'analyse des nouveaux faux positifs et de la maintenance du vocabulaire. Un catalogue changeant peut favoriser une interface textuelle, mais une catégorie visuellement très spécifique peut rester difficile à décrire ou à reconnaître sans données ciblées.

**Essai de transfert** : réserver de nouveaux produits inconnus du réglage, ajouter des catégories proches et des images sans cible, puis mesurer localisation et rejet au point de fonctionnement utile. Conserver aussi les anciens produits pour détecter une régression. Le choix peut être hybride, avec un détecteur spécialisé pour le fréquent et une autre procédure pour les nouveautés. La comparaison doit annoncer disponibilité des données et interventions humaines, plutôt qu'utiliser une démonstration sélectionnée comme preuve de maintenance facile.

**Erreurs bloquantes** : Choisir sur une démonstration favorable sans classes absentes ni protocole.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[80-detection-pose/references/83-detection-open-vocabulary|Fiche complète]] ; Cas et protocole conçus par le projet ; architectures de référence : [OWL-ViT, §3](https://arxiv.org/abs/2205.06230) et [Grounding DINO, §3](https://arxiv.org/abs/2303.05499).
Tags: cv::pilote cv::d08 famille::conception cv_id::CV-OPENVOC-002 provenance::agent pole::A pole::D cas_pole::A::conception
END

## CV-OPENVOC-003

Objectif : vérifier la spécificité du texte. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-OPENVOC-003
Question: Un prompt large donne des boîtes sur des objets apparentés mais hors cible. Que tester ?
Reponse: **Noyau attendu** : Définition de classe, formulations/négatifs et score de région sur validation ; inspecter les confusions et annotations.

**Approfondissement** : Évaluer un rejet plutôt que supposer le seuil transférable à toutes descriptions.

**Pourquoi le texte peut être en cause** : une description générale peut correspondre à plusieurs catégories visuelles que la taxonomie industrielle sépare. Un modèle peut donc retourner une région plausible pour le langage courant mais incorrecte pour le besoin. Un seuil unique ne résout pas nécessairement cette ambiguïté.

**Enquête construite** : consigner les classes visées et exclues, comparer des formulations plus précises et des négatifs proches sur validation, puis inspecter les régions et annotations. Séparer défaut de localisation et confusion de vocabulaire. Évaluer aussi l'absence de cible, car choisir le meilleur candidat ne prouve pas sa présence. Une nouvelle formulation doit être figée avant le test final. Si le domaine ne fournit pas d'indice discriminant visible, un meilleur prompt peut rester insuffisant ; l'interface doit alors permettre refus ou vérification plutôt que garantir une catégorie exacte.

**Erreurs bloquantes** : Conclure qu’un modèle open-vocabulary connaît la taxonomie métier sans supervision.
Source: [[80-detection-pose/references/83-detection-open-vocabulary|Fiche complète]] ; Diagnostic proposé par le projet à partir du conditionnement textuel ; [Grounding DINO, §§3.2–3.3](https://arxiv.org/abs/2303.05499).
Tags: cv::pilote cv::d08 famille::diagnostic cv_id::CV-OPENVOC-003 provenance::agent pole::A pole::D
END
