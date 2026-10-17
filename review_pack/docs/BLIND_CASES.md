# Blind case descriptions

This shared packet omits the proposed F and I ratings. Read it with the agreed criteria. Do not discuss initial ratings until both students have submitted. The original project already exposed prior example ratings. Report that anchoring limitation honestly.

## T-01 — Spoofed pre-authentication access signalling

- **Mechanism:** A local transmitter imitates access signalling before a protected session is established. The candidate concerns disruption of attachment. Successful impersonation after mutual authentication is not claimed.
- **Actor:** External actor with suitable transmitting equipment and protocol knowledge.
- **Conditions:** Radio proximity and a suitable transmitter plus an assumed pre-authentication handling weakness. The weakness has not been demonstrated for a selected NR implementation.
- **Assumed controls:** Primary authentication and applicable signalling integrity are assumed effective after security activation. The proposed threat is limited to the earlier access stage.
- **Consequence:** The assumed effect is repeated attachment disruption for nearby users of the shared service. Subscriber keys and protected sessions are not assumed compromised.
- **Mappings:** C1 · C2 · A2 · A3 · F1 · TB1

F: ____   I: ____

Reason for F: ____

Reason for I: ____

## T-02 — NTN gateway tampering

- **Mechanism:** An insider or attacker with write-capable ground administration access changes gateway or gNB configuration through F5. The altered configuration affects the ground transport service.
- **Actor:** Insider or attacker with gateway management access.
- **Conditions:** Write-capable management access and missing or bypassed change approval or integrity checking.
- **Assumed controls:** Account authentication and recoverable configuration backups are assumed. The write workflow is assumed not to require independent approval. These are model assumptions.
- **Consequence:** Unauthorized changes compromise the selected ground administration configuration.
- **Mappings:** C3 · C4 · A4 · F3 · F5 · TB4

F: ____   I: ____

Reason for F: ____

Reason for I: ____

## T-03 — Satellite relay eavesdropping

- **Mechanism:** A passive receiver in the footprint observes radio traffic. The record concerns metadata rather than decryption of ciphertext.
- **Actor:** Passive receiver in the satellite footprint.
- **Conditions:** Radio access and specialist receiving capability for the selected signal. No decryption key is assumed available.
- **Assumed controls:** User-plane ciphering is assumed active.
- **Consequence:** Limited metadata exposure. Ciphertext is not assumed to be decrypted.
- **Mappings:** C1 · C2 · C3 · A1 · F1 · F2 · TB1 · TB2

F: ____   I: ____

Reason for F: ____

Reason for I: ____

## T-04 — 5G Core interface DoS

- **Mechanism:** An attacker floods signalling or user traffic towards the selected core path.
- **Actor:** Attacker with a path towards the core interfaces.
- **Conditions:** Access to an accepted core-facing traffic path and an assumed policing or capacity weakness. Unauthenticated traffic is not assumed able to bypass every interface control.
- **Assumed controls:** Peer protection and partial traffic policing are assumed. The candidate asks what happens when admitted traffic exceeds the selected service capacity.
- **Consequence:** Disruption affecting several users of the shared service.
- **Mappings:** C4 · C5 · A3 · F4 · TB3

F: ____   I: ____

Reason for F: ____

Reason for I: ____

## T-05 — Administration repudiation

- **Mechanism:** A privileged operator denies changes or removes selected local administration records. The modeled consequence is a limited audit gap that temporarily disrupts change verification.
- **Actor:** Administrator or attacker with stolen administration credentials.
- **Conditions:** Permission to affect local audit records and no independently protected copy for the selected change period. The local C6 history represents changes to C3 and C4.
- **Assumed controls:** Only local administration logs are assumed.
- **Consequence:** Temporary disruption of administrative investigation and change verification. Service loss and disclosure of sensitive configuration are not established by log loss alone.
- **Mappings:** C3 · C4 · C6 · A5 · F5 · TB4

F: ____   I: ____

Reason for F: ____

Reason for I: ____

## T-06 — Jamming of the service radio link

- **Mechanism:** Interference on the service radio link may disrupt the selected shared access service.
- **Actor:** Attacker with access to the relevant radio environment.
- **Conditions:** Suitable interference equipment and a suitable location.
- **Assumed controls:** Protocol authentication and payload ciphering are assumed. No validated anti-jam waveform or diverse access path is assumed.
- **Consequence:** The plan assumes disruption for several users sharing the affected service.
- **Mappings:** C1 · C2 · A3 · F1 · TB1

F: ____   I: ____

Reason for F: ____

Reason for I: ____

## T-07 — Use of stolen administration credentials

- **Mechanism:** An attacker obtains valid credentials and reaches the administration interface to change important ground configuration.
- **Actor:** Attacker holding stolen administration credentials.
- **Conditions:** Valid credentials and a reachable administration interface.
- **Assumed controls:** Password-based account authentication and a restricted management network are assumed. Independent MFA is absent in this conditional scenario.
- **Consequence:** The plan assumes important configuration changes could interrupt the selected service.
- **Mappings:** C3 · C4 · C6 · A3 · A4 · A5 · F5 · TB4

F: ____   I: ____

Reason for F: ____

Reason for I: ____

## T-08 — Elevation from limited to full management privileges

- **Mechanism:** A valid limited management identity performs a configuration action outside its assigned permissions because an authorization check is missing or incorrect.
- **Actor:** Actor with a valid low-privilege management identity.
- **Conditions:** Reachability of F5 and an assumed authorization defect. Theft of an existing full-administrator identity is not required.
- **Assumed controls:** Account authentication and named roles exist. Per-action authorization is assumed defective for the selected action.
- **Consequence:** The actor gains the ability to change protected ground administration configuration.
- **Mappings:** C3 · C4 · C6 · A4 · A5 · F5 · TB4

F: ____   I: ____

Reason for F: ____

Reason for I: ____

## T-09 — Disclosure of unprotected administration traffic

- **Mechanism:** An on-path observer reads sensitive credentials or configuration when the F5 management channel lacks effective confidentiality.
- **Actor:** Actor with on-path access to the restricted management transport.
- **Conditions:** Access to the management path plus an absent or failed protected channel. Properly functioning protected transport would prevent the stated content exposure.
- **Assumed controls:** Account authentication is assumed. Channel confidentiality is deliberately treated as a failed control for this conditional record.
- **Consequence:** Sensitive configuration or management credentials are disclosed. Subsequent takeover is not counted as an already achieved consequence.
- **Mappings:** C3 · C4 · C6 · A4 · F5 · TB4

F: ____   I: ____

Reason for F: ____

Reason for I: ____

## T-10 — Tampering with N3 user-plane transport

- **Mechanism:** An actor on the core-facing transport modifies admitted user-plane traffic when integrity protection on the selected N3 path is absent or ineffective.
- **Actor:** Actor with on-path access to the ground core-facing transport.
- **Conditions:** An on-path position and failed transport-integrity enforcement. With effective protected N3 transport the proposed modification would be rejected.
- **Assumed controls:** Peer association is assumed. Integrity protection is deliberately treated as failed for this conditional record.
- **Consequence:** Traffic integrity is lost for several users assumed to share the selected S1 core-facing path. Full core internals remain outside the model.
- **Mappings:** C4 · C5 · A1 · F4 · TB3

F: ____   I: ____

Reason for F: ____

Reason for I: ____

