# Exam to Moodle

## Purpose

Exam to Moodle turns an exam or test written in Word (or saved as a PDF) into a Moodle XML file that you can import straight into a Moodle question bank. It finds the correct answers you have marked in red, reads the marks and tags for each question, and keeps your wording exactly as written. It can also add short feedback for students, either taken from your document or written by AI with a clear disclaimer.

## Supported question types and features

| Question type or feature | What the skill does |
|---|---|
| Multiple choice (one answer) | Marks the red option as correct (100%) |
| Multiple response (several answers) | Shares the marks equally across the red options and applies matching penalties to the wrong ones |
| Matching | Builds pairs from direct pairs, a table with a key column, or two lists with an answer key |
| Essay and long answer | Puts the memo or model answer in the marker's information, not in the question |
| Complete the table | Gives students the empty table and puts the completed table in the marker's information |
| MEQ (modified essay question) | Splits each sub-part with its own mark into a separate question, showing only the scenario revealed up to that point |
| Essay settings | Applies word limits, file uploads and rubrics only when your document states them |
| Marks and tags | Uses the Marks value as the question grade, and turns Topic, Task, SubT, Bloom and Module into Moodle tags |
| Question names and category | Names questions in order (for example `Pharmacology_Q001`) and places them in a category named after your file |
| Student feedback | None, feedback from your document only, or AI feedback with a disclaimer (you choose each time) |

## Differences between the Claude and Copilot versions

The two versions produce the same Moodle XML and follow the same rules for marks, tags, Bloom's levels, essay settings, scoring, feedback and question names. They differ only in the following ways.

| Area | Claude | Copilot |
|---|---|---|
| Reading documents | Reads red font directly from the Word or PDF file | Relies on `[[CORRECT]]` markers added by the Word macro (see below) |
| Images | Embeds images from Word documents in the questions | Puts a placeholder, `[Image: brief description]`, where each image was. You add the image in Moodle afterwards. |
| Checking the result | Runs a checking program on the XML, then works through a checklist | Works through the full checklist |
| Output | A downloadable `.xml` file | A file, or the XML in a code block that you copy and save as `.xml` |
| If no correct answers are found | Explains the likely cause (theme or unusual red, answers not coloured, scanned PDF) and how to fix it | Gives step-by-step Find and Replace instructions for adding `[[CORRECT]]` markers in Word |

## Preparing your exam document

### 1. Mark the correct answers in red

Colour each correct option, matching key or table answer in **red font**. Use the standard Red or Dark Red from Word's Font colour menu. Avoid theme colours and unusual shades, which may not be recognised.

### 2. Add a metadata table after each question

Put a small table directly after each question. Leave a cell empty, or write "N/A", if it does not apply.

| Marks | Topic | Task | SubT | Bloom | Module |
|---|---|---|---|---|---|
| 2 | Hypertension | Diagnosis | Investigations | Apply | FMED401 |

- **Marks** becomes the question's grade.
- **Topic, Task, SubT, Bloom** and **Module** become tags (for example `Topic_Hypertension`, `Bloom_Apply`).
- Bloom's levels are standardised, so "Application" and "Applying" both become `Bloom_Apply`.
- For essays, you may also add **Word limit**, **Upload** and **File types**.

### 3. Label essay memos

Put the memo directly after the essay question and label it **Memo**, **Model answer**, **Marking guide**, **Expected answer** or **Answer**. The memo goes to the marker only; students never see it. Text labelled **Feedback** or **Rationale** is treated as student feedback, not as a memo.

### 4. Copilot only: run the Word macro

Copilot cannot reliably see font colour, so before uploading, run this macro in Word. It adds `[[CORRECT]]` in front of every piece of red text. The skill removes these markers from the final XML.

```vba
Sub MarkCorrectAnswers()
    ' Adds [[CORRECT]] before every red text run (Red FF0000 and Dark Red C00000)
    Dim colours As Variant, c As Variant
    Dim rng As Range, count As Long
    colours = Array(RGB(255, 0, 0), RGB(192, 0, 0))

    For Each c In colours
        Set rng = ActiveDocument.Content
        With rng.Find
            .ClearFormatting
            .Text = ""
            .Font.Color = c
            .Format = True
            .Forward = True
            .Wrap = wdFindStop
            Do While .Execute
                If Not AlreadyMarked(rng) Then
                    rng.InsertBefore "[[CORRECT]]"
                    count = count + 1
                End If
                rng.Collapse wdCollapseEnd
            Loop
        End With
    Next c

    MsgBox count & " correct answer(s) marked.", vbInformation, "Exam to Moodle"
End Sub

Private Function AlreadyMarked(r As Range) As Boolean
    ' Prevents double-marking if the macro is run twice
    Dim chk As Range
    If r.Start < 11 Then Exit Function
    Set chk = ActiveDocument.Range(r.Start - 11, r.Start)
    AlreadyMarked = (chk.Text = "[[CORRECT]]") Or (Left(r.Text, 11) = "[[CORRECT]]")
End Function
```

**To install the macro (once only):**

1. In Word, press **Alt+F11** to open the macro editor.
2. In the list on the left, select **Normal**, then choose **Insert → Module**.
3. Paste the code above into the empty window, then close the editor.
4. Go to **File → Options → Quick Access Toolbar**, choose **Macros** under "Choose commands from", select **MarkCorrectAnswers**, click **Add**, then **OK**.

**To use it:** open your exam, click the new button on the Quick Access Toolbar, and check the message saying how many answers were marked. Save the document and upload it. Running the macro twice does no harm; answers already marked are skipped.

**Other shades of red:** the macro only recognises Red (FF0000) and Dark Red (C00000). If your document uses another shade, find its values by selecting the text and choosing **Font colour → More Colours → Custom**, then add it to the `colours` line. For example, for red 230, green 0, blue 0:

```vba
colours = Array(RGB(255, 0, 0), RGB(192, 0, 0), RGB(230, 0, 0))
```

The Claude version reads red font directly and does not need the macro, but it also accepts documents that have already been marked with it.

## Installing

### Copilot (Cowork)

Use either method:

- Zip the `copilot/exam-to-moodle` folder and upload the zip on the **Skills** tab in Cowork, or
- Copy the `exam-to-moodle` folder to OneDrive at `Documents/Cowork/skills/exam-to-moodle/`.

### Copilot (agent)

1. Create a new agent in Microsoft 365 Copilot.
2. Paste the contents of `copilot/agent-instructions.md` into the agent's **Instructions**.
3. Upload the four files from `copilot/exam-to-moodle/references/` as **Knowledge**. If an upload is refused, rename the file from `.md` to `.txt` and try again.

### Claude

1. Zip the `claude/exam-to-moodle` folder (the zip must contain the `exam-to-moodle` folder itself).
2. In Claude, go to **Settings → Capabilities** and make sure **Code execution** is switched on.
3. Under **Skills**, upload the zip.

## Using it

Upload your prepared document and ask, for example:

> Convert HB_Paper1.docx to Moodle XML

The skill first asks which feedback students should see:

1. **No feedback** (for exams)
2. **Only the feedback written in the document**
3. **AI-generated feedback**, with a disclaimer, plus any feedback in the document. You may attach lecture notes, guidelines or a memo for the AI to base its feedback on.

It then gives you `HB_Paper1.xml` and a short report listing:

- how many questions were converted, by type
- questions left out, and why (for example, no correct answer marked or an unsupported question type)
- questions to check (missing mark, image, uncertain type, unrecognised Bloom's level, unclear essay settings)
- the feedback option used and, with AI feedback, any questions where the marked answer may be wrong (feedback is withheld for these; the answer is never changed)

## Importing into Moodle

1. In your course, go to **Question bank → Import**.
2. Choose **Moodle XML format**, upload the `.xml` file and click **Import**.
3. Check the questions in the question bank, especially any listed in the report.

Test the import in a sandbox or practice course first, and preview a few questions before using them in a live quiz.

If you chose document or AI feedback, open the quiz settings and, under **Review options**, switch on **General feedback** and **Specific feedback**. Otherwise students will not see the feedback.

## Known limitations

- **Images:** the Claude version cannot extract images from PDFs, and the Copilot version cannot embed images at all. A placeholder is put in their place and the question is listed in the report, so that you can add the image in Moodle. With Claude, upload the Word file to keep images.
- **Shades of red:** the Copilot macro only recognises Red and Dark Red unless you add other shades (see above). Theme colours may also be missed by the Claude version.
- **Unsupported question types:** fill-in-the-blank, calculated, drag-and-drop and other types are not converted. They are listed in the report.
- **Scanned PDFs:** a PDF with no selectable text cannot be read. Use the original Word document.
- **Word limits:** minimum and maximum word limits on essays need Moodle 3.11 or later (MDL-68597). Older versions ignore them.
- **Academic judgement:** the skill does not check whether your answers are right, and AI feedback may contain errors. Always review the questions and feedback before students see them.

---

Version 1.0 / Last updated: 30 October 2026
