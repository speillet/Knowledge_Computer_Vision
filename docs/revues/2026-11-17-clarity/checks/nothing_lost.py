#!/usr/bin/env python3
"""Check that clarification lost no content (2026-11-17 clarity pass).

For each flashcard file given, every answer paragraph present at the base commit but absent
from the current card is searched in the current canonical reference and in the current card
(a paragraph may have been merged into a restructured step). The best difflib ratio is
reported; below the threshold, a person must check the content and justify it in the
subject report (for example, a one-sentence explanation absorbed by the new Further
explanation).

Usage:
    python3 docs/revues/2026-11-17-clarity/checks/nothing_lost.py CARD_FILE... [--base REV] [--threshold 0.9]

Standard library and git only.
"""

import argparse
from difflib import SequenceMatcher
from pathlib import Path
import re
import subprocess
import sys

REPO = Path(__file__).resolve().parents[4]
BASE = "594603f"          # commit of the 2026-11-16 deepening, baseline of the clarity pass


def answers(text):
    """Map card ID to the list of normalized answer paragraphs."""
    out = {}
    for block in re.finditer(r"^START\n(.*?)\nEND$", text, re.M | re.S):
        body = block[1]
        cid = re.search(r"^ID: (\S+)", body, re.M)[1]
        answer = re.search(r"^Reponse: (.*?)^Source: ", body, re.M | re.S)[1]
        out[cid] = paragraphs(answer)
    return out


def paragraphs(text):
    result = []
    for para in re.split(r"\n[ \t]*\n", text):
        para = re.sub(r"^\*\*[^*\n]+\*\*(?:\s*\([^\n]*?\))?\s*:\s*", "", para.strip())
        para = re.sub(r"\s+", " ", para).strip()
        if len(para) > 40:
            result.append(para)
    return result


def best_match(para, candidates):
    best, where = 0.0, None
    for name, cand in candidates:
        matcher = SequenceMatcher(None, para, cand, autojunk=False)
        if matcher.real_quick_ratio() < best or matcher.quick_ratio() < best:
            continue
        ratio = matcher.ratio()
        if ratio > best:
            best, where = ratio, name
        if len(cand) > len(para):                 # paragraph contained in a longer one
            block = matcher.find_longest_match(0, len(para), 0, len(cand))
            contained = block.size / len(para)
            if contained > best:
                best, where = contained, name
    return best, where


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("cards", nargs="+")
    parser.add_argument("--base", default=BASE)
    parser.add_argument("--threshold", type=float, default=0.9)
    args = parser.parse_args()
    flagged = 0
    for card_arg in args.cards:
        card = Path(card_arg).resolve()
        rel = card.relative_to(REPO)
        reference = card.parent / "references" / card.name
        old = subprocess.run(["git", "show", f"{args.base}:{rel.as_posix()}"], cwd=REPO,
                             capture_output=True, text=True, check=True).stdout
        new_text = card.read_text(encoding="utf-8")
        before, after = answers(old), answers(new_text)
        candidates = [("reference", p) for p in paragraphs(reference.read_text(encoding="utf-8"))]
        for cid, paras in before.items():
            current = set(after.get(cid, []))
            own = [("card", p) for p in after.get(cid, [])]
            for para in paras:
                if para in current:
                    continue
                ratio, where = best_match(para, candidates + own)
                status = "ok" if ratio >= args.threshold else "CHECK"
                flagged += status == "CHECK"
                print(f"{status:5s} {cid} {ratio:.2f} {where or '-':9s} {para[:90]}")
    print(f"{flagged} removed paragraph(s) below {args.threshold} to check by hand")
    return 0


if __name__ == "__main__":
    sys.exit(main())
