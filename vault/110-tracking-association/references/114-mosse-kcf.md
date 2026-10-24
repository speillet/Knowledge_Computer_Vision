---
id: CV-CORRELATION
type: methode
domaine: d11
poles: ["C", "D", "E", "F"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 2
prerequis: ["CV-SOT", "CV-FILTRES"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d11]
---
# MOSSE et KCF — tracking par filtres de corrélation

## Prérequis et compétences

**Prérequis obligatoires** : [CV-SOT](113-tracking-monoobjet.md), [CV-FILTRES](../../30-traitement-image/references/31-filtrage-gradients.md).
**Compétences visées** : expliquer la boucle d’un filtre de tracking; distinguer MOSSE et KCF; interpréter un PSR; rechercher une contamination du modèle; définir une comparaison honnête de trackers.
Les notions connexes restent des alternatives, pas des dépendances implicites.

## Problème et contrat des données

Suivre une cible initialisée dans une ROI, à partir de son apparence et d’une recherche locale. Entrées : image initiale, boîte cible et frames suivantes ; sortie : position ou boîte et éventuel score de réponse. Ce suivi mono-objet ne crée pas automatiquement des pistes pour tous les objets et ne garantit pas une ré-identification après disparition prolongée.

## Intuition et mécanisme

Un filtre apprend à produire un pic centré sur la cible et une réponse plus faible autour. MOSSE adapte un filtre linéaire à partir d’exemples transformés et des frames acceptées ; KCF exploite une régression à noyau sur les décalages cycliques du patch. La structure circulante se diagonalise en Fourier, ce qui évite de résoudre une grande régression dense. Au suivi : extraire le patch → calculer la réponse → localiser le pic → contrôler la confiance → mettre à jour sous conditions. Une mise à jour sur la mauvaise cible renforce la dérive.

## Mathématiques et conventions

Un objectif simplifié est $\min_h\sum_i\|h\star x_i-y_i\|^2+\lambda\|h\|^2$, où $x_i$ représente les features du patch, $h$ le filtre, $\star$ la corrélation circulaire et $y_i$ une réponse cible synthétique, souvent gaussienne. $\lambda\ge0$ régularise le filtre ; ces scores sont des unités arbitraires, pas des probabilités calibrées. Pour MOSSE, $\mathrm{PSR}=(r_{max}-\mu_{horspic})/\sigma_{horspic}$ compare le maximum à la moyenne et à l’écart-type du fond de réponse hors voisinage du pic. Définir ce voisinage et traiter un écart-type nul. Le seuil historique d’un papier ne vaut pas pour toute implémentation.

## Paramètres, coût et limites

La fenêtre de recherche limite le mouvement récupérable. La taille du patch, les features, le noyau, la régularisation et le taux d’apprentissage changent précision, mémoire et calcul. Les FFT coûtent typiquement $O(n\log n)$ pour $n$ échantillons par canal, mais tout le pipeline et les noyaux doivent être mesurés. Une fenêtre de Hann limite les discontinuités de bord sans supprimer le biais des décalages cycliques. Les extensions d’échelle ou de recherche long terme sont des variantes à nommer ; un KCF de base n’est pas automatiquement invariant à l’échelle.

## Évaluation et variation contrôlée

Baseline proposée : apparence figée après initialisation ; variation : mise à jour en ligne à taux fixé. Mesurer erreur de centre, overlap/success, perte de cible et délai de reprise, avec protocole de réinitialisation explicite. Introduire une occultation identique dans les deux essais pour tester la contamination du modèle. Exemple analytique : pic 0,8, moyenne hors pic 0,2 et écart-type 0,1 donnent PSR=6 ; ce score n’est pas une probabilité de 60 % ni un seuil universel de succès.

## Diagnostic et alternatives

Si la boîte part sur le fond après une occultation, vérifier la mise à jour durant les frames ambiguës, la taille de recherche et les pics concurrents. Geler le modèle, déclarer la perte ou relancer un détecteur peut être préférable à toujours émettre une boîte. Pour un grand changement d’apparence ou une disparition, comparer un tracker siamois ou un pipeline détecteur+association. Les propositions sont des raisonnements du projet ; aucun tracker ni benchmark vidéo exécuté pour cette fiche.

## Raisonnement guidé et contrôles proposés

Ces cas construits développent circulant, fenêtre et risque de contamination du modèle. Ils servent à expliquer ou tester le raisonnement ; leurs résultats image, vidéo ou matériels ne sont pas annoncés comme mesurés. Les propriétés de méthode restent attachées aux sources ci-dessous.

### Cas lié à CV-CORRELATION-001

**Question de travail** : Comment un filtre de corrélation initialisé par une boîte suit-il la cible à la frame suivante ?

**Réponse de référence** : Extraire une région de recherche et ses features, corréler avec le modèle, localiser le pic, contrôler la fiabilité puis adapter le modèle seulement selon la politique retenue. La réponse vise un pic de localisation, pas une classe sémantique.

**Interprétation de la réponse** : chaque déplacement candidat dans la région de recherche reçoit un score de ressemblance au modèle. Le pic localise l'hypothèse préférée, mais son contraste et la présence de concurrents doivent être examinés avant une mise à jour. La zone de recherche exprime déjà une hypothèse sur le mouvement possible.

**Exemple construit** : une cible qui se déplace au-delà de cette zone peut laisser au fond le meilleur pic disponible. Apprendre alors ce fond transforme une perte de localisation en dérive persistante du modèle. Définir une politique de perte et de récupération, puis la tester sur grands déplacements et occultations. La vitesse de corrélation est utile seulement si les hypothèses de recherche et de mise à jour conviennent au besoin.

### Cas lié à CV-CORRELATION-005

**Question de travail** : Deux trackers donnent des scores proches, mais l’un est réinitialisé après chaque perte. Que faut-il préciser pour comparer ?

**Réponse de référence** : Le protocole d’initialisation et de réinitialisation, les séquences, les pertes, l’overlap et l’erreur de centre, ainsi que la latence complète. Un redémarrage après erreur change la tâche évaluée.

**Pourquoi les resets changent la tâche** : une réinitialisation fournit au tracker une nouvelle localisation après un échec. Un système sans cette aide doit retrouver la cible ou rester en perte. Les deux protocoles n'exposent donc pas le modèle à la même accumulation d'erreurs ni à la même quantité d'information externe.

**Comparaison proposée** : conserver séquences, initialisation, règle de présence et critère de perte. Rapporter les échecs et les périodes de récupération en plus des mesures de localisation. Une moyenne calculée uniquement sur les frames réussies peut favoriser une méthode qui abandonne les cas difficiles. Pour un produit, inclure le coût et le délai de la procédure réelle de relance, qu'elle soit automatique ou humaine. Les scores restent interprétables uniquement avec ce contrat d'évaluation.

**Repère documentaire de cette passe** : [Bolme et al., MOSSE](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf), §§3–4, filtre et suivi. Les autres développements figurent dans les [cartes associées](../114-mosse-kcf.md).

## Sources et cartes

- [Bolme et al. 2010, §§3.2–3.5, MOSSE, mise à jour et PSR](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf).
- [Henriques et al., KCF, §§4–5, structure circulante et noyaux](https://arxiv.org/pdf/1404.7584).
- [Cartes associées](../114-mosse-kcf.md) : CV-CORRELATION-001 à 005.

Rédaction : Agent Codex, 2026-10-24. Sources primaires consultées et API OpenCV 4.13 vérifiées avec Context7. Calculs analytiques et protocoles proposés sont distingués des expériences ; aucun export réel, benchmark vidéo ni validation scientifique indépendante annoncé.
