# PDF Generator

> Optional companion tool that renders a tailored resume JSON to a single-page PDF.

## Install

```bash
cd generator
npm install
```

Requires Node.js 18+.

## Usage

```bash
# Render Resumes/resume.json -> Resumes/<Name>-Resume.pdf
node generate-pdf.js

# Render a specific tailored version
node generate-pdf.js --input acme-corp.json --output AcmeCorp

# Render from anywhere on disk with an absolute path
node generate-pdf.js --input /path/to/resume.json --output Acme
```

### CLI flags

| Flag | Default | Purpose |
|---|---|---|
| `--input` | `resume.json` | Path to the resume JSON. Resolved from `../Resumes/` unless absolute. |
| `--output` | `""` | Suffix appended to the PDF filename. Usually the target company. |
| `--output-dir` | `../Resumes` | Where the PDF is written. |
| `--padding` | `20` | Horizontal page padding in points. |
| `--top` | `18` | Top/bottom page padding in points. |
| `--contact-gap` | `5` | Gap between the name and the contact row. |

The PDF filename is `<Name>-Resume[-Suffix].pdf`, where `<Name>` is taken from `profile.name` in the JSON. If `profile.name` is empty, the file is named `Resume[-Suffix].pdf`.

## Resume JSON schema

The expected structure is in `../templates/resume-data.json`. The shape is:

```json
{
  "profile": { "name": "", "email": "", "location": "", "url": "", "summary": "" },
  "skills": { "descriptions": ["Label: items, separated, by commas"] },
  "workExperiences": [{ "company": "", "jobTitle": "", "date": "", "descriptions": ["bullet 1", "bullet 2"] }],
  "projects": [{ "project": "", "date": "", "descriptions": ["bullet 1"] }],
  "educations": [{ "school": "", "degree": "", "date": "", "gpa": "", "descriptions": [] }]
}
```

Notes:

- `skills.descriptions` — each entry is one bullet. If the entry contains a colon, everything before the colon is rendered bold (the category label).
- `workExperiences[].descriptions` — bullet points. If the first entry contains `" | "` it is treated as a stacked-title line (e.g., `"Senior Manager | Manager | Analyst"`) and rendered under the current `jobTitle` instead of as a bullet.
- All sections are optional. Empty arrays are skipped automatically.

## Customizing

Everything in `generate-pdf.js` is meant to be edited. Common changes:

- **Remove the summary.** Delete `summary` from `profile` in your JSON, or remove the line that renders it in `ProfileSection`.
- **Reorder sections.** Edit the `sections` array near the bottom of `generate-pdf.js` (e.g., move Education before Experience).
- **Change the font.** Drop new `.ttf` files into `public/fonts/` and update the `Font.register` block.
- **Change colors.** Edit `COLORS` near the top.
- **Change bullet density.** Adjust `lineHeight`, `marginTop`, or `paddingTop` in the `StyleSheet`.

You can also ask Claude inside career-os: "remove the summary from my resume", "move education to the top", "use Lora instead of Roboto" — and it will edit this file for you.

## Page-fit tips

- Keep total bullet count around 11-13 for a balanced single page.
- If the PDF spills to a second page, lower `--padding` or `--top`, or cut the weakest bullet.
- If the page has bottom whitespace, add a bullet to a project or experience, or raise `--top`.

## License

The generator code is under the career-os repo license. Roboto fonts in `public/fonts/` are under Apache 2.0 (see `public/fonts/LICENSE.md`).
