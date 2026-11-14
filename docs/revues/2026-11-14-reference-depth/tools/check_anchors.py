"""Check local Markdown links and heading anchors in vault/ and docs/revues/.

Usage: python3 check_anchors.py <repo-root> [subdir ...]
Slugs follow the GitHub rule: lowercase, drop punctuation except '-' and '_',
spaces to '-'. Wiki links ([[...]]) resolve from the vault root.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

FENCE = re.compile(r"^```.*?^```\s*$", re.M | re.S)


def slug(h):
    h = re.sub(r"\$[^$]*\$", lambda m: m[0].replace("$", ""), h).strip().lower()
    h = re.sub(r"[^\w\- ]", "", h, flags=re.U)
    return h.replace(" ", "-")


def anchors(path, cache={}):
    if path not in cache:
        text = FENCE.sub("", path.read_text(encoding="utf-8"))
        seen, out = {}, set()
        for h in re.findall(r"^#{1,6} (.+?)\s*#*\s*$", text, re.M):
            s = slug(h)
            n = seen.get(s, 0)
            out.add(s if n == 0 else f"{s}-{n}")
            seen[s] = n + 1
        cache[path] = out
    return cache[path]


def main():
    root = Path(sys.argv[1]).resolve()
    subdirs = sys.argv[2:] or ["vault", "docs/revues/2026-11-14-reference-depth"]
    vault = root / "vault"
    errors, checked = [], 0
    for sub in subdirs:
        for path in sorted((root / sub).rglob("*.md")):
            text = FENCE.sub("", path.read_text(encoding="utf-8"))
            text = re.sub(r"`[^`\n]*`", "", text)
            targets = [m for m in re.findall(r"\]\(([^\s)]+)\)", text)]
            targets += re.findall(r"^\[[^\]]+\]:\s*(\S+)", text, re.M)
            wiki = re.findall(r"\[\[([^\]]+)\]\]", text)
            for t in targets:
                if re.match(r"[a-z]+:", t):
                    continue
                checked += 1
                file_part, _, frag = unquote(t).partition("#")
                target = (path.parent / file_part).resolve() if file_part else path
                if not target.is_file():
                    errors.append(f"{path.relative_to(root)}: missing {t}")
                elif frag and target.suffix == ".md" and frag.lower() not in anchors(target):
                    errors.append(f"{path.relative_to(root)}: missing anchor {t}")
            for w in wiki:
                checked += 1
                file_part = w.split("|", 1)[0]
                file_part, _, frag = file_part.partition("#")
                target = (vault / file_part)
                if not target.suffix:
                    target = target.with_suffix(".md")
                if not target.is_file():
                    errors.append(f"{path.relative_to(root)}: missing wiki {w}")
    for e in errors:
        print("ERROR", e)
    print(f"checked {checked} local links, {len(errors)} errors")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
