---
name: find-referrals
description: Find warm referral paths into target companies from the user's own LinkedIn connections export, rank who to ask, and draft the ask (never send it). Use when the user says "who do I know at X?", "can I get a referral?", "find me a warm intro", or after deciding to apply somewhere.
user_invocable: true
---

# Find Referrals

Uses only the user's own data. Never scrape LinkedIn or open profiles automatically.

## Steps

1. **Get the export.** Ask the user for LinkedIn's `Connections.csv`: LinkedIn → Settings → Data privacy → Get a copy of your data → Connections. It arrives by email within minutes. Keep it outside the repo or in a git-ignored folder; it's personal data.
2. **Match.** Run `python3 scripts/match_connections.py <path-to-Connections.csv> --targets "<Company>"` (or omit `--targets` to use the watchlist), with `--role "<a few words from the role's function>"`, for example `--role "product,analytics"`.
3. **Check before trusting.** The company on a LinkedIn profile is whatever the person last typed. For the top 3 matches, confirm their current company and title with a public web search. Drop anyone who has left. Partial matches ("Northwind" vs "Northwind Pet Supply") must be confirmed or dropped.
4. **Rank and explain:** someone on or near the hiring team first, then a recruiter, then someone senior who knows the manager, then anyone who works there. Say how well the user knows each person if they can tell you.
5. **Draft the ask** for the best one or two: short, specific, easy to say yes to. Name the role and link, one line on why the user fits, an offer to send a blurb they can forward. Draft only.
6. **Record it.** Create or update `People/` pages for anyone the user decides to contact, with an "Open with them" row, and note the path on the company page. Backlink audit, index, `LOG.md`.

## Rules

- Never send messages, connection requests or InMails.
- Never store the full connections export in the wiki; only the people the user chooses to contact get pages.
