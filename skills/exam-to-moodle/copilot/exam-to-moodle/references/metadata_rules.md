# Metadata Rules

## Where metadata comes from

Metadata is usually a small table immediately after the question, but may be key–value lines ("Marks: 2") or a mix. Use this order of preference:

1. the metadata table
2. key–value lines
3. the question heading, for marks only, e.g. "Question 3 (4 marks)"

Never take metadata from a different question.

## Field labels

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

## Mapping

- Mark → `<defaultgrade>`. Use the number only ("3 marks" becomes 3). Decimals are allowed. If the mark is a range or text, use 1 and flag it.
- Topic, Task, SubT, Bloom and Module → tags.
- Do not create a tag for Mark.

## Essay settings mapping

These fields apply to essay questions only and never become tags.

- Words: "300" → `<maxwordlimit>300</maxwordlimit>`; "250–400" → `<minwordlimit>250</minwordlimit>` and `<maxwordlimit>400</maxwordlimit>`; "at least 200" → `<minwordlimit>200</minwordlimit>`.
- Upload: "Yes" or "1" → `<attachments>1</attachments>`; a number → that number; "unlimited" → `-1`. When the document requires an upload, set `<attachmentsrequired>` to the same number (use 1 if unlimited).
- FileTypes: write as a comma-separated list of extensions with dots: "PDF or Word" → `.pdf,.docx`; "image" → `.jpg,.png`. Leave empty if not stated.

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

## Example

Input:

    Marks: 1
    Topic: Shock
    Task: Definition
    Bloom's: Understanding
    SubT: -
    Module: HB

Output:

    <defaultgrade>1</defaultgrade>
    <tags>
      <tag><text>Topic_Shock</text></tag>
      <tag><text>Task_Definition</text></tag>
      <tag><text>Bloom_Understand</text></tag>
      <tag><text>Module_HB</text></tag>
    </tags>