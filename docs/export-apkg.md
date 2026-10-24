# Contrat d'export direct vers AnkiDroid

Le lot du 2026-10-24 publie l'exporteur local et son skill. Il rend possible
l'import sans installer Anki Desktop ni AnkiConnect. Les fiches et cartes
du vault restent la source canonique ; les états pédagogiques restent inchangés.

## Critères d'acceptation

1. Refuser un vault invalide avant construction. Chaque bloc contrôlé devient
   une note `CV-Pilote`, quatre champs dans l'ordre `ID`, `Question`, `Reponse`,
   `Source`, une carte et le sous-deck thématique déclaré. Préserver les tags.
2. Garder le `modelId` 1153189853 du paquet local préexistant et calculer le
   GUID avec `genanki.guid_for("CV-Pilote", ID)`, indépendamment du contenu.
   Ne pas changer champs, nom ou nombre de gabarits sans migration explicite.
3. Convertir paragraphes, listes simples, gras, italique, code, formules et
   liens des cartes. Échapper le texte HTML. Transformer `$…$` en `\(…\)` et
   `$$…$$` en `\[…\]`, sans transformer le dollar à l'intérieur du code.
   Refuser titres, tableaux, citations, dollars orphelins et images introuvables
   avec l'ID de la carte concernée. Ce n'est pas un moteur Markdown général.
4. Embarquer les images locales du vault sous leur basename unique et utiliser
   les gabarits et CSS locaux. Les liens de référence pointent sur GitHub ;
   leur ouverture nécessite Internet. Les réponses restent autonomes.
5. Générer `dist/CV-Pilote.apkg` et `dist/CV-Pilote-manifest.json`, sans les
   committer. Relire ZIP/SQLite et contrôler IDs, GUID dérivés des IDs, modèle,
   champs, tags, médias et exactement une carte par note dans son sous-deck,
   sans carte orpheline et avec l'unique gabarit attendu.
   Le manifeste conserve commit, version de genanki, comptes et empreintes
   du contenu et des tags. La comparaison liste ajouts, corrections et retraits ;
   elle ne mesure pas les modifications des CSS/gabarits ou des octets d'une image.
6. Tester dans une collection jetable une première importation, trois révisions,
   une correction de contenu, puis une correction de contenu et du style.
   Refuser doublons, notes recréées, contenu ou style non mis à jour et historique
   modifié. Une simulation moteur ne valide ni le rendu ni les réglages Android.

## Vérifications reproductibles

```sh
python3 scripts/check_vault.py
python3 scripts/sync_catalog.py --check
uv run --no-project --with genanki==0.13.1 python -m unittest discover -s tests
uv run --no-project --with genanki==0.13.1 python scripts/build_apkg.py
python3 scripts/build_apkg.py --verifier dist/CV-Pilote.apkg
uv run --no-project --python 3.12 --with anki==26.9.3 --with genanki==0.13.1 \
  python scripts/simulate_anki_import.py
```

Comparer deux versions avec `python3 scripts/build_apkg.py --comparer
<ancien-manifeste.json>` ; l'ancien manifeste doit être sauvegardé avant
reconstruction. Les résultats sont consignés dans le
[journal du pilote](../vault/01-Parcours/Suivi-pilote.md).

## Mise à jour et limites

Importer un paquet plus récent avec mise à jour conditionnelle des notes et types
de notes, sans importer de progression. Une édition plus récente dans Anki peut
empêcher la mise à jour : résoudre le conflit dans le vault, puis reconstruire.
Une carte retirée du paquet reste dans la collection jusqu'à suppression manuelle.
Le champ et le tag `cv_id::<ID>` aident à retrouver la note.

Les commentaires numériques du plugin restent intacts dans le vault mais ne
déterminent pas les GUID de ce paquet. Les deux chaînes ne doivent pas alimenter
la même collection. Aucun outil de migration ou de suppression distante n'est fourni.

Les tests ne touchent aucune collection personnelle. Le rendu MathJax, SVG,
code, liens et mode sombre, ainsi que la réimportation après révision sur le
téléphone, restent à essayer. Une release est distincte d'une PR : la fusion
publie le code, et la construction locale suffit à obtenir le fichier importable.

## Sources

- [genanki : identités des notes](https://github.com/kerrickstaley/genanki#note-guids),
  consulté via Context7 puis vérifié avec genanki 0.13.1.
- [Anki : import et mises à jour des paquets](https://docs.ankiweb.net/manual/importing/packaged-decks).
- [AnkiDroid : import](https://docs.ankidroid.org/#_importing_anki_files).
