---
id: CV-CORRELATION
type: methode
domaine: d11
poles: ["C", "D", "E", "F"]
priorite: V0
profondeur: usage-operationnel
statut: redige
provenance: agent
revision: 1
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

## Sources et cartes

- [Bolme et al. 2010, §§3.2–3.5, MOSSE, mise à jour et PSR](https://www.cs.colostate.edu/~draper/papers/bolme_cvpr10.pdf).
- [Henriques et al., KCF, §§4–5, structure circulante et noyaux](https://arxiv.org/pdf/1404.7584).
- [Cartes associées](../114-mosse-kcf.md) : CV-CORRELATION-001 à 005.

Rédaction : Agent Codex, 2026-10-24. Sources primaires consultées et API OpenCV 4.13 vérifiées avec Context7. Calculs analytiques et protocoles proposés sont distingués des expériences ; aucun export réel, benchmark vidéo ni validation scientifique indépendante annoncé.
