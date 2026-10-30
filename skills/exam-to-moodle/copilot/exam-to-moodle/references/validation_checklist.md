# Validation Checklist

Check every item before returning output. Fix any failure. If a question cannot be fixed, remove it and list it in the report.

## File

- [ ] The first line is `<?xml version="1.0" encoding="UTF-8"?>`
- [ ] `<quiz>` is the only root element, and the category question comes first.
- [ ] Every element that is opened is closed, in the correct order.
- [ ] Outside CDATA, `&`, `<` and `>` are escaped as `&amp;`, `&lt;` and `&gt;`.
- [ ] No `[[CORRECT]]` markers remain anywhere.

## Every question

- [ ] Its name is unique.
- [ ] `<questiontext>` has `format="html"` and is not empty.
- [ ] `<defaultgrade>` is a number greater than 0.
- [ ] `<penalty>0</penalty>` and `<hidden>0</hidden>` are present.
- [ ] Tags follow `metadata_rules.md`.

## Multichoice

- [ ] There are at least two answers.
- [ ] With `<single>true</single>`, exactly one answer has fraction 100.
- [ ] With `<single>false</single>`, the positive fractions total 100 (3 × 33.33333 is acceptable).
- [ ] Every fraction comes from the table in `SKILL.md`.
- [ ] No option labels (A., b), (i)) remain in option text.

## Matching

- [ ] There are at least two subquestions with text.
- [ ] There are at least three answers, including distractors.
- [ ] Every key letter has been resolved to its Column B text.
- [ ] Answer text contains no HTML tags.

## Essay

- [ ] `<responseformat>` is one of: editor, editorfilepicker, plain, noinline.
- [ ] Any memo or rubric is in `<graderinfo>`, and a marker-only rubric is not in `<questiontext>`.
- [ ] `<minwordlimit>`, when present, is lower than `<maxwordlimit>`.
- [ ] Word limits are absent on upload-only (`noinline`) questions.
- [ ] `<attachmentsrequired>` is not greater than `<attachments>` (unless attachments is -1).
- [ ] An upload-only question has `<responserequired>0</responserequired>` and `<attachmentsrequired>` of at least 1.
- [ ] A "complete the table" question has the table in `<responsetemplate>` with every marked answer removed and every unmarked cell kept, and the filled table in `<graderinfo>`.
- [ ] No `[[CORRECT]]` markers or answer text remain in `<responsetemplate>`.
- [ ] Template headings in `<responsetemplate>` are not repeated in `<questiontext>`.
- [ ] `<filetypeslist>` entries start with a dot and are separated by commas.

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
- [ ] Every feedback element containing AI-generated text ends with the exact disclaimer paragraph from `SKILL.md`.
- [ ] Possible key errors have no AI feedback at all and are listed in the report with a one-line reason.

## Report

- [ ] The counts in the report match the questions in the XML.
- [ ] The report states the feedback option used.
- [ ] With Document feedback only, the report says so if the document contains no feedback.
- [ ] Possible key errors are listed with a one-line reason, with AI feedback.