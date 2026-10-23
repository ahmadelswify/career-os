# The Career Wiki

career-os keeps your job search as a small wiki that you and the assistant build together. Every call, interview, email and piece of research goes in once, and from then on everything else can find it. This is what makes each application start stronger than the last: nothing you learn is lost in a chat history.

It follows the LLM-wiki pattern: the assistant doesn't just write notes, it **maintains** them. The value is in the upkeep.

## The pieces

| Piece | What it holds | Rule |
|---|---|---|
| `Sources/` | Raw input: call transcripts, interview notes, emails, job descriptions, research crawls | **Immutable.** Saved verbatim once, never edited. Named `YYYY-MM-DD-<company>-<what>.md`. |
| `Companies/` | One page per company | Updated after every source that mentions it. |
| `People/` | One page per person: recruiters, hiring managers, interviewers, referrers | Updated after every conversation with or about them. |
| `Stories/`, `Learnings/`, `Impact-Library/` | Your stories, lessons and achievements | Linked to the companies and sources they came from. |
| `Applications/` | One folder per application | Links to its company page and people. |
| `index.md` | One line per page, by section | **The entry point.** The assistant reads it first to find anything. |
| `LOG.md` | Every ingest, lint and filed answer | **Append-only.** Format: `## [YYYY-MM-DD] <op> \| <title>`. |

## Links

- Refer to any page by its file name in double brackets: `[[northwind]]`, `[[jane-doe]]`, `[[quantify-every-story]]`. Never mention a person or company that has a page without linking it.
- Every page has a `related:` list in its frontmatter, written as a block list:

  ```yaml
  related:
    - "[[northwind]]"
    - "[[jane-doe]]"
  ```

  Never the inline `related: ["[[northwind]]"]` form; it breaks link resolution.
- File names are unique across the workspace, lowercase and hyphenated: `People/jane-doe.md`, not `People/Jane Doe.md`.

## The backlink audit (the step that makes it compound)

Every time you write or noticeably change a page, before saying "done":

1. Scan what you wrote for names that already have a page (people, companies, stories, lessons).
2. Turn the first unlinked mention of each into a `[[link]]`. Once per page is enough.
3. Add each one to the page's `related:` list if it isn't there.
4. Set `updated:` to today.

Skip code blocks and the entity's own page. Skipping this step is how a wiki stops compounding.

## Contradictions

When a new source disagrees with a page (the recruiter said remote, the job description says hybrid; a salary range moved), don't silently overwrite. Update the page to the newest claim, keep the old one with its date and source underneath, and record the contradiction in the `LOG.md` entry. Tell the user about it: contradictions are often the most useful thing in a source.

## Health

`python3 scripts/wiki_health.py` reports, in priority order:

1. **Index coverage:** pages `index.md` doesn't list. A page the index can't see is invisible to the assistant, however well linked. Keep this at 100%.
2. **Broken links**
3. **Malformed `related:` lists**
4. **Self-links**
5. **Duplicate file names**

Run `/lint` every 5–10 ingests, and before any big write.
