---
id: CV-OCR
type: comparaison
domaine: d07
poles: [E]
priorite: V2
profondeur: reperage
statut: redige
provenance: agent
revision: 2
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

## Sources et cartes

- [CRNN, méthode](https://arxiv.org/abs/1507.05717).
- [TrOCR](https://arxiv.org/abs/2109.10282).
- [LayoutLM](https://arxiv.org/abs/1912.13318).
- [Donut](https://arxiv.org/abs/2111.15664).
- [OCR-D, évaluation](https://ocr-d.de/en/spec/ocrd_eval.html).
- [Cartes associées](../74-ocr-documents.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
