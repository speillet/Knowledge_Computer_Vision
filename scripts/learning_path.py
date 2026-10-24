"""Contrôle l'ordre du parcours et repère les réponses insuffisamment développées."""

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MIN_ANSWER_WORDS = 180


def validate_order(entries, steps):
    """Exige une occurrence par fiche et un ordre respectant tous les prérequis."""
    by_id = {entry['id']: entry for entry in entries}
    ordered = [identity for step in steps for identity in step['sujets']]
    errors, positions = [], {}
    for index, identity in enumerate(ordered):
        if identity in positions:
            errors.append('Sujet dupliqué : ' + identity)
        positions[identity] = index
        if identity not in by_id:
            errors.append('Sujet inconnu : ' + identity)
    for identity, entry in by_id.items():
        if identity not in positions:
            errors.append('Sujet absent du parcours : ' + identity)
        for prerequisite in json.loads(entry.get('prerequis', '[]')):
            if prerequisite not in by_id:
                errors.append(f'{identity} : prérequis inconnu {prerequisite}')
            elif identity in positions and prerequisite in positions:
                if positions[prerequisite] >= positions[identity]:
                    errors.append(f'{identity} doit suivre {prerequisite}')
    return errors


def render_path(entries, steps, open_target_count):
    errors = validate_order(entries, steps)
    if errors:
        raise ValueError('\n'.join(errors))
    by_id = {entry['id']: entry for entry in entries}
    text = f'''# Parcours senior : comprendre, vérifier, intégrer

Ce parcours ordonne les {len(entries)} sujets présents. Les dossiers restent un classement
thématique ; leur numéro ne fixe pas l'ordre de révision. Les {open_target_count} approfondissements
encore ouverts dans l'[inventaire](Inventaire.md) restent à construire.

Tu maîtrises déjà le ML/DL et la segmentation sémantique : utiliser les critères
de passage comme tests d'entrée, et consacrer davantage de travail au classique,
à la géométrie, à la détection et au tracking. Une étape connue peut être parcourue
par ses diagnostics, sans réciter à nouveau tout le cours de deep learning.

```mermaid
flowchart TD
    A[Acquisition, conventions et évaluation] --> B[Traitement et features]
    B --> C[Matching et géométrie robuste]
    C --> D[Calibration, multivue et 3D]
    A --> E[Représentations, détection et segmentation]
    E --> F[Mouvement, association et tracking]
    D --> G[VIO, fusion et perception spatiale]
    F --> G
    E --> H[Vision générative et multimodale]
    G --> I[Intégration et déploiement]
    H --> I
```

Le schéma donne les grandes branches ; les tables ci-dessous donnent l'ordre
complet contrôlé et les prérequis déclarés dans les fiches. Un prérequis vise les
notions utilisées, pas nécessairement chaque approfondissement de sa fiche :
SORT requiert par exemple l'IoU et les bases de Kalman, sans exiger toute l'AP COCO
ni un ESKF complet. Les rappels locaux sont dans les [conventions](Pre-requis.md).
Les liens d'alternatives ne deviennent pas des dépendances obligatoires.

## Comment travailler une étape

1. Essayer le noyau sans lire la réponse, puis expliquer le mécanisme avec ses mots.
2. Lire l'approfondissement long, suivre l'exemple et vérifier unités et hypothèses.
3. Changer un facteur du cas : bruit, cadence, échelle, visibilité ou contrainte.
4. Prédire l'effet, proposer une vérification et discuter la limite de la conclusion.
5. Consigner les erreurs et un rappel différé dans le [journal](Suivi-pilote.md).

Le noyau reste la règle de correction du rappel ; l'approfondissement explique
et permet de reconstruire le raisonnement. La longueur n'impose pas une récitation
intégrale. Les preuves de passage suivantes sont des activités proposées, pas des
expériences annoncées comme exécutées ni une certification de niveau senior.

'''
    for number, step in enumerate(steps, 1):
        text += f"## {number}. {step['titre']}\n\n{step['objectif']}\n\n"
        text += '| Ordre | Sujet et fiche | Cartes | Prérequis déclarés |\n| --- | --- | --- | --- |\n'
        for index, identity in enumerate(step['sujets'], 1):
            entry = by_id[identity]
            prerequisites = json.loads(entry.get('prerequis', '[]'))
            links = ', '.join(f"[{p}](../{by_id[p]['ref']})" for p in prerequisites) or '[Conventions](Pre-requis.md)'
            text += (f"| {number}.{index} | [{entry['title']}](../{entry['ref']}) | "
                     f"[{len(entry['card_ids'])} cartes](../{entry['cards_path']}) | {links} |\n")
        text += f"\n**Critère de passage proposé** : {step['preuve']}\n\n"
    text += f'''## Trois intégrations pour vérifier le transfert

- **Recalage et mesure d'une pièce** : acquisition contrôlée → features → matches
  → modèle géométrique → calibration → mesure indépendante. Départager faible
  résidu, mauvaise couverture et modèle faux sur une nouvelle configuration.
- **Détection et suivi vidéo** : données groupées par séquence → métriques de
  détection → posttraitement → filtre et association → métriques d'identité →
  latence de bout en bout. Reconstituer un échange d'IDs à partir des événements.
- **Perception spatiale** : repères et horloges → calibration → profondeur ou
  nuages → pose/fusion → représentation avec visibilité → validation métrique.
  Tester une région inconnue et une rotation sans masquer le défaut par alignement.

Pour chaque cas : baseline simple, variation contrôlée, prédiction, mesure sur
référence et explication des écarts. Les [cas de transfert](Cas-transfert.md)
et les [pôles métiers](Poles-metiers.md) fournissent d'autres scénarios.
Des cartes rappelées correctement ne prouvent pas seules ce transfert.

## Contrôles du parcours

`python3 scripts/learning_path.py` contrôle couverture des fiches, unicité,
ordre des prérequis et seuil éditorial de {MIN_ANSWER_WORDS} mots lexicaux par réponse.
Un ordre strict respectant chaque dépendance exclut un cycle ; un lien inconnu
ou une nouvelle fiche non intégrée fait échouer le contrôle. Le seuil signale
une réponse courte, sans certifier sa justesse ni sa qualité pédagogique.
`python3 scripts/sync_catalog.py --check` contrôle que cette page est à jour.

[Accueil](../00-Accueil.md) · [Inventaire](Inventaire.md) · [Guide Anki](Guide-Anki.md).
'''
    return text


def main():
    if __package__:
        from .build_apkg import parse_cards
        from .sync_catalog import collect
    else:
        from build_apkg import parse_cards
        from sync_catalog import collect
    entries = collect(ROOT / 'vault')
    steps = json.loads((ROOT / 'scripts/learning_path.json').read_text())['etapes']
    errors = validate_order(entries, steps)
    cards = parse_cards(ROOT / 'vault')
    lengths = {card['id']: len(re.findall(r'\w+', card['fields']['Reponse'])) for card in cards}
    for identity, words in lengths.items():
        if words < MIN_ANSWER_WORDS:
            errors.append(f'{identity} : réponse courte ({words} < {MIN_ANSWER_WORDS} mots lexicaux)')
    for error in errors:
        print(error, file=sys.stderr)
    print(json.dumps({'resultat': 'ECHEC' if errors else 'OK', 'fiches': len(entries),
                      'cartes': len(cards), 'minimum_mots': min(lengths.values(), default=0),
                      'erreurs': len(errors)}, ensure_ascii=False))
    return int(bool(errors))


if __name__ == '__main__':
    sys.exit(main())
