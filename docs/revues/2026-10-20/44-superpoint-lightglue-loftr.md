# Revue — SuperPoint, LightGlue et LoFTR — 2026-10-20

## Synthèse

5 cartes auditées. 0 bloquant, 0 important ; 1 constat mineur partagé (traçabilité).
Auto-revue documentaire par Agent Codex (`revue-cartes`) ; statut `redige` conservé.

5 cartes auditées. Gravité maximale relevée par carte avant correction : 0 bloquante, 0 importante, 5 mineure, 0 sans défaut relevé. Les constats portant uniquement sur la fiche sont détaillés séparément ci-dessous.

## Constats par carte

| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-MATCH-APPRIS-001 | Confirmé : sorties distinctes | attribuer le rôle des composants. | 41 mots à l’entrée ; deux rôles | Fiche et format contrôlés | Mineur | Références ciblées |
| CV-MATCH-APPRIS-002 | Confirmé : sélection puis raffinement | distinguer detector-free et flot dense. | 52 mots à l’entrée ; distinction unique | Fiche et format contrôlés | Mineur | §§3.3–3.4 |
| CV-MATCH-APPRIS-003 | Confirmé : poids par extracteur ; généralisation déduite | garder des features compatibles. | 41 mots à l’entrée ; contrat précis | Fiche et format contrôlés | Mineur | Documentation datée |
| CV-MATCH-APPRIS-004 | Protocole du projet compatible avec §4 | construire une baseline comparable. | 56 mots à l’entrée ; critères comparables | Fiche et format contrôlés | Mineur | Attribution explicite |
| CV-MATCH-APPRIS-005 | Déduction de changement de coordonnées | contrôler les coordonnées du matching. | 46 mots à l’entrée ; test discriminant | Fiche et format contrôlés | Mineur | Attribution explicite |

### Affirmations de la fiche et des cartes

Confirmés : architecture SuperPoint et adaptation homographique, entrées keypoints/descripteurs de LightGlue, adaptation en largeur/profondeur, sélection des correspondances grossières de LoFTR et raffinement local. Le score non calibré et les contrôles resize/padding sont des précautions déduites, pas un taux de défaillance publié. La baseline n’est pas exécutée ; aucune garantie de supériorité. Noyaux complémentaires et pas de doublon.

## Corrections appliquées

Fiche révision 2 ; champs Source datés et ciblés, sans changer les objectifs.

## Enrichissements proposés (en attente d'accord)

| Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue |
| --- | --- | --- | --- | --- |
| Expliquer la sortie anticipée et le pruning LightGlue | Mécanisme de coût absent des questions | Algorithme | Une carte, trois étapes ; durée à mesurer | LightGlue, article §3 |

Familles absentes : algorithme, conception, raisonnement. Leur absence ne commande pas de remplissage automatique ; les propositions visent une lacune concrète. Aucun ajout de carte effectué.

## Sources

- [DeTone et al. 2018, SuperPoint, §§3 et 5](https://arxiv.org/abs/1712.07629) : PDF, §§3.2–3.3 et 5.
- [LightGlue, README, Usage et Advanced configuration, consulté le 2026-10-20](https://github.com/cvg/LightGlue) : README téléchargé, poids distincts et adaptation.
- [Sun et al. 2021, LoFTR, §§3.1–3.4 et 4.1–4.2](https://arxiv.org/abs/2104.00680) : HTML, figure 2 et §§3–4.

## Contrôles et limites

Les longueurs proviennent de l'inventaire initial ; ce sont celles du verso entier, pas du seul noyau. Pas de plafond arbitraire ; durée et charge de rappel non mesurées.

Contrôleur, 34 tests unitaires, comparaison des 224 IDs et identités Anki et diff : résultats finaux dans le [bilan commun](00-bilan.md). Context7 indisponible ; recours direct aux documentations officielles pour les API.

Export Anki réel, rendu Obsidian/AnkiDroid, maîtrise de l'apprenant et validation scientifique indépendante non vérifiés. Les propositions de protocoles et diagnostics restent des raisonnements du projet, pas des expériences exécutées.
