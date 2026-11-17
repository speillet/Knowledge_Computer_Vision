#!/usr/bin/env python3
"""Clarity metrics for flashcard answers (2026-11-17 clarity pass).

For each card, report the lexical word count of the answer, its bold rubrics
in order, template-order problems and acronyms that the card does not appear
to define. The acronym check is a heuristic: every flagged token must be read
by a person, who either defines it in the card or records it as a false
positive (proper noun, dataset or library name already explained).

Usage:
    python3 docs/revues/2026-11-17-clarity/checks/clarity_metrics.py [PATH] [--json] [--flagged]

PATH is the vault (default), a topic directory or a flashcard file.
Standard library only; parsing reuses scripts/build_apkg.parse_cards.
"""

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import statistics
import sys

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "scripts"))
from build_apkg import parse_cards  # noqa: E402

MAX_RUBRICS = 6
FIRST, LAST, TERMS = "Expected answer", "Blocking errors", "Key terms"
RUBRIC = re.compile(r"^\*\*([^*\n]+?)\*\*(?:\s*\([^\n]*?\))?\s*:", re.M)
KNOWN = {"ID", "IDs", "2D", "3D", "4D", "6D", "CPU", "GPU", "RGB", "API", "URL",
         "JSON", "CSV", "PDF", "SVG", "PNG", "HTTP", "HTTPS", "OK", "TODO",
         # library and product names, not acronyms
         "OpenCV", "PyTorch", "NumPy", "SciPy", "TensorFlow", "TensorRT",
         "TrackEval", "GitHub", "OpenVINO", "AnkiDroid"}
ACRONYM = re.compile(r"(?<![\w-])([A-Za-z0-9]*[A-Z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*)(?![\w-])")


def strip_noise(text):
    """Remove math, code, link targets, images and card IDs before scanning."""
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.S)
    text = re.sub(r"\$[^$\n]*\$", " ", text)
    text = re.sub(r"`[^`\n]*`", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    text = re.sub(r"\[\[[^\]]*\]\]", " ", text)
    text = re.sub(r"\bCV-[A-Z0-9-]+\b", " ", text)
    return text


def defined(token, text):
    if token.endswith("s") and len(token) > 2 and defined(token[:-1], text):
        return True                                  # plural of a defined token (TPs)
    t = re.escape(token)
    group = r"(?:\(\d\))?"                           # SE(3), SO(3), Sim(3)
    patterns = [
        rf"\(\s*{t}\s*[),;]",                        # expansion (TOKEN)
        rf"\b{t}\s*\(\s*[a-z]",                      # TOKEN (expansion
        rf"\b{t}\b{group}\s*\$?\s*(?::\s|=|—\s|–\s)",  # TOKEN: definition, TOKEN = ..., TOKEN $=
        rf"\b{t}\b{group},?\s+(?:is|are|means|stands for|denotes|counts|measures|the)\b",
        rf"\bwith {t}\b",                            # "with GT the number of ..."
    ]
    if any(re.search(p, text) for p in patterns):
        return True
    for item in re.findall(r"^- (.+?):\s", text, re.M):   # Key terms item: "TP, FN, FP: ..."
        if re.search(rf"\b{t}\b", item):
            return True
    return False


def analyse(card):
    answer = card["fields"]["Reponse"]
    question = card["fields"]["Question"]
    rubrics = [m.group(1).strip() for m in RUBRIC.finditer(answer)]
    problems = []
    if len(rubrics) > MAX_RUBRICS:
        problems.append(f"{len(rubrics)} rubrics > {MAX_RUBRICS}")
    if not rubrics or rubrics[0] != FIRST:
        problems.append("first rubric is not Expected answer")
    if not rubrics or rubrics[-1] != LAST:
        problems.append("last rubric is not Blocking errors")
    if TERMS in rubrics and rubrics.index(TERMS) != 1:
        problems.append("Key terms is not second")
    scan = strip_noise(question + "\n" + answer)
    tokens = []
    for token in ACRONYM.findall(scan):
        if token in KNOWN or token in tokens:
            continue
        if not defined(token, question + "\n" + answer):
            tokens.append(token)
    return {
        "id": card["id"],
        "file": str(card["file"].relative_to(REPO)),
        "words": len(re.findall(r"\w+", answer)),
        "rubrics": rubrics,
        "problems": problems,
        "undefined": tokens,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", nargs="?", default=str(REPO / "vault"))
    parser.add_argument("--json", action="store_true", help="print JSON rows")
    parser.add_argument("--flagged", action="store_true",
                        help="list only cards with a problem or an undefined token")
    args = parser.parse_args()
    target = Path(args.path).resolve()
    if not target.exists():
        parser.error(f"path not found: {args.path}")
    rows = [analyse(c) for c in parse_cards(REPO / "vault")
            if c["file"].resolve() == target or target in c["file"].resolve().parents]
    if not rows:
        parser.error(f"no card under {args.path}")
    if args.flagged:
        shown = [r for r in rows if r["problems"] or r["undefined"]]
    else:
        shown = rows
    if args.json:
        print(json.dumps(shown, ensure_ascii=False, indent=1))
        return
    for r in shown:
        flags = "; ".join(r["problems"]) or "-"
        print(f"{r['id']:28s} words={r['words']:4d} rubrics={len(r['rubrics'])} [{flags}]"
              f" undefined: {', '.join(r['undefined']) or '-'}")
    counts = Counter(t for r in rows for t in r["undefined"])
    print(json.dumps({
        "cards": len(rows),
        "median_words": statistics.median(r["words"] for r in rows),
        "median_rubrics": statistics.median(len(r["rubrics"]) for r in rows),
        "over_max_rubrics": sum(len(r["rubrics"]) > MAX_RUBRICS for r in rows),
        "order_problems": sum(any("rubric" in p and ">" not in p for p in r["problems"])
                              for r in rows),
        "cards_with_undefined": sum(bool(r["undefined"]) for r in rows),
        "top_undefined": counts.most_common(15),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
