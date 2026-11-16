"""Generate Hugo reading pages from the vault without changing learning sources.

The source parser is shared with the Anki exporter; no export dependency is needed.
Only website/content/ and website/static/vault/ are replaced by this script.
"""

import argparse
import base64
from collections import defaultdict
import html
import json
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import quote, unquote, urlsplit

if __package__:
    from .build_apkg import parse_cards
    from .check_vault import HEADER, SECTIONS, check_vault
else:
    from build_apkg import parse_cards
    from check_vault import HEADER, SECTIONS, check_vault

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "https://github.com/speillet/Knowledge_Computer_Vision"
WIKI = re.compile(r"\[\[([^\]\n]+)\]\]")
LINK = re.compile(r"(!?\[[^\]\n]*\])\(([^\s)]+)\)")
REFERENCE = re.compile(r"^(\[[^\]]+\]:\s*)(\S+)", re.M)
CODE = re.compile(r"(`+[^`\n]+`+)")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")


def content_path(source):
    """Keep vault paths, mapping home and domain indexes to Hugo branch bundles."""
    source = Path(source)
    if source == Path("00-Accueil.md"):
        return Path("_index.md")
    if source.name == "00-index.md":
        return source.with_name("_index.md")
    return source


def ref(source, fragment=""):
    target = "/" + content_path(source).as_posix()
    if fragment:
        target += "#" + fragment
    return "{{< relref " + json.dumps(target, ensure_ascii=False) + " >}}"


def heading_and_body(text):
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    heading = re.search(r"^# (.+)$", text, re.M)
    if not heading:
        raise ValueError("Page has no level-one title")
    return heading[1], text[:heading.start()] + text[heading.end():]


def front_matter(title, source=None, **params):
    data = {"title": title, **params}
    if source:
        data["source"] = "vault/" + source.as_posix()
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n\n"


def fold(summary, body, ident, *, css_class="kv-fold", is_open=False):
    """Use the reference site's collapsible layout with Markdown-safe blank lines."""
    attribute = " open" if is_open else ""
    return "\n".join([
        f'<details class="{css_class}" id="{ident}"{attribute}>',
        f'<summary><span class="kv-fold-title">{summary}</span>'
        '<span class="kv-chevron" aria-hidden="true"></span></summary>',
        '<div class="kv-fold-body">', "", body.strip(), "", "</div>", "</details>", "",
    ])


def topic_tile(source, title, cards, objectives):
    points = "".join(f"<li>{html.escape(objective)}</li>" for objective in objectives)
    return (
        f'<li class="kv-tile"><a class="kv-tile-title" href="{ref(source)}">'
        f'{html.escape(title)}</a><span class="kv-tile-meta">{cards} flashcards</span>'
        f'<details class="kv-tile-more"><summary>{len(objectives)} points covered</summary>'
        f'<ul class="kv-points kv-small">{points}</ul></details></li>'
    )


def convert_links(markdown, source, vault, pages):
    """Resolve local links, preserving code and mathematical backslashes."""
    vault = Path(vault).resolve()

    def local_url(url, wiki=False):
        parts = urlsplit(url)
        if parts.scheme or parts.netloc or url.startswith("#"):
            return url
        local = unquote(parts.path)
        target = ((vault if wiki else (vault / source).parent) / local).resolve()
        if wiki and not target.suffix:
            target = target.with_suffix(".md")
        if not target.is_relative_to(vault):
            repo_root = vault.parent
            if not target.is_relative_to(repo_root) or not target.is_file():
                raise ValueError(f"{source}: missing local link {url}")
            suffix = "#" + parts.fragment if parts.fragment else ""
            return REPOSITORY + "/blob/main/" + quote(target.relative_to(repo_root).as_posix()) + suffix
        relative = target.relative_to(vault)
        if relative in pages:
            return ref(relative, parts.fragment)
        if not target.is_file():
            raise ValueError(f"{source}: missing local link {url}")
        return "{{< vault-asset " + json.dumps(relative.as_posix()) + " >}}"

    def wiki(match):
        target, _, label = match[1].partition("|")
        return "[" + (label or target.split("#", 1)[0].rsplit("/", 1)[-1]) + "](" + local_url(target, True) + ")"

    def line(text):
        chunks = CODE.split(text)
        for i in range(0, len(chunks), 2):
            chunks[i] = LINK.sub(lambda m: m[1] + "(" + local_url(m[2]) + ")", chunks[i])
            chunks[i] = WIKI.sub(wiki, chunks[i])
            chunks[i] = REFERENCE.sub(lambda m: m[1] + local_url(m[2]), chunks[i])
        return "".join(chunks)

    result, fence, mermaid = [], None, False
    for text in markdown.splitlines():
        match = FENCE.match(text)
        if match and fence is None:
            fence = match[1]
            mermaid = text[match.end():].strip() == "mermaid"
            result.append("{{< mermaid >}}" if mermaid else text)
        elif fence and match and match[1][0] == fence[0] and len(match[1]) >= len(fence):
            result.append("{{< /mermaid >}}" if mermaid else text)
            fence, mermaid = None, False
        else:
            result.append(text if fence else line(text))
    return "\n".join(result)


def stage(vault, website):
    vault, website = Path(vault).resolve(), Path(website).resolve()
    errors, _ = check_vault(vault)
    if errors:
        raise ValueError("Invalid vault:\n" + "\n".join(errors))
    pages = {p.relative_to(vault) for p in vault.rglob("*.md")
             if ".obsidian" not in p.relative_to(vault).parts}
    cards = parse_cards(vault)
    by_file = defaultdict(list)
    for card in cards:
        by_file[card["file"].relative_to(vault)].append(card)
    objectives_by_file = {}

    # Generate everything in memory before replacing previous staged pages.
    generated = {}
    for source in sorted(pages):
        text = (vault / source).read_text(encoding="utf-8")
        title, body = heading_and_body(text)
        convert = lambda value: convert_links(value, source, vault, pages)
        params = {"weight": int(re.match(r"\d+", source.stem)[0]) if re.match(r"\d+", source.stem) else 0}
        if source in by_file:
            file_cards = by_file[source]
            title = re.sub(r"^Flashcards\s*[—–-]\s*", "", title)
            params.update(cards=len(file_cards), count_text=f"{len(file_cards)} flashcards",
                          description=f"{len(file_cards)} flashcards with detailed answers and sources.")
            reference = source.parent / "references" / source.name
            objectives = HEADER.findall(text)
            if len(objectives) != len(file_cards):
                raise ValueError(f"{source}: recall objectives do not match cards")
            objectives_by_file[source] = [objective for objective, _family, _provenance in objectives]
            points = "".join(f"<li>{html.escape(objective)}</li>" for objective in objectives_by_file[source])
            blocks = [
                '<div class="kv-meta not-prose">'
                f'<a class="kv-chip" href="#flashcards"><b>{len(file_cards)}</b> flashcards</a>'
                f'<a class="kv-chip" href="{ref(reference)}">Read the reference note</a></div>',
                fold(f'What this topic covers <span class="kv-count">{len(objectives)}</span>',
                     f'<ul class="kv-points not-prose">{points}</ul>', "what-this-topic-covers", css_class="kv-fold kv-covers"),
                "{{< card-tools >}}",
                '## Flashcards {#flashcards}\n\n<div class="kv-cards">',
            ]
            search = [title]
            for card, (objective, _family, _provenance) in zip(file_cards, objectives):
                fields = card["fields"]
                # Shortcode attributes do not decode JSON's backslash escapes.
                # Encode the question so LaTeX and quoted text survive unchanged.
                question = base64.b64encode(convert(fields["Question"]).encode("utf-8")).decode("ascii")
                args = {"id": card["id"], "question": question, "objective": objective}
                opening = "{{< flashcard " + " ".join(key + "=" + json.dumps(value, ensure_ascii=False)
                                                        for key, value in args.items()) + " >}}"
                blocks.extend([opening, convert(fields["Reponse"]),
                               "\n**Sources:** " + convert(fields["Source"]), "{{< /flashcard >}}\n"])
                search.extend([objective, fields["Question"], fields["Reponse"], fields["Source"]])
            blocks.append("</div>")
            params["search"] = "\n".join(search)
            body = "\n\n".join(blocks)
        else:
            body = convert(body)
            if source.parent.name == "references":
                sibling = source.parent.parent / source.name
                body = f"[Practice the flashcards]({ref(sibling)})\n\n" + body
        generated[content_path(source)] = front_matter(title, source, **params) + body.strip() + "\n"

    catalog = ["Browse a domain, practice its flashcards, or open a complete reference note.\n"]
    for index, section in enumerate(SECTIONS, 1):
        folder = Path(section["dossier"])
        topics = sorted(source for source in by_file if source.parent == folder)
        total = sum(len(by_file[source]) for source in topics)
        tiles = []
        for source in topics:
            title, _ = heading_and_body((vault / folder / "references" / source.name).read_text(encoding="utf-8"))
            tiles.append(topic_tile(source, title, len(by_file[source]), objectives_by_file[source]))
        intro = (
            "{{< lead >}}\n" + section["description"] + "\n{{< /lead >}}\n\n"
            '<div class="kv-stats not-prose">'
            f'<div class="kv-stat"><b>{len(topics)}</b><span>topics</span></div>'
            f'<div class="kv-stat"><b>{total}</b><span>cards</span></div></div>\n\n'
            "## Before you start {#before-you-start}\n\n"
            f"Use the [senior curriculum]({ref(Path('01-Parcours/Parcours-senior.md'))}) "
            "to check prerequisites and choose a learning sequence.\n\n"
            f"[Read the complete reference notes]({ref(folder / 'references/_index.md')}).\n\n"
            '<div id="go-further"></div>\n\n## All topics {#all-topics}\n'
        )
        generated[folder / "_index.md"] = front_matter(
            section["titre"], folder / "00-index.md", domain=True, number=folder.name.split("-", 1)[0],
            weight=index, description=section["description"]) + intro
        generated[folder / "references/_index.md"] = front_matter("Reference notes", weight=10000) + (
            f"Complete explanations for [{section['titre']}]({ref(folder / '00-index.md')}).\n")
        summary = (f'<span class="kv-num">{folder.name.split("-", 1)[0]}</span>'
                   f'{html.escape(section["titre"])} <span class="kv-count">{len(topics)}</span>')
        body = (f'<p class="kv-domain-intro">{html.escape(section["description"])} '
                f'<a href="{ref(folder / "00-index.md")}">Open the domain →</a></p>\n\n'
                '<ul class="kv-tiles not-prose">\n' + "\n".join(tiles) + "\n</ul>")
        catalog.append(fold(summary, body, "domain-" + section["domaine"], css_class="kv-fold kv-domain", is_open=index == 1))
    generated[Path("catalog.md")] = front_matter("Topic catalog") + "\n".join(catalog)
    generated[Path("01-Parcours/_index.md")] = front_matter("Learning guides") + "Curriculum, prerequisites, career tracks and review guidance.\n"

    content, media = website / "content", website / "static/vault"
    for output in (content, media):
        if output.exists():
            shutil.rmtree(output)
        output.mkdir(parents=True)
    for relative, text in generated.items():
        target = content / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    for source in sorted(vault.rglob("*")):
        relative = source.relative_to(vault)
        if source.is_file() and source.suffix.lower() in {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".pdf"} and ".obsidian" not in relative.parts:
            target = media / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    return len(generated), len(cards)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", type=Path, default=ROOT / "vault")
    parser.add_argument("--website", type=Path, default=ROOT / "website")
    args = parser.parse_args()
    try:
        pages, cards = stage(args.vault, args.website)
    except (ValueError, OSError) as error:
        print(error, file=sys.stderr)
        return 1
    print(f"Staged {pages} pages and {cards} flashcards for Hugo.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
