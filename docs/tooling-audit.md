# Audit de l'outillage

Vérifié le 18 octobre 2026 pour `speillet/Knowledge_Computer_Vision`.

## État du dépôt et de la machine

Le dépôt contenait initialement uniquement sa licence. Aucun workflow de
contribution, skill local ou paramétrage Spec Kit n'était présent.

| Élément | État vérifié |
| --- | --- |
| Git et dépôt distant | Disponibles ; remote GitHub configuré |
| GitHub CLI | Authentifié pour `speillet`, avec accès repo et workflow |
| Identité d'auteur Git | Absente ; configuration reportée à la demande de l'utilisateur |
| Codex CLI et uv | Disponibles |
| Node.js, npm et npx | Absents du PATH ; inutiles pour le MCP distant retenu |
| Specify CLI | Version 1.2.1 installée avec uv ; `specify check` réussit |
| Spec Kit dans le dépôt | Intégration Codex initialisée ; 10 skills locaux |
| Constitution du projet | Modèle généré, à remplir pendant le cadrage |
| Context7 | MCP distant configuré ; résolution et lecture de documentation réussies |
| Obsidian et Anki | Applications et synchronisation non vérifiées pendant cet audit |
| Hooks et CI | Aucun contrôle automatique ajouté ; conventions documentées |

## Skills complémentaires installés

Ces dix skills ont été installés dans `~/.agents/skills/`, au niveau utilisateur,
sur la machine auditée. Ils ne sont pas embarqués dans le dépôt. Si une nouvelle
installation n'apparaît pas dans le sélecteur, redémarrer Codex, conformément à la
[documentation officielle des skills](https://developers.openai.com/codex/skills).

| Besoin | Skills | Source |
| --- | --- | --- |
| Clarifier une idée | `grill-me`, `grilling` | [Matt Pocock](https://github.com/mattpocock/skills) |
| Rédiger une spec et préparer son tracker | `to-spec`, `setup-matt-pocock-skills` | Matt Pocock |
| Rédiger une PR et relire les changements | `pr`, `code-review` | Matt Pocock |
| Préparer des commits conventionnels | `git-commit` | [GitHub awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/git-commit) |
| Traiter les retours de PR et la CI | `gh-address-comments`, `gh-fix-ci` | [OpenAI skills](https://github.com/openai/skills/tree/main/skills/.curated) |
| Consulter la documentation actuelle | `context7-mcp` | [Upstash Context7](https://github.com/upstash/context7/tree/master/skills/context7-mcp) |

Dans la révision installée, `grill-me` délègue à `grilling` : les deux ont donc
été installés. `to-spec` synthétise la discussion et publie la spec dans le tracker
configuré. Sa destination reste à choisir avec `$setup-matt-pocock-skills` ;
aucune configuration de tracker, issue ou étiquette distante n'a été créée.

`code-review` dépend des conventions et de la source de spec du projet. Lui
indiquer une référence de départ ; `CONTRIBUTING.md` fournit les conventions.

Les skills ont été récupérés avec le script officiel `skill-installer` aux
révisions suivantes, plutôt qu'à une branche mobile :

| Dépôt source | Révision installée |
| --- | --- |
| `mattpocock/skills` | `49dd158d1076134a641b33efb035946536778336` |
| `github/awesome-copilot` | `cb64ad12e32737ae764becd6885462e9b4c7cb00` |
| `openai/skills` | `49f948faa9258a0c61caceaf225e179651397431` |
| `upstash/context7` | `6b636d3c35e051a1a653a236afb7f612c02a1ad3` |

## GitHub Spec Kit

[Spec Kit 1.2.1](https://github.com/github/spec-kit/releases/tag/v1.2.1) a été
installé depuis son dépôt officiel au tag publié :

```sh
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.2.1
specify init --here --force --non-interactive --integration codex --script sh
```

La seconde commande décrit l'initialisation effectuée. Pour une mise à jour,
relire le diff avant toute réinitialisation avec `--force`.

Les skills Codex sont dans `.agents/skills/` et s'invoquent dans la conversation :

```text
$speckit-constitution
$speckit-specify
$speckit-clarify
$speckit-plan
$speckit-checklist
$speckit-tasks
$speckit-analyze
$speckit-implement
$speckit-converge
```

`$speckit-taskstoissues` est également installé ; il sert à publier des tâches
en issues et ne doit être invoqué que lorsque cette publication est souhaitée.
L'invocation avec `$speckit-…` est celle documentée pour
[l'intégration Codex](https://github.github.com/spec-kit/reference/integrations.html).

## Skill local de revue des cartes

`.agents/skills/revue-cartes/` est un skill propre au projet, versionné avec
le dépôt. Codex l'invoque avec `$revue-cartes`. Claude Code y accède par le
lien symbolique `.claude/skills/revue-cartes` et l'invoque avec `/revue-cartes`.

Il a trois modes :

- `approfondir`, le mode par défaut à la demande de l'apprenant, audite d'abord
  puis développe les réponses sans changer IDs, questions ni noyaux ;
- `audit`, sur demande (« audit seulement »), vérifie une fiche et ses cartes
  sur l'exactitude, la pertinence, la corrigibilité et la cohérence, puis
  applique les corrections et les consigne dans le journal du suivi ;
- `ajouter` rédige les cartes que l'apprenant a acceptées.

Les propositions sont suivies jusqu'à décision dans `docs/revues/propositions.md`.
Les rapports suivent les conventions de `references/rapports.md`.

Son script `scripts/inventaire_cartes.py` est en lecture seule. Il liste les
cartes avec le GUID de leur note Anki et signale les réponses sous le plancher
de 180 mots ainsi que les syntaxes refusées par le paquet. Il compare aussi
deux inventaires pour vérifier qu'aucun ID n'a disparu. Le skill ne remplace
ni `scripts/check_vault.py` ni une relecture par l'apprenant.

## Context7 : configuration et utilisation réelle

Le serveur est enregistré dans `~/.codex/config.toml` :

```toml
[mcp_servers.context7]
url = "https://mcp.context7.com/mcp"
```

La configuration a été vérifiée avec `codex mcp get context7 --json`. L'accès
anonyme a permis les appels MCP `initialize`, `tools/list`,
`resolve-library-id`, puis `query-docs` sur
`/obsidiantoanki/obsidian_to_anki`. Ces appels ont été effectués directement en
HTTP pendant l'audit ; l'apparition des outils dans le sélecteur d'une nouvelle
session Codex n'a pas été vérifiée.

L'ajout par CLI a proposé OAuth automatiquement ; ce parcours a été interrompu,
sans connexion de compte, puisque les lectures anonymes fonctionnaient.
Une authentification pourra être ajoutée si les quotas le nécessitent ; voir la
[configuration officielle Context7](https://context7.com/docs/resources/all-clients).
Le plugin Context7 du catalogue n'a pas été installé ; la configuration MCP
locale ci-dessus constitue l'intégration utilisée ici.

La documentation récupérée confirme qu'Obsidian to Anki accepte des champs
multilignes entre marqueurs `START` et `END`, et utilise un identifiant pour
retrouver les notes lors des mises à jour.
Sources : [format des champs](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Field-formatting)
et [mise à jour des notes](https://github.com/ObsidianToAnki/Obsidian_to_Anki/wiki/Updating-existing-notes).
Cette vérification documentaire ne constitue pas un test de synchronisation.

## Prochaines décisions du projet

- Configurer l'identité Git persistante quand l'utilisateur le souhaite ;
  une identité vérifiée peut être fournie ponctuellement aux commandes de commit.
- Choisir la destination des specs de Matt Pocock via `$setup-matt-pocock-skills`.
- Remplir la constitution Spec Kit avec les principes convenus pendant le cadrage.
- Choisir le plugin Obsidian, la structure du vault et le format des cartes.
- Vérifier un cycle création/mise à jour sur quelques cartes dans Anki avant
  de produire un grand volume de contenu.
