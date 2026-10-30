# Modèle de carte du pilote

Format attendu par `scripts/check_vault.py` et exporté vers AnkiDroid par
`scripts/build_apkg.py` (modèle `CV-Pilote`, voir `docs/export-apkg.md`). Il est
expérimental : ne pas le modifier sans passer par la spec et le contrat
`specs/001-cv-knowledge-base/contracts/obsidian-anki.md`. Ce modèle reste hors du
vault : le contrôleur refuse une ligne `START` dans un guide, un index ou une fiche.

## Bloc

```text
## CV-<SUJET>-NNN

Objectif : <verbe à l'infinitif + objet>. Famille : <famille>. Provenance : agent.

START
CV-Pilote
ID: CV-<SUJET>-NNN
Question: <contexte et question autonome, sans révéler la réponse>
Reponse: **Noyau attendu** : <points nécessaires pour satisfaire l'objectif>

**Approfondissement** : <mécanisme, raisonnement, limites, exemple>

**Erreurs bloquantes** : <contresens qui invalident la réponse>
Source: [[<dossier>/references/<fiche>|Fiche <Nom>]] ; [<Auteur année, §x>](https://…).
Tags: cv::pilote cv::dXX famille::<famille> cv_id::CV-<SUJET>-NNN provenance::agent pole::B pole::E
END
```

## Règles

- **Fichier** : une seule ligne `TARGET DECK: CV::Pilote::<dossier>` en tête,
  où `<dossier>` est le répertoire thématique, par exemple
  `40-features-matching`. Les cartes vivent à la racine du thème, la fiche
  dans `references/` sous le même nom de fichier.
- **ID** : `CV-<SUJET>-NNN`, au format `CV-[A-Z0-9-]+-\d{3}`. Prendre le
  prochain numéro libre donné par l'inventaire. Ne jamais réutiliser ni
  renuméroter un ID existant.
- **En-tête** : le titre `## <ID>` et la ligne
  `Objectif : … Famille : … Provenance : …` précèdent le bloc ; le contrôleur
  les exige.
- **Familles** acceptées (sans accent) : `comprehension`, `raisonnement`,
  `algorithme`, `comparaison`, `diagnostic`, `pratique`, `evaluation`,
  `conception`. La famille de l'en-tête et le tag `famille::` sont identiques.
- **Champs** : `ID`, `Question`, `Reponse` (sans accent) et `Source`, dans cet
  ordre et non traduits. `Reponse` peut s'étendre sur plusieurs lignes et
  contenir des lignes vides ; les trois rubriques en gras sont obligatoires.
- **Source** : un seul wikilink vers la fiche parente, depuis la racine du
  vault et sans `.md`, plus au moins une source HTTPS avec sa section, sa
  ligne ou son commit.
- **Tags** : une seule ligne, juste avant `END`, avec `cv::pilote`, le domaine
  `cv::dXX` de la fiche, `famille::…`, `cv_id::<ID>`, `provenance::agent`
  et un tag `pole::<lettre>` pour chaque pôle de sa fiche. L’ensemble des tags
  de pôles correspond exactement à son champ `poles`, sans doublon. Les tags
  `pole::B pole::E` du bloc sont un exemple pour une fiche `poles: [B, E]` ;
  les adapter à la fiche parente.
  Le contrôleur du pilote exige `provenance::agent` : une carte rédigée par
  l'apprenant demandera de faire évoluer le contrôleur.
- **Identité Anki** : le paquet calcule le GUID de la note à partir de l'ID
  (`genanki.guid_for("CV-Pilote", ID)`), indépendamment du contenu. Changer
  l'ID d'une carte existante crée une nouvelle note sur le téléphone et y laisse
  l'ancienne. Les commentaires `<!--ID: …-->` de l'ancien plugin ne sont plus
  produits : s'il en reste un, ne pas le modifier ni le copier.
- **Contenu** : maths en `$…$` et `$$…$$` ; paragraphes, listes simples, gras,
  italique, code et liens ; image locale avec un nom de fichier unique dans le
  vault ; aucun espace en fin de ligne. Le paquet refuse titres, tableaux,
  citations et `$` hors formule : l'inventaire le signale.
- **Longueur** : au moins 180 mots lexicaux dans `Reponse`, sans plafond ni
  remplissage ; le noyau reste court et corrigible.
