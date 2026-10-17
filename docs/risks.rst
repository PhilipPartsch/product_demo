.. _full-risks:

Risks
=====

Risks found during the engineering workflow, recorded by the ``record-risk``
skill (template ``.agents/templates/risk.rst``). Each risk links the needs it
affects and, once mitigated, the needs that mitigate it.

.. risk:: Lockout used to block legitimate users
   :id: RISK_LOCKOUT_DOS
   :status: accepted
   :affects: REQ_LOCKOUT[fp=="39fbc2f42b58d4db6d21a0e9cbcb3d4128dcb2fc6e30d27ae86f0ad93704771e"], SPEC_LOCKOUT[fp=="ca1c72cdf17d6d7c2a50cf1a94c368807d04a4d9425d76c89f93db735898119b"]
   :risk_category: security
   :severity: medium
   :likelihood: medium
   :safety_relevant: false
   :security_relevant: true

   **Cause**

   Anyone who knows an account name can send 5 wrong passwords on purpose.

   **Effect**

   The legitimate user cannot log in for 15 minutes; repeated, the account
   stays unusable.

   **Mitigation**

   Accepted by DEC_REQ_LOCKOUT_LIMITS: the lock is time-limited (15
   minutes) instead of permanent, which bounds the damage of each abuse.

.. risk:: Lockout state lost on restart
   :id: RISK_LOCKOUT_RESTART
   :status: accepted
   :affects: SPEC_LOCKOUT[fp=="ca1c72cdf17d6d7c2a50cf1a94c368807d04a4d9425d76c89f93db735898119b"]
   :risk_category: security
   :severity: low
   :likelihood: low
   :safety_relevant: false
   :security_relevant: true

   **Cause**

   Counters and locks are kept in memory only.

   **Effect**

   A restart ends all locks, so an attacker who can cause a restart gets 5
   new guesses.

   **Mitigation**

   Accepted by DEC_LOCKOUT_STATE until the product has a persistent store;
   a restart is not under the attacker's control in the current setup.

.. risk:: Audit records lost on restart
   :id: RISK_AUDIT_VOLATILE
   :status: accepted
   :affects: SPEC_AUDIT[fp=="346a0a0f9a26825d58a833e102253b992bc3da075150e44f01bb06875974620b"], REQ_LOG[fp=="b4fce8e953ca7ed87708ee948641b646833a56aa668efc09b264313e6767d648"]
   :risk_category: technical
   :severity: medium
   :likelihood: high
   :safety_relevant: false
   :security_relevant: true

   **Cause**

   The audit log lives in memory.

   **Effect**

   Every restart deletes the audit trail, so older login attempts cannot be
   investigated.

   **Mitigation**

   Accepted by DEC_AUDIT_FORMAT for the demo product; persisting the log is
   the next change when the product needs a durable trail.

.. risk:: Lockout values chosen by the authoring agent
   :id: RISK_AI_LOCKOUT_VALUES
   :status: closed
   :affects: REQ_LOCKOUT[fp=="39fbc2f42b58d4db6d21a0e9cbcb3d4128dcb2fc6e30d27ae86f0ad93704771e"]
   :mitigated_by: DEC_REQ_LOCKOUT_LIMITS[fp=="9db1ee4f5b85eb7f550079e36d67a8070786028b19f4b5ab8a71f7b3f2ad2c47"]
   :risk_category: ai-workflow
   :severity: medium
   :likelihood: medium
   :safety_relevant: false
   :security_relevant: true

   **Cause**

   The pilot ran without a stakeholder in the loop; the AI agent chose the
   failure limit (5) and the lock duration (15 minutes).

   **Effect**

   The values may not fit the users' needs or the organisation's security
   policy.

   **Mitigation**

   The values and their alternatives are recorded in DEC_REQ_LOCKOUT_LIMITS,
   and the decision is part of the pilot's HTML review by the user, who
   confirms or changes them. Confirmed by the user at the pilot review
   (plan 001 P8, 2026-10-17): 5 failures, 15 minutes.
