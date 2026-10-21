# Revue — CLIP, SigLIP et reconnaissance par texte — 2026-10-20

## Synthèse

4 cartes auditées. 0 bloquant ; 1 important partagé (mauvais passage cité) ; 2 mineurs.
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

4 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 2 mineure, 2 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-CLIP-001 | Confirmé : encodeurs et classes textuelles | interpréter le zero-shot CLIP. | 51 mots à l’entrée ; phrase ambiguë clarifiée | Fiche et format contrôlés | Mineur | Reformuler |
| CV-CLIP-002 | Déduit de la normalisation sur candidats | refuser une probabilité trompeuse. | 45 mots à l’entrée ; contre-exemple fini | Fiche et format contrôlés | Aucune | Conserver |
| CV-CLIP-003 | Confirmé : softmax bidirectionnel vs sigmoid par paire | distinguer objectifs contrastifs. | 51 mots à l’entrée ; distinction centrale | Fiche et format contrôlés | Aucune | Conserver |
| CV-CLIP-004 | Protocole du projet | tester la sensibilité au texte. | 55 mots à l’entrée ; séparation validation/test | Fiche et format contrôlés | Mineur | Attribution |

### Affirmations de la fiche et des cartes

Forme normalisée des embeddings et température, classement zero-shot, sensibilités aux prompts, objectif sigmoid avec température et biais confirmés par les passages consultés. Les limites générales sont au §6 de CLIP, le §7 traite les impacts. La non-calibration automatique est une limite logique ; pas de seuil ni performance cible attribués aux auteurs.

## Corrections appliquées

Fiche révision 2 ; §6 partout ; approfondissement 001 clarifié.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Effet d’un candidat supplémentaire sur softmax | Exemple numérique du raisonnement de 002 | Approfondissement | Aucun nouveau rappel nécessaire | Définition du softmax ; CLIP §2.3 |

Familles absentes : algorithme, conception, diagnostic, pratique. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [Radford et al., CLIP, §§2.3, 3.1 et limites §6](https://arxiv.org/abs/2103.00020) : PDF, pseudocode §2.3, §3.1.4 et §6.
- [Zhai et al., SigLIP, §3 et algorithme 1](https://arxiv.org/abs/2303.15343) : PDF, algorithme 1 et §3.

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
