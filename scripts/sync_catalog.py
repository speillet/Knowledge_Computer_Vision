"""Rebuild indexes from reference notes without generating learning content."""
import argparse
import json
from pathlib import Path
import re
import sys

if __package__:
    from .check_vault import SECTIONS, parse_poles
    from .learning_path import render_path
else:
    from check_vault import SECTIONS, parse_poles
    from learning_path import render_path

ROOT = Path(__file__).resolve().parents[1]
POLES = {
    'A': 'Deep Learning & Image Understanding',
    'B': 'Geometric Vision & Spatial AI',
    'C': 'Robotics & Autonomous Perception',
    'D': 'Multimodal AI & Video Intelligence',
    'E': 'Applied Computer Vision',
    'F': 'Vision Systems & Deployment',
}
# Metadata values remain stable; these labels are for readers.
LABELS = {
    'methode': 'method', 'probleme': 'problem', 'comparaison': 'comparison',
    'metrique-protocole': 'metric/protocol', 'pipeline': 'pipeline',
    'reperage': 'overview', 'usage-operationnel': 'operational use',
    'approfondissement': 'in-depth study', 'redige': 'drafted',
    'conception': 'design', 'diagnostic': 'diagnosis',
}


def collect(vault):
    entries = []
    for section in SECTIONS:
        folder = vault / section['dossier']
        for ref in sorted((folder / 'references').glob('*.md')):
            text = ref.read_text(encoding='utf-8')
            front = re.match(r'---\n(.*?)\n---\n', text, re.S)
            if not front:
                raise ValueError(f'Missing metadata: {ref}')
            meta = dict(re.findall(r'^(\w+):\s*(.+)$', front[1], re.M))
            path = folder / ref.name
            cards = path.read_text(encoding='utf-8')
            ids = re.findall(r'^ID: (.+)$', cards, re.M)
            cases = []
            for block in re.findall(r'^START\n(.*?)\nEND$', cards, re.M | re.S):
                identity = re.search(r'^ID: (.+)$', block, re.M)[1]
                for match in re.finditer(r'cas_pole::([A-F])::(conception|diagnostic)', block):
                    cases.append((match[1], match[2], identity))
            entries.append({**meta, 'poles': parse_poles(meta['poles']),
                            'title': re.search(r'^# (.+)$', text, re.M)[1],
                            'ref': ref.relative_to(vault).as_posix(),
                            'cards_path': path.relative_to(vault).as_posix(),
                            'card_ids': ids,
                            'cases': cases})
    return entries


def partition_targets(targets, known_ids):
    """Retain every target; promotion requires an existing reference note."""
    opened, drafted, seen = [], [], set()
    for target in targets:
        identity = target['id']
        if identity in seen:
            raise ValueError('Duplicate coverage target: ' + identity)
        seen.add(identity)
        reference = target.get('fiche')
        if reference:
            if reference not in known_ids:
                raise ValueError('Missing coverage reference note: ' + reference)
            drafted.append(target)
        else:
            opened.append(target)
    return opened, drafted


def outputs(root):
    vault = root / 'vault'
    entries = collect(vault)
    by_id = {e['id']: e for e in entries}
    targets = json.loads((root / 'scripts/coverage_targets.json').read_text(encoding='utf-8'))
    opened, drafted = partition_targets(targets, by_id)
    result = {}
    total = sum(len(e['card_ids']) for e in entries)
    active = sum(any(e['domaine'] == s['domaine'] for e in entries) for s in SECTIONS)
    summary = f"**{len(entries)} reference notes and {total} flashcards**, spanning {active} of {len(SECTIONS)} topics. "
    summary += 'Agent-authored content; actual device import, recall and personal mastery remain unvalidated.\n\n'
    table = '| Topic | Reference notes | Flashcards |\n| --- | ---: | ---: |\n'
    for s in SECTIONS:
        local = [e for e in entries if e['domaine'] == s['domaine']]
        table += f"| [{s['titre']}]({s['dossier']}/00-index.md) | {len(local)} | {sum(len(e['card_ids']) for e in local)} |\n"
        index = '# ' + s['titre'] + '\n\n' + s['description'] + '\n\n'
        if local:
            index += '| Subject | Reference | Flashcards | Career tracks |\n| --- | --- | ---: | --- |\n'
            for e in local:
                index += f"| [{e['title']}]({Path(e['cards_path']).name}) | [Read](references/{Path(e['ref']).name}) | {len(e['card_ids'])} | {', '.join(e['poles'])} |\n"
            index += f"\nSubdeck: `CV::Pilote::{s['dossier']}`. Status: drafted; device import and mastery unverified.\n"
        else:
            index += 'No reference notes or flashcards drafted yet; see planned subjects in the inventory.\n'
        index += '\n[Home](../00-Accueil.md) · [Inventory](../01-Parcours/Inventaire.md) · [Career tracks](../01-Parcours/Poles-metiers.md).\n'
        result[vault / s['dossier'] / '00-index.md'] = index
    home = '# Computer vision — understand, choose, diagnose\n\n'
    home += summary + 'This curriculum targets an engineer already comfortable with ML/DL. Reference notes explain concepts; flashcards train recall with explicit grading criteria. Coverage of a topic does not imply in-depth coverage of all its variants.\n\n'
    home += '## Getting started\n\n1. Read the [conventions](01-Parcours/Pre-requis.md).\n2. Follow the [inventory](01-Parcours/Inventaire.md) or a [career track](01-Parcours/Poles-metiers.md).\n3. Attempt each question before reading its expected answer, then explain it in your own words.\n4. Prepare Android reviews with the [AnkiDroid guide](01-Parcours/Guide-Anki.md).\n5. Record recall and import results in the [progress log](01-Parcours/Suivi-pilote.md).\n\n'
    home += '[Ordered senior curriculum](01-Parcours/Parcours-senior.md): prerequisites, stages and progression criteria.\n\n'
    home += '## Browse by topic\n\n' + table
    home += '\nOne directory per topic, with flashcards in that directory and reference notes in `references/`, following the layout of [Knowledge_AI_Engineering](https://github.com/speillet/Knowledge_AI_Engineering). Python examples live outside the vault and state their limitations.\n'
    result[vault / '00-Accueil.md'] = home
    steps = json.loads((root / 'scripts/learning_path.json').read_text(encoding='utf-8'))['etapes']
    result[vault / '01-Parcours/Parcours-senior.md'] = render_path(entries, steps, len(opened))
    inv = '# Coverage inventory\n\n' + summary
    inv += 'Each entry below identifies a canonical reference note for a method, pipeline, comparison or protocol. Depth applies to that subject; mentioning a method in a comparison does not constitute full coverage. Competencies and sources are detailed in each reference.\n\nV0 = priority gaps; V1 = career-track foundations; V2 = further study. Drafted content, independent review, verified import and personal mastery are separate states; agent self-review never qualifies as independent review.\n\n'
    for s in SECTIONS:
        inv += '## ' + str(int(s['domaine'][1:])) + ' — ' + s['titre'] + '\n\n'
        inv += '| Entry / type | Priority / depth | Career tracks | Prerequisites | Artifacts, competencies and sources | Status |\n| --- | --- | --- | --- | --- | --- |\n'
        for e in entries:
            if e['domaine'] != s['domaine']:
                continue
            prereqs = json.loads(e.get('prerequis', '[]'))
            pre = ', '.join(f"[{p}](../{by_id[p]['ref']})" if p in by_id else p for p in prereqs) or '[Conventions](Pre-requis.md)'
            inv += f"| {e['id']} — {e['title']} / {LABELS[e['type']]} | {e['priorite']} / {LABELS[e['profondeur']]} | {', '.join(e['poles'])} | {pre} | [Reference](../{e['ref']}) · [{len(e['card_ids'])} cards](../{e['cards_path']}) | {LABELS.get(e['statut'], e['statut'])}, device import unverified; mastery unmeasured |\n"
    inv += '\n## Open topics for further study\n\nThis list retains methods and variants named in the curriculum but not yet individually covered at the target depth. An introduction in a comparison or pipeline does not close a gap. Learning objectives, required dependencies and sources must be specified before drafting. Links below indicate thematic connections, rather than validated prerequisites.\n\n'
    if drafted:
        inv += f'{len(opened)} entries remain open; {len(drafted)} entries now have reference notes at the target depth. Drafting and validation remain separate.\n\n'
    inv += '| Entry | Domain | Career tracks | Target | Thematic connection | Status |\n| --- | --- | --- | --- | --- | --- |\n'
    for t in opened:
        parent = by_id.get(t.get('connexe'))
        link = f"[Related introduction](../{parent['ref']})" if parent else 'Specify before drafting'
        inv += f"| {t['id']} — {t['titre']} | {t['domaine']} | {', '.join(t['poles'])} | {t['priorite']} / {LABELS[t['profondeur']]} | {link} | Further study needed; specify competencies, prerequisites and sources |\n"
    if drafted:
        inv += '\n## Backlog entries now drafted\n\nAPP IDs are retained to track progress. Content exists at the stated depth; additional variants, import and mastery must be validated separately.\n\n'
        inv += '| Entry | Reference and depth | Target competencies | Required prerequisites | Status |\n| --- | --- | --- | --- | --- |\n'
        for target in drafted:
            entry = by_id[target['fiche']]
            prerequisites = ', '.join(f"[{identity}](../{by_id[identity]['ref']})" for identity in target['prerequis']) or '[Conventions](Pre-requis.md)'
            inv += f"| {target['id']} — {target['titre']} | [{entry['title']}](../{entry['ref']}) / {LABELS[entry['profondeur']]} | {'; '.join(target['competences'])} | {prerequisites} | Drafted; device import and mastery unverified |\n"
    result[vault / '01-Parcours/Inventaire.md'] = inv
    pole_doc = '# Learning paths by career track\n\nCareer tracks overlay the topic structure; a shared reference note retains one domain and one ID. These counts track drafting, rather than job readiness or mastery. V0 remains the priority.\n\n'
    for letter, title in POLES.items():
        local = [e for e in entries if letter in e['poles']]
        pole_doc += f"## {letter} — {title}\n\n{len(local)} associated reference notes, {sum(len(e['card_ids']) for e in local)} flashcards; device import unverified, mastery unmeasured.\n\n"
        pole_doc += '| Subject | Reference target depth | Artifacts |\n| --- | --- | --- |\n'
        for e in local:
            pole_doc += f"| {e['title']} | {LABELS[e['profondeur']]} | [Reference](../{e['ref']}) · [Flashcards](../{e['cards_path']}) |\n"
        pole_doc += '\nTrack-specific cases, with answers and grading criteria in each card:\n\n'
        cases = [(e, c) for e in entries for c in e['cases'] if c[0] == letter]
        for kind in ['conception', 'diagnostic']:
            selected = [(e, c) for e, c in cases if c[1] == kind]
            if selected:
                for e, c in selected:
                    pole_doc += f"- {LABELS[kind].capitalize()}: [{c[2]}](../{e['cards_path']}#{c[2].lower()}).\n"
            else:
                pole_doc += '- ' + LABELS[kind].capitalize() + ': to be drafted.\n'
        pole_doc += '\n'
    pole_doc += '[Home](../00-Accueil.md) · [Inventory](Inventaire.md) · [Progress log](Suivi-pilote.md).\n'
    result[vault / '01-Parcours/Poles-metiers.md'] = pole_doc
    readme = (root / 'README.md').read_text(encoding='utf-8')
    block = '<!-- cv-catalog:start -->\n' + summary + table.replace('](', '](vault/') + '<!-- cv-catalog:end -->'
    if '<!-- cv-catalog:start -->' in readme:
        readme = re.sub(r'<!-- cv-catalog:start -->.*?<!-- cv-catalog:end -->', lambda _: block, readme, flags=re.S)
    else:
        readme += '\n## Current coverage\n\n' + block + '\n'
    result[root / 'README.md'] = readme
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    rendered = outputs(ROOT)
    stale = [p for p, text in rendered.items() if not p.exists() or p.read_text(encoding='utf-8') != text]
    if args.check:
        for path in stale:
            print('Outdated catalogue: ' + str(path.relative_to(ROOT)), file=sys.stderr)
    else:
        for path, text in rendered.items():
            path.write_text(text, encoding='utf-8')
    print(json.dumps({'generated_documents': len(rendered), 'stale': len(stale)}, ensure_ascii=False))
    return int(args.check and bool(stale))


if __name__ == '__main__':
    sys.exit(main())
