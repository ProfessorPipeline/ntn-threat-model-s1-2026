# Software verification

Build checked on 17 October 2026 with Python 3.12.14 on Linux.

## Automated application checks

13 tests passed using `python -m unittest discover -s tests -v`.

The checks cover source provenance and empty evaluation data plus the specified score order. They test all 16 matrix positions and filter intersections. They check that CSV values and selected IDs match the query. They reject invalid mappings and sources plus invalid ratings or review fields.

They also test persistence and stale-edit conflicts. Initial ratings stay hidden until paired and cannot be overwritten. Agreement uses only complete current-revision pairs. Old ratings remain in history. Consensus and escalation do not silently change catalogue scores.

Coverage checks require matching mappings and human reasons. Editing a linked threat resets its affected review outcomes. New matching candidates invalidate an earlier no-threat outcome. SQLite backups reopen with a successful integrity check. HTTP checks cover asset routes and local write restrictions.

All synthetic test judgments stay in temporary databases. The delivered database contains seven candidate records and zero independent ratings or completed human reviews.

## Browser workflow checks

Chromium headless browser checks passed at a 1440 × 1000 desktop viewport and a 390 × 844 phone viewport.

- Loaded all seven application screens without page errors.
- Filtered C3 + Tampering and downloaded a CSV containing T-02 only.
- Confirmed the no-results state.
- Loaded the architecture image and all 16 matrix cells.
- Confirmed all 66 worksheet cells and saved a valid review outcome.
- Submitted a temporary John's rating and confirmed it stayed hidden from Marius.
- Submitted a second rating and recorded a discussion outcome.
- Edited a record and checked its new revision.
- Created a temporary candidate through the full editor.
- Checked the phone layout for horizontal page overflow.
- Opened the portable viewer through a file URL and filtered it without a server.
- Downloaded the portable viewer's CSV with complete evidence and reasons.

The backup video shows real interface states from a separate clean temporary database. It performs no evaluation writes.

## Limits of these checks

Docker was unavailable and has not been run here. Neither student's computer was available. Windows startup is documented but still needs a local check. Screen recording and video playback should be rehearsed on the actual presentation computers.

The software checks do not verify the scientific references or threat mechanisms. They do not count as the independent scoring exercise or usability study. Those are separate human tasks recorded in EVALUATION.md.
