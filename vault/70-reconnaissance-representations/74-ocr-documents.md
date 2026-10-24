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

**Exemple de différence métier** : une facture peut contenir presque tous les caractères corrects tout en associant le montant d'une ligne à la mauvaise référence, ou en inversant deux colonnes. Une petite erreur sur un chiffre critique peut aussi compter peu dans la CER globale d'un long document.

**Contrat proposé** : définir séparément transcription, ordre de lecture, boîtes, clés et valeurs attendues, avec une référence adaptée pour chacun. Conserver les règles de normalisation des espaces, de casse et de nombres dans l'évaluation. Mesurer exactitude des champs critiques, documents entièrement corrects et taux de vérification humaine au seuil retenu. Une génération linguistiquement plausible doit encore correspondre à l'image source. La validation du produit porte donc sur les informations effectivement utilisées par le processus aval ; elle ne se déduit pas du seul score de reconnaissance caractère ni de l'aspect lisible du texte reconstruit.

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

**Exemple analytique** : une référence contient cinq caractères ; si le système produit ces cinq caractères suivis de dix caractères supplémentaires, une convention d'édition qui compte dix insertions donne une CER de $10/5=2$, soit 200 %. Le dénominateur décrit la longueur de référence, pas la longueur de sortie.

**Interprétation du protocole** : une variante normalisée peut utiliser un autre dénominateur et être bornée ; elle mesure alors une quantité différente. Annoncer la convention avant de comparer deux outils. Définir aussi le cas d'une référence vide, la normalisation Unicode et l'agrégation entre pages. Une moyenne par page n'accorde pas le même poids aux documents qu'un ratio sur tous les caractères. Ces choix peuvent changer le classement apparent sans changement du reconnaisseur. Le score reste une mesure d'édition, et ne valide pas à lui seul l'ordre de lecture ou la bonne extraction des montants.

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

**Décomposition du pipeline** : les boîtes ou régions déterminent quelles lignes sont envoyées à la reconnaissance ; leur structure détermine ensuite comment les textes sont assemblés. Un reconnaisseur peut être exact sur chaque crop et le document final être faux parce que ces crops sont parcourus dans le mauvais ordre.

**Test construit** : conserver les transcriptions des lignes et remplacer uniquement l'ordre ou l'assemblage à l'aide d'une annotation de référence. Si le document redevient correct, le diagnostic porte sur layout ou lecture plutôt que sur les caractères. Tester colonnes, tableaux, encarts et lignes inclinées avec les mêmes règles de normalisation. Vérifier les liens entre champs et valeurs, car un ordre plausible ne suffit pas toujours à extraire la structure métier. Cette approche localise une responsabilité avant de choisir des annotations ou un entraînement supplémentaires pour un composant qui ne traite pas la cause.

**Erreurs bloquantes** : Réentraîner seulement le reconnaisseur sans vérifier les régions.
Source: [[70-reconnaissance-representations/references/74-ocr-documents|Fiche complète]] ; [OCR-D, Text Evaluation, CER and WER, consulté le 2026-10-20](https://ocr-d.de/en/spec/ocrd_eval.html) ; diagnostic d’assemblage déduit par le projet.
Tags: cv::pilote cv::d07 famille::diagnostic cv_id::CV-OCR-003 provenance::agent pole::E
END
