.. _full-risks:

Risks
=====

Risks found during the engineering workflow, recorded by the ``record-risk``
skill (template ``.agents/templates/risk.rst``). Each risk links the needs it
affects and, once mitigated, the needs that mitigate it.

.. risk:: Lockout used to block legitimate users
   :id: RISK_LOCKOUT_DOS
   :status: accepted
   :affects: REQ_LOCKOUT[fp=="39fbc2f42b58d4db6d21a0e9cbcb3d4128dcb2fc6e30d27ae86f0ad93704771e"], SPEC_LOCKOUT[fp=="a364470eb1bb5ccece2b4ec99251caeee4a8e73ba5d2dc0333e6d13955ffb680"]
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
   :affects: SPEC_LOCKOUT[fp=="a364470eb1bb5ccece2b4ec99251caeee4a8e73ba5d2dc0333e6d13955ffb680"]
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
   :affects: SPEC_AUDIT[fp=="e3b5575dc924185b52ba6916878ca9bad2f24f4f5fb6f3cc80d7048af8629658"], REQ_LOG[fp=="b4fce8e953ca7ed87708ee948641b646833a56aa668efc09b264313e6767d648"]
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

.. risk:: Credentials cross the boundary without an architected transport protection
   :id: RISK_AUTH_TRANSPORT
   :status: accepted
   :affects: ARCH_AUTH_SERVICE[fp=="170654dd2dacc645da876a29367cc2e0034eab741afeb1888a651769d5bfb333"]
   :risk_category: security
   :severity: high
   :likelihood: medium
   :safety_relevant: false
   :security_relevant: true

   **Cause**

   Neither REQ_AUTH nor ARCH_AUTH_SERVICE requires that the channel
   carrying the account name and password is encrypted (e.g. TLS); the
   architecture element only says the password is checked against a stored
   hash.

   **Effect**

   An attacker positioned on the network path between the client and the
   service can read a submitted password in transit and log in as the user,
   bypassing the authentication the service otherwise enforces.

   **Mitigation**

   Not yet mitigated. A future specification or deployment requirement
   should mandate an encrypted transport (e.g. TLS) for every request that
   carries the login credential.

.. risk:: Concurrent login attempts can race the failure counter
   :id: RISK_LOCKOUT_RACE
   :status: accepted
   :affects: ARCH_LOCKOUT_GUARD[fp=="f43185c0d69b59c01de9b8bb4b5f736d6d8dcd104bbf2686e47b61619e2dd569"]
   :risk_category: security
   :severity: medium
   :likelihood: low
   :safety_relevant: false
   :security_relevant: true

   **Cause**

   The "record failed attempt" interface increments a per-account counter
   and checks it against the 5-failure threshold; the architecture does
   not specify that this read-increment-compare sequence is atomic across
   concurrent calls.

   **Effect**

   Two failed login attempts for the same account arriving at nearly the
   same time could each read the counter before either write is applied,
   under-counting the burst and letting more than 5 guesses through
   before the account locks, weakening the limit REQ_LOCKOUT guarantees.

   **Mitigation**

   Not yet mitigated. A future specification should require the counter
   increment and the lock-threshold check to execute as a single atomic
   operation (e.g. a per-account lock or an atomic compare-and-increment).

.. risk:: Lockout response can reveal whether an account exists
   :id: RISK_LOCKOUT_ENUM
   :status: accepted
   :affects: ARCH_LOCKOUT_GUARD[fp=="f43185c0d69b59c01de9b8bb4b5f736d6d8dcd104bbf2686e47b61619e2dd569"]
   :risk_category: security
   :severity: low
   :likelihood: medium
   :safety_relevant: false
   :security_relevant: true

   **Cause**

   The Guard's "check lockout" interface lets the Authentication Service
   distinguish a locked-out account from one that is simply rejected for a
   wrong credential; neither ``REQ_LOCKOUT`` nor this architecture element
   requires the two outcomes to look identical to the caller.

   **Effect**

   An attacker who sends 5 wrong passwords for a guessed account name and
   then observes whether the next attempt is reported as "locked" instead
   of "invalid credentials" can tell that the account exists, even without
   ever guessing its password.

   **Mitigation**

   Not yet mitigated. A future specification should require the login
   interface to return the same outward response for a locked-out account
   and for one rejected on a wrong credential.

.. risk:: Audit trail read interface has no defined caller or access control
   :id: RISK_AUDIT_READ_UNGUARDED
   :status: accepted
   :affects: ARCH_AUDIT_LOGGER[fp=="f3d0dee37fbcf08a1007eaf93900d05351b8f2a40c86f4fffe40655cff16c17f"]
   :risk_category: security
   :severity: medium
   :likelihood: medium
   :safety_relevant: false
   :security_relevant: true

   **Cause**

   ARCH_AUDIT_LOGGER's internal "read trail" interface is not restricted
   to a specific, authenticated caller; the architecture names the
   administrator use case (``US_AUDIT``) but does not allocate who is
   allowed to invoke the interface or how that caller is authenticated.

   **Effect**

   Any component or process able to reach the internal interface could
   read the full audit trail, including every account identifier and
   outcome it contains, without being the intended administrator.

   **Mitigation**

   Not yet mitigated at the architecture level. When the system gains an
   administrative interface or role, restrict the "read trail" interface
   to it and record the decision that allocates that access control.
