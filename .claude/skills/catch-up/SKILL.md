---
name: catch-up
description: Bring the career wiki up to date after a busy stretch - find every call, interview or email that hasn't been ingested yet and ingest them in date order. Use when the user says "catch up", "I had a bunch of calls this week", "what haven't you seen yet", or after time away.
user_invocable: true
---

# Catch Up

## Steps

1. **List candidates.** If a meeting-notes tool (such as Granola) is connected, list meetings since the newest file in `Sources/`. Otherwise ask the user to paste or drop in what they have (notes, emails, job descriptions).
2. **Diff against `Sources/`.** Skip anything already saved (same date and company, or the same origin id recorded in a source's `origin:`). Skip personal meetings that aren't about the job search, and say you skipped them.
3. **Show the list** with dates and who it was with, and confirm before ingesting.
4. **Ingest oldest first** with `/ingest`, so later sources update earlier pages in the right order.
5. **Run `/lint`** once at the end, not after each one.

## Tell the user

What was ingested, any contradictions found across the batch, and every open loop the batch created, oldest first.
