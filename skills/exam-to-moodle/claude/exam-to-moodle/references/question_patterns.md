# Question Patterns

## Multiple choice (single answer)

A stem followed by labelled options: A–E, a–e, (a), a), 1., (i) and similar. One option is marked correct.

True/False items are converted as multichoice with two options, True and False.

## Multiple response

The same layout with two or more options marked correct. Stems such as "Select all that apply" or "Choose TWO" support this, but the number of marked options decides the scoring. If the stem asks for a number different from the number marked, convert as marked and flag it in the report.

## Matching

Every matching question must give at least 2 pairs and at least 3 answer texts in total, counting distractors. If not, convert it anyway and flag it.

### Layout 1: direct pairs

"Match ..." followed by lines such as "Item -> Answer" or "Item – Answer", or a two-column table where each row is a pair. The pairing is explicit, so no marker is needed.

### Layout 2: examination table with a key column

    Column A              Key   Column B
    Cardiogenic shock     B     A. Pathological reduction in systemic vascular resistance...
    Obstructive shock     C     B. Myocardial dysfunction resulting in...
    Hypovolaemic shock    D     C. Physical restriction of the great vessels or heart...
    Distributive shock    A     D. Acute deficit in intravascular volume...

- Column A items become the subquestions.
- The key column holds the letter of the correct Column B option. It is usually marked or red.
- Column B rows are in a different order from Column A. Always pair through the key letter, never by row position.
- Column B options that no key points to are distractors.

Expected pairing for the example:

- Cardiogenic shock → Myocardial dysfunction resulting in...
- Obstructive shock → Physical restriction of the great vessels or heart...
- Hypovolaemic shock → Acute deficit in intravascular volume...
- Distributive shock → Pathological reduction in systemic vascular resistance...

### Layout 3: two lists with an answer key

A numbered list, a lettered list, and a key such as "1–C, 2–A, 3–D". The key may be marked, red, or in a separate memo section. Pair through the key.

## Essay / long answer

There are no options; the student writes a response ("Discuss", "Describe", "Explain", "Outline", "Complete the table", case-based questions).

### Memo

A memo is text labelled Memo, Model answer, Marking guide, Expected answer or Answer, or marked text following an essay question. The memo goes into `<graderinfo>`, never into the question text.

### Tables to complete

When the question asks the student to complete, fill in or populate a table ("Complete the table below", "Fill in the missing information"):

- The table goes in `<responsetemplate>` as an HTML table, so the student types into it. Remove the table from the question text.
- Marked content in the table (`[[CORRECT]]...[[/CORRECT]]`, or text from a lone `[[CORRECT]]` marker to the end of that cell) is the expected answer. Strip it from the template. A cell that becomes empty gets `&nbsp;`.
- Keep all unmarked content (black or any colour other than red): headings, row labels, units, pre-filled cells and unmarked text in a partly marked cell ("Effect: [[CORRECT]]Dry cough[[/CORRECT]]" becomes "Effect: ").
- Copy the full table, with the marked answers in place and the markers removed, into `<graderinfo>` as the model answer. Put any other memo text after it.
- Keep the original row and column order, merged cells and headings.

Example as it appears in `document.md`:

    [TABLE 2]
    | Drug | Class | Main adverse effect |
    | Enalapril | [[CORRECT]]ACE inhibitor[[/CORRECT]] | [[CORRECT]]Dry cough[[/CORRECT]] |
    | Amlodipine | [[CORRECT]]Calcium channel blocker[[/CORRECT]] | [[CORRECT]]Ankle oedema[[/CORRECT]] |
    [/TABLE 2]

The template keeps the header row and the Drug column, and leaves the other cells empty. `<graderinfo>` holds the complete table.

### Other templates

Headings or a structure the student must follow ("Structure your answer under:", "Use the headings below") also go in `<responsetemplate>`, removed from the question text.

### Essay settings

Look for these in the question text, the metadata table, or a note directly under the question. Apply only what the document states; otherwise use the defaults in `templates.md` ("Essay setting values").

| Setting | Recognise phrases such as |
|---|---|
| Word limit | "Word limit: 300", "(250–400 words)", "Maximum 500 words", "Minimum 200 words", "Answer in not more than 300 words" |
| File upload | "Upload", "Attach", "Submit as PDF/Word", "Upload a diagram", "Attach your care plan" |
| Upload only | "Upload your answer" with no space or instruction to type an answer |
| Rubric | Text labelled Rubric, Marking rubric, Assessment criteria, Mark allocation, or a table of criteria with marks or levels |

### Rubric placement

- A rubric labelled for markers goes in `<graderinfo>` as an HTML table.
- Criteria the document presents to students inside the question ("You will be assessed on: ...") stay in the question text, and a copy also goes in `<graderinfo>`.

## MEQ (modified essay question)

A clinical scenario followed by sub-parts such as (a), (b) or 1.1, 1.2, usually each with its own mark.

- Each sub-part with its own mark becomes a separate essay question.
- Each sub-part's question text starts with the scenario, plus any scenario updates given before that sub-part, followed by the sub-part question. Do not include information revealed after that sub-part.
- Name sub-parts with letters: Q004a, Q004b.
- If one metadata table covers the whole MEQ, apply its tags to every sub-part, and use each sub-part's own mark for `<defaultgrade>`.
- If the sub-parts have no individual marks, convert the whole MEQ as one essay question.

## Feedback in the document

Text labelled Feedback, Rationale or Explanation after a question is student feedback, not a memo. With Document feedback only or AI feedback, it goes in `<generalfeedback>` as written, wrapped in `<div class="doc-feedback">`, with no disclaimer. With No feedback, leave it out (see "Ask about feedback" in `SKILL.md`).

## Reading document.md

- `[TABLE n]` ... `[/TABLE n]` encloses a Word table; each line is one row and `|` separates cells. Several paragraphs in one cell are joined with ` / `.
- Word's automatic list numbering is written out (`A.`, `b)`, `1.`). Numbering may restart or continue across questions as in Word, so identify options by their position under the stem, not only by the label.
- `[[IMAGE:imageN.ext]]` marks where an image sits.
- `[END OF PAGE n]` appears in PDF extractions only; ignore it when splitting questions.

## Unsupported types

Fill-in-the-blank, calculated, drag-and-drop and other types are not converted. List them in the report as unsupported.