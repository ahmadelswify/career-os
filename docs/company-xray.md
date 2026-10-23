# Company X-ray

Most candidates read the careers page and the About page. An X-ray reads what the company publishes for engineers, machines and customers, and compares it with what marketing says. You walk in knowing what they're actually building, what's breaking, and what changed since your last round.

## Rules

- **Passive and public only.** No logins, no signups, no free trials, no contacting anyone. Respect `robots.txt`. Never download and run code.
- **Save before you conclude.** Every page or file you read goes into `Sources/` verbatim (or as a dated excerpt with its URL) before any summary is written.
- **Every claim carries a source and a confidence**: `confirmed` (the company says so in a primary source), `likely` (two independent sources agree), or `unverified` (one secondary source, or sources conflict). Never average conflicting numbers; show both.
- **"No data" is not "no."** If you can't find something, say so. Don't infer a negative.
- **Mark guesses as guesses.** Interview angles are suggestions, not facts.

## Layers, in order

Stop when you have enough for the user's goal. A first-round screen needs layers 1–3; a final round deserves all of them.

1. **The role and the team.** The job description (saved to `Sources/`), other open roles on the same team (the ATS feed shows team size and what they're building), how long the role has been open, whether it's a repost.
2. **The company's own machine-readable pages.** `/llms.txt` and `/llms-full.txt` (many companies now publish their whole docs in one file for AI), `/sitemap.xml` (what pages exist and when they changed), the changelog or release notes, the status page, the docs.
3. **Health.** Funding, layoffs, leadership changes, acquisitions, from news and the company's newsroom. Dates matter more than adjectives.
4. **What they're actually building.** Their public GitHub organisation: which repos are active, recent releases, the size and pace of the team shipping. Engineering blog posts. Compare with the marketing site: a product the homepage leads with but the docs and changelog never mention is a signal worth knowing.
5. **What customers say.** App store reviews, G2/Trustpilot, Reddit, support forums. Group complaints into themes with rough counts. For customer-facing roles this is gold: it's the job you'll be doing.
6. **The people.** The likely hiring manager and the chain above them, from the job description, the company site, talks, posts and news (public web search only). Add each to `People/`. Then run `/find-referrals` for warm paths.
7. **How they hire.** Interview process reports (Glassdoor and similar), with dates. Old reports may be stale.

## Output

Update `Companies/<company>.md` (see `templates/company-research.md`). The key sections are **Product reality** (marketing vs what's shipped), **What customers complain about**, **People**, and **Interview angles**: 3–5 specific, sourced things the user can bring up, phrased as curiosity, never as a gotcha.

Then offer to add the company to the watchlist so `/watch` reports what changes before the next round.
