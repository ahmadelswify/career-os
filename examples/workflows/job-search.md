# Job Search Workflow

> Monitor target company career boards directly. Skip job boards and middlemen. 3-5 quality applications per week beats 30 spray-and-pray apps.

## Trigger

User says any of:
- "find jobs" / "what should I apply to"
- "run my weekly board scan"
- "is there anything new at [company]"
- Or a recurring weekly cadence

## Required Assets

| Asset | Path | Purpose |
|---|---|---|
| Target companies | `Companies/target-companies.md` | Curated list of career boards to scan |
| Per-company research | `Companies/[company].md` | Background to inform fit assessment |
| Application history | `templates/application-tracker.md` (or your live tracker) | Avoid double-applying |
| Resume tailoring workflow | `examples/workflows/resume-tailoring.md` | What to run after a role passes the filter |

---

## Step 1: Weekly Board Scan

Open each career board from `Companies/target-companies.md` and search for your target role keywords. This typically takes 30-45 minutes once a week.

### Search keywords

Use the role-type keywords you've defined for yourself. Put your own list in a top-of-file comment in `Companies/target-companies.md` so you don't reinvent it each week. Examples of search terms a user might define:

```
[role keyword 1]
[role keyword 2]
[role keyword 3]
```

Filter each board by your target location(s) when available.

### Google X-ray shortcut

Instead of clicking through every board individually, batch-search entire ATS platforms at once:

```
site:boards.greenhouse.io ("[role keyword 1]" OR "[role keyword 2]") ("[city 1]" OR "[city 2]")
```

```
site:jobs.ashbyhq.com ("[role keyword 1]" OR "[role keyword 2]") ("[city 1]" OR "[city 2]")
```

```
site:jobs.lever.co ("[role keyword 1]" OR "[role keyword 2]") ("[city 1]" OR "[city 2]")
```

These surface roles across all companies on that ATS, not just your target list. Useful for discovering new companies to add to the watchlist.

---

## Step 2: Go/No-Go Filter

Run this before investing time in any application:

| Check | Pass | Fail |
|---|---|---|
| Years of experience | Meets minimum or within 1 year | Below minimum by 2+ years |
| Title level (Senior / Staff / Principal) | Not required, or company is flexible | Required and company is strict about levels |
| "Experienced" at large tech | Not in title | In title (often means 3-5 years minimum) |
| Domain experience required | Your background covers it, or domain is soft | Hard requirement in a domain you have none of |
| Already applied to this company recently | 0 or 1 active applications | 2+ active applications |
| Keyword overlap with resume | 50%+ of JD keywords map naturally | Below 30% |
| Location | Your target location, or remote OK | Other location, no remote option |

**0-1 fails:** Apply with full tailoring (run `resume-tailoring.md`).
**2 fails:** Stretch. Only proceed if the company or mission is unusually compelling.
**3+ fails:** Skip. Time is better spent on stronger-fit roles.

---

## Step 3: Tier Your Targets

Rank role types by how strong your evidence is. Keep this list in `Companies/target-companies.md`. A typical tiering:

### Tier 1: Apply immediately when found
Roles where your strongest stories and metrics map directly to the JD's responsibilities.

### Tier 2: Apply if the company or mission is compelling
Roles that are an adjacent fit; you can defend it but the resume needs more reframing.

### Tier 3: Only with a referral
Roles where you'd be a stretch on paper; a warm intro is what makes the application viable.

---

## Step 4: Weekly Cadence

| Day | Action |
|---|---|
| Monday | Run the board scan. Identify the strongest fits. |
| Tuesday-Thursday | Tailor resume and apply (1-2 per day, using `resume-tailoring.md`). |
| Friday | Follow up on active applications. Update the tracker. |

---

## Step 5: When You Find a Role

1. Run the go/no-go filter above.
2. If it passes, create `Applications/[company]/`.
3. Save the JD as `Applications/[company]/jd.md`.
4. Run `examples/workflows/resume-tailoring.md`.
5. Apply directly on the company's career board (not a job aggregator).
6. Update the application tracker.
7. Check whether you have any contacts at the company. Reach out if you have a real connection (not a cold scrape).
8. After the outcome, update the tracker, story outcome logs, and `Learnings/`.

---

## Step 6: Adding New Companies to Monitor

When you discover a company worth watching:

1. Find their career board URL (Greenhouse, Ashby, Lever, Workday, or custom).
2. Add to `Companies/target-companies.md` in the right section.
3. Optionally create `Companies/[company].md` with initial research.
4. Include in next week's scan.

---

## Anti-Patterns

- **Applying to 5+ roles at the same company in the same month.** ATS systems flag this as spray-and-pray. Pick the 1-2 strongest fits.
- **Applying to roles with "Experienced" or "Senior" in the title without the required years.** This is usually an auto-filter, not a soft preference.
- **Applying through aggregators (LinkedIn Easy Apply, Indeed) instead of the company's career page.** You lose the chance to reference a specific recruiter or hiring manager, and your resume often gets stripped of formatting.
- **Skipping the go/no-go filter "just this once."** The filter exists because tailoring a resume costs 1-2 hours. Spend that time on roles that have a chance.
