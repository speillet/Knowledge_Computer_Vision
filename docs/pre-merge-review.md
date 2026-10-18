# Revue avant fusion — 2026-10-18

Base fixe : `19c54feb830c459858850030880432c2f466e6d2`, ancien `origin/main`.
Périmètre : specs, workflow de revue, socle Obsidian/Anki et extension aux
quatorze thèmes. Deux agents ont examiné le diff séparément avec `code-review`.
La revue initiale portait sur `3fa8127` ; les commits encore non publiés ont
ensuite été réordonnés pour inclure la correction du gabarit dès la première PR.
Cette revue ne constitue pas une expertise scientifique indépendante.

## Standards

**P2 — Gabarit de carte incomplet.** Le modèle du skill omettait les tags de
pôles alors que le contrôleur exige leur correspondance exacte avec la fiche.
**Corrigé** dans le commit `db664e5` : exemple `pole::B pole::E` et règle de
correspondance avec `poles`, sans doublon. Aucun ID existant modifié.

Aucun autre écart bloquant identifié. Commits Conventional Commits, prose
française, organisation par thème, provenance et limites des preuves sont
cohérents avec les conventions. Aucun smell de conception ne justifie une
restructuration dans ce lot. La duplication limitée de parsing entre les
outils constitue un point de maintenance, pas une violation documentée.

## Spec

**P2 — Métadonnées des approfondissements partielles.** FR-030 et SC-001
demandent compétences et dépendances par méthode. Les 129 entrées APP ont une
priorité, une profondeur et une connexion, sans compétences propres ni
prérequis obligatoires validés. **Suivi ouvert dans T023** ; les colonnes et
états de l’inventaire indiquent explicitement cette limite. SC-001 reste
partiellement satisfait pour ce backlog. Cette lacune ne bloque pas la
publication provisoire couvrant les quatorze thèmes selon SC-013.

Les validations applicatives et pédagogiques restent ouvertes dans
T009/T010/T013. La simulation du parseur ne leur est pas substituée.
Aucun débordement de périmètre injustifié ni autre exigence incorrectement
implémentée identifié dans ce passage. Les six pôles ont leurs cas conception
et diagnostic ; les douze cas de transfert couvrent les six familles avec
corrigés. Les prérequis inspectés sont liés et sans cycle.

## Contrôles et limites

34 tests réussis ; contrôleur : 125 documents Markdown, 52 fiches et 224 cartes ;
catalogue sans divergence ; inventaire sans anomalie ; liens locaux, JSON,
SVG et espaces de fin de ligne vérifiés. Le parseur officiel 3.6.0 a reconnu
224 notes, puis 224 mises à jour et zéro ajout avec des IDs simulés.
Ces contrôles ne prouvent ni la justesse de chaque phrase, ni l’export réel,
le rendu Android ou la maîtrise de l’apprenant. Aucun check CI n’est configuré.

Standards : un constat corrigé ; Spec : un constat suivi dans T023 et les
validations applicatives/pédagogiques déjà ouvertes. Aucun blocage de fusion
identifié pour le périmètre éditorial autorisé.
