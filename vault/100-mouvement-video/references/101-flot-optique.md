---
id: CV-FLOT
type: methode
domaine: d10
poles: [B, C, D]
priorite: V0
profondeur: approfondissement
statut: redige
provenance: agent
revision: 1
prerequis: ["CV-MATCHING"]
competences: [expliquer, appliquer, comparer, evaluer, diagnostiquer]
tags: [cv/d10]
---
# Flot optique : Lucas–Kanade, Farnebäck et RAFT

## Problème, données et hypothèses

Estimer des déplacements image entre frames, sparse ou denses, sans les confondre avec des identités d'objets. Entrées : images avec cadence, prétraitement et sens temporel ; sortie : vecteurs dans le repère pixel et indicateurs selon méthode.

## Prérequis et compétences

**Prérequis obligatoires** : [CV-MATCHING](../../40-features-matching/references/43-detecteurs-matchers.md).
**Compétences visées** : expliquer le mécanisme, comparer sous contraintes, interpréter une mesure et diagnostiquer un échec. Le niveau affiché porte sur cette fiche ; les variantes seulement citées ne sont pas toutes approfondies.

## Intuition et déroulement

Lucas–Kanade linéarise une constance photométrique et suppose un mouvement cohérent local. La pyramide étend les déplacements utiles ; Farnebäck propose une estimation dense par représentation polynomiale locale. RAFT exploite features, corrélations all-pairs et mises à jour récurrentes.

## Mathématiques, conventions et unités

La linéarisation donne $I_xu+I_yv+I_t\approx0$, u,v en pixels entre frames si les dérivées suivent ce pas. Le système local nécessite des gradients dans plusieurs directions. Un flux entre frames n'est une vitesse px/s qu'après division par l'intervalle approprié.

## Paramètres et propriétés

Fenêtre, pyramide, texture, bruit, résolution et occultation. RAFT à deux images n'apporte pas intrinsèquement une identité long terme. Constance d'intensité et petits déplacements sont des hypothèses de la méthode linéarisée, pas de toute vision vidéo.

## Coût et implémentation

Une corrélation all-pairs a un coût mémoire important selon la résolution des features ; une implémentation peut l'optimiser. Aucun code de flot exécuté ; pas de FPS comparé hors matériel/protocole.

## Évaluation et variation contrôlée

Baseline : translation synthétique et référence de déplacement ; varier illumination puis occultation séparément. Mesurer EPE sur régions observables et masques d'occlusion, pas seulement une visualisation de couleurs.

## Échecs et diagnostic

Sur une arête, l'aperture problem laisse une direction ambiguë ; sous occultation, la correspondance peut disparaître. `status=1` d'une API ne prouve pas la vérité physique ; contrôler aller-retour et validité.

## Alternatives et usages

Features suivies, flot dense, tracker d'objets ou ReID selon la sortie. Une caméra mobile crée du flot de fond même si aucun objet ne bouge dans le monde.

## Sources et cartes

- [OpenCV, optical flow/Lucas–Kanade](https://docs.opencv.org/4.13.0/d4/dee/tutorial_optical_flow.html).
- [RAFT, §§3.1–3.3](https://arxiv.org/abs/2003.12039).
- [Cartes associées](../101-flot-optique.md).

Rédaction : agent, 2026-10-18. Confrontation documentaire des affirmations centrales aux passages cités ; aucune expérience image/vidéo, performance matérielle ou validation indépendante annoncée. Les cas construits sont des raisonnements du projet.
