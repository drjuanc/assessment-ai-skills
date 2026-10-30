# AI Feedback Rules

Apply these rules only when the user chose AI feedback. "Feedback already in the document" also applies to Document feedback only. With No feedback, every feedback element is empty.

## Sources, in order of authority

1. The marked correct answer, matching key or memo in the document. Feedback must always agree with it. Never change a fraction or key.
2. Material the user provided (lecture notes, guidelines, textbook extracts). Base the feedback on it wherever it covers the question, and prefer its terminology, values and recommendations.
3. Your own knowledge, limited to established, mainstream content, and only where the document and material say nothing. Use South African guidelines and terminology when the content is clinical and the user has not supplied other material.

Do not state drug doses, cut-off values, statistics, guideline numbers or references unless they appear in the document or the provided material. If a detail is uncertain, leave it out.

## Where feedback goes

| Type | `<feedback>` in each answer | `<generalfeedback>` |
|---|---|---|
| Multiple choice / multiple response | One sentence per option, saying why that option is correct or incorrect | The key concept behind the correct option(s) |
| Matching | none | Each correct pair with a short reason, as a list |
| Essay / long answer | none | The key points a good answer covers. Never copy the full memo, rubric or mark allocation. |
| Complete the table | none | The pattern or principle behind the answers, not the filled table |
| MEQ sub-part | none | That sub-part only. Never reveal scenario information from later sub-parts. |

- Leave `<correctfeedback>`, `<partiallycorrectfeedback>` and `<incorrectfeedback>` empty.
- Refer to options by their text, never by letter, because options are shuffled.

## Feedback already in the document

With Document feedback only or AI feedback, text labelled Feedback, Rationale or Explanation after a question is used as written in `<generalfeedback>`, wrapped in `<div class="doc-feedback">...</div>`, with no disclaimer. Do not add AI text to that `<generalfeedback>`. With AI feedback, per-option feedback for multiple choice is still written as above. With No feedback, leave it out.

## Style

- Written for students, in UK English and plain clinical language, at the level of the question.
- General feedback: 40–120 words, not counting the disclaimer. Per-option feedback: one sentence.
- Simple HTML: `<p>`, `<ul>`, `<li>`, `<strong>`.
- No greetings ("Well done!"), no mention of marks, no reference to other questions' answers.

## Disclaimer

End every feedback element that contains AI-generated text (each answer's `<feedback>` and the `<generalfeedback>`) with exactly this paragraph:

    <p><em>AI-generated feedback: this explanation was produced by artificial intelligence and may contain errors. Check it against your course materials or ask your lecturer.</em></p>

Never add it to feedback that came from the document.

## Possible key errors

If you believe a marked answer or key may be wrong, withhold all AI feedback for that question: leave `<generalfeedback>` and every answer's `<feedback>` empty, apart from any feedback from the document. List the question in the report as "Possible key error – feedback withheld", with a one-line reason. Never change the marked answer or key.
