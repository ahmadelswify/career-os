#!/usr/bin/env python3
"""Health check for the career wiki. Standard library only (Python 3.9+).

Reports five defects, most important first:
  1. index_coverage      entity pages that index.md doesn't link to (the agent finds pages through the index)
  2. broken_links        [[links]] that point at no page
  3. malformed_related   `related:` written inline as [ ... ] instead of a block list
  4. self_loops          a page listing itself in `related:`
  5. duplicate_basenames two pages with the same file name, so [[name]] is ambiguous

Usage:
  python3 scripts/wiki_health.py [workspace] [--json]
Exit code 0 when healthy, 1 when any defect is found.
"""
import json
import re
import sys
from pathlib import Path

# Folders whose pages are wiki entities and must be reachable from index.md.
ENTITY_DIRS = ("Companies", "People", "Stories", "Learnings", "Impact-Library")
# Folders whose pages may link and be linked, but needn't be indexed.
OTHER_DIRS = ("Sources", "Applications", "Resumes")
ROOT_PAGES = ("index.md", "LOG.md")
DEFECT_ORDER = ("index_coverage", "broken_links", "malformed_related", "self_loops", "duplicate_basenames")

LINK = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
FENCE = re.compile(r"```.*?```", re.S)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def pages(root):
    """Every wiki page as (relative path string, Path)."""
    found = []
    for d in ENTITY_DIRS + OTHER_DIRS:
        base = root / d
        if base.is_dir():
            found += [(p.relative_to(root).as_posix(), p) for p in sorted(base.rglob("*.md")) if p.name != ".gitkeep"]
    for name in ROOT_PAGES:
        if (root / name).is_file():
            found.append((name, root / name))
    return found


def split_frontmatter(text):
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            return text[4:end], text[end + 4:]
    return "", text


def links_in(text):
    text = FENCE.sub("", text)
    text = INLINE_CODE.sub("", text)
    return [m.strip() for m in LINK.findall(text)]


def related_of(frontmatter):
    """(slugs, malformed) for the `related:` key."""
    lines = frontmatter.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("related:"):
            rest = line[len("related:"):].strip()
            if rest and rest != "[]":
                return links_in(rest), True
            slugs = []
            for item in lines[i + 1:]:
                if not item.startswith((" ", "\t", "-")):
                    break
                slugs += links_in(item)
            return slugs, False
    return [], False


def check(root):
    root = Path(root)
    all_pages = pages(root)
    by_slug = {}
    for rel, p in all_pages:
        by_slug.setdefault(p.stem, []).append(rel)

    defects = {k: [] for k in DEFECT_ORDER}

    index_links = set(links_in((root / "index.md").read_text())) if (root / "index.md").is_file() else set()
    entities = [(rel, p) for rel, p in all_pages if rel.split("/")[0] in ENTITY_DIRS]
    for rel, p in entities:
        if p.stem not in index_links:
            defects["index_coverage"].append(rel)

    for rel, p in all_pages:
        text = p.read_text(errors="replace")
        front, _ = split_frontmatter(text)
        for slug in links_in(text):
            if slug not in by_slug:
                defects["broken_links"].append(f"{rel} -> {slug}")
        related, malformed = related_of(front)
        if malformed:
            defects["malformed_related"].append(rel)
        if p.stem in related:
            defects["self_loops"].append(rel)

    for slug, rels in sorted(by_slug.items()):
        if len(rels) > 1:
            defects["duplicate_basenames"].append(f"{slug}: {', '.join(sorted(rels))}")

    for k in defects:
        defects[k] = sorted(dict.fromkeys(defects[k]))
    return {
        "coverage": {"indexed": len(entities) - len(defects["index_coverage"]), "total": len(entities)},
        "defects": defects,
    }


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    report = check(Path(args[0]) if args else Path.cwd())
    bad = any(report["defects"].values())
    if "--json" in argv:
        print(json.dumps(report, indent=2))
    else:
        c = report["coverage"]
        print(f"Index coverage: {c['indexed']}/{c['total']} pages")
        if not bad:
            print("Wiki is healthy.")
        for k in DEFECT_ORDER:
            items = report["defects"][k]
            if items:
                print(f"\n{k.replace('_', ' ')} ({len(items)}):")
                for item in items:
                    print(f"  - {item}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
