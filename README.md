# career-os: Land Your Next Role with AI

> Drop a job description. Get a tailored resume, interview prep, and tracked application, all through conversation.

A complete career management system that handles the full job search lifecycle: resume tailoring, STAR story preparation, interview coaching, application tracking, and learnings capture. Built for [Claude Code](https://claude.com/claude-code).

## How It Works

1. **Build your impact library** by documenting achievements with metrics, context, and alternate framings
2. **Drop a job description** and say "tailor my resume"
3. **AI parses the JD**, assesses fit, maps your experience, translates domain language, and rewrites your resume
4. **Prepare for interviews** with algorithm-labeled STAR stories, probe answer practice, and company research
5. **Track everything** from application to outcome, capturing learnings that improve your next attempt
6. **Remember every conversation.** Each recruiter call, interview and email goes into a linked career wiki: one page per company and per person, with who owes whom what
7. **X-ray companies** from public sources before you apply or interview: what they're actually building, what customers complain about, who's hiring, with a source on every claim
8. **Find warm referrals** in your own LinkedIn connections, and watch target companies for new roles and changes

## Core Question

**"How do I land my next role?"**

If you need professional task management, see [work-os](https://github.com/ahmadelswify/work-os). If you need life management, see [personal-os](https://github.com/ahmadelswify/personal-os).

## Quick Start

```bash
git clone https://github.com/ahmadelswify/career-os.git
cd career-os
claude
```

Then say: `"Help me set up career-os"`

Claude will walk you through:
1. Building your initial impact library from your resume
2. Creating your first set of STAR stories
3. Setting up your application tracker

## What's Inside

```
career-os/
├── CLAUDE.md                     # Points to AGENTS.md
├── AGENTS.md                     # Full career agent instructions
├── Impact-Library/               # Your achievements (filled in as you go)
├── Stories/                      # Your STAR stories
├── Applications/                 # One folder per company you apply to
├── Companies/                    # Persistent company research and target list
├── Learnings/                    # Communication rules, interviewer types, metrics, fit calibration
├── People/                       # One page per recruiter, hiring manager, interviewer, referrer
├── Sources/                      # Raw call notes, transcripts, emails, JDs (never edited)
├── index.md                      # Entry point to the wiki (created by setup)
├── LOG.md                        # Append-only log of everything ingested (created by setup)
├── scripts/                      # wiki_health.py, watch.py, match_connections.py (no installs)
├── Resumes/                      # Resume JSON files and generated PDFs
├── docs/
│   ├── how-it-works.md           # End-to-end flywheel explanation
│   ├── domain-translation.md     # How to translate experience across industries
│   ├── stories-framework.md      # Building reusable STAR stories
│   ├── career-wiki.md            # How the linked wiki works and stays healthy
│   └── company-xray.md           # Public-source company research method
├── templates/
│   ├── resume-data.json          # Empty resume JSON schema
│   ├── impact-library.md         # Achievement documentation template
│   ├── jd-analysis.md            # Job description parsing template
│   ├── application-tracker.md    # Track applications and outcomes
│   ├── company-research.md       # Persistent per-company research template
│   ├── target-companies.md       # Curated career boards to scan weekly
│   ├── star-story.md             # Reusable STAR story template
│   ├── interview-prep.md         # Pre-interview checklist
│   └── outcome-log.md            # Post-interview capture template
├── examples/
│   └── workflows/
│       ├── resume-tailoring.md   # Step-by-step resume tailoring workflow
│       ├── interview-prep.md     # Interview preparation workflow
│       └── job-search.md         # Weekly board scan + go/no-go filter
└── generator/                    # Optional Node.js PDF generator
    ├── generate-pdf.js
    ├── package.json
    └── public/fonts/             # Bundled Roboto (Apache 2.0)
```

## Configurable by Default

The structure, schemas, templates, and tools above are starting points, not constraints. Ask Claude to:

- Remove the summary from your resume, or move education to the top
- Add fields to a template (e.g., a "salary range" column in the tracker)
- Rename `Applications/` to `applications/` if you prefer lowercase
- Swap the bundled Roboto font for Lora, Merriweather, or anything else
- Skip a section you don't use, or add one this template doesn't have

The whole workspace is meant to be edited.

## Key Workflows

### Resume Tailoring
```
You: [paste job description] Tailor my resume for this role.

AI: Parsing JD... Here's my analysis:

    Fit Score: 78/100
    Strong matches: Technical operations, cross-functional leadership, process optimization
    Gaps to address: No direct experience with their specific tooling
    Domain translation needed: "Support engineering" → "Technical Operations"

    Ready to generate tailored resume?
```

### Interview Prep
```
You: I have an interview with [Company] tomorrow. Help me prepare.

AI: Reading your application and stories...

    Company Research: [key findings]
    Role Focus: [what they care about most]

    Top 3 stories to prepare:
    1. [Story] — covers their #1 requirement
    2. [Story] — addresses the gap in your resume
    3. [Story] — shows leadership at scale

    Let's practice. Tell me the first story in 90 seconds.
```

### After a Call
```
You: Just got off with the Northwind recruiter. [pastes notes]

AI: Saved. Three things:
    - The next round is a SQL case study, not a behavioral screen (new)
    - She said the role is fully remote; the job post says hybrid. Worth confirming in writing
    - You owe her your availability for next week by Friday
    I've updated Northwind, added her page, and logged it.
```

### Company X-ray
```
You: I have a final round at Northwind on Thursday. X-ray them.

AI: Worth it. The useful parts:
    - The homepage leads with an AI assistant, but the docs and changelog show it's
      still in beta; the shipping work is in reporting (likely, two sources)
    - Top public complaints: slow support replies, confusing billing
    - Likely hiring manager: Head of Product Analytics (likely, two sources)
    - Couldn't verify: headcount after last year's restructuring
    Best angle: ask how the analytics team feeds the AI roadmap.
```

## The Career Flywheel

Every application makes the next one better:

```
Impact Library → Tailored Resume → Interview → Outcome
      ↑                                          |
      └──── Learnings ← Outcome Log ←────────────┘
```

- **Wins** become new stories with verified metrics
- **Rejections** produce learnings about positioning and domain language
- **Interview feedback** refines how you tell stories
- **New achievements** expand your impact library
- **Every conversation** lands in the wiki, linked to the company, the people and the lessons, so nothing is relearned

## Quick Commands

| Command | What it does |
|---------|-------------|
| `/setup` | Set up your career-os workspace (~10 min) |
| `/tailor-resume` | Parse a JD and produce a tailored resume |
| `/prep-interview` | Prepare for an interview with stories and practice |
| `/log-outcome` | Capture result and learnings from an application |
| `/ingest` | Add a call, interview, email or job description to your wiki |
| `/ask` | Ask anything about your search; answers cite your own notes |
| `/person <name>` | Where things stand with someone, and who owes whom |
| `/catch-up` | Add every call or email you haven't ingested yet |
| `/lint` | Find stale applications, open loops and contradictions |
| `/xray-company <company>` | Deep public research with sources and interview angles |
| `/watch` | What changed at the companies you're tracking |
| `/find-referrals` | Warm intro paths from your LinkedIn connections export |

## Requirements

- [Claude Code](https://claude.com/claude-code)
- Python 3.9+ for the bundled scripts (standard library only; on a Mac, the first run offers to install it if it's missing)
- Node.js v18+ only if you want PDF resumes from the bundled generator

## License

[MIT](LICENSE)
