---
id: CV-ANOMALIES
type: methode
domaine: d07
poles: [A, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
prerequis: ["CV-REPRESENTATIONS", "CV-ACQUISITION"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d07]
---
# Inspection : golden template, PatchCore et PaDiM

## Problème, données et hypothèses

Détecter des écarts au nominal lorsque les défauts sont rares. Entrées : images nominales de référence et acquisition ; sorties : score image et/ou carte de localisation. L'anomalie dépend de la distribution de référence : changement d'éclairage et défaut produit ne sont pas équivalents.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-REPRESENTATIONS](71-representations-transfert.md) ; [CV-ACQUISITION](../../20-acquisition-images/references/21-exposition-bruit-echantillonnage.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Dans la baseline proposée par le projet, golden template signifie comparer à une référence après recalage. PatchCore garde une banque de features de patches nominaux, réduite par coreset, et score par proximité. PaDiM modélise des distributions gaussiennes de features par position et utilise leurs corrélations.

## Mathématiques, conventions et unités

Un score de proximité simple est $a(p)=\min_{m\in M}\|f(p)-m\|_2$ pour feature f et banque M ; le papier PatchCore inclut une agrégation/repondération à distinguer de ce résumé. PaDiM utilise $\sqrt{(f-\mu)^T\Sigma^{-1}(f-\mu)}$ avec covariance estimée/régularisée. Ces scores ne sont pas des probabilités de défaut calibrées.

## Paramètres et propriétés

Sélection nominale, couches, échelle, coreset/covariance, alignement et seuil. Une contamination du nominal ou une variabilité non couverte change le résultat. La détection de tous défauts futurs n'est pas garantie.

## Coût et implémentation

Banque et recherche de voisins consomment mémoire/calcul ; covariance et carte ont un autre coût. Aucun modèle ni jeu industriel exécuté.

## Évaluation et variation contrôlée

Comparer une baseline template et les méthodes avec mêmes splits par pièce/lot. Varier éclairage ou orientation séparément ; mesurer taux de faux rejets, défauts manqués et localisation, pas seulement AUROC image.

## Échecs et diagnostic

Scores élevés sur toutes les pièces d'une nouvelle caméra : vérifier acquisition, domaine nominal et recalage avant de réétiqueter tout comme défaut. Un fond dominant peut masquer une petite anomalie dans une métrique pixel globale.

## Alternatives et usages

Détection supervisée si défauts connus annotables ; hybride classique/appris selon variation et tolérance métier. Conserver procédure d'analyse des faux positifs.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent référence normale, voisinage de patches et décision métier. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-ANOMALIES-001

**Question de travail** : Quel compromis distingue golden template, PatchCore et PaDiM pour inspection ?

**Réponse de référence** : Template compare à une référence alignée ; PatchCore utilise une banque de features ; PaDiM estime des distributions avec covariance par position.

**Lecture des hypothèses** : une comparaison directe au template exige que les écarts géométriques et photométriques légitimes soient suffisamment maîtrisés. Une banque de patches nominaux cherche des voisins représentatifs ; un modèle de distribution par position représente autrement la variabilité et les corrélations. Le mot anomalie désigne ici un écart à cette référence, pas une définition universelle du défaut métier.

**Exemple construit** : un éclairage nouveau peut déplacer toutes les features et augmenter les scores sans pièce physiquement défectueuse. Un défaut absent de l'apprentissage peut au contraire être peu visible dans la représentation. Comparer les méthodes sur lots indépendants, défauts critiques et variations nominales, avec coût complet et seuil de décision. Une bonne localisation de score doit encore être reliée à une tolérance métier. Le choix dépend de ce qui est stable dans l'acquisition et de ce qui doit être considéré comme acceptable.

### Cas lié à CV-ANOMALIES-004

**Question de travail** : Cas E — conception : très peu d’images défectueuses, ligne cadencée. Quelle baseline et quelle validation proposer ?

**Réponse de référence** : Stabiliser acquisition, définir défauts critiques et tolérances, comparer template/anomalie nominale puis mesurer rejets et défauts manqués sur lots indépendants et variations réalistes.

**Conception proposée** : distinguer une pièce rejetée à tort, un défaut manqué et un cas soumis à vérification. Leur coût n'est pas identique. Stabiliser d'abord l'image et le recalage rend la baseline interprétable ; choisir ensuite si une référence unique ou une distribution nominale représente suffisamment la variabilité acceptable.

**Validation** : séparer pièces et lots entre réglage et test, couvrir les défauts critiques même rares et les perturbations nominales réalistes. Mesurer le point de décision retenu, le taux de vérification et la latence complète sur la ligne visée. Une AUROC résume une courbe de classement ; elle ne donne pas directement le nombre de défauts manqués au seuil exploité. Prévoir collecte et revue de nouveaux cas avant de modifier la référence, afin de ne pas intégrer silencieusement une dérive produit au nominal.

**Repère documentaire de cette passe** : [PatchCore](https://arxiv.org/html/2106.08265v2), §3, banque de caractéristiques et scoring. Les autres développements figurent dans les [cartes associées](../73-patchcore-padim.md).

## Sources et cartes

- [PatchCore, §§3.1–3.3](https://arxiv.org/abs/2106.08265).
- [PaDiM, §III](https://arxiv.org/abs/2011.08785).
- [Cartes associées](../73-patchcore-padim.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
