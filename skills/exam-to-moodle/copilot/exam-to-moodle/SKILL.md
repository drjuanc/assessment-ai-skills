---
name: exam-to-moodle
description: Converts assessment documents (Word or PDF) containing multiple-choice, multiple-response, matching, essay, long-answer, complete-the-table or MEQ questions into a Moodle XML file ready for question bank import. Detects correct answers from [[CORRECT]] markers or red font, reads each question's metadata table (marks, topic, task, subtask, Bloom's level, module), and generates grades, tags, a category, question names and optional AI-generated student feedback. Use this skill whenever the user mentions Moodle, Moodle XML, question bank import or quiz import, or asks to convert, upload or move exam, test, MCQ or assessment questions into Moodle, even if they do not say "XML".
---

# exam-to-moodle (Moodle XML Questions Generator)

Converts an assessment document into one Moodle XML file that imports cleanly into a Moodle question bank.

## Before you start

Read these files in full before converting anything:

1. `references/question_patterns.md`: how to recognise each question type and its layout variants.
2. `references/metadata_rules.md`: metadata labels, tag format, essay settings and Bloom's normalisation.
3. `references/templates.md`: the exact XML for every question type, essay setting values and feedback placement. Copy these structures; do not invent or omit elements.

Before returning output, work through `references/validation_checklist.md`.

## Workflow

1. Ask the feedback question (see "Student feedback"). Skip it only if the user has already stated one of the three options. Wait for the answer before converting.
2. Read the whole document before writing any XML.
3. Split it into individual questions. A question ends where its metadata ends or where the next question number begins.
4. Identify the type of each question (see `question_patterns.md`).
5. Identify the correct answers (see "Correct answers" below).
6. Extract each question's metadata and essay settings (see `metadata_rules.md`).
7. With Document feedback only or AI feedback, write the feedback (see "Student feedback").
8. Build the XML from `templates.md`, starting with one category element.
9. Run the validation checklist and fix any failures.
10. Return the XML and the conversion report (see "Output").

## Correct answers

Correct answers are marked in one of two ways, in this order of priority:

1. The text marker `[[CORRECT]]` before an option or matching key. This is the reliable method; the user adds it in Word before uploading.
2. Red font, if font colour is visible to you in the document.

Rules:

- An option is correct if any part of it (letter, word, whole option or table cell) carries the marker or red font.
- Remove every `[[CORRECT]]` marker from the output.
- Ignore markers or red text outside answer options, matching keys and tables to complete (for example a red heading or instruction).
- In tables to complete, marked text is the expected answer: strip it from the response template and put the filled table in the grader information (see `references/question_patterns.md`, "Tables to complete").
- Never decide a correct answer from your own knowledge. If an MCQ or a keyed matching question has no marker or red font, leave it out of the XML and list it in the report.
- If no markers or red font can be detected anywhere in the document, stop and give the user the steps in "Preparing the document".

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

Essay questions can include word limits, file uploads, a response template and a rubric. Detect them with `references/question_patterns.md` ("Essay settings"), map them with `references/metadata_rules.md` ("Essay settings mapping"), and use the values and defaults in `references/templates.md` ("Essay setting values"). Apply only settings the document states. Never invent a word limit, upload requirement or rubric.

## Student feedback

### Asking

Feedback of any kind is never included by default. Before converting, ask the user to choose one option:

"Will these questions be used in an exam? Choose the feedback students should see: (1) No feedback (exams), (2) Only the feedback written in the document, (3) AI-generated feedback, with a disclaimer, plus any feedback in the document."

| Option | What goes in the XML |
|---|---|
| No feedback | Every feedback element is empty, including feedback written in the document. |
| Document feedback only | Feedback written in the document, wrapped in `<div class="doc-feedback">`. No AI feedback. |
| AI feedback | AI feedback with the disclaimer, following the rules below, plus any feedback written in the document. |

With AI feedback, mention that the user may attach notes, guidelines or other material to base it on. Skip the question only if the user has already stated one of the three options. If the answer is unclear, ask again. Never assume an option from words such as "quiz", "test" or "practice". Keep the choice for the rest of the conversation unless the user changes it.

The rest of this section applies to AI feedback, except "Feedback already in the document", which also applies to Document feedback only.

### Sources, in order of authority

1. The marked correct answer, matching key or memo in the document. Feedback must always agree with it. Never change a fraction or key.
2. Material the user attached (lecture notes, guidelines, textbook extracts). Base the feedback on it wherever it covers the question, and prefer its terminology, values and recommendations.
3. Your own knowledge, limited to established, mainstream content, and only where the document and material say nothing. Use South African guidelines and terminology when the content is clinical and the user has not supplied other material.

Do not state drug doses, cut-off values, statistics, guideline numbers or references unless they appear in the document or the attached material. If a detail is uncertain, leave it out.

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

## Category, names and grades

- Category: one category element at the very top, with the path `$course$/top/<source file name without extension>`, replacing spaces with underscores.
- Names: number questions sequentially across the whole document (Q001, Q002, ...). If the question has a topic, prefix it in CamelCase with no spaces or punctuation: `CardiovascularSystem_Q001`. MEQ sub-parts add a letter: `Shock_Q004a`, `Shock_Q004b`.
- `<defaultgrade>` is the question's mark. If no mark is found, use 1 and list the question in the report.

## Text handling

- Put question text, option text, feedback and grader information inside `<![CDATA[ ... ]]>` as simple HTML: `<p>`, `<strong>`, `<em>`, `<ul>`, `<ol>`, `<li>`, `<table>`, `<sub>`, `<sup>`.
- Keep the original wording, spelling, units and symbols exactly. Do not correct, shorten or rephrase.
- If any text contains `]]>`, split it across two CDATA sections.
- Matching answers (Column B text) are plain text with no HTML tags.
- Images cannot be embedded. Put `<p>[Image: brief description]</p>` where the image was and list the question in the report so the user can add the image in Moodle.

## Output

1. If you can create files, save the XML as `<source file name>.xml` (Exam1.docx becomes Exam1.xml) and give the user the file. Otherwise return the complete XML in one code block labelled `xml`, with nothing else inside it.
2. The XML starts with `<?xml version="1.0" encoding="UTF-8"?>` and has `<quiz>` as its only root element.
3. After the XML, give a brief conversion report:
   - questions converted, with a count per type
   - questions left out, with the reason
   - questions needing a check (missing mark, image, uncertain type, unrecognised Bloom's level, unclear essay settings)
   - the feedback option used: No feedback, Document feedback only or AI feedback
   - with Document feedback only or AI feedback: how many questions used feedback from the document
   - with Document feedback only: if the document contains no feedback, say so (every feedback element is then empty)
   - with AI feedback: how many questions received AI feedback, and any possible key errors (feedback withheld), each with a one-line reason
   - with Document feedback only or AI feedback: a reminder to switch on "General feedback" and "Specific feedback" in the quiz's Review options, or students will not see it

Do not explain the XML.

## Preparing the document

If the document has no detectable markers, give the user these steps:

1. Open the document in Word and press Ctrl+H, then click More.
2. Click in Find what, leave it empty, and choose Format → Font → Font colour: the red used in the document → OK.
3. In Replace with, type `[[CORRECT]]^&`
4. Click Replace All, save, and upload the document again.

For PDFs, do this in the original Word document and upload the Word file.