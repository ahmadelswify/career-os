---
name: tailor-resume
description: Tailor your resume to a specific job description
user_invocable: true
---

# Tailor Resume

The user has a job description and wants a tailored resume. Parse the JD, assess fit, map experience, translate domain language, and produce a tailored resume.

## How to Do This

1. **Save the JD** as a source (`Sources/YYYY-MM-DD-<company>-job-description.md`); postings disappear.
2. **Read what you already know:** the company page in `Companies/` (product reality, customer complaints, people, interview angles), and in `Learnings/` the never-use list, verified metrics, and any lesson linked to this company or role type.
3. Parse the JD into requirements (must-have, preferred, responsibilities, metrics, vocabulary). Check hard requirements first (years of a specific kind of experience, location, required tools): a miss on one is a long shot, however good the keyword overlap.
4. Score fit on 5 dimensions (1-10). Be honest about gaps.
5. Map each requirement to the best achievement from Impact Library
6. Translate bullets into the target company's vocabulary
7. Produce tailored resume JSON
8. Verify: single page, metrics-first, no promotion metrics, no unrecognizable jargon, nothing from the never-use list, and every number is one the user has verified
9. **Record the fit score** as a new row in `Learnings/fit-calibration.md` (date, company, role, score, result left blank) so `/log-outcome` can compare it with what actually happened.

## Important

- Lead every bullet with a measurable outcome
- Use the target's vocabulary, not your internal jargon
- Be honest about fit. If below 5/10, say so.
- Save the JD analysis and tailored resume in `Applications/[company]/`, linked to the company page
- If the company page is missing or older than 30 days and the user is serious about the role, offer `/xray-company` first
