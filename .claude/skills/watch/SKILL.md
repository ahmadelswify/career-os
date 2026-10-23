---
name: watch
description: Check the companies the user is tracking for anything new - roles opened or closed on their job board, site pages added or changed, careers page edits, engineering activity. Use when the user says "anything new?", "check my companies", "watch X", before an interview round, or on a schedule. Reports only what changed since the last check.
user_invocable: true
---

# Watch

## Adding a company

The watchlist lives in `Companies/watchlist.json` (start from `templates/watchlist.json`). For each company, find its public sources:

- **Job board:** look at a job link on their careers page. `boards.greenhouse.io/<board>` or `job-boards.greenhouse.io/<board>` → `{"type": "greenhouse", "board": "<board>"}`; `jobs.lever.co/<company>` → lever; `jobs.ashbyhq.com/<org>` → ashby. Confirm the board is really this company: slugs collide (a board called `northwind` may belong to a different Northwind).
- **Sitemap:** `https://<domain>/sitemap.xml` if it exists.
- **Careers page:** `{"type": "page", "url": ...}` for text changes.
- **GitHub org**, if they have a public one.

Add `aliases` (other names people write on LinkedIn) so `/find-referrals` can use the same list. Set `watched: true` on the company page.

## Checking

1. Run `python3 scripts/watch.py`. The first run for a new source only records a snapshot.
2. For each change, decide if it matters to the user's search: a new role matching their target, their role closing, a careers page edit (new benefits, a remote policy change), a burst of new pages (a launch), a team's repos going quiet.
3. Save anything that matters as a source and run `/ingest` on it, so the company page and `LOG.md` (op `watch`) pick it up.

## Tell the user

Only what matters, most actionable first: "Northwind opened a second analyst role on the same team; yours is still open." If nothing relevant changed, say so in one line. Never apply, email or sign up for anything.
