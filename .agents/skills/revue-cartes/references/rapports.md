# Conventions des rapports de revue

Les rapports gardent la trace de ce qui a été vérifié, avec quelles sources et
avec quelles limites. Ils ne valent ni relecture indépendante ni preuve de
maîtrise. Les rapports existants de `docs/revues/` suivent ces conventions.

1. [Emplacement](#emplacement)
2. [Cadrage d'un passage](#cadrage-dun-passage)
3. [Rapport par sujet](#rapport-par-sujet)
4. [Bilan d'un passage](#bilan-dun-passage)
5. [Registre des propositions](#registre-des-propositions)

## Emplacement

```text
docs/revues/
  propositions.md                      # registre unique, tous passages confondus
  <AAAA-MM-JJ>[-<objet>]/              # un dossier par passage, objet facultatif
    00-cadrage.md                      # passages à plusieurs sujets
    <fichier-de-cartes>.md             # un rapport par sujet, ex. 81-nms.md
    00-bilan.md                        # passages à plusieurs sujets
```

Nommer le rapport comme le fichier de cartes du sujet : on retrouve ainsi tout
l'historique d'un sujet avec `ls docs/revues/*/81-nms.md`. Ne pas réécrire un
rapport d'un passage antérieur ; un nouveau passage crée un nouveau rapport.

## Cadrage d'un passage

À écrire avant le premier sujet, quand le passage en couvre plusieurs.

```markdown
# <Objet du passage> — <AAAA-MM-JJ>

Demande : <reformulation fidèle, avec les ajouts acceptés s'il y en a>.
Mode : <approfondir (défaut) | audit seulement>. Périmètre : <sujets, nombre de fiches et de cartes>.

## Critères de livraison
- <ce qui peut changer et ce qui doit rester stable : IDs, questions, noyaux…>
- <niveau d'exigence sur les sources>
- <contrôles à passer à la fin>
```

## Rapport par sujet

```markdown
# Revue — <titre de la fiche> — <AAAA-MM-JJ>

## Synthèse
<n> cartes auditées, mode <…>. Gravité maximale par carte avant correction :
<b> bloquante, <i> importante, <m> mineure, <s> sans défaut relevé.
Auto-revue : Agent <Codex ou Claude Code> (`revue-cartes`). Statut éditorial : `redige`.

## Constats par carte
| Carte | Exactitude | Pertinence | Corrigibilité | Cohérence | Gravité | Action |
| --- | --- | --- | --- | --- | --- | --- |
| CV-NMS-004 | Non soutenu : seuil final attribué au §4, décrit au §5 | Senior : ordre de traitement après pénalité | Noyau en 2 points ; 234 mots | IoU sans arguments dans la formule | Importante | Source et notation corrigées |

## Constats sur la fiche
<affirmations vérifiées, divergences entre sources, rubriques creuses>

## Corrections appliquées
<fichier, changement et raison, source consultée ; révision de la fiche>

## Propositions
<identifiants du registre créés ou mis à jour par ce passage, avec leur statut>

## Sources
<passages réellement consultés ; accès échoués et affirmations non revalidées>

## Contrôles et limites
<commandes et résultats ; reste non vérifié : rendu AnkiDroid, maîtrise de
l'apprenant, validation indépendante>
```

Dans le tableau :

- **Exactitude** donne le verdict et l'affirmation en cause, pas seulement
  « confirmé ».
- **Pertinence** est un jugement court : ce que la carte entraîne (mécanisme,
  choix, diagnostic, évaluation) ou pourquoi elle est faible (anecdote, doublon,
  cours général de DL).
- **Corrigibilité** donne la taille du noyau et le nombre de mots lexicaux.
- **Gravité** retient la plus haute de la carte.
- « Sans défaut relevé » ne vaut pas certification.

## Bilan d'un passage

```markdown
# <Objet du passage> — bilan — <AAAA-MM-JJ>

## Résultat
<sujets et cartes examinés ; cartes modifiées ou conservées ; aucun ajout ni retrait d'ID, ou lesquels>

| Gravité maximale par carte avant correction | Cartes |
| --- | ---: |
| Bloquante | |
| Importante | |
| Mineure | |
| Aucun défaut relevé | |
| Total | |

## Corrections principales
<regroupées par nature : sources, conventions, critères de réponse…>

## Propositions à décider
<extrait du registre : les plus utiles d'abord, avec la décision de l'apprenant si elle a été prise>

## Contrôles exécutés
<commandes et résultats, comparaison des inventaires>

## Limites
```

Pour le mode `approfondir`, ajouter au résultat un tableau des mots lexicaux par
réponse avant et après (minimum, médiane, maximum). Rappeler que ce compte
repère les réponses trop brèves sans mesurer leur qualité.

## Registre des propositions

`docs/revues/propositions.md` contient un tableau unique. Une ligne par
proposition, avec un identifiant stable `P-<ID-fiche>-<NN>`, par exemple
`P-CV-NMS-01` :

| ID | Fiche | Proposition | Lacune comblée | Famille ou rubrique | Coût de révision | Source primaire prévue | Statut |
| --- | --- | --- | --- | --- | --- | --- | --- |

Statuts possibles :

- `à décider` : la proposition attend le choix de l'apprenant ;
- `acceptée (AAAA-MM-JJ)` : à rédiger en mode `ajouter` ;
- `refusée (AAAA-MM-JJ) : <raison>` : ne pas la reproposer sans fait nouveau ;
- `reportée (AAAA-MM-JJ)` ;
- `faite (AAAA-MM-JJ) : <IDs créés>`.

Une proposition qui approfondit seulement une carte existante, sans nouvel ID,
relève du mode `approfondir` et peut être appliquée dans un passage par défaut ;
le noter dans le statut.
