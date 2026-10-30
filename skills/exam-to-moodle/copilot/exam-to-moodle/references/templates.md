# XML Templates

Copy these structures exactly. The comments are for guidance only; do not include them in the output.

With No feedback, every feedback element is empty, as in the multiple-response and matching examples. With AI feedback, fill them as in the single-answer MCQ and the first essay example, ending each AI-generated feedback element with the disclaimer paragraph. With Document feedback only, see "Feedback placement".

```xml
<?xml version="1.0" encoding="UTF-8"?>
<quiz>

  <!-- CATEGORY: always first, exactly once -->
  <question type="category">
    <category>
      <text>$course$/top/Nursing_Final_Exam</text>
    </category>
    <info format="html">
      <text></text>
    </info>
  </question>

  <!-- MULTIPLE CHOICE: single answer, WITH AI feedback -->
  <question type="multichoice">
    <name>
      <text>CardiovascularSystem_Q001</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p>Which organ pumps blood through the systemic circulation?</p>]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text><![CDATA[<p>The heart is the only one of these organs that pumps blood. The left ventricle contracts to eject oxygenated blood into the aorta, which carries it to the body through the systemic circulation. The kidneys, liver and lungs all receive a blood supply, but none of them generates the pressure that moves blood around the body.</p><p><em>AI-generated feedback: this explanation was produced by artificial intelligence and may contain errors. Check it against your course materials or ask your lecturer.</em></p>]]></text>
    </generalfeedback>
    <defaultgrade>1</defaultgrade>
    <penalty>0</penalty>
    <hidden>0</hidden>
    <single>true</single>
    <shuffleanswers>true</shuffleanswers>
    <answernumbering>ABCD</answernumbering>
    <showstandardinstruction>0</showstandardinstruction>
    <correctfeedback format="html"><text></text></correctfeedback>
    <partiallycorrectfeedback format="html"><text></text></partiallycorrectfeedback>
    <incorrectfeedback format="html"><text></text></incorrectfeedback>
    <answer fraction="0" format="html">
      <text><![CDATA[<p>Kidney</p>]]></text>
      <feedback format="html"><text><![CDATA[<p>Incorrect. The kidneys filter blood but do not pump it.</p><p><em>AI-generated feedback: this explanation was produced by artificial intelligence and may contain errors. Check it against your course materials or ask your lecturer.</em></p>]]></text></feedback>
    </answer>
    <answer fraction="0" format="html">
      <text><![CDATA[<p>Liver</p>]]></text>
      <feedback format="html"><text><![CDATA[<p>Incorrect. The liver processes blood from the portal circulation but has no pumping function.</p><p><em>AI-generated feedback: this explanation was produced by artificial intelligence and may contain errors. Check it against your course materials or ask your lecturer.</em></p>]]></text></feedback>
    </answer>
    <answer fraction="100" format="html">
      <text><![CDATA[<p>Heart</p>]]></text>
      <feedback format="html"><text><![CDATA[<p>Correct. The left ventricle pumps blood into the aorta and the systemic circulation.</p><p><em>AI-generated feedback: this explanation was produced by artificial intelligence and may contain errors. Check it against your course materials or ask your lecturer.</em></p>]]></text></feedback>
    </answer>
    <answer fraction="0" format="html">
      <text><![CDATA[<p>Lung</p>]]></text>
      <feedback format="html"><text><![CDATA[<p>Incorrect. The lungs are part of the pulmonary circulation and exchange gases; they do not pump blood.</p><p><em>AI-generated feedback: this explanation was produced by artificial intelligence and may contain errors. Check it against your course materials or ask your lecturer.</em></p>]]></text></feedback>
    </answer>
    <tags>
      <tag><text>Topic_Cardiovascular_System</text></tag>
      <tag><text>Task_Knowledge</text></tag>
      <tag><text>SubT_Recall</text></tag>
      <tag><text>Bloom_Remember</text></tag>
      <tag><text>Module_HB</text></tag>
    </tags>
  </question>

  <!-- MULTIPLE RESPONSE: two correct options, no feedback -->
  <question type="multichoice">
    <name>
      <text>Shock_Q002</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p>Which TWO findings are typical of hypovolaemic shock?</p>]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text></text>
    </generalfeedback>
    <defaultgrade>2</defaultgrade>
    <penalty>0</penalty>
    <hidden>0</hidden>
    <single>false</single>
    <shuffleanswers>true</shuffleanswers>
    <answernumbering>ABCD</answernumbering>
    <showstandardinstruction>0</showstandardinstruction>
    <correctfeedback format="html"><text></text></correctfeedback>
    <partiallycorrectfeedback format="html"><text></text></partiallycorrectfeedback>
    <incorrectfeedback format="html"><text></text></incorrectfeedback>
    <answer fraction="50" format="html">
      <text><![CDATA[<p>Tachycardia</p>]]></text>
      <feedback format="html"><text></text></feedback>
    </answer>
    <answer fraction="-50" format="html">
      <text><![CDATA[<p>Bradycardia</p>]]></text>
      <feedback format="html"><text></text></feedback>
    </answer>
    <answer fraction="50" format="html">
      <text><![CDATA[<p>Cool peripheries</p>]]></text>
      <feedback format="html"><text></text></feedback>
    </answer>
    <answer fraction="-50" format="html">
      <text><![CDATA[<p>Hypertension</p>]]></text>
      <feedback format="html"><text></text></feedback>
    </answer>
    <tags>
      <tag><text>Topic_Shock</text></tag>
      <tag><text>Bloom_Understand</text></tag>
      <tag><text>Module_HB</text></tag>
    </tags>
  </question>

  <!-- MATCHING: answers are plain text; a distractor has empty subquestion text; no feedback -->
  <question type="matching">
    <name>
      <text>Shock_Q003</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p>Match each type of shock with its pathophysiological description.</p>]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text></text>
    </generalfeedback>
    <defaultgrade>4</defaultgrade>
    <penalty>0</penalty>
    <hidden>0</hidden>
    <shuffleanswers>true</shuffleanswers>
    <correctfeedback format="html"><text></text></correctfeedback>
    <partiallycorrectfeedback format="html"><text></text></partiallycorrectfeedback>
    <incorrectfeedback format="html"><text></text></incorrectfeedback>
    <subquestion format="html">
      <text><![CDATA[<p>Cardiogenic shock</p>]]></text>
      <answer><text><![CDATA[Myocardial dysfunction resulting in a critical decrease in stroke volume and elevated pulmonary capillary pressure.]]></text></answer>
    </subquestion>
    <subquestion format="html">
      <text><![CDATA[<p>Obstructive shock</p>]]></text>
      <answer><text><![CDATA[Physical restriction of the great vessels or heart, severely limiting diastolic filling or systolic outflow.]]></text></answer>
    </subquestion>
    <subquestion format="html">
      <text><![CDATA[<p>Hypovolaemic shock</p>]]></text>
      <answer><text><![CDATA[Acute deficit in intravascular volume leading to inadequate ventricular end-diastolic pressure and reduced stroke volume.]]></text></answer>
    </subquestion>
    <subquestion format="html">
      <text><![CDATA[<p>Distributive shock</p>]]></text>
      <answer><text><![CDATA[Pathological reduction in systemic vascular resistance causing a functional mismatch between vascular bed and blood volume.]]></text></answer>
    </subquestion>
    <!-- distractor: an unused Column B option -->
    <subquestion format="html">
      <text></text>
      <answer><text><![CDATA[Increased cardiac output with normal tissue perfusion.]]></text></answer>
    </subquestion>
    <tags>
      <tag><text>Topic_Shock</text></tag>
      <tag><text>Task_Definition</text></tag>
      <tag><text>Bloom_Understand</text></tag>
      <tag><text>Module_HB</text></tag>
    </tags>
  </question>

  <!-- ESSAY: basic, memo in graderinfo, WITH AI feedback -->
  <question type="essay">
    <name>
      <text>Shock_Q004</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p>Describe the initial management of an adult presenting with hypovolaemic shock.</p>]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text><![CDATA[<p>A good answer follows a structured ABC approach: securing the airway and oxygenation, establishing wide-bore IV access, starting fluid resuscitation, controlling the source of loss, and monitoring the response to treatment. It should also recognise when the patient needs blood products or urgent referral, and explain how vital signs and urine output show whether resuscitation is working.</p><p><em>AI-generated feedback: this explanation was produced by artificial intelligence and may contain errors. Check it against your course materials or ask your lecturer.</em></p>]]></text>
    </generalfeedback>
    <defaultgrade>6</defaultgrade>
    <penalty>0</penalty>
    <hidden>0</hidden>
    <responseformat>editor</responseformat>
    <responserequired>1</responserequired>
    <responsefieldlines>15</responsefieldlines>
    <attachments>0</attachments>
    <attachmentsrequired>0</attachmentsrequired>
    <graderinfo format="html">
      <text><![CDATA[<ul><li>Airway and breathing assessment, high-flow oxygen (1)</li><li>Two large-bore IV cannulae (1)</li><li>Fluid resuscitation with crystalloid (1)</li><li>Identify and control the source of loss (1)</li><li>Monitor vital signs and urine output (1)</li><li>Early referral or blood products as indicated (1)</li></ul>]]></text>
    </graderinfo>
    <responsetemplate format="html">
      <text></text>
    </responsetemplate>
    <tags>
      <tag><text>Topic_Shock</text></tag>
      <tag><text>Bloom_Apply</text></tag>
      <tag><text>Module_HB</text></tag>
    </tags>
  </question>

  <!-- ESSAY WITH SETTINGS: word limits, upload, response template, rubric; no feedback -->
  <question type="essay">
    <name>
      <text>CommunityHealth_Q005</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p>Write a health education plan for a rural clinic addressing hypertension. Answer in 250–400 words and attach any supporting diagram.</p>]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text></text>
    </generalfeedback>
    <defaultgrade>10</defaultgrade>
    <penalty>0</penalty>
    <hidden>0</hidden>
    <responseformat>editor</responseformat>
    <responserequired>1</responserequired>
    <responsefieldlines>20</responsefieldlines>
    <minwordlimit>250</minwordlimit>
    <maxwordlimit>400</maxwordlimit>
    <attachments>1</attachments>
    <attachmentsrequired>0</attachmentsrequired>
    <maxbytes>0</maxbytes>
    <filetypeslist>.pdf,.docx,.jpg,.png</filetypeslist>
    <graderinfo format="html">
      <text><![CDATA[<table border="1"><thead><tr><th>Criterion</th><th>Excellent</th><th>Adequate</th><th>Poor</th></tr></thead><tbody><tr><td>Needs assessment</td><td>3</td><td>2</td><td>0–1</td></tr><tr><td>Objectives and content</td><td>4</td><td>2–3</td><td>0–1</td></tr><tr><td>Evaluation plan</td><td>3</td><td>2</td><td>0–1</td></tr></tbody></table>]]></text>
    </graderinfo>
    <responsetemplate format="html">
      <text><![CDATA[<p><strong>Target group:</strong></p><p><strong>Objectives:</strong></p><p><strong>Key messages:</strong></p><p><strong>Evaluation:</strong></p>]]></text>
    </responsetemplate>
    <tags>
      <tag><text>Topic_Community_Health</text></tag>
      <tag><text>Bloom_Create</text></tag>
      <tag><text>Module_FM</text></tag>
    </tags>
  </question>

  <!-- ESSAY: complete the table (answers stripped from template, full table in graderinfo); no feedback -->
  <question type="essay">
    <name>
      <text>Pharmacology_Q006</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p>Complete the table below for each antihypertensive drug.</p>]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text></text>
    </generalfeedback>
    <defaultgrade>4</defaultgrade>
    <penalty>0</penalty>
    <hidden>0</hidden>
    <responseformat>editor</responseformat>
    <responserequired>1</responserequired>
    <responsefieldlines>15</responsefieldlines>
    <attachments>0</attachments>
    <attachmentsrequired>0</attachmentsrequired>
    <graderinfo format="html">
      <text><![CDATA[<table border="1" style="width: 100%; border-collapse: collapse;"><thead><tr><th style="padding: 6px;">Drug</th><th style="padding: 6px;">Class</th><th style="padding: 6px;">Main adverse effect</th></tr></thead><tbody><tr><td style="padding: 6px;">Enalapril</td><td style="padding: 6px;">ACE inhibitor</td><td style="padding: 6px;">Dry cough</td></tr><tr><td style="padding: 6px;">Amlodipine</td><td style="padding: 6px;">Calcium channel blocker</td><td style="padding: 6px;">Ankle oedema</td></tr></tbody></table>]]></text>
    </graderinfo>
    <responsetemplate format="html">
      <text><![CDATA[<table border="1" style="width: 100%; border-collapse: collapse;"><thead><tr><th style="width: 28%; padding: 6px; vertical-align: top; text-align: left;">Drug</th><th style="width: 36%; padding: 6px; vertical-align: top;">Class</th><th style="width: 36%; padding: 6px; vertical-align: top;">Main adverse effect</th></tr></thead><tbody><tr><td style="padding: 6px; vertical-align: top;">Enalapril</td><td style="padding: 6px; vertical-align: top; height: 40px;">&nbsp;</td><td style="padding: 6px; vertical-align: top; height: 40px;">&nbsp;</td></tr><tr><td style="padding: 6px; vertical-align: top;">Amlodipine</td><td style="padding: 6px; vertical-align: top; height: 40px;">&nbsp;</td><td style="padding: 6px; vertical-align: top; height: 40px;">&nbsp;</td></tr></tbody></table>]]></text>
    </responsetemplate>
    <tags>
      <tag><text>Topic_Pharmacology</text></tag>
      <tag><text>Bloom_Remember</text></tag>
      <tag><text>Module_FM</text></tag>
    </tags>
  </question>

  <!-- IMAGE: images cannot be embedded in Copilot; the placeholder stays in the text, the question is listed in the report, and the user adds the image in Moodle after import -->
  <question type="essay">
    <name>
      <text>Anatomy_Q007</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p>Identify the structure shown.</p><p>[Image: labelled diagram of a structure]</p>]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text></text>
    </generalfeedback>
    <defaultgrade>1</defaultgrade>
    <penalty>0</penalty>
    <hidden>0</hidden>
    <responseformat>editor</responseformat>
    <responserequired>1</responserequired>
    <responsefieldlines>5</responsefieldlines>
    <attachments>0</attachments>
    <attachmentsrequired>0</attachmentsrequired>
    <graderinfo format="html">
      <text></text>
    </graderinfo>
    <responsetemplate format="html">
      <text></text>
    </responsetemplate>
  </question>

</quiz>
```

## Essay setting values

| Element | Values | Default |
|---|---|---|
| `<responseformat>` | `editor` (typed answer); `editorfilepicker` (typed answer with inline images); `plain` (plain text); `noinline` (upload only, no typed answer) | `editor` |
| `<responserequired>` | `1` required, `0` optional | `1` |
| `<responsefieldlines>` | 5, 10, 15, 20, 25, 30, 35, 40 (size of the answer box) | 15; use 20 if max words > 300; 30 if > 600 |
| `<minwordlimit>`, `<maxwordlimit>` | whole number, or leave out the element | not included |
| `<attachments>` | `0` none, `1`–`3` a fixed number, `-1` unlimited | `0` |
| `<attachmentsrequired>` | `0` optional, or 1 up to the number allowed | `0` |
| `<maxbytes>` | `0` uses the course limit | `0` |
| `<filetypeslist>` | comma-separated extensions, e.g. `.pdf,.docx` | empty |

Upload-only questions use `<responseformat>noinline</responseformat>`, `<responserequired>0</responserequired>`, at least `1` in `<attachments>`, and at least `1` in `<attachmentsrequired>`. Do not include word limits for upload-only questions.

Leave out `<minwordlimit>` and `<maxwordlimit>` entirely when no limit is stated; do not write `0`.

## Feedback placement

| Element | No feedback | Document feedback only | AI feedback |
|---|---|---|---|
| `<feedback>` in each multichoice `<answer>` | empty | empty | One sentence on why that option is correct or incorrect, as in `CardiovascularSystem_Q001` |
| `<generalfeedback>`, multichoice | empty | Feedback from the document, otherwise empty | The key concept, 40–120 words, as in `CardiovascularSystem_Q001` |
| `<generalfeedback>`, matching | empty | Feedback from the document, otherwise empty | Each correct pair with a short reason, as a list, 40–120 words |
| `<generalfeedback>`, essay | empty | Feedback from the document, otherwise empty | The key points a good answer covers, 40–120 words, as in `Shock_Q004` |
| `<correctfeedback>`, `<partiallycorrectfeedback>`, `<incorrectfeedback>` | empty | empty | empty |

- With AI feedback, end every feedback element that contains AI-generated text with the exact disclaimer paragraph from `SKILL.md`.
- With Document feedback only or AI feedback, feedback already in the document goes in `<generalfeedback>` as written, wrapped as `<div class="doc-feedback"><p>...</p></div>`, with no disclaimer, in place of AI general feedback. With No feedback, leave it out.
- With AI feedback, if a key error is suspected, withhold all AI feedback for that question (leave every feedback element empty, apart from any feedback from the document) and flag it in the report as a possible key error, with a one-line reason.

## Images

Images cannot be embedded. Write `<p>[Image: brief description]</p>` where the image was, as in `Anatomy_Q007`, and list the question in the report so the user can add the image in Moodle after import.