---
name: lint
description: Health check for the career wiki - broken links, pages missing from the index, stale applications, contradictions, promises nobody followed up on. Use every 5-10 ingests, before a big application push, or when the user says "clean up", "what's stale", "check my workspace".
user_invocable: true
---

# Lint

## Steps

1. **Run the deterministic check:** `python3 scripts/wiki_health.py`. It lists, most important first: pages missing from the index, broken links, malformed `related:` lists, self-links, duplicate file names.
2. **Then the judgment pass** (read `index.md`, then skim the pages):
   - **Stale applications:** no activity in 14+ days. Ask about status.
   - **Open loops:** "Open with them" rows on people pages older than a week, especially ones the user owes.
   - **Contradictions:** pages that disagree with each other (pay, location, stage, process).
   - **Stale research:** company pages whose `xray:` date is older than 30 days with an interview coming up.
   - **Lessons not yet used:** lessons in `Learnings/` that no story or tailoring note links to.
   - **Fit calibration:** if `Learnings/fit-calibration.md` has 5+ rows, compare fit scores with results and say whether scores run high or low.
3. **Write a short report** to `LOG.md` (op `lint`).
4. **Offer safe fixes** (add index lines, fix malformed lists, link first mentions) and apply them only after the user agrees. Never delete pages.

## Tell the user

Lead with the one or two things that need them (a promise they owe, a stale application), then the counts.
