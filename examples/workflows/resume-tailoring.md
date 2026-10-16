# Resume Tailoring Workflow

## Trigger
User provides a job description and asks to tailor their resume.

## Steps

### 1. Parse the Job Description
Read the JD and extract:
- Role title, company, team, level
- Required skills (hard requirements)
- Preferred skills (nice-to-haves)
- Key responsibilities
- Success metrics (stated or implied)
- Domain language (specific vocabulary the company uses)

Create a JD analysis file using `templates/jd-analysis.md`.

### 2. Assess Fit
Score 1-10 on five dimensions:

| Dimension | What to Evaluate |
|---|---|
| Technical skill match | Do your skills map to their requirements? |
| Domain experience relevance | Have you worked in their industry or adjacent? |
| Leadership/scope alignment | Does your level of ownership match? |
| Culture/values fit | Based on company research and JD tone |
| Growth trajectory alignment | Does this role fit your career direction? |

Be honest. If the fit is below 5/10 overall, tell the user and explain why. They may still want to apply, but they should know.

### 3. Map Experience
For each JD requirement, find the best matching achievement from the Impact Library.

Create a mapping table:

| JD Requirement | Best Match from Impact Library | Confidence |
|---|---|---|
| [requirement] | [achievement] | [high/medium/low] |

Gaps (requirements with no match) become the "address in cover letter or interview" list.

### 4. Translate Domain Language
Using `docs/domain-translation.md` as reference:
- Replace your company's internal jargon with the target company's vocabulary
- Use the JD's exact phrasing when your experience genuinely matches
- Preserve your metrics (numbers don't change, framing does)

### 5. Rewrite Resume JSON
Produce a tailored `resume-data.json`:
- Lead every bullet with a measurable outcome
- Never use promotion history as a selling point
- Use the target's vocabulary throughout
- Each bullet must pass the "so what?" test
- Ensure the content fits on a single page

### 6. Verify
Checklist before generating PDF:
- [ ] Single page (hard constraint)
- [ ] No promotion metrics used as selling points
- [ ] Every bullet leads with a metric or outcome
- [ ] Domain language matches the target company
- [ ] No jargon the target wouldn't recognize
- [ ] Skills section reflects the JD's priorities
- [ ] Summary (if included) speaks to this specific role

### 7. Generate PDF
If the user has a resume builder configured, generate the PDF using their preferred tool and settings.

### 8. Track the Application
Create an application folder: `Applications/[company]/`
- Save the JD analysis
- Save the tailored resume JSON
- Initialize the application in the tracker
