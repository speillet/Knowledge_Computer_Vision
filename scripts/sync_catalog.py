"""Reconstruit les index depuis les fiches ; ne génère pas le contenu pédagogique."""
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

def collect(vault):
    entries = []
    for section in SECTIONS:
        folder = vault / section['dossier']
        for ref in sorted((folder / 'references').glob('*.md')):
            text = ref.read_text(encoding='utf-8')
            front = re.match(r'---\n(.*?)\n---\n', text, re.S)
            if not front:
                raise ValueError(f'Métadonnées absentes : {ref}')
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
    """Conserve chaque cible ; une promotion exige une fiche existante."""
    opened, drafted, seen = [], [], set()
    for target in targets:
        identity = target['id']
        if identity in seen:
            raise ValueError('Cible de couverture dupliquée : ' + identity)
        seen.add(identity)
        reference = target.get('fiche')
        if reference:
            if reference not in known_ids:
                raise ValueError('Fiche de couverture absente : ' + reference)
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
    summary = f"**{len(entries)} fiches et {total} cartes**, réparties dans {active} des {len(SECTIONS)} thématiques. "
    summary += 'Rédaction par agent ; export réel, rappel et maîtrise personnelle non validés.\n\n'
    table = '| Thématique | Fiches | Cartes |\n| --- | ---: | ---: |\n'
    for s in SECTIONS:
        local = [e for e in entries if e['domaine'] == s['domaine']]
        table += f"| [{s['titre']}]({s['dossier']}/00-index.md) | {len(local)} | {sum(len(e['card_ids']) for e in local)} |\n"
        index = '# ' + s['titre'] + '\n\n' + s['description'] + '\n\n'
        if local:
            index += '| Sujet | Référence | Cartes | Pôles |\n| --- | --- | ---: | --- |\n'
            for e in local:
                index += f"| [{e['title']}]({Path(e['cards_path']).name}) | [Lire](references/{Path(e['ref']).name}) | {len(e['card_ids'])} | {', '.join(e['poles'])} |\n"
            index += f"\nSous-deck : `CV::Pilote::{s['dossier']}`. Statut : rédigé ; export et maîtrise non vérifiés.\n"
        else:
            index += 'Aucune fiche ni carte rédigée pour le moment ; voir les sujets prévus dans l’inventaire.\n'
        index += '\n[Accueil](../00-Accueil.md) · [Inventaire](../01-Parcours/Inventaire.md) · [Pôles](../01-Parcours/Poles-metiers.md).\n'
        result[vault / s['dossier'] / '00-index.md'] = index
    home = '# Computer vision — comprendre, choisir, diagnostiquer\n\n'
    home += summary + 'Ce parcours vise un ingénieur déjà à l’aise en ML/DL. Les fiches expliquent ; les cartes entraînent un rappel corrigible. Une thématique représentée ne signifie pas que toutes ses variantes sont approfondies.\n\n'
    home += '## Commencer\n\n1. Lire les [conventions](01-Parcours/Pre-requis.md).\n2. Suivre l’[inventaire](01-Parcours/Inventaire.md) ou un [pôle métier](01-Parcours/Poles-metiers.md).\n3. Essayer les cartes avant de lire leur noyau attendu, puis reformuler.\n4. Préparer la révision Android avec le [guide AnkiDroid](01-Parcours/Guide-Anki.md).\n5. Consigner rappel et export dans le [journal](01-Parcours/Suivi-pilote.md).\n\n'
    home += '[Parcours senior ordonné](01-Parcours/Parcours-senior.md) : prérequis, étapes et critères de passage.\n\n'
    home += '## Navigation par thématique\n\n' + table
    home += '\nUn répertoire par thème, cartes dans le thème et fiches dans `references/`, selon l’organisation de [Knowledge_AI_Engineering](https://github.com/speillet/Knowledge_AI_Engineering). Les exemples Python du dépôt sont hors vault et précisent leurs limites.\n'
    result[vault / '00-Accueil.md'] = home
    steps = json.loads((root / 'scripts/learning_path.json').read_text(encoding='utf-8'))['etapes']
    result[vault / '01-Parcours/Parcours-senior.md'] = render_path(entries, steps, len(opened))
    inv = '# Inventaire de couverture\n\n' + summary
    inv += 'Les lignes ci-dessous désignent des fiches canoniques de méthode, pipeline, comparaison ou protocole. La profondeur porte sur ce sujet ; un nom cité en comparaison ne devient pas une méthode entièrement approfondie. Les compétences et sources sont détaillées dans chaque référence.\n\nV0 = lacunes prioritaires ; V1 = socle des pôles ; V2 = approfondissements. Rédigé, relu, export vérifié et maîtrise personnelle sont distincts ; aucun contenu n’est déclaré relu par une auto-revue.\n\n'
    for s in SECTIONS:
        inv += '## ' + str(int(s['domaine'][1:])) + ' — ' + s['titre'] + '\n\n'
        inv += '| Entrée / type | Priorité / profondeur | Pôles | Prérequis | Artefacts, compétences et sources | État |\n| --- | --- | --- | --- | --- | --- |\n'
        for e in entries:
            if e['domaine'] != s['domaine']: continue
            prereqs = json.loads(e.get('prerequis', '[]'))
            pre = ', '.join(f"[{p}](../{by_id[p]['ref']})" if p in by_id else p for p in prereqs) or '[Conventions](Pre-requis.md)'
            inv += f"| {e['id']} — {e['title']} / {e['type']} | {e['priorite']} / {e['profondeur']} | {', '.join(e['poles'])} | {pre} | [Fiche](../{e['ref']}) · [{len(e['card_ids'])} cartes](../{e['cards_path']}) | {e['statut']}, export non vérifié ; maîtrise non mesurée |\n"
    inv += '\n## Approfondissements encore ouverts\n\nCette liste conserve des méthodes/variantes nommées dans la cartographie mais non traitées individuellement à la profondeur cible. Une introduction dans une comparaison ou un pipeline ne ferme pas cette lacune. Les objectifs d’apprentissage, dépendances obligatoires et sources seront précisés avant leur rédaction. Les liens ci-dessous sont des connexions thématiques, pas des prérequis déjà validés.\n\n'
    if drafted:
        inv += f'{len(opened)} entrées encore ouvertes ; {len(drafted)} entrées disposent désormais de fiches au niveau cible. Rédaction et validation restent distinctes.\n\n'
    inv += '| Entrée | Domaine | Pôles | Cible | Connexion thématique | État |\n| --- | --- | --- | --- | --- | --- |\n'
    for t in opened:
        parent = by_id.get(t.get('connexe'))
        link = f"[Introduction connexe](../{parent['ref']})" if parent else 'À préciser avant rédaction'
        inv += f"| {t['id']} — {t['titre']} | {t['domaine']} | {', '.join(t['poles'])} | {t['priorite']} / {t['profondeur']} | {link} | À approfondir ; compétences, prérequis et source à préciser |\n"
    if drafted:
        inv += '\n## Entrées du backlog désormais rédigées\n\nLes IDs APP sont conservés pour retracer la progression. Le contenu existe au niveau indiqué ; variantes supplémentaires, export et maîtrise restent à valider séparément.\n\n'
        inv += '| Entrée | Fiche et profondeur | Compétences visées | Prérequis obligatoires | État |\n| --- | --- | --- | --- | --- |\n'
        for target in drafted:
            entry = by_id[target['fiche']]
            prerequisites = ', '.join(f"[{identity}](../{by_id[identity]['ref']})" for identity in target['prerequis']) or '[Conventions](Pre-requis.md)'
            inv += f"| {target['id']} — {target['titre']} | [{entry['title']}](../{entry['ref']}) / {entry['profondeur']} | {' ; '.join(target['competences'])} | {prerequisites} | Rédigé ; export et maîtrise non vérifiés |\n"
    result[vault / '01-Parcours/Inventaire.md'] = inv
    pole_doc = '# Parcours par pôle métier\n\nLes pôles sont une surcouche des thèmes ; une fiche partagée conserve un seul domaine et un seul ID. Ces comptes suivent la rédaction, pas l’aptitude à un poste ni la maîtrise. La vague V0 reste prioritaire.\n\n'
    for letter, title in POLES.items():
        local = [e for e in entries if letter in e['poles']]
        pole_doc += f"## {letter} — {title}\n\n{len(local)} fiches rattachées, {sum(len(e['card_ids']) for e in local)} cartes ; export non vérifié, maîtrise non mesurée.\n\n"
        pole_doc += '| Sujet | Profondeur cible de la fiche | Artefacts |\n| --- | --- | --- |\n'
        for e in local:
            pole_doc += f"| {e['title']} | {e['profondeur']} | [Fiche](../{e['ref']}) · [Cartes](../{e['cards_path']}) |\n"
        pole_doc += '\nCas propres au pôle, avec réponse et critères dans la carte :\n\n'
        cases = [(e,c) for e in entries for c in e['cases'] if c[0]==letter]
        for kind in ['conception','diagnostic']:
            selected = [(e,c) for e,c in cases if c[1]==kind]
            if selected:
                for e,c in selected: pole_doc += f"- {kind.capitalize()} : [{c[2]}](../{e['cards_path']}#{c[2].lower()}).\n"
            else: pole_doc += '- ' + kind.capitalize() + ' : à rédiger.\n'
        pole_doc += '\n'
    pole_doc += '[Accueil](../00-Accueil.md) · [Inventaire](Inventaire.md) · [Suivi](Suivi-pilote.md).\n'
    result[vault / '01-Parcours/Poles-metiers.md'] = pole_doc
    readme = (root/'README.md').read_text(encoding='utf-8')
    block = '<!-- cv-catalog:start -->\n' + summary + table.replace('](', '](vault/') + '<!-- cv-catalog:end -->'
    if '<!-- cv-catalog:start -->' in readme:
        readme = re.sub(r'<!-- cv-catalog:start -->.*?<!-- cv-catalog:end -->',lambda _:block,readme,flags=re.S)
    else: readme += '\n## Couverture actuelle\n\n' + block + '\n'
    result[root/'README.md'] = readme
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    rendered=outputs(ROOT)
    stale=[p for p,text in rendered.items() if not p.exists() or p.read_text(encoding='utf-8')!=text]
    if args.check:
        for path in stale:print('Catalogue périmé : '+str(path.relative_to(ROOT)),file=sys.stderr)
    else:
        for path,text in rendered.items():path.write_text(text,encoding='utf-8')
    print(json.dumps({'generated_documents':len(rendered),'stale':len(stale)},ensure_ascii=False))
    return int(args.check and bool(stale))

if __name__=='__main__':
    sys.exit(main())
