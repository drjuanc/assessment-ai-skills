---
name: exam-to-moodle
description: Converts assessment documents (Word or PDF) containing multiple-choice, multiple-response, matching, essay, long-answer, complete-the-table or MEQ questions into a Moodle XML file ready for question bank import. Reads red-font correct answers directly from the file, reads each question's metadata (marks, topic, task, subtask, Bloom's level, module), embeds images, and can add AI-generated student feedback with a disclaimer. Use this skill whenever the user mentions Moodle, Moodle XML, question bank import or quiz import, or asks to convert, upload or move exam, test, MCQ or assessment questions into Moodle, even if they do not say "XML".
---

# Exam to Moodle

Converts an assessment document into one Moodle XML file that imports cleanly into a Moodle question bank.

## Files in this skill

| File | Use |
|---|---|
| `scripts/extract_document.py` | Reads the DOCX or PDF; marks red text, writes out list labels, tables and image placeholders |
| `scripts/embed_images.py` | Embeds extracted images into the finished XML |
| `scripts/validate_moodle_xml.py` | Checks the XML before delivery |
| `references/question_patterns.md` | Read before step 3: question types and layouts |
| `references/metadata_rules.md` | Read before step 3: metadata, tags, essay settings |
| `references/templates.md` | Read before step 4: exact XML per question type |
| `references/feedback_rules.md` | Read before step 4, only with AI feedback |
| `references/validation_checklist.md` | Read at step 6: checks the script cannot do |

Run scripts from this skill's folder (`python <skill folder>/scripts/<script>.py`). Use `/home/claude/exam-to-moodle/` as the working folder.

## Workflow

### 1. Ask about feedback

Feedback of any kind is never included by default. Before converting, ask the user to choose one option, using the `ask_user_input_v0` tool if it is available:

> Will these questions be used in an exam? Choose the feedback students should see: (1) No feedback (exams), (2) Only the feedback written in the document, (3) AI-generated feedback, with a disclaimer, plus any feedback in the document.

| Option | What goes in the XML |
|---|---|
| No feedback | Every feedback element is empty, including feedback written in the document. |
| Document feedback only | Feedback written in the document, wrapped in `<div class="doc-feedback">`. No AI feedback. |
| AI feedback | AI feedback with the disclaimer, following `references/feedback_rules.md`, plus any feedback written in the document. |

With AI feedback, mention that the user may attach supporting material (lecture notes, guidelines, a memo). Skip the question only if the user has already stated one of the three options. If the answer is unclear, ask again. Never assume an option from words such as "quiz", "test" or "practice". Keep the choice for the rest of the conversation unless the user changes it. Wait for the answer before converting.

### 2. Extract the document

```bash
python <skill folder>/scripts/extract_document.py "<uploaded file>" --out /home/claude/exam-to-moodle/work
```

Read `work/document.md` in full and work from it. Use the summary the script prints:

- "no red text or markers found": stop and give the user the steps in "Preparing the document".
- A theme-colour warning: if questions then have no answer, mention it in the report.
- A `.doc` file is refused: ask the user to save it as `.docx`.

### 3. Identify the questions

Read `references/question_patterns.md` and `references/metadata_rules.md`. Split the document into questions; a question ends where its metadata ends or where the next question number begins. For each question identify its type, correct answers, metadata and any essay settings.

### 4. Build the XML

Read `references/templates.md` (and `references/feedback_rules.md` with AI feedback). Write the XML to `/home/claude/exam-to-moodle/<source file name>.xml`, starting with one category element. Copy the template structures exactly; do not invent or omit elements. With Document feedback only or AI feedback, write each question's feedback as you build it.

### 5. Embed images

If the XML contains `[[IMAGE:...]]` placeholders:

```bash
python <skill folder>/scripts/embed_images.py <xml file> --images /home/claude/exam-to-moodle/work/images
```

### 6. Validate

```bash
python <skill folder>/scripts/validate_moodle_xml.py <xml file>
```

Add `--no-feedback` with No feedback, or `--ai-feedback` with AI feedback. Use neither with Document feedback only.

Fix every ERROR and run it again until the result is PASS. Review each WARNING. Then work through `references/validation_checklist.md`, which covers content the script cannot check.

### 7. Deliver

Copy the file to `/mnt/user-data/outputs/<source file name>.xml` and share it with `present_files`. Then give the report (see "Report").

## Correct answers

The extraction script wraps red text as `[[CORRECT]]text[[/CORRECT]]`. A document already prepared with the Word macro may contain `[[CORRECT]]` without an end marker; the answer then runs from the marker to the end of that option, table cell or line.

- An option is correct if any part of it (letter, word, whole option or table cell) is marked.
- Remove every marker from the output.
- Ignore marked text outside answer options, matching keys and tables to complete (for example a red heading or instruction).
- In tables to complete, marked text is the expected answer: strip it from the response template and put the filled table in the grader information (see `question_patterns.md`, "Tables to complete").
- Never decide a correct answer from your own knowledge. If an MCQ or a keyed matching question has no marked answer, leave it out of the XML and list it in the report.

## MCQ scoring

- One correct option: `<single>true</single>`; the correct option gets `fraction="100"`, all others `fraction="0"`.
- Two or more correct options: `<single>false</single>` with these fractions only (Moodle rejects other values):

| Correct options | Each correct | Each incorrect |
|---|---|---|
| 2 | 50 | -50 |
| 3 | 33.33333 | -33.33333 |
| 4 | 25 | -25 |
| 5 | 20 | -20 |

- Remove option labels (A., b), (iii), 1.) from option text; Moodle adds its own with `<answernumbering>ABCD</answernumbering>`.
- Use `<shuffleanswers>false</shuffleanswers>` if any option refers to other options ("All of the above", "None of the above", "Both A and C"); otherwise use `true`.

## Essay settings

Essays can include word limits, file uploads, a response template (headings or a table to complete) and a rubric. Detect them with `question_patterns.md`, map them with `metadata_rules.md` ("Essay settings mapping"), and use the values and defaults in `templates.md` ("Essay setting values"). Apply only settings the document states; never invent a word limit, upload requirement or rubric.

## Category, names and grades

- Category: one category element at the very top, with the path `$course$/top/<source file name without extension>`, replacing spaces with underscores.
- Names: number questions sequentially across the whole document (Q001, Q002, ...). If the question has a topic, prefix it in CamelCase with no spaces or punctuation: `CardiovascularSystem_Q001`. MEQ sub-parts add a letter: `Shock_Q004a`, `Shock_Q004b`.
- `<defaultgrade>` is the question's mark. If no mark is found, use 1 and list the question in the report.

## Text handling

- Put question text, option text, feedback and grader information inside `<![CDATA[ ... ]]>` as simple HTML: `<p>`, `<strong>`, `<em>`, `<ul>`, `<ol>`, `<li>`, `<table>`, `<sub>`, `<sup>`.
- Keep the original wording, spelling, units and symbols exactly. Do not correct, shorten or rephrase.
- If any text contains `]]>`, split it across two CDATA sections.
- Matching answers (Column B text) are plain text with no HTML tags.
- Images: keep each `[[IMAGE:name]]` placeholder exactly where the image belongs, in its own `<p>`; `embed_images.py` does the rest. PDFs give no image files: write `<p>[Image: brief description]</p>` and list the question in the report.

## Report

After sharing the file, give a brief report in UK English:

- questions converted, with a count per type
- questions left out, with the reason
- questions needing a check (missing mark, PDF image, uncertain type, unrecognised Bloom's level, unclear essay settings)
- the feedback option used: No feedback, Document feedback only or AI feedback
- with Document feedback only or AI feedback: how many questions used feedback from the document
- with Document feedback only: if the document contains no feedback, say so (every feedback element is then empty)
- with AI feedback: how many questions received AI feedback, and any possible key errors (feedback withheld), each with a one-line reason
- with Document feedback only or AI feedback: a reminder to switch on "General feedback" and "Specific feedback" in the quiz's Review options, or students will not see it

Do not explain the XML.

## Preparing the document

If no marked answers are found, tell the user the likely causes and fixes:

1. The answers use a theme colour or an unusual shade: select the answers in Word and apply standard Red from Font colour.
2. The answers are not coloured at all: colour them red, or type `[[CORRECT]]` before each correct option or key.
3. The PDF is scanned (no selectable text): provide the original Word file instead.