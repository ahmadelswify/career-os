import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import watch  # noqa: E402

GREENHOUSE = json.dumps({"jobs": [
    {"id": 1, "title": "Senior Product Analyst", "location": {"name": "US - Remote"}, "absolute_url": "https://x/1"},
    {"id": 2, "title": "Data Engineer", "location": {"name": "Austin, TX"}, "absolute_url": "https://x/2"},
]}).encode()
LEVER = json.dumps([{"id": "a", "text": "CSM", "categories": {"location": "Remote"}, "hostedUrl": "https://l/a"}]).encode()
ASHBY = json.dumps({"jobs": [{"title": "Operations Lead", "location": "NYC", "jobUrl": "https://a/1"}]}).encode()
SITEMAP = b"""<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>https://co.com/</loc><lastmod>2026-10-01</lastmod></url>
<url><loc>https://co.com/pricing</loc><lastmod>2026-10-02</lastmod></url></urlset>"""
GITHUB = json.dumps([{"name": "app", "pushed_at": "2026-10-20T00:00:00Z"}]).encode()
PAGE = b"<html><head><style>x{}</style></head><body><h1>Careers</h1><p>We are hiring.</p><script>var a=1</script></body></html>"


class FakeFetch:
    def __init__(self, responses, robots=b""):
        self.responses = dict(responses)
        self.robots = robots
        self.calls = []

    def __call__(self, url):
        self.calls.append(url)
        if url.endswith("/robots.txt"):
            return self.robots
        if url not in self.responses:
            raise OSError(f"no fake for {url}")
        return self.responses[url]


class ParseTest(unittest.TestCase):
    def test_greenhouse_jobs_keyed_by_id(self):
        jobs = watch.parse("greenhouse", GREENHOUSE)
        self.assertEqual(jobs["1"], "Senior Product Analyst · US - Remote · https://x/1")
        self.assertEqual(len(jobs), 2)

    def test_lever_and_ashby(self):
        self.assertEqual(watch.parse("lever", LEVER), {"a": "CSM · Remote · https://l/a"})
        self.assertEqual(watch.parse("ashby", ASHBY), {"https://a/1": "Operations Lead · NYC · https://a/1"})

    def test_sitemap_urls_with_lastmod(self):
        self.assertEqual(watch.parse("sitemap", SITEMAP), {"https://co.com/": "2026-10-01", "https://co.com/pricing": "2026-10-02"})

    def test_github_repos(self):
        self.assertEqual(watch.parse("github", GITHUB), {"app": "pushed 2026-10-20"})

    def test_page_text_lines_without_scripts_or_styles(self):
        self.assertEqual(watch.parse("page", PAGE), {"Careers": "", "We are hiring.": ""})


class DiffTest(unittest.TestCase):
    def test_added_removed_changed(self):
        old = {"1": "A", "2": "B", "3": "C"}
        new = {"1": "A", "2": "B2", "4": "D"}
        self.assertEqual(watch.diff(old, new), [
            {"kind": "added", "key": "4", "detail": "D"},
            {"kind": "removed", "key": "3", "detail": "C"},
            {"kind": "changed", "key": "2", "detail": "B -> B2"},
        ])

    def test_page_lines_report_the_line_not_a_key(self):
        self.assertEqual(watch.diff({"Old line": ""}, {"New line": ""}, page=True), [
            {"kind": "added", "key": "New line", "detail": "New line"},
            {"kind": "removed", "key": "Old line", "detail": "Old line"},
        ])


class RunTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.snap = Path(self.tmp.name)
        self.watchlist = {"companies": [{"name": "Northwind", "slug": "northwind", "sources": [
            {"type": "greenhouse", "board": "northwindtraders"},
            {"type": "sitemap", "url": "https://co.com/sitemap.xml"},
        ]}]}
        self.gh = "https://boards-api.greenhouse.io/v1/boards/northwindtraders/jobs"

    def tearDown(self):
        self.tmp.cleanup()

    def test_first_run_seeds_then_reports_only_changes(self):
        fetch = FakeFetch({self.gh: GREENHOUSE, "https://co.com/sitemap.xml": SITEMAP})
        first = watch.run(self.watchlist, self.snap, fetch)
        self.assertEqual(first["changes"], [])
        self.assertEqual(first["seeded"], ["Northwind: greenhouse northwindtraders", "Northwind: sitemap https://co.com/sitemap.xml"])

        newer = json.loads(GREENHOUSE)
        newer["jobs"].append({"id": 3, "title": "Data Analyst II", "location": {"name": "Remote"}, "absolute_url": "https://x/3"})
        fetch.responses[self.gh] = json.dumps(newer).encode()
        second = watch.run(self.watchlist, self.snap, fetch)
        self.assertEqual(second["changes"], [{"company": "Northwind", "source": "greenhouse northwindtraders",
                                              "kind": "added", "key": "3", "detail": "Data Analyst II · Remote · https://x/3"}])

    def test_failed_fetch_is_an_error_and_keeps_the_old_snapshot(self):
        fetch = FakeFetch({self.gh: GREENHOUSE, "https://co.com/sitemap.xml": SITEMAP})
        watch.run(self.watchlist, self.snap, fetch)
        del fetch.responses[self.gh]
        result = watch.run(self.watchlist, self.snap, fetch)
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("greenhouse northwindtraders", result["errors"][0])
        saved = json.loads((self.snap / "northwind.json").read_text())
        self.assertEqual(len(saved["greenhouse northwindtraders"]), 2)

    def test_dry_run_does_not_write_snapshot(self):
        fetch = FakeFetch({self.gh: GREENHOUSE, "https://co.com/sitemap.xml": SITEMAP})
        watch.run(self.watchlist, self.snap, fetch, dry_run=True)
        self.assertFalse((self.snap / "northwind.json").exists())

    def test_robots_disallow_skips_site_sources_but_not_job_apis(self):
        fetch = FakeFetch({self.gh: GREENHOUSE, "https://co.com/sitemap.xml": SITEMAP},
                          robots=b"User-agent: *\nDisallow: /\n")
        result = watch.run(self.watchlist, self.snap, fetch)
        self.assertEqual(result["skipped"], ["Northwind: sitemap https://co.com/sitemap.xml (robots.txt disallows it)"])
        self.assertNotIn("https://co.com/sitemap.xml", fetch.calls)
        self.assertIn(self.gh, fetch.calls)


class MessageTest(unittest.TestCase):
    def test_not_found_says_to_check_the_name(self):
        import urllib.error

        def fetch(url):
            raise urllib.error.HTTPError(url, 404, "Not Found", None, None)

        with tempfile.TemporaryDirectory() as d:
            result = watch.run({"companies": [{"name": "Plaid", "sources": [{"type": "lever", "company": "plaidx"}]}]}, Path(d), fetch)
        self.assertEqual(result["errors"], ["Plaid: lever plaidx: not found (check the board or org name)"])

    def test_summary_lines(self):
        self.assertEqual(watch.summary({"changes": [], "seeded": ["A: x"], "errors": [], "skipped": []})[0],
                         "First snapshot recorded for 1 source(s); changes show from the next run.")
        self.assertEqual(watch.summary({"changes": [], "seeded": [], "errors": [], "skipped": []}),
                         ["No changes since the last run."])


if __name__ == "__main__":
    unittest.main()
