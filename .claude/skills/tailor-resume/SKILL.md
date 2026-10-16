---
name: tailor-resume
description: Tailor your resume to a specific job description
user_invocable: true
---

# Tailor Resume

The user has a job description and wants a tailored resume. Parse the JD, assess fit, map experience, translate domain language, and produce a tailored resume.

## How to Do This

1. Parse the JD into requirements (must-have, preferred, responsibilities, metrics, vocabulary)
2. Score fit on 5 dimensions (1-10). Be honest about gaps.
3. Map each requirement to the best achievement from Impact Library
4. Translate bullets into the target company's vocabulary
5. Produce tailored resume JSON
6. Verify: single page, metrics-first, no promotion metrics, no unrecognizable jargon

## Important

- Lead every bullet with a measurable outcome
- Use the target's vocabulary, not your internal jargon
- Be honest about fit. If below 5/10, say so.
- Save the JD analysis and tailored resume in `Applications/[company]/`
