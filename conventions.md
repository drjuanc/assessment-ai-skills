# Conventions

This file is the master copy of the rules shared by the skills in this collection.

Skills cannot read files outside their own folder, so these rules are copied into each skill (usually into its `references/` folder, sometimes into SKILL.md). When you change a rule here, copy the change to every skill that uses it, in the Claude version, the Copilot version and the Copilot agent instructions (`copilot/agent-instructions.md`).

| Rule | exam-to-moodle (claude) | exam-to-moodle (copilot) | exam-to-moodle (copilot agent) |
|---|---|---|---|
| Metadata, tags, Bloom's, essay settings mapping | `references/metadata_rules.md` | `references/metadata_rules.md` | `agent-instructions.md`, "Metadata and tags" and "Essay settings" |
| Essay settings: "Apply only settings the document states" | `SKILL.md`, "Essay settings" | `SKILL.md`, "Essay settings" | `agent-instructions.md`, "Essay settings" |
| Response template tables | `references/question_patterns.md`, "Response template tables" (example: `templates.md`, `Pharmacology_Q006`; checks: `validation_checklist.md`) | same as Claude | `agent-instructions.md`, "Essays, tables and MEQs" |
| MCQ fractions, question naming and category | `SKILL.md` | `SKILL.md` | `agent-instructions.md`, "Multiple choice and multiple response" and "Names and category" |
| Feedback rules and disclaimer | `references/feedback_rules.md` (asking: `SKILL.md`) | `SKILL.md`, "Student feedback" | `agent-instructions.md`, "Feedback" |

## Metadata

### Where metadata comes from

Metadata is usually a small table immediately after the question, but may be key–value lines ("Marks: 2") or a mix. Use this order of preference:

1. the metadata table
2. key–value lines
3. the question heading, for marks only, e.g. "Question 3 (4 marks)"

Never take metadata from a different question.

### Field labels

Match labels case-insensitively and ignore punctuation and trailing colons.

| Field | Accepted labels |
|---|---|
| Mark | Mark, Marks, Score, Points |
| Topic | Topic, Theme, Content area |
| Task | Task, Task type |
| SubT | SubT, Subt, Subtask, Sub task, Sub-task |
| Bloom | Bloom, Blooms, Bloom's, Bloom T, Bloom Taxonomy, Bloom's level, Cognitive level |
| Module | Module, Module code |
| Words | Word limit, Words, Word count, Length |
| Upload | Upload, Attachment, Attachments, Files, Submission |
| FileTypes | File type, File types, Format, Accepted files |

### Mapping

- Mark → `<defaultgrade>`. Use the number only ("3 marks" becomes 3). Decimals are allowed. If the mark is a range or text, use 1 and flag it.
- Topic, Task, SubT, Bloom and Module → tags.
- Do not create a tag for Mark.

## Tag format

Tags are written as `Prefix_Value`:

- Use exactly these prefixes: `Topic_`, `Task_`, `SubT_`, `Bloom_`, `Module_`
- Replace spaces in the value with underscores. Remove commas, slashes and quotation marks. Keep hyphens.
- Keep the value's original wording and capitalisation, except for Bloom (below).
- Skip the tag if the value is empty, "-", "–", "N/A" or "None".
- If a question has no tags at all, leave out the `<tags>` element.

## Bloom's normalisation

Normalise only the Bloom field (not Task or SubT) to the revised taxonomy:

| Value in document | Tag |
|---|---|
| Remember, Remembering, Knowledge, Recall | Bloom_Remember |
| Understand, Understanding, Comprehension | Bloom_Understand |
| Apply, Applying, Application | Bloom_Apply |
| Analyse, Analyze, Analysing, Analysis | Bloom_Analyse |
| Evaluate, Evaluating, Evaluation | Bloom_Evaluate |
| Create, Creating, Synthesis | Bloom_Create |

If the value is not in this table, keep it as written and flag it in the report.

## Essay settings mapping

These fields apply to essay questions only and never become tags. Apply only settings the document states; never invent a word limit, upload requirement or rubric.

- Words: "300" → `<maxwordlimit>300</maxwordlimit>`; "250–400" → `<minwordlimit>250</minwordlimit>` and `<maxwordlimit>400</maxwordlimit>`; "at least 200" → `<minwordlimit>200</minwordlimit>`.
- Upload: "Yes" or "1" → `<attachments>1</attachments>`; a number → that number; "unlimited" → `-1`. When the document requires an upload, set `<attachmentsrequired>` to the same number (1 if unlimited).
- FileTypes: a comma-separated list of extensions with dots: "PDF or Word" → `.pdf,.docx`; "image" → `.jpg,.png`. Leave empty if not stated.

## Response template tables

When a question has a table in `<responsetemplate>` (complete the table, label the diagram, three-stage assessment and similar), always style it so students have room to write:

- Table: `style="width: 100%; border-collapse: collapse;"`
- Column widths go on the header cells (`<th>`):
  - Label or number columns (e.g. "Label", "1, 2, 3"): 10–12%, `text-align: center`
  - Row-heading columns (e.g. "Stage of assessment", "Feature", "Brain structure"): 25–30%, `text-align: left`
  - Answer columns share the rest equally (e.g. one answer column = 70–75%; two answer columns = 35–37% each)
- Every `<th>` and `<td>`: `padding: 6px; vertical-align: top`
- Answer cell height, set on the empty answer cells (`<td>&nbsp;</td>`):
  - One word or short name: `height: 40px`
  - One phrase or a single point: `height: 80px`
  - Two or more points ("at least 2", "list", "describe"): `height: 120px`
- Keep label and row-heading cells unstyled apart from padding and alignment.
- Set `<responsefieldlines>` to at least 15 for any question with a template table.
- The filled table in `<graderinfo>` also uses `width: 100%` and `padding: 6px`, with no fixed heights.
- Only inline styles. No `<style>` blocks, classes or `<colgroup>`, because Moodle may strip them.

## MCQ fractions

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

## Feedback rules

### Asking

Feedback of any kind is never included by default. Before converting, ask the user to choose one option:

> Will these questions be used in an exam? Choose the feedback students should see: (1) No feedback (exams), (2) Only the feedback written in the document, (3) AI-generated feedback, with a disclaimer, plus any feedback in the document.

| Option | What goes in the XML |
|---|---|
| No feedback | Every feedback element is empty, including feedback written in the document. |
| Document feedback only | Feedback written in the document, wrapped in `<div class="doc-feedback">`. No AI feedback. |
| AI feedback | AI feedback with the disclaimer, following the rules below, plus any feedback written in the document. |

With AI feedback, mention that the user may attach supporting material (lecture notes, guidelines, a memo). Skip the question only if the user has already stated one of the three options. If the answer is unclear, ask again. Never assume an option from words such as "quiz", "test" or "practice". Keep the choice for the rest of the conversation unless the user changes it.

The rest of this section applies to AI feedback, except "Feedback already in the document", which also applies to Document feedback only.

### Sources, in order of authority

1. The marked correct answer, matching key or memo in the document. Feedback must always agree with it. Never change a fraction or key.
2. Material the user provided (lecture notes, guidelines, textbook extracts). Base the feedback on it wherever it covers the question, and prefer its terminology, values and recommendations.
3. Your own knowledge, limited to established, mainstream content, and only where the document and material say nothing. Use South African guidelines and terminology when the content is clinical and the user has not supplied other material.

Do not state drug doses, cut-off values, statistics, guideline numbers or references unless they appear in the document or the provided material. If a detail is uncertain, leave it out.

### Where feedback goes

| Type | `<feedback>` in each answer | `<generalfeedback>` |
|---|---|---|
| Multiple choice / multiple response | One sentence per option, saying why that option is correct or incorrect | The key concept behind the correct option(s) |
| Matching | none | Each correct pair with a short reason, as a list |
| Essay / long answer | none | The key points a good answer covers. Never copy the full memo, rubric or mark allocation. |
| Complete the table | none | The pattern or principle behind the answers, not the filled table |
| MEQ sub-part | none | That sub-part only. Never reveal scenario information from later sub-parts. |

- Leave `<correctfeedback>`, `<partiallycorrectfeedback>` and `<incorrectfeedback>` empty.
- Refer to options by their text, never by letter, because options are shuffled.

### Feedback already in the document

With Document feedback only or AI feedback, text labelled Feedback, Rationale or Explanation after a question is used as written in `<generalfeedback>`, wrapped in `<div class="doc-feedback">...</div>`, with no disclaimer. Do not add AI text to that `<generalfeedback>`. With AI feedback, per-option feedback for multiple choice is still written as above. With No feedback, leave it out.

### Style

- Written for students, in UK English and plain clinical language, at the level of the question.
- General feedback: 40–120 words, not counting the disclaimer. Per-option feedback: one sentence.
- Simple HTML: `<p>`, `<ul>`, `<li>`, `<strong>`.
- No greetings ("Well done!"), no mention of marks, no reference to other questions' answers.

### Disclaimer

End every feedback element that contains AI-generated text (each answer's `<feedback>` and the `<generalfeedback>`) with exactly this paragraph:

    <p><em>AI-generated feedback: this explanation was produced by artificial intelligence and may contain errors. Check it against your course materials or ask your lecturer.</em></p>

Never add it to feedback that came from the document.

### Possible key errors

If you believe a marked answer or key may be wrong, withhold all AI feedback for that question: leave `<generalfeedback>` and every answer's `<feedback>` empty, apart from any feedback from the document. List the question in the report as "Possible key error – feedback withheld", with a one-line reason. Never change the marked answer or key.

## Question naming and category

- Category: one category element at the very top, with the path `$course$/top/<source file name without extension>`, replacing spaces with underscores.
- Names: number questions sequentially across the whole document (Q001, Q002, ...). If the question has a topic, prefix it in CamelCase with no spaces or punctuation: `CardiovascularSystem_Q001`. MEQ sub-parts add a letter: `Shock_Q004a`, `Shock_Q004b`.
- `<defaultgrade>` is the question's mark. If no mark is found, use 1 and list the question in the report.
