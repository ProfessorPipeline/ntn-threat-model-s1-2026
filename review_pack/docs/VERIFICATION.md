# Preparation checks

Date: 17 October 2026.

These checks were performed by the assistant in an isolated Linux copy of the supplied project. They do not count as either student's work or a test on either student's computer.

## Completed software checks

- All 13 review-pack tests passed. They cover preview and backup behaviour plus safe import and preservation of existing edits and student judgments.
- The local setup checker passed all 12 automated checks with the caller label Buildcheck. Startup and API responses worked. Combined filters matched the stored mappings. CSV export retained the selected records and their ratings and reasons. Score products and worksheet sizes were consistent. The database backup endpoint returned a valid SQLite database.
- A headless browser exercised the updated desktop app and a narrow phone layout. It showed ten draft candidates and six represented STRIDE categories. The T-02 mitigation and clickable source links appeared. Filtering for Elevation of Privilege worked. Ten independent-scoring forms were present with no student scores. All coverage outcomes stayed pending. No page errors were observed.
- The standalone offline snapshot opened in the local browser check.
- An actual local UI recording was created. It is 47 seconds long at 1440 by 900 pixels. The MP4 uses H.264 video. It demonstrates the updated candidate catalogue and supporting views. It is not a record of a student presentation or an attack experiment.
- The isolated database had ten candidates and zero completed human reviews. It had zero independent student ratings and zero completed coverage outcomes. SQLite integrity checking returned ok.

## Still pending

- Installation and browser checks on John's actual computer.
- Installation and browser checks on Marius's actual computer.
- Playback of the backup video on the presentation computer.
- Opening the offline snapshot after disabling the presentation computer's network connection.
- The outside-person usability exercise.
- A timed rehearsal with both students taking part.
- Docker startup. No Docker execution claim is made.
- Student verification of the source locators and conditional attack assumptions.

The proposed ratings are qualitative model judgments. No RF experiment or live exploitation was performed. No full-text support is claimed where SOURCE_CHECKS.md records an access limit. Prepared worksheet notes do not complete the 66-cell review.
