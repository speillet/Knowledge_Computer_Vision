---
id: CV-ASSOCIATION
type: comparaison
domaine: d11
poles: [C, D, E]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 3
prerequis: ["CV-SORT"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d11]
---
# DeepSORT, ByteTrack et association multiobjet

## Problème, données et hypothèses

Améliorer l'association au-delà de SORT sous occultations, scores variables et apparence. Entrées : détections, timestamps, éventuellement embeddings et historique ; sortie : pistes avec IDs selon cycle de vie. La qualité du détecteur reste déterminante.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-SORT](111-sort.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

DeepSORT combine mouvement, gating Mahalanobis, distance d'apparence et cascade d'association. ByteTrack associe d'abord les détections de score élevé, puis les faibles aux pistes restantes selon la méthode ; les faibles non associées ne créent pas indistinctement de nouvelles pistes.

## Mathématiques, conventions et unités

Une distance d'apparence cosinus peut écrire $1-a^Tb$ pour vecteurs unitaires. Elle n'est pas la même mesure que l'IoU ou le résidu Mahalanobis de mouvement. Mélanger leurs seuils sans normalisation/protocole n'est pas une fusion de probabilités justifiée.

## Paramètres et propriétés

Seuils haut/bas, gating, mémoire d'apparence, confirmation et durée de perte. Le ReID piéton original peut mal transférer à des pièces identiques. Le suivi 3D, par exemple AB3DMOT, exige en plus un contrat de repère/boîte et de mouvement 3D, pas un simple renommage du tracker 2D.

## Coût et implémentation

Embeddings ajoutent extraction et mémoire ; détecteur, NMS, association et transferts doivent être comptés. Aucun tracker exécuté ni amélioration de score prétendue.

## Évaluation et variation contrôlée

Baseline SORT à détecteur fixe ; varier occultation et calibrage des scores séparément. Mesurer ID switches, fragments et métriques d'association, avec split par séquence et paramètres figés.

## Échecs et diagnostic

IDs échangés malgré apparence : vérifier domaines ReID, crops, normalisation et association. Fausses pistes : inspecter création et seuils ; ne pas baisser tous les seuils sans traces frame par frame.

## Alternatives et usages

Associer mouvement et apparence selon ambiguïtés ; compenser ego-motion si nécessaire. Les trackers monoobjet et ReID seul remplissent des contrats distincts.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent gating, apparence et association des scores faibles. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-ASSOCIATION-001

**Question de travail** : Que rajoute DeepSORT au raisonnement d’association d’un SORT géométrique simple ?

**Réponse de référence** : Apparence/ReID et stratégies de gating/cascade, en plus du mouvement, selon sa conception.

**Raisonnement d'association** : deux boîtes proches peuvent se ressembler géométriquement tout en appartenant à des personnes différentes. Une distance d'apparence ajoute une observation qui peut les distinguer ; le mouvement et le gating restreignent les candidats plausibles. La cascade organise ces décisions selon la méthode, au lieu de transformer le filtre en reconnaissance d'identité.

**Exemple de limite** : si les crops sont petits, occultés ou hors du domaine d'entraînement ReID, leurs embeddings peuvent devenir peu discriminants. Augmenter leur poids peut alors aggraver l'affectation. Contrôler distances de vraies et fausses paires dans le domaine cible, puis comparer mouvement seul, apparence seule et combinaison à détecteur fixe. La fusion de coûts doit avoir une interprétation et un protocole ; une proximité cosinus n'est pas automatiquement une probabilité calibrée d'être la même personne, ni une garantie après une disparition longue.

### Cas lié à CV-ASSOCIATION-004

**Question de travail** : Comment comparer deux trackers sans confondre leur association avec un détecteur différent ?

**Réponse de référence** : Fixer les mêmes détections ou rapporter explicitement les deux variations ; conserver séquences, seuils et protocole temporel.

**Ablation causale proposée** : utiliser un fichier de détections horodatées commun aux deux trackers, avec mêmes boîtes, scores et classes. Les différences de pistes proviennent alors de leurs étapes temporelles et de leurs paramètres, dans les limites de ce contrôle. Pour comparer les systèmes complets, mesurer ensuite aussi chaque détecteur avec son tracker.

**Exemple de facteur confondant** : un détecteur qui retrouve une personne après occultation peut améliorer le score d'identité sans changement d'association. À l'inverse, une meilleure association peut être masquée par de nombreuses boîtes absentes. Reporter donc qualité de détection, erreurs d'identité, fragments, coût et règles de naissance/perte. Conserver un split par séquence et des réglages figés sur le test. Une comparaison équitable ne demande pas forcément un détecteur unique pour tous les usages, mais exige de dire précisément quelle composante a changé et ce que l'on peut lui attribuer.

**Repère documentaire de cette passe** : [ByteTrack](https://arxiv.org/html/2110.06864v3), algorithme de deuxième association. Les autres développements figurent dans les [cartes associées](../112-deepsort-bytetrack.md).

## Sources et cartes

- [SORT, §3.1 et tableau 1](https://arxiv.org/abs/1602.00763) : effet du changement de détecteur, motivation pour le contrôle de l’amont.

- [DeepSORT, §§2.1–2.3](https://arxiv.org/abs/1703.07402).
- [ByteTrack, §3 Algorithm1](https://arxiv.org/abs/2110.06864).
- [AB3DMOT, contrat 3D](https://arxiv.org/abs/2008.08063).
- [Cartes associées](../112-deepsort-bytetrack.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
