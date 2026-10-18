# Inspection : golden template, PatchCore et PaDiM — cartes

Fiche : [[70-reconnaissance-representations/references/73-patchcore-padim|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::70-reconnaissance-representations

## CV-ANOMALIES-001

Objectif : choisir modèle de nominal. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-ANOMALIES-001
Question: Quel compromis distingue golden template, PatchCore et PaDiM pour inspection ?
Reponse: **Noyau attendu** : Template compare à une référence alignée ; PatchCore utilise une banque de features ; PaDiM estime des distributions avec covariance par position.

**Approfondissement** : Choisir selon variabilité nominale, alignement, mémoire et évaluation métier ; aucun ne connaît tous défauts possibles.

**Erreurs bloquantes** : Décrire ces scores comme des probabilités universelles de défectuosité.
Source: [[70-reconnaissance-representations/references/73-patchcore-padim|Fiche complète]] ; [PatchCore, §§3.1–3.3](https://arxiv.org/abs/2106.08265) ; [PaDiM, §III](https://arxiv.org/abs/2011.08785).
Tags: cv::pilote cv::d07 famille::comparaison cv_id::CV-ANOMALIES-001 provenance::agent pole::A pole::E
END

## CV-ANOMALIES-002

Objectif : expliquer le coreset. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-ANOMALIES-002
Question: Dans PatchCore, à quoi sert un coreset de features nominales ?
Reponse: **Noyau attendu** : Réduire la banque en conservant une représentation utile de sa diversité, pour limiter mémoire et recherche.

**Approfondissement** : Le sous-échantillonnage modifie un compromis couverture/coût ; mesurer les défauts et faux rejets, pas seulement la taille de banque.

**Erreurs bloquantes** : Prendre le coreset pour un ensemble de défauts supervisés.
Source: [[70-reconnaissance-representations/references/73-patchcore-padim|Fiche complète]] ; [PatchCore, §§3.1–3.3](https://arxiv.org/abs/2106.08265) ; [PaDiM, §III](https://arxiv.org/abs/2011.08785).
Tags: cv::pilote cv::d07 famille::raisonnement cv_id::CV-ANOMALIES-002 provenance::agent pole::A pole::E
END

## CV-ANOMALIES-003

Objectif : détecter une dérive du nominal. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-ANOMALIES-003
Question: Le score d’anomalie monte sur toutes les pièces après changement d’éclairage. Que tester ?
Reponse: **Noyau attendu** : Comparer acquisition/prétraitement, recalage et distribution des features au nominal, puis examiner des pièces réellement contrôlées.

**Approfondissement** : Réviser la référence ou le système lumineux après validation ; changer le seuil seul peut cacher de vrais défauts.

**Erreurs bloquantes** : Étiqueter automatiquement toute hausse de score comme défaut physique.
Source: [[70-reconnaissance-representations/references/73-patchcore-padim|Fiche complète]] ; [PatchCore, §§3.1–3.3](https://arxiv.org/abs/2106.08265) ; [PaDiM, §III](https://arxiv.org/abs/2011.08785).
Tags: cv::pilote cv::d07 famille::diagnostic cv_id::CV-ANOMALIES-003 provenance::agent pole::A pole::E
END

## CV-ANOMALIES-004

Objectif : concevoir une inspection à défauts rares. Famille : conception. Provenance : agent.

START
CV-Pilote
ID: CV-ANOMALIES-004
Question: Cas E — conception : très peu d’images défectueuses, ligne cadencée. Quelle baseline et quelle validation proposer ?
Reponse: **Noyau attendu** : Stabiliser acquisition, définir défauts critiques et tolérances, comparer template/anomalie nominale puis mesurer rejets et défauts manqués sur lots indépendants et variations réalistes.

**Approfondissement** : Prévoir revue des cas incertains, coût complet et suivi des dérives ; aucun taux global ne remplace les défauts rares du besoin.

**Erreurs bloquantes** : Valider sur les seules images nominales ou l’AUROC moyenne.

**Critères de correction du cas** : tâche et contraintes explicites, hypothèses annoncées, choix justifié, vérification discriminante, limite de la conclusion. Cas construit, sans observation terrain.
Source: [[70-reconnaissance-representations/references/73-patchcore-padim|Fiche complète]] ; [PatchCore, §§3.1–3.3](https://arxiv.org/abs/2106.08265) ; [PaDiM, §III](https://arxiv.org/abs/2011.08785).
Tags: cv::pilote cv::d07 famille::conception cv_id::CV-ANOMALIES-004 provenance::agent pole::A pole::E cas_pole::E::conception
END
