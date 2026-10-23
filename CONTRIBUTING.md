# Contributing to career-os

Thanks for your interest in contributing.

## Getting Started

1. Fork the repo
2. Clone: `git clone https://github.com/YOUR-USERNAME/career-os.git`
3. `cd career-os` and launch Claude Code: `claude`
4. Read AGENTS.md to understand how the system works

## What You Can Contribute

- **Templates:** New templates or workflows
- **Bug Fixes:** Issues labeled `bug`
- **Documentation:** Improvements to READMEs, docs, or examples

## Submitting Changes

- Keep PRs focused (one change per PR)
- Reference the issue number if applicable

## Style

- Primarily a markdown-based system. The exceptions are shell hooks (`.claude/hooks/*.sh`), JSON schemas, and the standard-library Python scripts in `scripts/`, which have tests: run `python3 -m unittest discover -s tests` before opening a PR.
- Follow existing patterns.
- Read CLAUDE.md and AGENTS.md before making changes.
- Don't commit your own user content. The `.gitignore` excludes your personal folders; confirm `git status` before committing.
