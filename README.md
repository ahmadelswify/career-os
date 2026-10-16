# career-os: Land Your Next Role with AI

> Drop a job description. Get a tailored resume, interview prep, and tracked application, all through conversation.

A complete career management system that handles the full job search lifecycle: resume tailoring, STAR story preparation, interview coaching, application tracking, and learnings capture. Built for [Claude Code](https://claude.com/claude-code).

## How It Works

1. **Build your impact library** by documenting achievements with metrics, context, and alternate framings
2. **Drop a job description** and say "tailor my resume"
3. **AI parses the JD**, assesses fit, maps your experience, translates domain language, and rewrites your resume
4. **Prepare for interviews** with algorithm-labeled STAR stories, probe answer practice, and company research
5. **Track everything** from application to outcome, capturing learnings that improve your next attempt

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
├── Learnings/                    # Communication rules, interviewer types, metrics
├── Resumes/                      # Resume JSON files and generated PDFs
├── docs/
│   ├── how-it-works.md           # End-to-end flywheel explanation
│   ├── domain-translation.md     # How to translate experience across industries
│   └── stories-framework.md      # Building reusable STAR stories
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

## Quick Commands

| Command | What it does |
|---------|-------------|
| `/setup` | Set up your career-os workspace (~10 min) |
| `/tailor-resume` | Parse a JD and produce a tailored resume |
| `/prep-interview` | Prepare for an interview with stories and practice |
| `/log-outcome` | Capture result and learnings from an application |

## Requirements

- [Claude Code](https://claude.com/claude-code) and Node.js v18+

## License

[MIT](LICENSE)
