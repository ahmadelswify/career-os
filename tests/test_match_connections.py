import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import match_connections as mc  # noqa: E402

EXPORT = """Notes:
"When exporting your connection data, you may notice that some of the email addresses are missing."

First Name,Last Name,URL,Email Address,Company,Position,Connected On
Jane,Doe,https://www.linkedin.com/in/jane,,Northwind Traders,"Senior Manager, Product Analytics",12 Mar 2025
Sam,Lee,https://www.linkedin.com/in/sam,,Northwind Pet Supply,Data Analyst,01 Jan 2024
Ana,Ruiz,https://www.linkedin.com/in/ana,,"Northwind, Inc.",Technical Recruiter,05 Jun 2026
Bo,Kim,https://www.linkedin.com/in/bo,,Acme Corp,Engineer,10 Feb 2019
Cy,Ng,https://www.linkedin.com/in/cy,,Globex,Designer,10 Feb 2026
"""


class NormalizeTest(unittest.TestCase):
    def test_strips_suffixes_and_punctuation(self):
        self.assertEqual(mc.normalize("Northwind, Inc."), "northwind")
        self.assertEqual(mc.normalize("The Acme Corporation"), "acme")
        self.assertEqual(mc.normalize("Contoso Supply Co."), "contoso supply")


class ReadTest(unittest.TestCase):
    def test_skips_the_notes_preamble(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as f:
            f.write(EXPORT)
        rows = mc.read_connections(Path(f.name))
        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[0]["Company"], "Northwind Traders")
        self.assertEqual(rows[0]["Position"], "Senior Manager, Product Analytics")


class MatchTest(unittest.TestCase):
    def setUp(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as f:
            f.write(EXPORT)
        self.rows = mc.read_connections(Path(f.name))
        self.targets = [{"name": "Northwind", "aliases": ["Northwind Traders"]}, {"name": "Acme"}]

    def test_exact_alias_and_partial_matches(self):
        out = mc.match(self.rows, self.targets, role_keywords=["product", "analytics"], today="2026-10-23")
        nw = {r["name"]: r for r in out["Northwind"]}
        self.assertEqual(nw["Jane Doe"]["match"], "exact")
        self.assertEqual(nw["Ana Ruiz"]["match"], "exact")
        self.assertEqual(nw["Sam Lee"]["match"], "partial")
        self.assertNotIn("Cy Ng", nw)

    def test_ranking_puts_the_closest_to_the_team_first(self):
        out = mc.match(self.rows, self.targets, role_keywords=["product", "analytics"], today="2026-10-23")
        names = [r["name"] for r in out["Northwind"]]
        self.assertEqual(names[0], "Jane Doe")      # exact, same function, senior
        self.assertEqual(names[1], "Ana Ruiz")      # exact, recruiter
        self.assertEqual(names[-1], "Sam Lee")      # partial match goes last
        self.assertIn("same function", out["Northwind"][0]["why"])
        self.assertIn("recruiter", out["Northwind"][1]["why"])

    def test_old_connections_are_flagged_as_possibly_stale(self):
        out = mc.match(self.rows, self.targets, role_keywords=[], today="2026-10-23")
        bo = out["Acme"][0]
        self.assertTrue(bo["stale"])
        self.assertIn("may have changed", bo["check"])
        self.assertFalse(out["Northwind"][0]["stale"])

    def test_partial_match_asks_to_confirm_company(self):
        out = mc.match(self.rows, self.targets, role_keywords=[], today="2026-10-23")
        sam = next(r for r in out["Northwind"] if r["name"] == "Sam Lee")
        self.assertIn("Northwind Pet Supply", sam["check"])


if __name__ == "__main__":
    unittest.main()
