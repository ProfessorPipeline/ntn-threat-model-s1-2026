# Ten draft threat records for joint review

Prepared on 17 October 2026 with AI assistance. These are technical proposals. They are not student reviews or independent student scores.

Use BLIND_CASES.md before reading these score proposals if you have not yet rated independently. Freeze the descriptions and assumptions first. Do not copy these proposed ratings into both students’ initial forms.

| ID | Proposed F | Proposed I | Priority | Change |
| --- | --- | --- | --- | --- |
| T-01 | 2 | 3 | 6 Medium | Narrowed to pre-authentication disruption. No successful authenticated impersonation claim. |
| T-02 | 2 | 4 | 8 High | TPM claim replaced with supported change controls. |
| T-03 | 2 | 2 | 4 Medium | F3 to F2 and Medium to Low confidence. VSAT results do not validate NR equipment. |
| T-04 | 2 | 3 | 6 Medium | Accepted-path and capacity assumptions made explicit. |
| T-05 | 2 | 2 | 4 Medium | I3 to I2 for explicitly limited temporary administration disruption. |
| T-06 | 2 | 3 | 6 Medium | New F2 / I3 proposal using the latest feasibility criteria. |
| T-07 | 2 | 4 | 8 High | New F2 / I4 proposal with explicit MFA assumption. |
| T-08 | 2 | 4 | 8 High | New limited-account authorization failure candidate. |
| T-09 | 2 | 3 | 6 Medium | New conditional management-channel disclosure candidate. |
| T-10 | 2 | 3 | 6 Medium | New conditional N3 integrity-failure candidate. |

## T-01 — Spoofed pre-authentication access signalling

STRIDE: Spoofing. Proposed F2 × I3 = 6 Medium. Scenario confidence: Low. Review status: Draft.

- **Mechanism:** A local transmitter imitates access signalling before a protected session is established. The candidate concerns disruption of attachment. Successful impersonation after mutual authentication is not claimed.
- **Actor:** External actor with suitable transmitting equipment and protocol knowledge.
- **Conditions:** Radio proximity and a suitable transmitter plus an assumed pre-authentication handling weakness. The weakness has not been demonstrated for a selected NR implementation.
- **Assumed controls:** Primary authentication and applicable signalling integrity are assumed effective after security activation. The proposed threat is limited to the earlier access stage.
- **Consequence:** The assumed effect is repeated attachment disruption for nearby users of the shared service. Subscriber keys and protected sessions are not assumed compromised.
- **F reason:** F2 is a conditional estimate because specialist radio access and an unconfirmed pre-authentication weakness are required. It is not evidence of a practical bypass.
- **I reason:** I3 assumes several nearby users of the shared service experience attachment disruption. If only one UE is affected then this score must be reduced.
- **Mappings:** C1 · C2 · A2 · A3 · F1 · TB1
- **Review change:** Narrowed to pre-authentication disruption. No successful authenticated impersonation claim.

Evidence and assumptions:

- R1 — v18.5.0 clause 5.1.2; printed p.30 / PDF p.31; clause 5.3.3; printed p.33 / PDF p.34. Authentication and signalling-protection context. The source does not establish the hypothesized pre-authentication exploit. Assistant-assisted source preparation dated 17 October 2026. Student source check is still pending.
- Assumption — S1 record-specific assumption. The selected pre-authentication weakness and the several-user effect are hypotheses for review. Reject or leave unscored if neither student can justify this conditional path.

Candidate mitigations:

- Apply primary authentication and the required signalling integrity checks. Review handling of unprotected access messages. R1: Clauses 5.1.2 and 5.3.3. The standard supports authentication and integrity controls. It does not say that every access request is digitally signed. Exact pre-authentication mitigation remains implementation-dependent.

Student decision: ______

Reviewer names: ______

Actual completion date: ______


## T-02 — NTN gateway tampering

STRIDE: Tampering. Proposed F2 × I4 = 8 High. Scenario confidence: Low. Review status: Draft.

- **Mechanism:** An insider or attacker with write-capable ground administration access changes gateway or gNB configuration through F5. The altered configuration affects the ground transport service.
- **Actor:** Insider or attacker with gateway management access.
- **Conditions:** Write-capable management access and missing or bypassed change approval or integrity checking.
- **Assumed controls:** Account authentication and recoverable configuration backups are assumed. The write workflow is assumed not to require independent approval. These are model assumptions.
- **Consequence:** Unauthorized changes compromise the selected ground administration configuration.
- **F reason:** F2 because a restricted management position or privileged account plus a plausible control weakness is required.
- **I reason:** I4 because the defined consequence is compromise of ground administration. This directly matches the severe-impact criterion.
- **Mappings:** C3 · C4 · A4 · F3 · F5 · TB4
- **Review change:** TPM claim replaced with supported change controls.

Evidence and assumptions:

- R1 — v18.5.0 clause 5.3.4; printed p.34 / PDF p.35. Direct requirement context for authenticated and authorized gNB configuration. Applying an equivalent control to the modeled gateway is a project design choice. Assistant-assisted source preparation dated 17 October 2026. Student source check is still pending.
- R8 — Release 5.2.0 control IDs CM-3 and CM-5 plus SI-7. General support for change governance and integrity monitoring. These controls do not prove that this gateway is vulnerable. Assistant-assisted source preparation dated 17 October 2026. Student source check is still pending.
- Assumption — S1 record-specific assumption. The actual gateway management software and its approval workflow are not known. Authorized configuration integrity can fail under the stated scenario.

Candidate mitigations:

- Require approved changes and restrict configuration writes. Compare critical configuration against an authorized baseline and retain change records. R8: CM-3; CM-5; SI-7. The previous TPM-specific proposal is withdrawn because its support and platform design were not established. Generic integrity checking is not a claim that a TPM checks arbitrary runtime gateway configuration.
- Authenticate and authorize gNB management changes and protect the O&M channel. R1: Clause 5.3.4; printed p.34 / PDF p.35. The normative requirement applies to C4. Extension to C3 is a stated S1 control proposal.

Student decision: ______

Reviewer names: ______

Actual completion date: ______


## T-03 — Satellite relay eavesdropping

STRIDE: Information Disclosure. Proposed F2 × I2 = 4 Medium. Scenario confidence: Low. Review status: Draft.

- **Mechanism:** A passive receiver in the footprint observes radio traffic. The record concerns metadata rather than decryption of ciphertext.
- **Actor:** Passive receiver in the satellite footprint.
- **Conditions:** Radio access and specialist receiving capability for the selected signal. No decryption key is assumed available.
- **Assumed controls:** User-plane ciphering is assumed active.
- **Consequence:** Limited metadata exposure. Ciphertext is not assumed to be decrypted.
- **F reason:** F2 is proposed because the selected NR signal and suitable receiver are unspecified. The maritime DVB-S2 equipment result is not enough to justify a commodity NR receiver claim.
- **I reason:** I2 for limited visible traffic-pattern metadata under the assumed active ciphering. No plaintext recovery is assumed.
- **Mappings:** C1 · C2 · C3 · A1 · F1 · F2 · TB1 · TB2
- **Review change:** F3 to F2 and Medium to Low confidence. VSAT results do not validate NR equipment.

Evidence and assumptions:

- R1 — v18.5.0 clause 5.3.2; printed p.33 / PDF p.34. The standard describes UE-to-gNB ciphering. Activation is policy-dependent. This record explicitly assumes ciphering is active. Assistant-assisted source preparation dated 17 October 2026. Student source check is still pending.
- R3 — Sections III.B and IV.A; author PDF pp.3–4. Observed maritime VSAT results use GEO and DVB-S2. They motivate exposure concerns but are not direct evidence for this NR LEO case. Assistant-assisted source preparation dated 17 October 2026. Student source check is still pending.
- Assumption — S1 record-specific assumption. Which metadata the selected NR receiver can recover is not established. The proposed impact is limited to observable patterns.

Candidate mitigations:

- Keep applicable access ciphering enabled and use end-to-end protection for sensitive application data. Review metadata exposure separately. R1: Clause 5.3.2. The 3GPP clause supports access ciphering. End-to-end protection is an additional project recommendation. Payload encryption does not hide every traffic pattern. The unsupported frequency-hopping claim is removed.

Student decision: ______

Reviewer names: ______

Actual completion date: ______


## T-04 — 5G Core interface DoS

STRIDE: Denial of Service. Proposed F2 × I3 = 6 Medium. Scenario confidence: Low. Review status: Draft.

- **Mechanism:** An attacker floods signalling or user traffic towards the selected core path.
- **Actor:** Attacker with a path towards the core interfaces.
- **Conditions:** Access to an accepted core-facing traffic path and an assumed policing or capacity weakness. Unauthenticated traffic is not assumed able to bypass every interface control.
- **Assumed controls:** Peer protection and partial traffic policing are assumed. The candidate asks what happens when admitted traffic exceeds the selected service capacity.
- **Consequence:** Disruption affecting several users of the shared service.
- **F reason:** F2 because the actor needs a privileged or otherwise accepted route into the selected core-facing path plus a policing weakness.
- **I reason:** I3 assumes temporary degradation for several users sharing S1. It does not claim sustained operator-wide failure.
- **Mappings:** C4 · C5 · A3 · F4 · TB3
- **Review change:** Accepted-path and capacity assumptions made explicit.

Evidence and assumptions:

- R1 — v18.5.0 clauses 9.2 and 9.3; printed p.156 / PDF p.157. Defines the selected N2 and N3 protection context. It does not establish a flood path or capacity threshold. Assistant-assisted source preparation dated 17 October 2026. Student source check is still pending.
- R8 — Release 5.2.0 control IDs SC-5 and SI-4. General support for traffic-related DoS controls and monitoring. Assistant-assisted source preparation dated 17 October 2026. Student source check is still pending.
- Assumption — S1 record-specific assumption. The accepted traffic path and saturation condition are scenario hypotheses. No traffic-volume test was run.

Candidate mitigations:

- Apply ingress traffic policing and monitor abnormal load at the relevant ground and core-facing interfaces. R8: SC-5; SI-4. Choose actual thresholds from the deployment. Protecting radio capacity and protecting core transport capacity are different tasks.

Student decision: ______

Reviewer names: ______

Actual completion date: ______


## T-05 — Administration repudiation

STRIDE: Repudiation. Proposed F2 × I2 = 4 Medium. Scenario confidence: Low. Review status: Draft.

- **Mechanism:** A privileged operator denies changes or removes selected local administration records. The modeled consequence is a limited audit gap that temporarily disrupts change verification.
- **Actor:** Administrator or attacker with stolen administration credentials.
- **Conditions:** Permission to affect local audit records and no independently protected copy for the selected change period. The local C6 history represents changes to C3 and C4.
- **Assumed controls:** Only local administration logs are assumed.
- **Consequence:** Temporary disruption of administrative investigation and change verification. Service loss and disclosure of sensitive configuration are not established by log loss alone.
- **F reason:** F2 because privileged access to the relevant local records is required.
- **I reason:** I2 is proposed for the explicitly limited and temporary disruption of administration work. The old I3 reason did not establish several-user service loss or sensitive-data exposure.
- **Mappings:** C3 · C4 · C6 · A5 · F5 · TB4
- **Review change:** I3 to I2 for explicitly limited temporary administration disruption.

Evidence and assumptions:

- R8 — Release 5.2.0 control IDs AU-9; AU-9(2); AU-9(3); AU-10; AU-12. Supports protecting action evidence and placing protected records outside the affected component. It does not quantify the S1 consequence. Assistant-assisted source preparation dated 17 October 2026. Student source check is still pending.
- Assumption — S1 record-specific assumption. Only the selected local change-history interval is affected. Temporary administrative disruption is the consequence used for I2. Reassess if broader irreversible loss is part of the agreed scenario.

Candidate mitigations:

- Keep protected remote audit copies with integrity protection and limit who can alter logging. Record attributable administrative actions. R8: AU-9; AU-9(2); AU-9(3); AU-10; AU-12. An append-only implementation or signed records may realize these aims. Neither was implemented or tested in the selected NTN system.

Student decision: ______

Reviewer names: ______

Actual completion date: ______


## T-06 — Jamming of the service radio link

STRIDE: Denial of Service. Proposed F2 × I3 = 6 Medium. Scenario confidence: Low. Review status: Draft.

- **Mechanism:** Interference on the service radio link may disrupt the selected shared access service.
- **Actor:** Attacker with access to the relevant radio environment.
- **Conditions:** Suitable interference equipment and a suitable location.
- **Assumed controls:** Protocol authentication and payload ciphering are assumed. No validated anti-jam waveform or diverse access path is assumed.
- **Consequence:** The plan assumes disruption for several users sharing the affected service.
- **F reason:** F2 because suitable interference equipment and access to the relevant local radio environment are required. Power and range are not estimated.
- **I reason:** I3 assumes several nearby users sharing the affected service experience temporary radio-access disruption. A one-UE-only effect would justify a lower impact.
- **Mappings:** C1 · C2 · A3 · F1 · TB1
- **Review change:** New F2 / I3 proposal using the latest feasibility criteria.

Evidence and assumptions:

- R8 — Release 5.2.0 controls SC-40 and SC-40(1). Identifies hostile wireless signal interference as a control concern. It does not quantify feasibility for this LEO radio profile. Assistant-assisted source preparation dated 17 October 2026. Student source check is still pending.
- P1 — Project plan pp.5–6. The original jamming candidate and its local-access assumptions. Its old likelihood rating has been reassessed rather than relabelled.
- Assumption — S1 record-specific assumption. Interference reaches nearby users of the modeled shared service. No operator-wide satellite outage is assumed.

Candidate mitigations:

- Assess compatible interference protection and monitoring plus an alternate service path. Confirm any radio countermeasure against the actual NR profile. R8: SC-40; SC-40(1). The cited enhancement discusses anti-jam waveform protection. Ordinary user-payload encryption alone is not an anti-jamming result. Profile compatibility remains unverified.

Student decision: ______

Reviewer names: ______

Actual completion date: ______


## T-07 — Use of stolen administration credentials

STRIDE: Spoofing. Proposed F2 × I4 = 8 High. Scenario confidence: Low. Review status: Draft.

- **Mechanism:** An attacker obtains valid credentials and reaches the administration interface to change important ground configuration.
- **Actor:** Attacker holding stolen administration credentials.
- **Conditions:** Valid credentials and a reachable administration interface.
- **Assumed controls:** Password-based account authentication and a restricted management network are assumed. Independent MFA is absent in this conditional scenario.
- **Consequence:** The plan assumes important configuration changes could interrupt the selected service.
- **F reason:** F2 because both compromised privileged credentials and a reachable restricted management interface are required. The scenario assumes no independent second factor.
- **I reason:** I4 because use of the stolen write-capable identity compromises selected ground administration.
- **Mappings:** C3 · C4 · C6 · A3 · A4 · A5 · F5 · TB4
- **Review change:** New F2 / I4 proposal with explicit MFA assumption.

Evidence and assumptions:

- R1 — v18.5.0 clause 5.3.4; printed p.34 / PDF p.35. Management authentication and authorization context for the gNB. Assistant-assisted source preparation dated 17 October 2026. Student source check is still pending.
- R8 — Release 5.2.0 control IDs IA-2(1); IA-5; AC-6. Supports stronger privileged authentication and credential handling. It does not prove credential theft has occurred. Assistant-assisted source preparation dated 17 October 2026. Student source check is still pending.
- Assumption — S1 record-specific assumption. A write-capable account is compromised and the actor can reach F5. No second factor prevents replay in this scenario.

Candidate mitigations:

- Use independent MFA for privileged accounts and revoke compromised authenticators. Limit each management identity to necessary permissions. R8: IA-2(1); IA-5; AC-6. Candidate design control only. No mitigation was deployed or tested in S1.

Student decision: ______

Reviewer names: ______

Actual completion date: ______


## T-08 — Elevation from limited to full management privileges

STRIDE: Elevation of Privilege. Proposed F2 × I4 = 8 High. Scenario confidence: Low. Review status: Draft.

- **Mechanism:** A valid limited management identity performs a configuration action outside its assigned permissions because an authorization check is missing or incorrect.
- **Actor:** Actor with a valid low-privilege management identity.
- **Conditions:** Reachability of F5 and an assumed authorization defect. Theft of an existing full-administrator identity is not required.
- **Assumed controls:** Account authentication and named roles exist. Per-action authorization is assumed defective for the selected action.
- **Consequence:** The actor gains the ability to change protected ground administration configuration.
- **F reason:** F2 because restricted management access and an unconfirmed authorization weakness are required.
- **I reason:** I4 because the conditional result is compromise of ground administration.
- **Mappings:** C3 · C4 · C6 · A4 · A5 · F5 · TB4
- **Review change:** New limited-account authorization failure candidate.

Evidence and assumptions:

- R1 — v18.5.0 clause 5.3.4; printed p.34 / PDF p.35. Configuration actions need authorization. A compliant check would block the proposed escalation. Assistant-assisted source preparation dated 17 October 2026. Student source check is still pending.
- R8 — Release 5.2.0 controls AC-3 and AC-6. Supports the separation between identifying an account and restricting its permissions. Assistant-assisted source preparation dated 17 October 2026. Student source check is still pending.
- Assumption — S1 record-specific assumption. A specific per-action authorization defect is postulated. Its existence has not been demonstrated.

Candidate mitigations:

- Enforce authorization for every management action and restrict each role to its required capabilities. Test denied operations as well as allowed ones. R8: AC-3; AC-6. Candidate design control only. No mitigation was deployed or tested in S1.

Student decision: ______

Reviewer names: ______

Actual completion date: ______


## T-09 — Disclosure of unprotected administration traffic

STRIDE: Information Disclosure. Proposed F2 × I3 = 6 Medium. Scenario confidence: Low. Review status: Draft.

- **Mechanism:** An on-path observer reads sensitive credentials or configuration when the F5 management channel lacks effective confidentiality.
- **Actor:** Actor with on-path access to the restricted management transport.
- **Conditions:** Access to the management path plus an absent or failed protected channel. Properly functioning protected transport would prevent the stated content exposure.
- **Assumed controls:** Account authentication is assumed. Channel confidentiality is deliberately treated as a failed control for this conditional record.
- **Consequence:** Sensitive configuration or management credentials are disclosed. Subsequent takeover is not counted as an already achieved consequence.
- **F reason:** F2 because a restricted on-path position and a channel-protection failure are required.
- **I reason:** I3 because the stated consequence is exposure of sensitive configuration or credentials. It does not assume completed administration takeover.
- **Mappings:** C3 · C4 · C6 · A4 · F5 · TB4
- **Review change:** New conditional management-channel disclosure candidate.

Evidence and assumptions:

- R1 — v18.5.0 clause 5.3.4; printed p.34 / PDF p.35. Protected gNB O&M communications are required. This is a failed-control scenario rather than a claim about a compliant deployment. Assistant-assisted source preparation dated 17 October 2026. Student source check is still pending.
- R8 — Release 5.2.0 control SC-8. Supports protection of data while it crosses a channel. Assistant-assisted source preparation dated 17 October 2026. Student source check is still pending.
- Assumption — S1 record-specific assumption. F5 carries sensitive management content and its protection fails. No such failure was observed.

Candidate mitigations:

- Protect the management channel with authenticated transport encryption and validate its peer identity and policy. Reject unprotected fallback. R1: Clause 5.3.4; printed p.34 / PDF p.35. The clause gives the gNB protection requirement. The equivalent gateway policy is an S1 proposal.

Student decision: ______

Reviewer names: ______

Actual completion date: ______


## T-10 — Tampering with N3 user-plane transport

STRIDE: Tampering. Proposed F2 × I3 = 6 Medium. Scenario confidence: Low. Review status: Draft.

- **Mechanism:** An actor on the core-facing transport modifies admitted user-plane traffic when integrity protection on the selected N3 path is absent or ineffective.
- **Actor:** Actor with on-path access to the ground core-facing transport.
- **Conditions:** An on-path position and failed transport-integrity enforcement. With effective protected N3 transport the proposed modification would be rejected.
- **Assumed controls:** Peer association is assumed. Integrity protection is deliberately treated as failed for this conditional record.
- **Consequence:** Traffic integrity is lost for several users assumed to share the selected S1 core-facing path. Full core internals remain outside the model.
- **F reason:** F2 because restricted transport access and a failed protection control are both required.
- **I reason:** I3 assumes several users of the shared service are affected by modified traffic. It does not assume an operator-wide or sustained outage.
- **Mappings:** C4 · C5 · A1 · F4 · TB3
- **Review change:** New conditional N3 integrity-failure candidate.

Evidence and assumptions:

- R1 — v18.5.0 clauses 9.1.2 and 9.3; printed pp.155–156 / PDF pp.156–157. Documents N3 transport protection and the implementation profile. The source does not claim the selected deployment has failed protection. Assistant-assisted source preparation dated 17 October 2026. Student source check is still pending.
- Assumption — S1 record-specific assumption. The attacker has the stated position and protected transport does not enforce integrity. Several users share the affected path. These are control-failure and shared-service assumptions.

Candidate mitigations:

- Apply the selected N3 protection policy and verify integrity and replay rejection. Use the required IPsec/IKE profile where cryptographic transport protection is selected. R1: Clauses 9.1.2 and 9.3; printed pp.155–156 / PDF pp.156–157. The specification also allows an operator decision about cryptographic use and a physically secured environment. Absence of an IPsec tunnel alone does not prove noncompliance or an exploitable path.

Student decision: ______

Reviewer names: ______

Actual completion date: ______

