# S1 review pack

This adds ten draft candidates and source locators to the existing project. It also prepares review worksheets and a plan for the human work. It does not create student reviews or independent ratings.

## Install into the existing project

1. Stop the app with Ctrl+C.
2. Extract this ZIP.
3. Copy the entire `review_pack` folder into the existing `ntn-threat-model` folder beside `run.py`.
4. Open a terminal in the folder containing `run.py`.
5. Preview the changes:

```powershell
py -3 review_pack/apply_review.py
```

6. Read the listed actions. Then apply:

```powershell
py -3 review_pack/apply_review.py --apply
```

7. Restart:

```powershell
py -3 run.py
```

Refresh the browser with Ctrl+F5.

The importer saves a complete database backup before applying changes. It updates untouched original records and creates new records. It skips records with student ratings or completed human reviews. It also skips other edited records and reused IDs. Customized source entries stop the import for manual comparison. Customized web files are preserved.

If a record was skipped then compare it with `docs/THREAT_REVIEW.md`. Do not assume its ID still represents the proposed candidate.

## Expected starting state after a clean import

- 10 candidates with proposed F and I ratings.
- All six STRIDE categories represented.
- 0 completed student reviews.
- 0 independent student ratings.
- 0 automatically completed coverage outcomes.

The proposed scores and the six-category count do not establish research completeness. The 66-cell guide still identifies research questions.

## Read in this order

1. `docs/START_HERE.md` — how to review T-02 together.
2. `docs/ASSUMPTIONS.md` — agree on the shared descriptions and conditional control failures.
3. `docs/SOURCE_CHECKS.md` — exact source locators and remaining evidence limits.
4. `docs/BLIND_CASES.md` — shared case descriptions without proposed scores.
5. `docs/RATING_SESSION.md` — actual independent student exercise.
6. `docs/THREAT_REVIEW.md` — proposed ratings and technical changes.
7. `docs/COVERAGE_PROPOSALS.md` and `docs/SCOPE_REVIEW_PROPOSALS.md` — draft review notes.
8. `docs/SEMINAR_AND_SUBMISSION.md` — rehearsal and submission prompts.

If you already saw the proposed scores then say so in the limitations. You can still rate independently of the other student but the exercise is not fully free from prior-score anchoring.

## What remains a human task

Read and approve the cases and sources. Enter your own reviewer names and completion dates. Submit your own initial ratings without discussion. Test setup on each computer. Run the outside-person usability review. Record actual contributions. Write and check the final slides and report. Submit through the actual course workflow.

This pack provides working material rather than completed academic results. It introduces NIST control support in response to the request to verify mitigation evidence. It does not expand the S1 architecture.

## Tests

`docs/VERIFICATION.md` records the preparation checks and their limits. The pack includes a 47-second backup video at `assets/demo-updated.mp4` and a standalone snapshot at `assets/offline-viewer.html`. Test both files on the presentation computer. Rebuild the snapshot and record a new video after your own approved changes if the demonstration should show those changes.

From the project folder after copying `review_pack`:

```powershell
py -3 -m unittest discover -s review_pack/tests -v
```

The core's original tests are still run with:

```powershell
py -3 -m unittest discover -s tests -v
```

Both suites use temporary databases for synthetic student judgments.
