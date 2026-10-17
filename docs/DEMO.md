# Mid-seminar rehearsal

The supervisor specifies about 20 minutes to present and 10 minutes for questions. Both students should take part. Submit the PPTX slides and progress report as well.

## Suggested demonstration

| Time | Presenter | Action |
| --- | --- | --- |
| 0–4 min | John | Problem and scope. Trace C1 to C5 and both F5 branches |
| 4–8 min | John | Explain STRIDE and the team's F × I adaptation |
| 8–13 min | Marius | Filter C3 and Tampering. Show T-02 and export its CSV |
| 13–16 min | Marius | Show T-03 evidence gaps and the local core without an LLM |
| 16–20 min | Both | Present actual evaluation progress and remaining work |
| 20–30 min | Both | Questions and feedback |

This is a suggested division. Record actual individual work in CONTRIBUTIONS.md.

## The exact record workflow

1. Start the app and open Architecture.
2. Trace the service and feeder radio segments. Explain that the gNB is on the ground.
3. Show that F5 reaches C3 and C4. Each path crosses TB4.
4. Open Ranking method. State that the matrix and priority bands are your adaptation.
5. Open Threat catalogue. Select component C3 and STRIDE Tampering.
6. Select T-02. Show F2 × I4 = 8 and the High band.
7. Read the actor and conditions plus assumed controls. Show the assumption entry and unchecked mitigation support.
8. Export CSV and open it. Confirm T-02 is the only record.
9. Reset. Open T-03. Explain its supplied Medium confidence label and the unchecked source transfer to S1.
10. Open Coverage and Independent scoring. Present only actual completed outcomes.

## Test beforehand

- Both students run the documented setup independently.
- Run the standard-library test command.
- Disconnect Wi-Fi. Load each app page and export CSV.
- Confirm each speaker knows how to recover if the server stops.
- Save a database backup and regenerate web/backup.html after final edits.
- Test any Docker setup on both computers if you intend to use it.
- Rehearse once with a timer.

## Record the short backup video

On Windows focus the browser and press Win + Alt + R if Xbox Game Bar is available. Use your normal screen recorder otherwise. Record a one- to two-minute version of the exact workflow above. End on the evidence explanation rather than a blank page. Avoid recording passwords or unrelated windows.

Keep the recording on both computers. Play it with the internet disconnected. A silent software walkthrough can show the interface but does not replace both students' explanation.

An actual silent interface walkthrough is included as `demo-backup.mp4` in this folder. It shows the original supplied catalogue and the pending evaluation state. It contains no student voice or invented research results. Record a replacement after your source reviews or data changes.

The `screenshots` folder shows the same initial software state. `example-filtered-export.csv` is an actual C3 + Tampering export containing T-02 only.

The portable viewer at web/backup.html works by opening the file directly in a browser. It is a fixed read-only snapshot. It is useful if Python or Docker fails. Regenerate it before recording if the catalogue has changed.

## Remaining seminar work

The project package does not author full academic slides or the progress report. This follows the supervisor's instruction to limit generated figures and full slides or report content. Check all content and references yourselves. Explain any AI assistance truthfully under the course rules.
