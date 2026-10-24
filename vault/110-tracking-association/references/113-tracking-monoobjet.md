---
id: CV-SOT
type: comparaison
domaine: d11
poles: [C, D, E]
priorite: V1
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 3
prerequis: []
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d11]
---
# Tracking monoobjet : corrélation, siamois et MeanShift

## Problème, données et hypothèses

Suivre une cible initialisée dans une séquence, sans supposer un détecteur multiobjet ni une identité globale. Entrées : cible initiale et frames ; sortie : localisation de cette cible avec confiance/visibilité selon méthode.

## Prérequis et compétences

**Prérequis obligatoires** : [Conventions du vault](../../01-Parcours/Pre-requis.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

MeanShift cherche un mode d'une distribution d'apparence locale ; CamShift adapte sa fenêtre selon sa conception. Filtres de corrélation et réseaux siamois comparent modèle de cible et zone de recherche. Dans les variantes qui actualisent leur modèle de cible, comme KCF, mise à jour et recherche locale créent un compromis adaptation/dérive. SiamFC original conserve au contraire son template d’apparence pendant le suivi (§4) ; cette mise à jour n’est pas universelle.

## Mathématiques, conventions et unités

Une réponse de corrélation élevée est un score relatif entre template et recherche, pas une probabilité d'identité. Le déplacement maximal observable dépend de la région de recherche et de la cadence. Sans observation discriminante après occultation, l'identité peut rester ambiguë.

## Paramètres et propriétés

Taille de recherche, échelle, fréquence de mise à jour, confiance et politique de perte. Une mise à jour sur un distracteur peut contaminer le modèle. Détection de présence et localisation doivent être distinguées.

## Coût et implémentation

Template, recherche et calcul multiéchelle dominent. Aucun tracker monoobjet exécuté ; les familles sont comparées au niveau du contrat, sans FPS universel.

## Évaluation et variation contrôlée

Baseline avec cible unique et perturbations séparées : occultation, distracteur, sortie de champ. Mesurer précision, robustesse, pertes et politique de réinitialisation plutôt que seuls frames réussis.

## Échecs et diagnostic

Dérive progressive : inspecter ce qui est intégré au template et la présence réelle de la cible. Un score haut sur un distracteur n'est pas une preuve de persistance.

## Alternatives et usages

Détecteur + association si plusieurs cibles et entrées/sorties sont attendues ; suivi de point si la sortie utile est un point. Définir le contrat avant la famille de modèle.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent recherche locale, adaptation et identité après occultation. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-SOT-001

**Question de travail** : Pourquoi un tracker monoobjet initialisé ne remplace-t-il pas directement un MOT de toutes les personnes d’une scène ?

**Réponse de référence** : Il part d’une cible fournie et doit la relocaliser ; MOT gère aussi détections multiples, association, créations et disparitions.

**Différence de problème** : une cible fournie dans la première frame donne au tracker une information d'initialisation qu'un système multiobjet doit souvent découvrir. Le MOT doit en plus décider quels objets entrent ou sortent, empêcher plusieurs pistes de représenter le même objet et maintenir des identités malgré les interactions.

**Exemple construit** : lancer un tracker monoobjet sur une personne n'identifie pas automatiquement une deuxième personne qui entre plus tard. Lancer plusieurs instances peut aider à localiser des cibles initialisées, mais ne résout pas seul leurs collisions d'identité, leurs créations et la suppression des doublons. Définir les entrées et les événements attendus avant le choix d'architecture. Les métriques doivent également refléter ce contrat : une précision conditionnée à une initialisation manuelle favorable n'est pas directement comparable à une évaluation où toutes les cibles doivent être découvertes automatiquement.

### Cas lié à CV-SOT-002

**Question de travail** : Une cible occultée est remplacée par un distracteur dans le template du tracker. Quel mécanisme peut entretenir l’erreur ?

**Réponse de référence** : La mise à jour du modèle sur une observation mal associée peut renforcer le distracteur et accroître la dérive.

**Boucle de dérive** : le modèle apprend l'apparence de la région qu'il croit être la cible. Si la localisation devient fausse puis sert de nouvelle supervision, l'erreur est intégrée au modèle ; les frames suivantes peuvent alors favoriser encore davantage le distracteur. Une adaptation plus rapide renforce parfois cette boucle au lieu de la corriger.

**Contrôle proposé** : enregistrer les crops utilisés pour la mise à jour, les réponses et les décisions de perte. Comparer une politique de gel sous incertitude à la politique initiale, avec mêmes séquences et initialisation. Vérifier aussi le retour de la cible après occultation. Le gel protège éventuellement le modèle mais ne garantit pas la redétection si la cible sort de la région de recherche. Ce mécanisme concerne les variantes qui mettent leur modèle à jour ; il ne doit pas être attribué indistinctement à tout tracker siamois ou à tout template fixe.

**Repère documentaire de cette passe** : [KCF](https://arxiv.org/pdf/1404.7584), modèle de corrélation, décalages circulants et suivi. Les autres développements figurent dans les [cartes associées](../113-tracking-monoobjet.md).

## Sources et cartes

- [KCF, pipeline de tracking et interpolation du modèle](https://arxiv.org/abs/1404.7584) : exemple de mise à jour en ligne, distinct du template fixe de SiamFC.

- [OpenCV, Meanshift/Camshift](https://docs.opencv.org/4.13.0/d7/d00/tutorial_meanshift.html).
- [SiamFC, méthode](https://arxiv.org/abs/1606.09549).
- [Cartes associées](../113-tracking-monoobjet.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
