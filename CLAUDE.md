# assessment-ai-skills

A collection of AI skills for health professions assessment (exam conversion, item analysis, blueprinting), maintained by a senior lecturer in Family Medicine at Walter Sisulu University, South Africa. Skills follow the open Agent Skills standard (SKILL.md) and target two platforms: Claude and Microsoft 365 Copilot (the institutionally approved AI).

## Repository structure

    skills/<skill-name>/
    ├── README.md                     human documentation for the skill
    ├── copilot/<skill-name>/         install-ready Copilot version
    └── claude/<skill-name>/          install-ready Claude version

- The innermost folder is what users install, so its name must exactly match the `name` field in its SKILL.md.
- A skill may exist for only one platform.
- `conventions.md` in the root is the master copy of shared rules (metadata, tags, Bloom's normalisation). Skills cannot read files outside their own folder, so these rules are copied into each skill's `references/`.

## Platform differences

Copilot skills have no scripts (OneDrive and Cowork skills do not reliably run them). Claude skills may include `scripts/` (Python) that run in Claude's code-execution environment. The intended differences are:

| Area | Claude | Copilot |
|---|---|---|
| Reading documents | Reads documents with `extract_document.py` | Reads documents directly and relies on `[[CORRECT]]` markers added by a Word macro |
| Images | Embeds images with `embed_images.py` | Uses placeholders: `<p>[Image: brief description]</p>` |
| Validation | `validate_moodle_xml.py`, plus a content checklist for what the script cannot check | The full validation checklist only |
| Output | claude.ai output paths | Returns a file or an XML code block |
| Feedback rules location | `references/feedback_rules.md` (asking in SKILL.md) | SKILL.md, "Student feedback" |
| No answers found | Lists likely causes and fixes (theme or unusual red, uncoloured answers, scanned PDF) | Gives step-by-step Find and Replace instructions to add `[[CORRECT]]` markers in Word |

Everything else must stay identical, including Moodle XML rules, metadata, tags, Bloom's normalisation, essay settings, MCQ fractions, feedback rules and question naming. Shared rules are kept in `conventions.md`. When changing one version, check whether the other needs the same change, and say so.

## Rules

- UK/South African English in all files.
- Never add real exam items, memos, marks or student data. Examples must be invented. This is about exam security and POPIA.
- Do not rename skill folders or change `name` fields without asking.
- Do not change SKILL.md or reference files when the task is documentation only.
- Keep SKILL.md files under 500 lines and descriptions under 1,024 characters.
- Never use "Claude" or "Copilot" as trademarks in skill names.

## README conventions

- Root README.md: purpose of the collection, list of skills with one-line descriptions, how to install a skill on each platform, licence, and a note that the skills are tools to assist staff, not to replace academic judgement.
- Skill README.md: purpose, supported question types or features, differences between the platform versions, install steps for each platform, how to prepare input documents, a short example, known limitations, and a "Version / Last updated" line.
- Plain, professional tone for educators who are not developers. Minimal jargon.

## Git

- Commit messages: imperative, short, and naming the platforms affected, for example "Add AI feedback (copilot + claude)".
- Never commit or push. The user makes all commits.