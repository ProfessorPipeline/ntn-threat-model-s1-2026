# Source checks and limits

Assistant source inspection date: 17 October 2026. This date is not a student review date. Student validation remains pending.

The source preparation adds locators and corrects unsupported attributions. It does not turn hypothetical S1 conditions into observed attacks. All proposed case confidence levels remain Low.

## R1 — 3GPP TS 33.501

Pinned edition: v18.5.0 Release 18. ETSI TS 133 501 V18.5.0 dated May 2024.

[Official PDF](https://www.etsi.org/deliver/etsi_ts/133500_133599/133501/18.05.00_60/ts_133501v180500p.pdf)

| Locator | Use in this pack | Limit |
| --- | --- | --- |
| 5.1.2 — printed p.30 / PDF p.31 | Authentication context for T-01 | Does not establish the proposed early-stage exploit |
| 5.3.2 — printed p.33 / PDF p.34 | UE-to-gNB ciphering context for T-03 | Does not establish metadata recoverability for the chosen radio profile |
| 5.3.3 — printed p.33 / PDF p.34 | Signalling-integrity context for T-01 | Does not say every access message is a digital signature |
| 5.3.4 — printed p.34 / PDF p.35 | Management controls for T-02 and T-07 to T-09 | Applies directly to the gNB. Equivalent gateway controls are project proposals |
| 9.1.2 and 9.3 — printed pp.155–156 / PDF pp.156–157 | N3 protection context for T-10 | Interpret the operator-choice and physically secure environment notes |
| 9.2 and 9.3 — printed p.156 / PDF p.157 | Core-facing interface context for T-04 | Does not establish saturation thresholds or a bypass |

Section numbers are the main locators. The PDF page count includes the cover. Check the printed page header when comparing editions.

## R2 — 3GPP TR 38.821

[ETSI work-item record for v16.2.0](https://portal.etsi.org/webapp/workprogram/Report_WorkItem.asp?WKI_ID=68417)

Title and edition metadata were located. The full report could not be retrieved in this session. No exact report section or page was verified. The bounded S1 diagram remains the supplied project Figure A. Students still need to complete the primary architecture-source check.

## R3 — Pavur et al.

[Author-hosted paper](https://www.cs.ox.ac.uk/files/11922/Pavur%20et%20al%20A%20tale%20of%20sea%20and%20sky.pdf)

Sections III.B and IV.A on author-PDF pages 3–4 describe the maritime platform and collection setup. The paper concerns GEO maritime VSAT and DVB-S2. It provides context for exposed satellite radio traffic. It does not establish the cost or capability of a receiver for S1 NR LEO signals. The T-03 commodity-receiver claim and Medium case-confidence label were therefore not retained in the proposal.

## R4 — Shostack

The bibliography entry is retained from the supplied update. The full book and page-level support were not checked. Do not cite it as specific support for TPM deployment or operational satellite countermeasures. It remains a general threat-modeling reference.

## R5 — Ansong et al.

[Publisher DOI](https://doi.org/10.1016/j.cose.2024.104156)

Publisher-deposited Crossref metadata confirms the full title and authors plus the 2025 volume 149 article 104156 entry. Full-text matrix details were not verified in this session. The supervisor's supplied instruction already says the article uses a different matrix. State that the project's four-level matrix and bands are its own adaptation.

## R6 — Frøseth et al.

[Publisher DOI](https://doi.org/10.1007/978-3-031-82349-7_26)

Publisher-deposited metadata confirms the chapter title and authors plus pages 403–424 in the ESORICS 2024 International Workshops volume published in 2025. Full-text methodology and threat evidence were not verified. Do not invent a section locator or claim that the chapter directly validates a specific S1 attack.

## R7 — Suomalainen et al.

[Institution-hosted final paper](https://cris.vtt.fi/ws/portalfiles/portal/106665346/j.future.2024.107500.pdf)

Section 3.1 is on article pages 5–6 and PDF pages 6–7. It uses an 11-member Delphi panel with three rounds and five-level survey scales. This supports discussion of structured group judgment. It is not the same experiment as two students independently selecting four-level F and I ratings. Describe the project exercise as a small adaptation.

## R8 — NIST SP 800-53

[Official publication page](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)

[Official OSCAL catalog](https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json)

The inspected electronic catalog identifies Release 5.2.0 and last-modified metadata dated 11 May 2026. Its exact control IDs are used as locators. A canonical-content fingerprint is in data/source-check-metadata.json. The source URL is maintained upstream so later downloads can differ.

| Proposed use | Exact control locator |
| --- | --- |
| Configuration writes and integrity | CM-3 / CM-5 / SI-7 |
| Audit evidence and protected copies | AU-9 / AU-9(2) / AU-9(3) / AU-10 / AU-12 |
| Privileged credentials | IA-2(1) / IA-5 / AC-6 |
| Authorization checks | AC-3 / AC-6 |
| DoS handling and monitoring | SC-5 / SI-4 |
| Traffic protection | SC-8 |
| Wireless interference concern | SC-40 / SC-40(1) |

These controls support candidate safeguards. Selecting controls for S1 is a design inference. They do not show that an S1 attack occurred or that a proposed countermeasure was successfully deployed. SC-40(1) concerns anti-jam waveform protection. Do not present ordinary payload encryption alone as an anti-jamming demonstration.

## Practical source-review rule

For each record separate the source-supported control from the assumed weakness and consequence. Open the exact locator. Mark a student source check only after confirming that the note accurately describes the source. Record the actual checker and completion date.
