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

**Erreurs bloquantes** : Prendre un score image–texte pour une boîte correctement localisée.
Source: [[80-detection-pose/references/83-detection-open-vocabulary|Fiche complète]] ; [OWL-ViT, méthode](https://arxiv.org/abs/2205.06230) ; [Grounding DINO, méthode](https://arxiv.org/abs/2303.05499).
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

**Erreurs bloquantes** : Choisir sur une démonstration favorable sans classes absentes ni protocole.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[80-detection-pose/references/83-detection-open-vocabulary|Fiche complète]] ; [OWL-ViT, méthode](https://arxiv.org/abs/2205.06230) ; [Grounding DINO, méthode](https://arxiv.org/abs/2303.05499).
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

**Erreurs bloquantes** : Conclure qu’un modèle open-vocabulary connaît la taxonomie métier sans supervision.
Source: [[80-detection-pose/references/83-detection-open-vocabulary|Fiche complète]] ; [OWL-ViT, méthode](https://arxiv.org/abs/2205.06230) ; [Grounding DINO, méthode](https://arxiv.org/abs/2303.05499).
Tags: cv::pilote cv::d08 famille::diagnostic cv_id::CV-OPENVOC-003 provenance::agent pole::A pole::D
END
