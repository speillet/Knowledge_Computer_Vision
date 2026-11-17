#!/usr/bin/env python3
"""Compare protected flashcard fields with the base commit (2026-11-17 clarity pass).

Protected and required unchanged: card IDs and their order, `## ID` headings, the
Objective/Family/Provenance header, `Source:` and `Tags:` lines, `TARGET DECK:` lines and
legacy `<!--ID: ...-->` comments. Questions and expected answers may change only as listed
in the subject report: this script prints each change so that the report can record the
old and new text.

Usage:
    python3 docs/revues/2026-11-17-clarity/checks/protected_fields.py CARD_FILE... [--base REV]

Exit status 1 if a protected field changed. Standard library and git only.
"""

import argparse
from pathlib import Path
import re
import subprocess
import sys

REPO = Path(__file__).resolve().parents[4]
BASE = "594603f"


def cards(text):
    out = {}
    pattern = re.compile(r"^## (CV-[A-Z0-9-]+-\d{3})\n\n(Objective: .*?)\n\nSTART\n(.*?)\nEND$",
                         re.M | re.S)
    for m in pattern.finditer(text):
        body = m[3]
        field = lambda name: (re.search(rf"^{name}: (.*)$", body, re.M) or [None, None])[1]
        answer = re.search(r"^Reponse: (.*?)^Source: ", body, re.M | re.S)[1]
        expected = re.match(r"\*\*Expected answer\*\*: (.*?)(?:\n\n|\Z)", answer, re.S)
        out[m[1]] = {
            "header": m[2],
            "id_field": field("ID"),
            "source": field("Source"),
            "tags": field("Tags"),
            "legacy": re.findall(r"<!--ID: \d+-->", body),
            "question": field("Question"),
            "expected": expected[1].strip() if expected else None,
        }
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("cards", nargs="+")
    parser.add_argument("--base", default=BASE)
    args = parser.parse_args()
    broken = 0
    for card_arg in args.cards:
        path = Path(card_arg).resolve()
        rel = path.relative_to(REPO).as_posix()
        old_text = subprocess.run(["git", "show", f"{args.base}:{rel}"], cwd=REPO,
                                  capture_output=True, text=True, check=True).stdout
        new_text = path.read_text(encoding="utf-8")
        if re.findall(r"^TARGET DECK: .*$", old_text, re.M) != re.findall(r"^TARGET DECK: .*$", new_text, re.M):
            print(f"PROTECTED {rel}: TARGET DECK changed")
            broken += 1
        old, new = cards(old_text), cards(new_text)
        if list(old) != list(new):
            print(f"PROTECTED {rel}: card IDs or order changed: {list(old)} -> {list(new)}")
            broken += 1
        for cid in old:
            if cid not in new:
                continue
            for key in ("header", "id_field", "source", "tags", "legacy"):
                if old[cid][key] != new[cid][key]:
                    print(f"PROTECTED {cid}: {key} changed")
                    broken += 1
            for key in ("question", "expected"):
                if old[cid][key] != new[cid][key]:
                    print(f"CHANGED {cid} {key}:\n  old: {old[cid][key]}\n  new: {new[cid][key]}")
    print(f"{broken} protected field change(s)")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
