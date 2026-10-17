.. _full-reqs:

Requirements
============

.. req:: User authentication
   :id: REQ_AUTH
   :platform_note: Built for <{ var.platform }>
   :satisfies: US_LOGIN
   :safety_relevant: false
   :security_relevant: true

   The system shall authenticate users before granting access.
   ``platform_note`` embeds variant data.

   .. dec:: No anonymous access
      :id: DEC_REQ_AUTH_NO_ANONYMOUS
      :status: accepted
      :safety_relevant: false
      :security_relevant: true

      **Context**

      Some products allow parts to be used without logging in.

      **Alternatives**

      An anonymous read-only mode — would need a second access policy.

      **Consequences**

      Every access requires authentication; there is no public part.

      **Rationale**

      Mandatory authentication is chosen because the product holds only
      personal account data.

.. req:: Audit logging
   :id: REQ_LOG
   :satisfies: US_AUDIT
   :safety_relevant: false
   :security_relevant: true

   The system shall record an audit trail of authentication events.

   .. dec:: Record successful and failed attempts
      :id: DEC_REQ_LOG_ALL_ATTEMPTS
      :status: accepted
      :safety_relevant: false
      :security_relevant: true

      **Context**

      The audit trail could record failures only, or every attempt.

      **Alternatives**

      Failures only — a successful login by an attacker would leave no
      trace.

      **Consequences**

      Every login attempt produces one record, so the trail grows with use.

      **Rationale**

      Recording every attempt is chosen because a successful attack must be
      traceable.

.. req:: Account lockout after failed logins
   :id: REQ_LOCKOUT
   :satisfies: US_LOCKOUT
   :safety_relevant: false
   :security_relevant: true

   The system shall reject every login attempt for an account during 15
   minutes after 5 consecutive failed login attempts for that account.

   .. dec:: Lock for 15 minutes after 5 failures
      :id: DEC_REQ_LOCKOUT_LIMITS
      :status: accepted
      :decides: REQ_LOCKOUT, RISK_LOCKOUT_DOS
      :safety_relevant: false
      :security_relevant: true

      **Context**

      The lockout needs a failure limit and a lock duration that slow down
      guessing without locking legitimate users out for long.

      **Alternatives**

      3 failures, permanent lock until an administrator unlocks — too easy
      to abuse against legitimate users. Increasing delay per failure —
      harder to explain and to test.

      **Consequences**

      At most 5 guesses per 15 minutes and account (480 per day). An
      attacker can still lock a known account for 15 minutes at a time; this
      is accepted (RISK_LOCKOUT_DOS).

      **Rationale**

      5 failures and 15 minutes are chosen because they are a common,
      time-limited setting that bounds both guessing and lockout abuse.
