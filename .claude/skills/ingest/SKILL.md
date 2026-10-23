---
name: ingest
description: Add a new source to the career wiki - a recruiter call, interview transcript or notes, an email from a company, a job description, a referral conversation, research. Use whenever the user pastes or points to anything a company or person said, or says "I just had a call/interview with...". One source updates the company, people, application, stories and lessons it touches.
user_invocable: true
---

# Ingest

One source in, every affected page updated. Read `docs/career-wiki.md` for the rules if you haven't this session.

## Steps

1. **Get the source.** If the user pasted it, use that. If they mention a call and a meeting-notes tool (such as Granola) is connected, fetch the transcript from it. Otherwise ask them to paste notes; a rough summary is fine.
2. **Save it verbatim** to `Sources/YYYY-MM-DD-<company>-<what>.md` using `templates/source.md`. Never edit it afterwards.
3. **Read before writing.** Open `index.md`, then the pages the source touches: the company, each person, the application, any story the user told.
4. **Update every affected page:**
   - **Company** (`Companies/<slug>.md`, from `templates/company-research.md` if new): process, team, people, product facts, each with the source link and a confidence.
   - **People** (`People/<slug>.md`, from `templates/person.md` if new): one page per named person. Update "Where things stand", "Open with them" (who owes whom what) and "History".
   - **Application** (`Applications/<company>/notes.md`): stage, dates, next step.
   - **Stories**: if the user told a story, add a row to its outcome log (how it landed, which question prompted it).
   - **Learnings**: if something worked or flopped, add or strengthen a lesson and link it to this source and company.
5. **Backlink audit** on every page you touched (see `docs/career-wiki.md`): link first mentions, fill `related:`, bump `updated:`.
6. **Contradictions.** If the source disagrees with a page, keep both with dates, and tell the user plainly.
7. **Index.** Add a line to `index.md` for every new page.
8. **Log.** Append an entry to `LOG.md` in the format from `templates/log.md`.
9. **Check.** Run `python3 scripts/wiki_health.py` and fix anything it reports about the pages you touched.

## Tell the user

Three to six lines, in plain words: what you learned, any contradiction, and what they now owe or are owed ("You told Jane you'd send the case study by Friday"). No file paths.
