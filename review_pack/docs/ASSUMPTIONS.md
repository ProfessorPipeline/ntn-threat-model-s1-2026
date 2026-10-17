# Shared S1 assumptions to approve

The architecture remains the supplied bounded static scenario. These proposed assumptions make the candidate records explicit. They need joint student approval.

- C2 is a transparent relay. It does not become the ground gNB or terminate a new onboard core function.
- F1 and F2 are physical portions of the same access path. UE-to-gNB protection is considered at the logical endpoints.
- Project flow ID F1 means service radio. It is not the standardized split-gNB F1-C/F1-U interface.
- One representative UE uses a shared service. Several-user consequences are explicit assumptions rather than measured beam coverage.
- Full core administration and satellite command systems remain excluded.
- No live exploit or RF test was performed.

## Base controls and conditional failures

R1 documents intended security controls. A threat record that studies a failed control must state that failure. It must not claim that a compliant deployment normally exposes that weakness.

T-01 concerns an assumed early access-stage weakness. It does not claim successful impersonation after mutual authentication.

T-02 assumes a write-control weakness despite account authentication and backups.

T-03 assumes ciphering active. It concerns limited observable metadata. Maritime DVB-S2 results do not establish NR LEO receiver capability.

T-04 assumes an accepted traffic path and insufficient policing for the modeled load. No bypass of every peer control is assumed.

T-05 explicitly limits the consequence to a partial audit-history gap and temporary administration disruption. This is the reason for the proposed I2. Reassess if irreversible or wider damage is included.

T-06 assumes local interference can disrupt several nearby users. It does not assume an operator-wide satellite outage.

T-07 assumes compromised write-capable credentials and no independent second factor.

T-08 assumes a specific authorization defect despite account authentication.

T-09 assumes failed management-channel protection. Properly protected transport prevents the stated content disclosure.

T-10 assumes ineffective N3 integrity enforcement and several affected users. The standard permits an operator decision about cryptographic use within a physically secure environment. Lack of an IPsec tunnel alone does not demonstrate a violation or attack path.

## Meaning of the proposed scores

The scores compare the conditional scenarios under their stated control state. They do not estimate how often a control fails. If your agreed exercise instead assumes every control works fully then remove or rescore the failed-control cases before freezing the packet.

All scenario confidence labels are Low because the deployment details and attack outcomes are unobserved. This is separate from confidence that a cited control exists.

T-07 and T-08 can lead to the T-02 consequence. T-09 can support credential compromise. They represent different mechanisms and controls. Do not sum their priority scores or treat them as statistically independent events.
