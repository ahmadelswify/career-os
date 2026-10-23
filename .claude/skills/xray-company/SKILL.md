---
name: xray-company
description: Deep public research on a company before applying or interviewing - what they're actually building vs what marketing says, company health, what customers complain about, the likely hiring manager, and specific interview angles, every claim sourced. Use when the user says "research X", "X-ray X", "I have an interview with X", or before a final round. Usage /xray-company <company> [role].
user_invocable: true
---

# Company X-ray

Follow the method in `docs/company-xray.md`. Its rules are not optional: passive public reads only, save sources before concluding, a confidence on every claim, no data is not a no.

## Steps

1. **Scope it.** Ask (or infer) the goal: deciding whether to apply (layers 1-3), a first screen (1-3, 6), a later round (all seven). Read the existing company page first; refresh only what's older than 30 days.
2. **Work the layers** in `docs/company-xray.md`, saving each useful page or excerpt to `Sources/YYYY-MM-DD-<company>-xray-<what>.md` with its URL.
3. **Write the company page** in `Companies/<slug>.md` (from `templates/company-research.md`). Set `xray:` to today. Fill **Product reality**, **What customers complain about**, **People** (with `People/` pages) and **Interview angles**.
4. **Backlink audit, index line, `LOG.md` entry** (op `xray`), then `python3 scripts/wiki_health.py`.
5. **Offer next steps:** add the company to the watchlist for `/watch`; run `/find-referrals` for warm paths; tailor the resume with what you learned.

## Tell the user

Five to eight lines: the one-sentence verdict (worth it / worth it with caveats / not now), the most useful finding, the best interview angle, the person to know, and anything you couldn't verify. No file paths.
