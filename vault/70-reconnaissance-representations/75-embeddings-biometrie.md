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

**Erreurs bloquantes** : Déduire la liveness de la similarité faciale.
Source: [[70-reconnaissance-representations/references/75-embeddings-biometrie|Fiche complète]] ; [ArcFace, objectif et évaluation](https://arxiv.org/abs/1801.07698) ; [NIST FRTE 1:1, FMR/FNMR](https://pages.nist.gov/frvt/html/frvt11.html).
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

**Erreurs bloquantes** : Assimiler EER et performance à tout seuil.
Source: [[70-reconnaissance-representations/references/75-embeddings-biometrie|Fiche complète]] ; [ArcFace, objectif et évaluation](https://arxiv.org/abs/1801.07698) ; [NIST FRTE 1:1, FMR/FNMR](https://pages.nist.gov/frvt/html/frvt11.html).
Tags: cv::pilote cv::d07 famille::evaluation cv_id::CV-BIOMETRIE-002 provenance::agent pole::E
END
