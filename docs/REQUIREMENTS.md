# Requirements and source decisions

Only the three supplied PDFs and the email thread define this implementation. No new threat research or additional scientific citations were introduced.

## Order of authority

1. Latest supervisor email supplied in this request.
2. Mid-Seminar Progress Update v3 dated 16 October 2026.
3. Project plan and team charter for unchanged scope and functional requirements.

The later attack-feasibility method replaces the older likelihood wording. The later 10–15 record scoring exercise replaces the older plan's up-to-five exercise. The plan's score tie-break rules still apply.

## Traceability

| Requirement | Source | Implementation | Remaining human work |
| --- | --- | --- | --- |
| S1 bounded scenario | Plan sections 3 and 4.1 | Domain constants and Architecture screen | Confirm the diagram and assumptions |
| Six components with five assets | Plan section 4.1 and update Figure A | Validated mappings and architecture labels | Joint architecture review |
| F1–F5 and TB1–TB4 | Plan page 3 and update Figure A | Diagram includes both F5 destinations | Review interface interpretation |
| STRIDE identification | Plan section 4.2 and update section 3 | 66-cell worksheet | Record every review outcome |
| Feasibility and impact 1–4 | Update section 3 | Database validation and displayed criteria | Check rating reasons |
| Adapted matrix and bands | Latest supervisor email | Explicit label in app and offline viewer | Explain why four levels help |
| Evidence and controls plus mitigations | Update sections 3 and 5 | Structured threat editor and details | Verify direct support and applicability |
| Filters and ranked results | Plan section 4.3 | API and browser share one query path | Run on both computers |
| CSV export | Plan section 4.3 | Same filtered records and stored reasons | Check in the preferred spreadsheet app |
| Unscored records | Plan page 5 | Sorted last with explicit labels | Reassess the two plan drafts |
| 10–15 independent ratings | Update section 3 and latest email | Blind-until-paired form and immutable initial ratings | Add at least three suitable threats and perform actual ratings |
| F and I agreement separately | Update section 3 | Paired-record denominators and separate percentages | Interpret results and discuss differences |
| Agreed reasons or escalation | Update section 3 | Separate consensus records | Conduct real joint discussion |
| No LLM dependency | Plan sections 4.3 and 4.4 plus latest email | Zero-package Python core | Demonstrate offline |
| Demo participation | Latest supervisor email | Suggested roles in Demo guide | Rehearse and confirm actual responsibilities |
| Backup demonstration | Latest supervisor email | Offline viewer and recording instructions | Record a current version on your own computer |
| PPTX and progress report | Latest supervisor email | Submission reminder only | Create checked slides and report and submit both |
| Individual contributions | Email and update section 6 | Blank contribution log template | Write truthful work entries |

## Record provenance

| New ID | Supplied record | Treatment |
| --- | --- | --- |
| T-01 | Update T-01 UE-Sat link spoofing | F2 × I3 and Low confidence preserved |
| T-02 | Update T-02 NTN gateway tampering | F2 × I4 and Low confidence preserved |
| T-03 | Update T-03 Satellite relay eavesdropping | F3 × I2 and Medium confidence preserved with explicit source-check caveat |
| T-04 | Update T-04 5G Core interface DoS | F2 × I3 and Low confidence preserved |
| T-05 | Update T-05 Administration repudiation | F2 × I3 and Low confidence preserved with impact-criterion review note |
| T-06 | Plan T01 service-radio jamming | Renamed to avoid ID collision. Unscored pending F reassessment |
| T-07 | Plan T02 stolen admin credentials | Renamed to avoid ID collision. Unscored pending F reassessment |

Plan T03 passive observation overlaps update T-03. It is not counted as an additional threat.

## Evidence handling

- R1–R7 mirror the latest update's numbered references.
- Exact editions and page or section support were not supplied.
- The underlying publications were not fetched or checked.
- Imported source links are Context or Assumption entries rather than verified direct support.
- Candidate mitigation wording and its supplied reference are retained. The reference does not count as validated support.
- Medium confidence on T-03 is the supplied label. It is not a new verification result.
- The score for T-05 is preserved. Whether its consequence fits I3 needs a human review.
- No output claims a live attack succeeded or that a countermeasure was validated.

## Evaluation is intentionally unfinished

The initial database has zero completed human worksheet outcomes and zero independent ratings. It has no usability results or completed installation checks for either student. Seven threats cannot complete a 10–15 threat exercise.

The app provides the workflow. Students provide the evidence and judgments. Application tests verify software behavior. They are not the research evaluation.

## Scope remains bounded

One operator. One transparent LEO relay. One gateway and one ground gNB. Only the selected 5G Core interfaces and limited ground administration. No full core internals. No satellite command system. No orbital or RF simulation. No live attacks. No LLM training.
