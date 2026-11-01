"""Check curriculum order and flag answers that need fuller explanations."""

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MIN_ANSWER_WORDS = 180


def validate_order(entries, steps):
    """Require each reference once, with every prerequisite appearing first."""
    by_id = {entry['id']: entry for entry in entries}
    ordered = [identity for step in steps for identity in step['sujets']]
    errors, positions = [], {}
    for index, identity in enumerate(ordered):
        if identity in positions:
            errors.append('Duplicate subject: ' + identity)
        positions[identity] = index
        if identity not in by_id:
            errors.append('Unknown subject: ' + identity)
    for identity, entry in by_id.items():
        if identity not in positions:
            errors.append('Subject missing from curriculum: ' + identity)
        for prerequisite in json.loads(entry.get('prerequis', '[]')):
            if prerequisite not in by_id:
                errors.append(f'{identity}: unknown prerequisite {prerequisite}')
            elif identity in positions and prerequisite in positions:
                if positions[prerequisite] >= positions[identity]:
                    errors.append(f'{identity} must follow {prerequisite}')
    return errors


def render_path(entries, steps, open_target_count):
    errors = validate_order(entries, steps)
    if errors:
        raise ValueError('\n'.join(errors))
    by_id = {entry['id']: entry for entry in entries}
    text = f'''# Senior curriculum: understand, verify, integrate

This curriculum orders the {len(entries)} existing subjects. Directories classify
content by topic; their numbers do not prescribe review order. The {open_target_count}
open topics for further study in the [inventory](Inventaire.md) remain to be written.

You already know ML/DL and semantic segmentation: use the progression criteria
as entry tests and spend more time on classical vision, geometry, detection and
tracking. For a familiar stage, work through its diagnostic cases without
repeating an entire deep learning course.

```mermaid
flowchart TD
    A[Acquisition, conventions and evaluation] --> B[Image processing and features]
    B --> C[Matching and robust geometry]
    C --> D[Calibration, multiview and 3D]
    A --> E[Representations, detection and segmentation]
    E --> F[Motion, association and tracking]
    D --> G[VIO, fusion and spatial perception]
    F --> G
    E --> H[Generative and multimodal vision]
    G --> I[Integration and deployment]
    H --> I
```

The diagram shows the main branches; the tables below provide the complete
validated order and prerequisites declared in each reference note. A prerequisite
refers to the concepts being used, rather than every advanced detail of its note:
SORT needs IoU and basic Kalman filtering, for example, without requiring all of
COCO AP or a complete ESKF. Local reminders appear in the [conventions](Pre-requis.md).
Links to alternatives do not become mandatory dependencies.

## How to work through a stage

1. Attempt the expected answer before reading it, then explain the mechanism in your own words.
2. Read the detailed explanation, follow the example and check units and assumptions.
3. Change one factor: noise, frame rate, scale, visibility or a constraint.
4. Predict the effect, propose a check and discuss what the result can establish.
5. Record mistakes and delayed recall in the [progress log](Suivi-pilote.md).

The expected answer remains the grading rule; the detailed explanation helps
reconstruct the reasoning. Length does not require verbatim recitation of the
whole answer. The progression criteria below are proposed activities, rather
than completed experiments or certification of senior-level proficiency.

'''
    for number, step in enumerate(steps, 1):
        text += f"## {number}. {step['titre']}\n\n{step['objectif']}\n\n"
        text += '| Order | Subject and reference | Flashcards | Declared prerequisites |\n| --- | --- | --- | --- |\n'
        for index, identity in enumerate(step['sujets'], 1):
            entry = by_id[identity]
            prerequisites = json.loads(entry.get('prerequis', '[]'))
            links = ', '.join(f"[{p}](../{by_id[p]['ref']})" for p in prerequisites) or '[Conventions](Pre-requis.md)'
            text += (f"| {number}.{index} | [{entry['title']}](../{entry['ref']}) | "
                     f"[{len(entry['card_ids'])} cards](../{entry['cards_path']}) | {links} |\n")
        text += f"\n**Proposed progression criterion**: {step['preuve']}\n\n"
    text += f'''## Three integration cases to assess transfer

- **Part registration and measurement**: controlled acquisition → features → matches
  → geometric model → calibration → independent measurement. Distinguish a small
  residual, poor spatial coverage and an unsuitable model on a new configuration.
- **Video detection and tracking**: sequence-grouped data → detection metrics →
  postprocessing → filtering and association → identity metrics → end-to-end
  latency. Reconstruct an ID switch from the sequence of events.
- **Spatial perception**: coordinate frames and clocks → calibration → depth or
  point clouds → pose/fusion → visibility-aware representation → metric validation.
  Test an unknown region and a rotation without hiding the defect through alignment.

For each case: a simple baseline, controlled variation, prediction, measurement
against a reference, and explanation of discrepancies. The [transfer cases](Cas-transfert.md)
and [career tracks](Poles-metiers.md) provide further scenarios.
Correct recall alone does not establish transfer to these tasks.

## Curriculum checks

`python3 scripts/learning_path.py` checks reference coverage, uniqueness,
prerequisite order and an editorial threshold of {MIN_ANSWER_WORDS} lexical words per answer.
Strict ordering of every dependency excludes cycles; an unknown dependency
or a new reference missing from the path fails the check. The threshold flags
short answers without certifying scientific accuracy or educational quality.
`python3 scripts/sync_catalog.py --check` checks that this page is current.

[Home](../00-Accueil.md) · [Inventory](Inventaire.md) · [Anki guide](Guide-Anki.md).
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
            errors.append(f'{identity}: short answer ({words} < {MIN_ANSWER_WORDS} lexical words)')
    for error in errors:
        print(error, file=sys.stderr)
    print(json.dumps({'resultat': 'ECHEC' if errors else 'OK', 'fiches': len(entries),
                      'cartes': len(cards), 'minimum_mots': min(lengths.values(), default=0),
                      'erreurs': len(errors)}, ensure_ascii=False))
    return int(bool(errors))


if __name__ == '__main__':
    sys.exit(main())
