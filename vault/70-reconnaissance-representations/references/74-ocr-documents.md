---
id: CV-OCR
type: comparaison
domaine: d07
poles: [E]
priorite: V2
profondeur: reperage
statut: redige
provenance: agent
revision: 3
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d07]
---
# OCR et compréhension documentaire

## Problème, données et hypothèses

Extraire texte, ordre de lecture et structure selon des sorties distinctes. Entrées : pages/images avec résolution et langue ; sorties : caractères, mots, boîtes, champs ou structure. Un texte exact dans le mauvais ordre peut être inutilisable.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Détecter régions/lignes puis reconnaître : CRNN/CTC est une référence séquentielle, TrOCR une approche transformer. LayoutLM combine texte et layout ; Donut étudie une extraction sans moteur OCR séparé. Ces noms ne désignent pas la même interface.

## Mathématiques, conventions et unités

La CER classique vaut $(S+D+I)/N$ pour $N>0$ caractères de référence, avec substitutions, suppressions et insertions d'édition. La WER classique applique la même logique aux mots. OCR-D décrit aussi une variante normalisée $(S+D+I)/(S+D+I+C)$, où $C$ compte les caractères corrects, et utilise cette variante bornée dans ses benchmarks ; ne pas assimiler leurs scores à la convention classique adoptée ici. Normalisation unicode, casse, espaces et segmentation changent le protocole ; le score peut dépasser 1 si les insertions sont nombreuses.

## Paramètres et propriétés

DPI, rotation, langues, découpe, lexique, tokenisation et ordre de lecture. Distinguer erreur de détection de ligne, reconnaissance, assemblage et extraction d'un champ.

## Coût et implémentation

Coût du rendu, détection, crops et génération ; grands documents demandent pagination et limites. Aucun OCR exécuté et aucune performance linguistique revendiquée.

## Évaluation et variation contrôlée

Baseline : page nette et texte de référence, puis flou/rotation contrôlés. Mesurer CER/WER et exactitude des champs/structure ; un score caractère global peut masquer un montant critique faux.

## Échecs et diagnostic

Texte lisible mais colonnes mélangées : vérifier détection et ordre de lecture. Erreurs sur chiffres : analyser coût métier et données de résolution, sans prétendre qu'une génération fluide est correcte.

## Alternatives et usages

OCR spécialisé ou pipeline multimodal selon sortie, données et contraintes ; conserver preuves visuelles et protocole des champs essentiels.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent chaîne OCR, normalisation et métrique adaptée au document. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-OCR-001

**Question de travail** : Pourquoi une bonne CER ne suffit-elle pas à valider l’extraction d’une facture ?

**Réponse de référence** : CER mesure l’édition de caractères selon un protocole ; ordre de lecture, association des champs et exactitude des montants sont d’autres sorties.

**Exemple de différence métier** : une facture peut contenir presque tous les caractères corrects tout en associant le montant d'une ligne à la mauvaise référence, ou en inversant deux colonnes. Une petite erreur sur un chiffre critique peut aussi compter peu dans la CER globale d'un long document.

**Contrat proposé** : définir séparément transcription, ordre de lecture, boîtes, clés et valeurs attendues, avec une référence adaptée pour chacun. Conserver les règles de normalisation des espaces, de casse et de nombres dans l'évaluation. Mesurer exactitude des champs critiques, documents entièrement corrects et taux de vérification humaine au seuil retenu. Une génération linguistiquement plausible doit encore correspondre à l'image source. La validation du produit porte donc sur les informations effectivement utilisées par le processus aval ; elle ne se déduit pas du seul score de reconnaissance caractère ni de l'aspect lisible du texte reconstruit.

### Cas lié à CV-OCR-003

**Question de travail** : Des lignes sont reconnues correctement mais le texte entrelace les colonnes. Quel composant examiner ?

**Réponse de référence** : Détection/layout et assemblage de l’ordre de lecture, avant le reconnaisseur de caractères.

**Décomposition du pipeline** : les boîtes ou régions déterminent quelles lignes sont envoyées à la reconnaissance ; leur structure détermine ensuite comment les textes sont assemblés. Un reconnaisseur peut être exact sur chaque crop et le document final être faux parce que ces crops sont parcourus dans le mauvais ordre.

**Test construit** : conserver les transcriptions des lignes et remplacer uniquement l'ordre ou l'assemblage à l'aide d'une annotation de référence. Si le document redevient correct, le diagnostic porte sur layout ou lecture plutôt que sur les caractères. Tester colonnes, tableaux, encarts et lignes inclinées avec les mêmes règles de normalisation. Vérifier les liens entre champs et valeurs, car un ordre plausible ne suffit pas toujours à extraire la structure métier. Cette approche localise une responsabilité avant de choisir des annotations ou un entraînement supplémentaires pour un composant qui ne traite pas la cause.

**Repère documentaire de cette passe** : [OCR-D, Evaluation](https://ocr-d.de/en/spec/ocrd_eval.html), définitions, alignement et normalisation des erreurs. Les autres développements figurent dans les [cartes associées](../74-ocr-documents.md).

## Sources et cartes

- [CRNN, méthode](https://arxiv.org/abs/1507.05717).
- [TrOCR](https://arxiv.org/abs/2109.10282).
- [LayoutLM](https://arxiv.org/abs/1912.13318).
- [Donut](https://arxiv.org/abs/2111.15664).
- [OCR-D, évaluation](https://ocr-d.de/en/spec/ocrd_eval.html).
- [Cartes associées](../74-ocr-documents.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
