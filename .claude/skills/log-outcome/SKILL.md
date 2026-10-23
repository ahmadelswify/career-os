---
name: log-outcome
description: Capture the result of an interview or application with learnings
user_invocable: true
---

# Log Outcome

The user has an outcome (offer, rejection, or withdrawal) to capture.

## How to Do This

1. **Save what they told you** (the email, the feedback, the user's own notes) as a source with `/ingest`. Ingest updates the company, people and application pages.
2. Record the outcome in `Applications/[company]/outcome.md`
3. Capture: what worked, what didn't, stage reached
4. Update story outcome logs for any stories used
5. Extract learnings to propagate to `Learnings/`, each linked to this company and source:
   - Communication patterns that worked or failed
   - Domain vocabulary insights
   - Story adjustments needed
   - Items for the never-use list
6. **Fill the result** on this application's row in `Learnings/fit-calibration.md`. With 5+ rows, say whether fit scores have been running high or low.
7. Update the application tracker and the company page's application history

## Important

- Handle rejections constructively
- Always extract at least one learning
- Push for specifics: "What feedback did they give?"
- If offer: capture compensation and decision timeline
