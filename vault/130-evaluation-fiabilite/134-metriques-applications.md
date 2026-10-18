# Métriques de segmentation, inspection et applications — cartes

Fiche : [[130-evaluation-fiabilite/references/134-metriques-applications|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::130-evaluation-fiabilite

## CV-METRIQUES-APPLIQUEES-001

Objectif : distinguer recouvrement et frontière. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-METRIQUES-APPLIQUEES-001
Question: Pourquoi Dice et HD95 peuvent-ils raconter des choses différentes sur un même masque ?
Reponse: **Noyau attendu** : Dice mesure un recouvrement ; HD95 une distance de surface selon un percentile/protocole, avec unité physique si les coordonnées sont calibrées.

**Approfondissement** : Définir masques vides, directions et agrégation ; un contour éloigné ou une petite région peut peser différemment.

**Erreurs bloquantes** : Comparer directement un nombre sans unité à une longueur.
Source: [[130-evaluation-fiabilite/references/134-metriques-applications|Fiche complète]] ; [Metrics Reloaded](https://doi.org/10.1038/s41592-023-02151-z) ; [NIST, Gauge R&R](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc4.htm) ; [MVTec AD2, PRO et protocole](https://www.mvtec.com/fileadmin/Redaktion/mvtec.com/company/research/datasets/MVTecAD2_arXiv_preprint_2503.21622v1.pdf).
Tags: cv::pilote cv::d13 famille::comparaison cv_id::CV-METRIQUES-APPLIQUEES-001 provenance::agent pole::A pole::E
END

## CV-METRIQUES-APPLIQUEES-002

Objectif : mesurer les petits défauts. Famille : evaluation. Provenance : agent.

START
CV-Pilote
ID: CV-METRIQUES-APPLIQUEES-002
Question: Pourquoi un score pixel global peut-il masquer de petits défauts manqués en inspection ?
Reponse: **Noyau attendu** : Les pixels de fond ou grands défauts dominent certains agrégats ; une analyse par région/pièce et taille peut révéler les manques.

**Approfondissement** : Préciser AU-PRO et sa plage FPR si utilisée, plus taux de rejets/manques au seuil utile.

**Erreurs bloquantes** : Comparer des AU-PRO avec plages différentes sans le signaler.
Source: [[130-evaluation-fiabilite/references/134-metriques-applications|Fiche complète]] ; [Metrics Reloaded](https://doi.org/10.1038/s41592-023-02151-z) ; [NIST, Gauge R&R](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc4.htm) ; [MVTec AD2, PRO et protocole](https://www.mvtec.com/fileadmin/Redaktion/mvtec.com/company/research/datasets/MVTecAD2_arXiv_preprint_2503.21622v1.pdf).
Tags: cv::pilote cv::d13 famille::evaluation cv_id::CV-METRIQUES-APPLIQUEES-002 provenance::agent pole::A pole::E
END

## CV-METRIQUES-APPLIQUEES-003

Objectif : séparer calibration et métrologie. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-METRIQUES-APPLIQUEES-003
Question: Un faible RMS caméra suffit-il à valider répétabilité et reproductibilité d’une mesure de longueur ?
Reponse: **Noyau attendu** : Non : répéter les mesures et varier les conditions/configurations pertinentes, avec référence dimensionnelle et analyse des sources de variation.

**Approfondissement** : Distinguer biais, répétabilité, reproductibilité et stabilité ; fixer la tolérance métier.

**Erreurs bloquantes** : Transformer directement une erreur pixel d’ajustement en garantie millimétrique.
Source: [[130-evaluation-fiabilite/references/134-metriques-applications|Fiche complète]] ; [Metrics Reloaded](https://doi.org/10.1038/s41592-023-02151-z) ; [NIST, Gauge R&R](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc4.htm) ; [MVTec AD2, PRO et protocole](https://www.mvtec.com/fileadmin/Redaktion/mvtec.com/company/research/datasets/MVTecAD2_arXiv_preprint_2503.21622v1.pdf).
Tags: cv::pilote cv::d13 famille::diagnostic cv_id::CV-METRIQUES-APPLIQUEES-003 provenance::agent pole::A pole::E
END

## CV-METRIQUES-APPLIQUEES-004

Objectif : traiter les masques vides. Famille : pratique. Provenance : agent.

START
CV-Pilote
ID: CV-METRIQUES-APPLIQUEES-004
Question: Que faut-il annoncer lorsqu’une métrique de segmentation rencontre référence ou prédiction vide ?
Reponse: **Noyau attendu** : La convention choisie et son effet sur le score/agrégation ; ne pas laisser une division indéfinie devenir un résultat implicite.

**Approfondissement** : Les faux positifs sur cas négatifs et absences de détection doivent rester visibles.

**Erreurs bloquantes** : Retirer silencieusement tous les cas vides pour améliorer la moyenne.
Source: [[130-evaluation-fiabilite/references/134-metriques-applications|Fiche complète]] ; [Metrics Reloaded](https://doi.org/10.1038/s41592-023-02151-z) ; [NIST, Gauge R&R](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc4.htm) ; [MVTec AD2, PRO et protocole](https://www.mvtec.com/fileadmin/Redaktion/mvtec.com/company/research/datasets/MVTecAD2_arXiv_preprint_2503.21622v1.pdf).
Tags: cv::pilote cv::d13 famille::pratique cv_id::CV-METRIQUES-APPLIQUEES-004 provenance::agent pole::A pole::E
END
