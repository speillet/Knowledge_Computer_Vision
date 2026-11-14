"""Compare protected card and reference fields between two vault copies.

Usage: python3 compare_protected.py <vault-before> <vault-after> [--json out.json]
"""
import json
import re
import sys
from pathlib import Path

CARD_RE = re.compile(r"^## (CV-[A-Z0-9-]+)\n(.*?)^END$", re.M | re.S)


def parse_cards(text):
    cards = {}
    for m in CARD_RE.finditer(text):
        block = m[2]
        get = lambda key: (re.search(rf"^{key}:(.*)$", block, re.M) or [None, None])[1]
        reponse = re.search(r"^Reponse:(.*?)^Source:", block, re.M | re.S)
        expected = re.search(r"\*\*Expected answer\*\*:?(.*?)(?:\n\n|\Z)", reponse[1], re.S) if reponse else None
        cards[m[1]] = {
            "objective": re.search(r"^Objective:.*$", block, re.M)[0],
            "id": get("ID"), "question": get("Question"), "tags": get("Tags"),
            "start": "START\nCV-Pilote\n" in block,
            "legacy": re.findall(r"<!--ID:.*?-->", block),
            "reponse": reponse[1] if reponse else None,
            "expected": expected[1].strip() if expected else None,
            "source": get("Source"),
        }
    return cards


def front(text):
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    return dict(re.findall(r"^(\w+):\s*(.+)$", m[1], re.M)) if m else {}


def main():
    before, after = Path(sys.argv[1]), Path(sys.argv[2])
    errors, report = [], {"cards_changed": [], "expected_changed": [], "refs": {}}
    for old in sorted(before.rglob("*.md")):
        rel = old.relative_to(before)
        new = after / rel
        if not new.exists():
            errors.append(f"missing file {rel}")
            continue
        a, b = old.read_text(encoding="utf-8"), new.read_text(encoding="utf-8")
        if rel.parent.name == "references":
            fa, fb = front(a), front(b)
            for k in set(fa) | set(fb):
                if k != "revision" and fa.get(k) != fb.get(k):
                    errors.append(f"{rel}: front matter {k} changed")
            h1a = re.search(r"^# .*$", a, re.M)[0]
            h1b = re.search(r"^# .*$", b, re.M)[0]
            if h1a != h1b:
                errors.append(f"{rel}: H1 changed")
            ha = re.findall(r"^#+ (CV-[A-Z0-9-]+)\s*$", a, re.M)
            hb = re.findall(r"^#+ (CV-[A-Z0-9-]+)\s*$", b, re.M)
            if sorted(set(ha)) != sorted(set(hb)):
                errors.append(f"{rel}: per-card headings changed {sorted(set(ha) ^ set(hb))}")
            ra, rb = int(fa.get("revision", 0)), int(fb.get("revision", 0))
            changed = a != b
            if changed and rb != ra + 1:
                errors.append(f"{rel}: revision {ra} -> {rb} for a changed reference")
            if not changed and rb != ra:
                errors.append(f"{rel}: revision changed without edits")
            report["refs"][fa.get("id")] = {"file": str(rel), "revision": [ra, rb], "changed": changed}
            continue
        if "TARGET DECK" not in a:
            continue
        deck_a = re.search(r"^TARGET DECK:.*$", a, re.M)[0]
        deck_b = re.search(r"^TARGET DECK:.*$", b, re.M)
        if not deck_b or deck_b[0] != deck_a:
            errors.append(f"{rel}: TARGET DECK changed")
        ca, cb = parse_cards(a), parse_cards(b)
        if list(ca) != list(cb):
            errors.append(f"{rel}: card IDs/order changed {set(ca) ^ set(cb)}")
        for cid in ca:
            if cid not in cb:
                continue
            for key in ("objective", "id", "question", "tags", "start", "legacy"):
                if ca[cid][key] != cb[cid][key]:
                    errors.append(f"{cid}: {key} changed")
            if ca[cid]["reponse"] != cb[cid]["reponse"] or ca[cid]["source"] != cb[cid]["source"]:
                report["cards_changed"].append(cid)
            if ca[cid]["expected"] != cb[cid]["expected"]:
                report["expected_changed"].append({"id": cid, "before": ca[cid]["expected"], "after": cb[cid]["expected"]})
    for new in sorted(after.rglob("*.md")):
        if not (before / new.relative_to(after)).exists():
            errors.append(f"new file {new.relative_to(after)}")
    report["errors"] = errors
    summary = {"errors": len(errors), "cards_changed": len(report["cards_changed"]),
               "expected_changed": len(report["expected_changed"]),
               "refs_changed": sum(r["changed"] for r in report["refs"].values()),
               "refs": len(report["refs"])}
    report["summary"] = summary
    if "--json" in sys.argv:
        Path(sys.argv[sys.argv.index("--json") + 1]).write_text(json.dumps(report, indent=1, ensure_ascii=False))
    for e in errors:
        print("ERROR", e)
    print(json.dumps(summary))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
