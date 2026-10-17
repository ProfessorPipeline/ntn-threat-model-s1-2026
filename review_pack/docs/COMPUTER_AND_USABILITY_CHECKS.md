# Checks requiring real participants

## John’s computer

From the project folder run:

```powershell
py -3 review_pack/check_local_setup.py --student John
```

## Marius’s computer

Run on Marius’s actual computer:

```powershell
py -3 review_pack/check_local_setup.py --student Marius
```

Each command starts the real entry point on a local temporary port. It checks the model and record count plus filters and CSV values. It saves a dated JSON result under review_pack/results. It does not create research judgments or claim manual playback checks.

If a candidate import was skipped then inspect the report before interpreting the catalogue-size check. Keep both students' genuine outputs as reproducibility evidence.

## Manual offline and backup checks

On each presentation computer:

1. Start the normal app.
2. Disconnect Wi-Fi.
3. Open Architecture and Threat catalogue.
4. Filter C3 and Tampering.
5. Export CSV and open it. Confirm selected IDs and score reasons.
6. Stop the server.
7. Open web/backup.html directly in the browser.
8. Filter the offline viewer and export its selected CSV.
9. Play the updated backup video from a local file.
10. Record the actual result and date below.

| Manual task | John’s actual result and date | Marius’s actual result and date |
| --- | --- | --- |
| Live core with Wi-Fi disconnected | | |
| Selected CSV opened correctly | | |
| Offline viewer opened without server | | |
| Offline export worked | | |
| Local video played | | |
| Blocking problem and fix | | |

The included fixed viewer and video show draft proposals. Regenerate the viewer and record a replacement after final student edits. Test Docker separately only if you intend to use it.

## Outside-person usability check

Ask one person outside the team to attempt these tasks without step-by-step coaching. Observe rather than completing the tasks for them. Record help if it is needed.

| Task | Completed? | Error or help needed | Interface change |
| --- | --- | --- | --- |
| Find and view S1 architecture | | | |
| Filter a chosen component and STRIDE category | | | |
| Find a rating reason and a source or assumption | | | |
| Export the selected records | | | |

Participant label: ______

Actual test date: ______

Observer: ______

The criterion is no blocking issue for these four tasks. Report unsuccessful tasks and fixes. One participant gives limited usability evidence and is not a broad user study.
