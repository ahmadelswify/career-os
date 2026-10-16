// PDF Resume Generator
//
// Renders a resume JSON into a single-page PDF using @react-pdf/renderer.
// Designed as an optional companion to career-os.
//
// Usage:
//   node generate-pdf.js --input <path-or-filename> [--output <suffix>]
//                        [--output-dir <dir>] [--padding <pt>]
//                        [--top <pt>] [--contact-gap <pt>]
//
// Defaults:
//   --input         resume.json                (resolved from ../Resumes/ unless absolute)
//   --output-dir    ../Resumes
//   --padding       20
//   --top           18
//   --contact-gap   5
//
// The PDF filename is derived from `resume.profile.name`; pass --output to
// add a suffix (e.g., the target company name).
//
// Everything below is configurable. The layout, font, spacing, and section
// order are all defined in this file. Edit the constants below to customize.
// You can also ask Claude (in career-os) to: remove the summary, move
// education to the top, change the section order, swap the font, etc.

const React = require("react");
const {
  Document,
  Page,
  View,
  Text,
  Font,
  StyleSheet,
  renderToFile,
} = require("@react-pdf/renderer");
const fs = require("fs");
const path = require("path");

// --- CLI args ---
const args = process.argv.slice(2);
function getArg(name, fallback) {
  const idx = args.indexOf("--" + name);
  return idx > -1 && args[idx + 1] ? args[idx + 1] : fallback;
}

const rawInput = getArg("input", "resume.json");
const isAbsoluteInput = path.isAbsolute(rawInput);
const JSON_DIR = isAbsoluteInput
  ? path.dirname(rawInput)
  : path.resolve(__dirname, "../Resumes");
const PDF_DIR = path.resolve(__dirname, getArg("output-dir", "../Resumes"));

const inputFile = isAbsoluteInput ? path.basename(rawInput) : rawInput;
const outputSuffix = getArg("output", "");
const paddingH = Number(getArg("padding", "20"));
const paddingTop = Number(getArg("top", "18"));
const contactGap = Number(getArg("contact-gap", "5"));

// --- Load resume data ---
const inputPath = path.resolve(JSON_DIR, inputFile);
if (!fs.existsSync(inputPath)) {
  console.error(`Resume JSON not found: ${inputPath}`);
  process.exit(1);
}
const resume = JSON.parse(fs.readFileSync(inputPath, "utf-8"));

// --- Output filename ---
// Derives "<Name>-Resume[-Suffix].pdf" from the resume's profile.name.
const profileName = ((resume.profile && resume.profile.name) || "").trim();
const namePrefix = profileName ? profileName.replace(/\s+/g, "-") + "-" : "";
const pdfName = outputSuffix
  ? `${namePrefix}Resume-${outputSuffix}.pdf`
  : `${namePrefix}Resume.pdf`;
fs.mkdirSync(PDF_DIR, { recursive: true });
const outputPath = path.resolve(PDF_DIR, pdfName);

// --- Font registration ---
// Default font is Roboto (Apache 2.0). To use a different font, drop the
// .ttf files into public/fonts/ and update the family + paths below.
const fontsDir = path.resolve(__dirname, "public/fonts");
Font.register({
  family: "Roboto",
  fonts: [
    { src: path.join(fontsDir, "Roboto-Regular.ttf") },
    { src: path.join(fontsDir, "Roboto-Bold.ttf"), fontWeight: "bold" },
  ],
});
Font.registerHyphenationCallback((word) => [word]);

// --- Design tokens (configurable) ---
const COLORS = {
  text: "#1a1a1a",
  accent: "#1a1a1a",
  muted: "#4b5563",
  divider: "#d1d5db",
  bg: "#ffffff",
};

const e = React.createElement;
const sp = (n) => n + "pt";

// --- Styles ---
const s = StyleSheet.create({
  page: {
    fontFamily: "Roboto",
    fontSize: sp(9.5),
    color: COLORS.text,
    paddingTop: sp(paddingTop),
    paddingBottom: sp(paddingTop),
    paddingHorizontal: sp(paddingH),
    lineHeight: 1.3,
  },
  row: { flexDirection: "row" },
  rowBetween: { flexDirection: "row", justifyContent: "space-between" },
  col: { flexDirection: "column" },
  name: {
    fontSize: sp(22),
    fontWeight: "bold",
    color: COLORS.accent,
    letterSpacing: sp(0.5),
  },
  summary: {
    fontSize: sp(9),
    color: COLORS.muted,
    marginTop: sp(4),
    lineHeight: 1.4,
  },
  contactRow: {
    flexDirection: "row",
    justifyContent: "center",
    gap: sp(6),
    marginTop: sp(contactGap),
    flexWrap: "wrap",
  },
  contactItem: { fontSize: sp(9), color: COLORS.text },
  contactSep: { fontSize: sp(9), color: COLORS.divider },
  sectionHeader: {
    flexDirection: "row",
    alignItems: "center",
    marginTop: sp(7),
    marginBottom: sp(3),
    borderBottomWidth: 0.75,
    borderBottomColor: COLORS.divider,
    paddingBottom: sp(2),
  },
  sectionTitle: {
    fontSize: sp(10),
    fontWeight: "bold",
    color: COLORS.accent,
    letterSpacing: sp(1.5),
    textTransform: "uppercase",
  },
  companyName: { fontWeight: "bold", fontSize: sp(10) },
  jobTitle: { fontSize: sp(9.5) },
  jobTitleItalic: { fontSize: sp(8.5), color: COLORS.muted },
  dateText: { fontSize: sp(9), color: COLORS.muted },
  bullet: {
    fontSize: sp(9.5),
    lineHeight: 1.35,
    flexGrow: 1,
    flexBasis: 0,
  },
  bulletDot: { width: sp(12), fontSize: sp(9.5), lineHeight: 1.35 },
  schoolName: { fontWeight: "bold", fontSize: sp(9.5) },
  degree: { fontSize: sp(9.5) },
  skillLine: {
    fontSize: sp(9.5),
    lineHeight: 1.35,
    flexGrow: 1,
    flexBasis: 0,
  },
  skillLabel: { fontWeight: "bold", fontSize: sp(9.5) },
});

// --- Components ---
function SectionHeading({ title }) {
  return e(
    View,
    { style: s.sectionHeader },
    e(Text, { style: s.sectionTitle }, title)
  );
}

function BulletItem({ text }) {
  return e(
    View,
    { style: { ...s.row, marginTop: sp(1) } },
    e(Text, { style: s.bulletDot }, "•"),
    e(Text, { style: s.bullet }, text)
  );
}

function SkillLine({ label, text }) {
  return e(
    View,
    { style: { ...s.row, marginTop: sp(1.5) } },
    e(Text, { style: s.bulletDot }, "•"),
    e(
      Text,
      { style: s.skillLine },
      e(Text, { style: s.skillLabel }, label + ": "),
      text
    )
  );
}

function ProfileSection({ profile }) {
  const { name, email, location, url, summary } = profile;
  const contacts = [email, location, url].filter(Boolean);
  return e(
    View,
    { style: { alignItems: "center" } },
    e(Text, { style: s.name }, name),
    e(
      View,
      { style: s.contactRow },
      ...contacts.flatMap((item, idx) => {
        const els = [e(Text, { key: "c" + idx, style: s.contactItem }, item)];
        if (idx < contacts.length - 1) {
          els.push(e(Text, { key: "s" + idx, style: s.contactSep }, "  |  "));
        }
        return els;
      })
    ),
    summary && e(Text, { style: s.summary }, summary)
  );
}

function SkillsSection({ skills }) {
  const descriptions = (skills && skills.descriptions) || [];
  return e(
    View,
    {},
    e(SectionHeading, { title: "Skills" }),
    ...descriptions.map((desc, idx) => {
      const colonIdx = desc.indexOf(":");
      if (colonIdx > -1) {
        const label = desc.substring(0, colonIdx);
        const rest = desc.substring(colonIdx + 1).trim();
        return e(SkillLine, { key: idx, label, text: rest });
      }
      return e(BulletItem, { key: idx, text: desc });
    })
  );
}

function WorkSection({ workExperiences }) {
  return e(
    View,
    {},
    e(SectionHeading, { title: "Experience" }),
    ...workExperiences.map(
      ({ company, jobTitle, date, descriptions }, idx) => {
        // Optional: if the first item in `descriptions` contains " | ", treat
        // it as a stacked-title line ("Manager | Specialist | Analyst") that
        // sits under the current jobTitle. This lets one company entry show
        // promotion history without separate sections.
        let subTitles = null;
        let bulletDescs = descriptions;
        if (descriptions.length > 0 && descriptions[0].includes(" | ")) {
          subTitles = descriptions[0];
          bulletDescs = descriptions.slice(1);
        }

        return e(
          View,
          { key: idx, style: idx !== 0 ? { marginTop: sp(6) } : {} },
          e(
            View,
            { style: s.rowBetween },
            e(Text, { style: s.companyName }, company),
            e(Text, { style: s.dateText }, date)
          ),
          e(
            View,
            { style: { marginTop: sp(1) } },
            e(Text, { style: s.jobTitle }, jobTitle)
          ),
          subTitles &&
            e(
              View,
              { style: { marginTop: sp(1) } },
              e(Text, { style: s.jobTitleItalic }, subTitles)
            ),
          e(
            View,
            { style: { marginTop: sp(2) } },
            ...bulletDescs.map((desc, i) =>
              e(BulletItem, { key: i, text: desc })
            )
          )
        );
      }
    )
  );
}

function EducationSection({ educations }) {
  return e(
    View,
    {},
    e(SectionHeading, { title: "Education" }),
    ...educations.map(
      ({ school, degree, date, gpa, descriptions }, idx) => {
        const degreeText = gpa
          ? `${degree} - ${Number(gpa) ? gpa + " GPA" : gpa}`
          : degree;
        return e(
          View,
          { key: idx, style: idx !== 0 ? { marginTop: sp(4) } : {} },
          e(
            View,
            { style: s.rowBetween },
            e(Text, { style: s.schoolName }, school),
            e(Text, { style: s.dateText }, date)
          ),
          e(
            View,
            { style: { marginTop: sp(1) } },
            e(Text, { style: s.degree }, degreeText)
          ),
          descriptions &&
            descriptions.length > 0 &&
            descriptions.join("") !== "" &&
            e(
              View,
              { style: { marginTop: sp(1) } },
              ...descriptions.map((d, i) =>
                e(BulletItem, { key: i, text: d })
              )
            )
        );
      }
    )
  );
}

function ProjectSection({ projects }) {
  return e(
    View,
    {},
    e(SectionHeading, { title: "Projects" }),
    ...projects.map(({ project, date, descriptions }, idx) =>
      e(
        View,
        { key: idx, style: idx !== 0 ? { marginTop: sp(4) } : {} },
        e(
          View,
          { style: s.rowBetween },
          e(Text, { style: { ...s.schoolName } }, project),
          e(Text, { style: s.dateText }, date)
        ),
        e(
          View,
          { style: { marginTop: sp(1) } },
          ...descriptions.map((d, i) => e(BulletItem, { key: i, text: d }))
        )
      )
    )
  );
}

// --- Main Document ---
// Default section order: Profile -> Skills -> Experience -> Projects -> Education.
// To reorder (e.g., put Education at the top), rearrange the children below.
// Sections are skipped automatically when the corresponding array is empty.
const sections = [
  e(ProfileSection, { key: "profile", profile: resume.profile || {} }),
  (resume.skills && resume.skills.descriptions && resume.skills.descriptions.length > 0) &&
    e(SkillsSection, { key: "skills", skills: resume.skills }),
  (resume.workExperiences && resume.workExperiences.length > 0) &&
    e(WorkSection, { key: "work", workExperiences: resume.workExperiences }),
  (resume.projects && resume.projects.length > 0) &&
    e(ProjectSection, { key: "projects", projects: resume.projects }),
  (resume.educations && resume.educations.length > 0) &&
    e(EducationSection, { key: "education", educations: resume.educations }),
].filter(Boolean);

const ResumePDF = e(
  Document,
  {
    title: `${(resume.profile && resume.profile.name) || "Resume"}`,
    author: (resume.profile && resume.profile.name) || "",
  },
  e(Page, { size: "LETTER", style: s.page }, ...sections)
);

// --- Render ---
renderToFile(ResumePDF, outputPath).then(() => {
  console.log(`PDF generated: ${outputPath}`);
});
