---
name: ask
description: Answer a question about the user's own job search from the career wiki - "what did the Northwind recruiter say about pay?", "which stories have I used with Acme?", "what have rejections taught me?", "who do I know at X?". Reads the wiki first, never guesses from general knowledge, cites where each answer came from, and offers to file useful answers back.
user_invocable: true
---

# Ask

## Steps

1. **Read `index.md` first** and pick the pages likely to hold the answer. A page the index doesn't list may as well not exist; if you find one by search, note it for `/lint`.
2. **Read those pages,** then follow their `[[links]]` and `related:` lists one step out. Open the cited `Sources/` when the exact wording matters (pay, dates, promises).
3. **Answer from what's written,** citing each fact with the page or source it came from, in plain words ("from your Oct 20 call with Jane"). If the wiki doesn't know, say so, and say what would answer it (an X-ray, a question for the recruiter).
4. **Offer to file it back.** If the answer pulled together several pages into something new (a pattern across rejections, a comparison of two offers), offer to save it as a page in `Learnings/` or on the company page, with links, an index line and a `LOG.md` entry, so the next question is faster.

## Rules

- Never fill a gap with general knowledge without labelling it as such.
- Old claims may be stale: give dates.
