# Reconnaissance biométrique, ArcFace et PAD — cartes

Fiche : [[70-reconnaissance-representations/references/75-embeddings-biometrie|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::70-reconnaissance-representations

## CV-BIOMETRIE-001

Objectif : distinguer identité et présentation. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-BIOMETRIE-001
Question: Un embedding ArcFace séparant bien les identités prouve-t-il qu’une présentation est authentique ?
Reponse: **Noyau attendu** : Non : la comparaison d’identité et PAD ont des cibles et données d’évaluation distinctes.

**Approfondissement** : Mesurer chaque composant dans le système réel ; un fort score d’identité peut aussi venir d’une reproduction.

**Différence des cibles** : la reconnaissance compare une acquisition à une identité de référence. La détection de présentation cherche à distinguer certains types d'acquisition ou d'attaque selon un autre protocole. Une reproduction peut conserver une apparence d'identité très proche sans être une présentation authentique.

**Exemple construit** : une photo nette peut produire un embedding proche de celui de la personne ; cette proximité répond à une question d'apparence, pas à la présence physique de cette personne au moment de l'acquisition. Définir et évaluer les deux sorties avec des données adaptées, puis leur intégration dans le système. Une détection de visage correcte ne résout pas non plus la vérification d'identité. Le propos reste un contrat technique de perception et d'évaluation ; aucune conformité, certification ou garantie de résistance à toute présentation n'est déduite du seul modèle d'embedding.

**Erreurs bloquantes** : Déduire la liveness de la similarité faciale.
Source: [[70-reconnaissance-representations/references/75-embeddings-biometrie|Fiche complète]] ; [Deng et al., ArcFace, objectif de marge angulaire](https://arxiv.org/abs/1801.07698) ; [Ngan et al. 2023, NISTIR 8491, résumé PAD](https://www.nist.gov/publications/face-analysis-technology-evaluation-fate-part-10-performance-passive-software-based).
Tags: cv::pilote cv::d07 famille::comparaison cv_id::CV-BIOMETRIE-001 provenance::agent pole::E
END

## CV-BIOMETRIE-002

Objectif : choisir un point d’exploitation. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-BIOMETRIE-002
Question: Pourquoi l’EER ne suffit-il pas pour un système exploitant un seuil à très faible FMR ?
Reponse: **Noyau attendu** : Il décrit un point d’équilibre qui peut différer fortement du seuil visé ; mesurer FNMR et autres erreurs au point requis.

**Approfondissement** : Préciser données, acquisition et sous-groupes ; une moyenne ne donne pas toute la courbe.

**Lecture de la courbe** : déplacer le seuil modifie simultanément comparaisons acceptées à tort et identités rejetées à tort. L'EER désigne une égalité de ces taux dans un protocole donné ; un produit visant un très faible taux de fausse correspondance fonctionne généralement ailleurs sur la courbe.

**Évaluation proposée** : fixer le seuil sur des données de réglage, puis mesurer le taux de faux non-matches au niveau de FMR visé sur un test indépendant. Consigner qualité d'acquisition, population, enrôlement et taille des ensembles ; examiner les sous-groupes et l'incertitude statistique lorsqu'elle est pertinente. Des échecs de capture ajoutent encore des événements au niveau système. Une bonne valeur moyenne ne prédit donc pas toutes les conditions d'exploitation. Le point de fonctionnement et les unités de comparaison doivent rester visibles pour que deux résultats de reconnaissance soient interprétables.

**Erreurs bloquantes** : Assimiler EER et performance à tout seuil.
Source: [[70-reconnaissance-representations/references/75-embeddings-biometrie|Fiche complète]] ; [NIST FRTE 1:1, définitions FMR/FNMR, consulté le 2026-10-20](https://pages.nist.gov/frvt/html/frvt11.html) ; comparaison de points d’exploitation déduite de la courbe d’erreurs.
Tags: cv::pilote cv::d07 famille::evaluation cv_id::CV-BIOMETRIE-002 provenance::agent pole::E
END
