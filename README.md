# assessment-ai-skills

AI skills for health professions assessment: exam conversion, item analysis and blueprinting, for Claude and Microsoft 365 Copilot.

## What is a skill?

A skill is a folder of written instructions (and, for Claude, sometimes small helper programs) that teaches an AI assistant how to do one specific task the same way every time. You install it once, and the assistant uses it whenever you ask for that task, so you do not have to explain the rules again.

## Skills

| Skill | What it does | Platforms | Status |
|---|---|---|---|
| [exam-to-moodle](skills/exam-to-moodle/README.md) | Converts a Word or PDF exam, with correct answers marked in red, into a Moodle XML file for question bank import | Claude, Copilot | Available |
| Item analysis | Will analyse exam results to show how well each question performed | To be confirmed | Planned |
| Blueprinting | Will help map exam questions against topics, tasks and Bloom's levels | To be confirmed | Planned |

## How the repository is organised

Each skill has its own folder under `skills/`, with a README and a separate version for each platform:

    skills/<skill-name>/
    ├── README.md                    how to use the skill
    ├── claude/<skill-name>/         the folder you install in Claude
    └── copilot/<skill-name>/        the folder you install in Copilot

The folder you install is always the inner one, `<platform>/<skill-name>`, not the whole skill folder. Some skills also include a Copilot agent version (`copilot/agent-instructions.md`). `conventions.md` holds the shared rules that every skill follows.

## Installing a skill

In short:

- **Claude:** zip the `claude/<skill-name>` folder, switch on **Code execution** under **Settings → Capabilities**, then upload the zip under **Skills**.
- **Copilot (Cowork):** zip the `copilot/<skill-name>` folder and upload it on the **Skills** tab, or copy the folder to OneDrive at `Documents/Cowork/skills/<skill-name>/`.

Each skill's README gives the full steps, including how to prepare your documents and, where available, how to set up a Copilot agent. For example, see the [exam-to-moodle README](skills/exam-to-moodle/README.md).

## Data and exam security

Never put real exam items, memos, marks or student data into this repository or into issues, comments or pull requests. This protects exam security and complies with the Protection of Personal Information Act (POPIA). All examples in this repository are invented.

## Academic judgement

These skills assist staff; they do not replace academic judgement. All output, including converted questions, answer keys, marks, tags and any AI-generated feedback, must be checked by the responsible lecturer before it is used with students.

## Licence

MIT. See [LICENSE](LICENSE).

## Trademarks

Claude is a trademark of Anthropic. Microsoft 365 Copilot is a trademark of Microsoft. This project is independent and is not affiliated with or endorsed by either company.

## Contributing

Changes must keep the Claude and Copilot versions of a skill aligned. Only the intended platform differences are allowed; everything else, including Moodle XML rules, metadata, tags and feedback rules, must stay identical. When you change one version, check whether the others (including any Copilot agent instructions) need the same change. See [CLAUDE.md](CLAUDE.md) for the full list of platform differences and rules, and [conventions.md](conventions.md) for the shared conventions.

## Maintainer

Dr Juan Carlos Garcia-Alonso, Department of Family Medicine and Rural Health, Walter Sisulu University.
