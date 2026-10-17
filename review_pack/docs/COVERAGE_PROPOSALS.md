# Proposed notes for all 66 STRIDE cells

These are working notes. No student outcome is completed. The importer does not copy them into the coverage-results table. Some cells remain research questions. Do not turn those into no-threat outcomes merely to reach 66.

| Unit | STRIDE | Proposed outcome | Candidates | Reason |
| --- | --- | --- | --- | --- |
| C1 | Spoofing | Proposed link | T-01 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C1 | Tampering | Research question — pending | — | Could user-side state or transmitted data be changed before endpoint protection? Define the in-scope UE state and a separate mechanism before claiming this cell is closed. |
| C1 | Repudiation | Proposed no separate threat identified | — | The bounded UE model has no selected administrative action history. User content authorship and full UE application auditing are outside the chosen workflow. |
| C1 | Information Disclosure | Proposed link | T-03 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C1 | Denial of Service | Proposed link | T-06 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C1 | Elevation of Privilege | Proposed no separate threat identified | — | The selected UE has no modeled operating-system roles or privilege transition. Revisit if UE software internals are introduced. |
| C2 | Spoofing | Proposed link | T-01 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C2 | Tampering | Proposed no separate threat identified | — | C2 is a transparent relay. Onboard configuration and command-system changes are excluded. Transit integrity questions are kept on the radio-flow review rather than claiming a modeled onboard mutation path. |
| C2 | Repudiation | Proposed no separate threat identified | — | No in-scope administrative action or audit store is assigned to the transparent relay. |
| C2 | Information Disclosure | Proposed link | T-03 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C2 | Denial of Service | Proposed link | T-06 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C2 | Elevation of Privilege | Proposed no separate threat identified | — | C2 has no modeled software authorization role. Regenerative payloads and satellite command systems are excluded. |
| C3 | Spoofing | Proposed link | T-07 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C3 | Tampering | Proposed link | T-02 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C3 | Repudiation | Proposed link | T-05 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C3 | Information Disclosure | Proposed link | T-03 / T-09 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C3 | Denial of Service | Research question — pending | — | Check gateway resource exhaustion separately from service-radio jamming and core-facing overload. Its capacities and transport implementation are unknown. |
| C3 | Elevation of Privilege | Proposed link | T-08 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C4 | Spoofing | Proposed link | T-07 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C4 | Tampering | Proposed link | T-02 / T-10 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C4 | Repudiation | Proposed link | T-05 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C4 | Information Disclosure | Proposed link | T-09 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C4 | Denial of Service | Proposed link | T-04 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C4 | Elevation of Privilege | Proposed link | T-08 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C5 | Spoofing | Research question — pending | — | Consider impersonation of an authorized core-facing peer. Establish identity and credential assumptions. T-10 concerns traffic integrity and is not automatically a peer-spoofing record. |
| C5 | Tampering | Proposed link | T-10 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C5 | Repudiation | Proposed no separate threat identified | — | C5 represents N2/N3 interfaces. Full core administration and its action history are excluded. Revisit if interface-level accountability becomes a selected asset. |
| C5 | Information Disclosure | Research question — pending | — | Consider core-facing transport disclosure separately from T-10 tampering. Define the failed confidentiality control and scope of exposed data. |
| C5 | Denial of Service | Proposed link | T-04 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C5 | Elevation of Privilege | Proposed no separate threat identified | — | Core privilege-management internals are excluded. Interface data handling alone is not a modeled core administrator role transition. |
| C6 | Spoofing | Proposed link | T-07 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C6 | Tampering | Research question — pending | — | Decide whether local C6 tools or stored configuration can be altered. This is different from changing C3/C4 through an otherwise legitimate administrator. |
| C6 | Repudiation | Proposed link | T-05 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C6 | Information Disclosure | Proposed link | T-09 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| C6 | Denial of Service | Research question — pending | — | Determine the consequence of losing the administration endpoint while the access service continues. Add an administration-availability candidate if justified. |
| C6 | Elevation of Privilege | Proposed link | T-08 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| F1 | Spoofing | Proposed link | T-01 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| F1 | Tampering | Research question — pending | — | Specify whether an on-path radio manipulation could survive the assumed endpoint integrity checks. Do not infer plaintext modification merely from exposed radio signals. |
| F1 | Repudiation | Proposed no separate threat identified | — | This flow does not store an administrative action history. Accountability is assessed at the selected administration endpoints. Revisit if independent message-receipt evidence becomes an explicit requirement. |
| F1 | Information Disclosure | Proposed link | T-03 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| F1 | Denial of Service | Proposed link | T-06 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| F1 | Elevation of Privilege | Proposed no separate threat identified | — | The flow itself makes no authorization decision. Privilege transitions belong to its endpoints. This does not rule out endpoint authorization defects. |
| F2 | Spoofing | Proposed no separate threat identified | — | No separately authenticated feeder-source identity is defined in this transparent-relay model. This is a scope interpretation for student approval. Revisit when a feeder identity or control protocol is specified. |
| F2 | Tampering | Research question — pending | — | Assess feeder-segment modification with the stated endpoint protections. No independent unprotected feeder protocol has been specified. |
| F2 | Repudiation | Proposed no separate threat identified | — | This flow does not store an administrative action history. Accountability is assessed at the selected administration endpoints. Revisit if independent message-receipt evidence becomes an explicit requirement. |
| F2 | Information Disclosure | Proposed link | T-03 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| F2 | Denial of Service | Research question — pending | — | Feeder interference is distinct from T-06 service-radio interference. The location and victim differ. Add a justified separate candidate if it belongs in the final catalogue. |
| F2 | Elevation of Privilege | Proposed no separate threat identified | — | The flow itself makes no authorization decision. Privilege transitions belong to its endpoints. This does not rule out endpoint authorization defects. |
| F3 | Spoofing | Proposed no separate threat identified | — | No separately identified F3 application principal is selected. The transport technology is unspecified. Revisit rather than claiming immunity if F3 peer authentication is introduced. |
| F3 | Tampering | Proposed link | T-02 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| F3 | Repudiation | Proposed no separate threat identified | — | This flow does not store an administrative action history. Accountability is assessed at the selected administration endpoints. Revisit if independent message-receipt evidence becomes an explicit requirement. |
| F3 | Information Disclosure | Research question — pending | — | First define the ground-transport technology and its confidentiality boundary. Project F3 must not be assumed to be the standardized split-gNB F1 interface. |
| F3 | Denial of Service | Research question — pending | — | Define how ground transport fails or saturates and who can reach it. Current interface-capacity assumptions do not establish this case. |
| F3 | Elevation of Privilege | Proposed no separate threat identified | — | The flow itself makes no authorization decision. Privilege transitions belong to its endpoints. This does not rule out endpoint authorization defects. |
| F4 | Spoofing | Research question — pending | — | Consider unauthorized core-facing peer identity separately from a payload-integrity failure. Keep N2 and N3 requirements distinct where necessary. |
| F4 | Tampering | Proposed link | T-10 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| F4 | Repudiation | Proposed no separate threat identified | — | This flow does not store an administrative action history. Accountability is assessed at the selected administration endpoints. Revisit if independent message-receipt evidence becomes an explicit requirement. |
| F4 | Information Disclosure | Research question — pending | — | Consider confidentiality failure on the selected N3 or N2 transport. T-10 is a Tampering record rather than a completed disclosure analysis. |
| F4 | Denial of Service | Proposed link | T-04 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| F4 | Elevation of Privilege | Proposed no separate threat identified | — | The flow itself makes no authorization decision. Privilege transitions belong to its endpoints. This does not rule out endpoint authorization defects. |
| F5 | Spoofing | Proposed link | T-07 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| F5 | Tampering | Proposed link | T-02 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| F5 | Repudiation | Proposed link | T-05 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| F5 | Information Disclosure | Proposed link | T-09 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |
| F5 | Denial of Service | Research question — pending | — | Define the availability consequence of losing management transport. Avoid reusing the core-traffic DoS record without a matching mechanism. |
| F5 | Elevation of Privilege | Proposed link | T-08 | The listed candidate explicitly maps to this architecture unit and STRIDE category. Check its conditions and evidence before recording a human outcome. |

After joint review use the app’s worksheet to record a matching link or a justified no-applicable-threat outcome. Enter the actual reviewer names and actual date. Research-question cells stay Pending until the missing analysis is done.
