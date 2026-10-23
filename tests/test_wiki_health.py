import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import wiki_health  # noqa: E402


def write(base, rel, text):
    p = Path(base) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


PAGE = """---
type: {type}
related:
{related}
---

# {title}

{body}
"""


def page(title, body="", related=(), type_="company"):
    rel = "\n".join(f'  - "[[{r}]]"' for r in related) or "  []"
    return PAGE.format(type=type_, related=rel, title=title, body=body)


class WikiHealthTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def healthy(self):
        write(self.root, "Companies/northwind.md", page("Northwind", "Recruiter is [[jane-doe]].", ["jane-doe"]))
        write(self.root, "People/jane-doe.md", page("Jane Doe", "Recruits for [[northwind]].", ["northwind"], "person"))
        write(self.root, "index.md", "# Index\n\n- [[northwind]]\n- [[jane-doe]]\n")
        write(self.root, "LOG.md", "# Log\n")

    def test_healthy_workspace_has_no_defects(self):
        self.healthy()
        report = wiki_health.check(self.root)
        self.assertEqual(report["defects"], {k: [] for k in wiki_health.DEFECT_ORDER})

    def test_page_missing_from_index_is_reported(self):
        self.healthy()
        write(self.root, "People/sam-lee.md", page("Sam Lee", "", [], "person"))
        report = wiki_health.check(self.root)
        self.assertEqual(report["defects"]["index_coverage"], ["People/sam-lee.md"])
        self.assertEqual(report["coverage"], {"indexed": 2, "total": 3})

    def test_broken_link_is_reported_with_file(self):
        self.healthy()
        write(self.root, "Companies/acme.md", page("Acme", "See [[nobody-here]] and [[northwind|Northwind Traders]].", ["northwind"]))
        write(self.root, "index.md", "- [[northwind]]\n- [[jane-doe]]\n- [[acme]]\n")
        report = wiki_health.check(self.root)
        self.assertEqual(report["defects"]["broken_links"], ["Companies/acme.md -> nobody-here"])

    def test_links_inside_code_blocks_are_ignored(self):
        self.healthy()
        write(self.root, "Companies/acme.md", page("Acme", "```\n[[not-a-link]]\n```\nInline `[[also-not]]` too."))
        write(self.root, "index.md", "- [[northwind]]\n- [[jane-doe]]\n- [[acme]]\n")
        self.assertEqual(wiki_health.check(self.root)["defects"]["broken_links"], [])

    def test_inline_related_array_is_malformed(self):
        self.healthy()
        write(self.root, "Companies/acme.md", '---\ntype: company\nrelated: ["[[northwind]]"]\n---\n# Acme\n')
        write(self.root, "index.md", "- [[northwind]]\n- [[jane-doe]]\n- [[acme]]\n")
        self.assertEqual(wiki_health.check(self.root)["defects"]["malformed_related"], ["Companies/acme.md"])

    def test_self_loop_in_related_is_reported(self):
        self.healthy()
        write(self.root, "Companies/northwind.md", page("Northwind", "", ["northwind", "jane-doe"]))
        self.assertEqual(wiki_health.check(self.root)["defects"]["self_loops"], ["Companies/northwind.md"])

    def test_duplicate_basenames_are_reported(self):
        self.healthy()
        write(self.root, "Stories/northwind.md", page("Northwind story", "", [], "story"))
        write(self.root, "index.md", "- [[northwind]]\n- [[jane-doe]]\n")
        dupes = wiki_health.check(self.root)["defects"]["duplicate_basenames"]
        self.assertEqual(dupes, ["northwind: Companies/northwind.md, Stories/northwind.md"])

    def test_sources_and_applications_need_not_be_indexed(self):
        self.healthy()
        write(self.root, "Sources/2026-10-20-northwind-recruiter-call.md", page("Call", "[[northwind]]", ["northwind"], "source"))
        write(self.root, "Applications/northwind/notes.md", "# Notes\n[[northwind]]\n")
        self.assertEqual(wiki_health.check(self.root)["defects"]["index_coverage"], [])

    def test_cli_exit_code_and_json(self):
        self.healthy()
        ok = subprocess.run([sys.executable, str(ROOT / "scripts/wiki_health.py"), str(self.root)], capture_output=True, text=True)
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
        self.assertIn("healthy", ok.stdout)
        write(self.root, "People/sam-lee.md", page("Sam Lee", "", [], "person"))
        bad = subprocess.run([sys.executable, str(ROOT / "scripts/wiki_health.py"), str(self.root), "--json"], capture_output=True, text=True)
        self.assertEqual(bad.returncode, 1)
        self.assertEqual(json.loads(bad.stdout)["defects"]["index_coverage"], ["People/sam-lee.md"])


if __name__ == "__main__":
    unittest.main()
