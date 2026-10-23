---
name: prep-interview
description: Prepare for an upcoming interview with stories, research, and practice
user_invocable: true
---

# Prep Interview

Help the user prepare for an interview with the right stories, company context, and practice.

## How to Do This

1. Read the application file and the company page for this company
2. **Know who's in the room:** run `/person` for each interviewer (create pages for new ones). Pull what each has said before.
3. **Refresh the research:** if the company page's X-ray is older than 30 days, or this is a later round, run `/xray-company`. If the company is watched, run `/watch` for anything new since the last round.
4. Review learnings for relevant patterns, especially lessons from earlier rounds with this company
5. Select 3-5 stories mapped to the role's priorities
6. Practice: enforce 90-second leads, flag "we" language, check algorithm labels
7. Prepare questions to ask, using the company's interview angles

## Important

- Every story needs an algorithm label and a metric
- 90 seconds or less for the executive lead
- "I" not "we" for every action
- Be honest about areas to strengthen
- After the interview, run `/ingest` on the notes or transcript
