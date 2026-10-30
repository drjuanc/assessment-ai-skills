# Validation Checklist

Run `scripts/validate_moodle_xml.py` first and fix every ERROR. The script checks structure: well-formed XML, the category, unique names, grades, MCQ fractions, matching counts, essay setting combinations, leftover markers and placeholders, and the feedback option: empty feedback with `--no-feedback`, or the disclaimer and general feedback length with `--ai-feedback`.

Then check these content points, which the script cannot judge. Fix any failure; if a question cannot be fixed, remove it and list it in the report.

## Answers

- [ ] Every correct answer in the XML matches marked text in `document.md`, and nothing unmarked was scored as correct.
- [ ] Matching pairs follow the key letters, not row order.
- [ ] Questions without a marked answer were left out and listed.

## Text

- [ ] Question and option wording matches the document exactly, apart from removed labels and markers.
- [ ] Each image placeholder sits where the image appears in the question.
- [ ] MEQ sub-parts contain no scenario information from later sub-parts.

## Essays

- [ ] Memo and marker-only rubrics are in `<graderinfo>`, not in `<questiontext>`.
- [ ] A "complete the table" question has the table in `<responsetemplate>` with every marked answer removed and every unmarked cell kept, and the filled table in `<graderinfo>`.
- [ ] Template headings or tables are not repeated in `<questiontext>`.
- [ ] Word limits, uploads and file types appear only where the document states them.

## Metadata

- [ ] Grades and tags come from each question's own metadata, following `metadata_rules.md`.

## Feedback

- [ ] The feedback option is the one the user chose.
- [ ] `<correctfeedback>`, `<partiallycorrectfeedback>` and `<incorrectfeedback>` are empty.

With No feedback:

- [ ] Every feedback element is empty, with no exceptions.

With Document feedback only:

- [ ] Feedback from the document is in `<generalfeedback>`, wrapped in `<div class="doc-feedback">`, with no disclaimer.
- [ ] Every other feedback element is empty, and no AI feedback appears.

With AI feedback:

- [ ] Feedback from the document is in `<generalfeedback>`, wrapped in `<div class="doc-feedback">`, with no disclaimer.
- [ ] Every multichoice answer has one sentence in `<feedback>`, and every question has `<generalfeedback>`, except possible key errors.
- [ ] Matching and essay questions have general feedback only.
- [ ] General feedback is 40–120 words, not counting the disclaimer.
- [ ] Feedback agrees with the marked answer or key.
- [ ] MCQ feedback refers to options by text, never by letter.
- [ ] Essay `<generalfeedback>` does not reproduce the full memo, rubric or mark allocation.
- [ ] No doses, values or references appear that are not in the document or provided material.
- [ ] Every feedback element containing AI-generated text ends with the exact disclaimer paragraph from `feedback_rules.md`.
- [ ] Possible key errors have no AI feedback at all and are listed in the report with a one-line reason.

## Report

- [ ] The counts in the report match the questions in the XML.
- [ ] The report states the feedback option used.
- [ ] With Document feedback only, the report says so if the document contains no feedback.