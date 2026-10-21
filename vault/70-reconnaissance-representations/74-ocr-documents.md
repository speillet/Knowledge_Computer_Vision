# OCR et compréhension documentaire — cartes

Fiche : [[70-reconnaissance-representations/references/74-ocr-documents|Référence complète]]. Provenance : agent. Statut : rédigé, export expérimental.

TARGET DECK: CV::Pilote::70-reconnaissance-representations

## CV-OCR-001

Objectif : séparer reconnaissance et structure. Famille : comparaison. Provenance : agent.

START
CV-Pilote
ID: CV-OCR-001
Question: Pourquoi une bonne CER ne suffit-elle pas à valider l’extraction d’une facture ?
Reponse: **Noyau attendu** : CER mesure l’édition de caractères selon un protocole ; ordre de lecture, association des champs et exactitude des montants sont d’autres sorties.

**Approfondissement** : Évaluer chacun des livrables utiles au produit avec référence et règles de normalisation.

**Erreurs bloquantes** : Confondre texte global proche et facture correctement structurée.
Source: [[70-reconnaissance-representations/references/74-ocr-documents|Fiche complète]] ; [OCR-D, Text Evaluation, CER and WER, consulté le 2026-10-20](https://ocr-d.de/en/spec/ocrd_eval.html) ; critères de facture proposés par le projet.
Tags: cv::pilote cv::d07 famille::comparaison cv_id::CV-OCR-001 provenance::agent pole::E
END

## CV-OCR-002

Objectif : interpréter CER. Famille : raisonnement. Provenance : agent.

START
CV-Pilote
ID: CV-OCR-002
Question: Une CER peut-elle dépasser 100 % et dans quelles conditions ?
Reponse: **Noyau attendu** : Oui : les insertions peuvent faire dépasser le nombre de caractères de référence dans (S+D+I)/N.

**Approfondissement** : Préciser normalisation, cas N=0 et agrégation ; ce n’est pas une proportion simple de caractères faux dans la prédiction.

**Erreurs bloquantes** : Tronquer arbitrairement à 1 sans annoncer un autre protocole.
Source: [[70-reconnaissance-representations/references/74-ocr-documents|Fiche complète]] ; [OCR-D, Text Evaluation, CER and WER, consulté le 2026-10-20](https://ocr-d.de/en/spec/ocrd_eval.html) ; convention classique à dénominateur N.
Tags: cv::pilote cv::d07 famille::raisonnement cv_id::CV-OCR-002 provenance::agent pole::E
END

## CV-OCR-003

Objectif : localiser un défaut d’ordre de lecture. Famille : diagnostic. Provenance : agent.

START
CV-Pilote
ID: CV-OCR-003
Question: Des lignes sont reconnues correctement mais le texte entrelace les colonnes. Quel composant examiner ?
Reponse: **Noyau attendu** : Détection/layout et assemblage de l’ordre de lecture, avant le reconnaisseur de caractères.

**Approfondissement** : Comparer boîtes et structure au document annoté ; une nouvelle langue de reconnaissance ne corrige pas ce contrat.

**Erreurs bloquantes** : Réentraîner seulement le reconnaisseur sans vérifier les régions.
Source: [[70-reconnaissance-representations/references/74-ocr-documents|Fiche complète]] ; [OCR-D, Text Evaluation, CER and WER, consulté le 2026-10-20](https://ocr-d.de/en/spec/ocrd_eval.html) ; diagnostic d’assemblage déduit par le projet.
Tags: cv::pilote cv::d07 famille::diagnostic cv_id::CV-OCR-003 provenance::agent pole::E
END
