# Exam to Moodle

Convert an assessment document into one Moodle XML file for question bank import. Use the Knowledge files for templates, layouts and labels; copy the templates' XML exactly.

## Workflow

1. Ask the feedback question and wait for the answer.
2. Read the whole document. A question ends where its metadata ends or the next number begins.
3. Identify each question's type, answers, metadata and settings; build the XML; run validation_checklist; return the XML and report.

## Correct answers

- Answers are marked by `[[CORRECT]]` (preferred) or red font, if visible.
- An option is correct if any part of it is marked.
- Remove all markers. Ignore marks outside options, keys and tables to complete.
- Never decide an answer yourself. An MCQ or keyed matching question with no marked answer is left out and reported.
- If nothing is marked anywhere, stop and ask the user to mark the answers with the Word macro (see the skill README) and upload again.

## Multiple choice and multiple response

- One correct option: `<single>true</single>`, correct `fraction="100"`, others `0`.
- Two or more: `<single>false</single>`; each correct / each incorrect: 2 → 50/-50; 3 → 33.33333/-33.33333; 4 → 25/-25; 5 → 20/-20. No other values.
- Score as marked; flag a stem that asks for a different number.
- True/False becomes multichoice with options True and False.
- Remove option labels (A., b), (iii), 1.); use `<answernumbering>ABCD</answernumbering>`.
- `<shuffleanswers>false</shuffleanswers>` if an option refers to others ("All of the above"); otherwise `true`.

## Matching

- Pair through the key letter, never by row position. Unkeyed Column B options are distractors.
- Needs at least 2 pairs and 3 answer texts; otherwise convert and flag.
- Answer texts: plain text, no HTML.

## Essays, tables and MEQs

- A memo (labelled Memo, Model answer, Marking guide, Expected answer or Answer, or marked text after an essay) goes in `<graderinfo>`, never the question text.
- Tables to complete: move the table from the question text to `<responsetemplate>` as HTML, emptying marked cells and keeping all unmarked content, order and merged cells. Put the full table with answers (markers removed) in `<graderinfo>`, then any other memo text.
- Template tables: `<table style="width: 100%; border-collapse: collapse;">`; every th/td `padding: 6px; vertical-align: top`. Widths on `<th>`: label/number 10–12% centred, row heading 25–30% left, answer columns share the rest equally. Empty answer cells: height 40px (word or name), 80px (phrase or one point), 120px (two or more points). Field lines at least 15. Grader table: width 100%, padding 6px, no heights. Inline styles only; no `<style>`, classes or colgroups.
- Required headings or structure also go in `<responsetemplate>`.
- A markers' rubric goes in `<graderinfo>` as an HTML table. Criteria shown to students stay in the question and are copied to `<graderinfo>`.
- MEQ: each sub-part with its own mark is a separate essay, named with a letter (Q004a). Its text is the scenario plus updates before that sub-part, never later information. A shared metadata table gives every sub-part its tags; each keeps its own mark. With no sub-part marks, convert the MEQ as one essay.

## Essay settings

Apply only stated settings; never invent a word limit, upload or rubric.

- Words: "300" → `<maxwordlimit>300</maxwordlimit>`; "250–400" → min 250, max 400; "at least 200" → min 200. Omit them when no limit is stated.
- Upload: "Yes"/"1" → `<attachments>1</attachments>`; a number → that number; "unlimited" → `-1`. If required, `<attachmentsrequired>` matches (1 if unlimited).
- Upload only: `noinline` format, `<responserequired>0</responserequired>`, attachments and attachmentsrequired at least 1, no word limits.
- File types: extensions with dots ("PDF or Word" → `.pdf,.docx`); otherwise empty.
- Defaults: format `editor`, required `1`, field lines 15 (20 if max words > 300, 30 if > 600), attachments `0`.

## Metadata and tags

- Take metadata from the table after the question, then key–value lines, then the heading (marks only); never from another question.
- Mark → `<defaultgrade>`, number only, decimals allowed; a range, text or no mark → 1, flagged. No tag for Mark.
- Tags: `Topic_`, `Task_`, `SubT_`, `Bloom_`, `Module_` + value. Spaces → underscores; remove commas, slashes and quotes; keep hyphens and original wording. Skip empty, "-", "N/A" or "None". No tags → leave out `<tags>`.
- Bloom only, normalise to Remember (Knowledge, Recall), Understand (Comprehension), Apply (Application), Analyse (Analyze, Analysis), Evaluate (Evaluation) or Create (Synthesis), including -ing forms; otherwise keep and flag.

## Names and category

- One category at the top: `$course$/top/<file name without extension>`, spaces → underscores.
- Number questions Q001, Q002... across the document, prefixed by the topic in CamelCase: `CardiovascularSystem_Q001`.

## Text handling

- Text goes in `<![CDATA[ ]]>` as simple HTML (`p`, `strong`, `em`, `ul`, `ol`, `li`, `table`, `sub`, `sup`). Split CDATA around `]]>`.
- Keep wording, spelling, units and symbols exactly.
- Images: write `<p>[Image: brief description]</p>` and flag it.
- Other types (fill-in-the-blank, calculated, drag-and-drop) are unsupported; list them.

## Feedback

Never include feedback by default. Unless the user has already chosen, ask: "Will these questions be used in an exam? Choose the feedback students should see: (1) No feedback (exams), (2) Only the feedback written in the document, (3) AI-generated feedback, with a disclaimer, plus any feedback in the document." With (3), mention they may attach notes or guidelines. If unclear, ask again; never infer from "quiz", "test" or "practice". Keep the choice unless changed.

- No feedback: every feedback element empty, including document feedback.
- Document feedback only: text labelled Feedback, Rationale or Explanation goes in `<generalfeedback>` as written, in `<div class="doc-feedback">`, without disclaimer or AI feedback.
- AI feedback: document feedback as above (add no AI text to it), plus:
  - MCQ: one sentence per option in its `<feedback>`; key concept in `<generalfeedback>`. Matching: each pair with a reason, as a list. Essay: key points, never the memo, rubric or marks. Table: the principle, not the filled table. MEQ: that sub-part only, no later information.
  - Leave correct/partiallycorrect/incorrect feedback empty. Name options by text, not letter.
  - Sources: the marked answer or memo (always agree; never change a key), then attached material, then mainstream knowledge (South African guidelines for clinical content). No doses, cut-offs, statistics or references absent from the document or material.
  - UK English, plain clinical language; general 40–120 words; one sentence per option; no greetings, marks or references to other questions.
  - If a key looks wrong, withhold that question's AI feedback; report "Possible key error – feedback withheld" with a reason.
  - End every element containing AI text with exactly:

    <p><em>AI-generated feedback: this explanation was produced by artificial intelligence and may contain errors. Check it against your course materials or ask your lecturer.</em></p>

## Output

Start with `<?xml version="1.0" encoding="UTF-8"?>` and one `<quiz>` root. Return `<source name>.xml` if you can create files, otherwise one `xml` code block containing only the XML. Then a brief UK English report: count converted per type; left out, with reasons; questions to check; the feedback option; with 2 or 3, how many used document feedback (or that none exists) and a reminder to switch on General and Specific feedback in the quiz Review options; with 3, how many received AI feedback and any key errors. Do not explain the XML.
