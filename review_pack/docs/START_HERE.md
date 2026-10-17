# Review T-02 together

Keep the record Draft while discussing it. A source locator prepared by the assistant is not a completed student review.

## 1. Agree on the threat

The attacker already has restricted management access or a write-capable identity. The failure is unauthorized configuration change. This differs from T-07 stealing an existing identity and T-08 gaining permissions that the current identity does not have.

Confirm the C3 and C4 mappings. Confirm A4 and flows F3/F5 plus TB4. F3 is affected by the changed configuration. The administration action takes place through F5.

## 2. Read the support

- R1: 3GPP TS 33.501 v18.5.0 clause 5.3.4. Printed page 34. PDF page 35.
- R8: NIST SP 800-53 Release 5.2.0 control IDs CM-3 and CM-5 plus SI-7.

R1 supports the gNB requirement for authenticated and authorized management. It does not define the complete C3 gateway implementation. R8 supports general configuration safeguards. Neither source proves your hypothetical gateway has an exploitable weakness.

The old TPM-specific claim is withdrawn from the proposal. No platform-specific design was supplied to justify it. The replacement requires approved changes and restricted write access plus checking configuration against an authorized baseline.

## 3. Decide whether the assumptions are acceptable

- Is account authentication assumed active?
- Is configuration backup assumed available?
- Is independent change approval absent or bypassable in this record?
- Does the actor have a restricted management position or account?
- Does the consequence actually compromise ground administration?

Reject or rewrite any assumption that does not belong in the agreed S1 model.

## 4. Consider the proposed rating

F2 is proposed because privileged access and a plausible control weakness are required. I4 is proposed because ground administration is compromised. The product is 8 and the band is High.

Confidence stays Low because no real deployment configuration or incident evidence was inspected. A good source for a control does not automatically establish high confidence in the hypothetical attack.

Use the shared feasibility and impact criteria to reach your own view. This is not either student's independent score.

## 5. Record the real review

After both students actually agree on the record:

1. Open T-02 and select Edit record.
2. Confirm the actor and conditions plus controls and mappings.
3. Open the cited sections. Check each source entry only after you have read and confirmed its stated support.
4. Enter the actual checker names and date for a completed source check.
5. Select Reviewed only after the technical review is complete.
6. Enter the actual joint reviewer names and the actual completion date.
7. Save.

The working names are John Nordin Saal and Marius Constantin Untaru. Their presence in this guide does not record a completed review.

## 6. Freeze before independent scoring

Complete the description review for all selected records before starting the independent exercise. A later edit creates a new revision. Earlier ratings remain in history but no longer enter current-revision comparisons.
