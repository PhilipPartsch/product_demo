.. _full-arch:

Architecture
============

Architecture elements allocate the requirements to components and
interfaces. Each element fulfills the requirements it is responsible for and
states whether it sits on a trust boundary; specifications refine the
elements.

.. mermaid::

   flowchart TD
       ARCH_AUTH_SERVICE["Authentication Service"]
       ARCH_LOCKOUT_GUARD["Login Lockout Guard"]
       ARCH_AUDIT_LOGGER["Audit Logger"]
       ARCH_AUTH_SERVICE -->|uses| ARCH_LOCKOUT_GUARD
       ARCH_AUTH_SERVICE -->|uses| ARCH_AUDIT_LOGGER

.. arch:: Authentication Service
   :id: ARCH_AUTH_SERVICE
   :fulfills: REQ_AUTH
   :trust_boundary: true
   :safety_relevant: false
   :security_relevant: true

   **Responsibility**

   Authenticates a user before access is granted: it checks a submitted
   account name and password against the stored, salted hash
   (``SPEC_HASH``) and reports success or failure. It consults the Login
   Lockout Guard before checking and records every attempt in the Audit
   Logger.

   **Interfaces**

   - Offers a login check: account name and password in, success or
     failure out.
   - Uses the Login Lockout Guard (``ARCH_LOCKOUT_GUARD``): is the account
     locked, record a failure or a success.
   - Uses the Audit Logger (``ARCH_AUDIT_LOGGER``): record the attempt.

   **Boundary**

   The account name and password come from outside the product; this is the
   only element where they enter. The password is never stored or compared
   in plain text — only its salted hash is kept and compared in constant
   time — and a locked account is rejected before the password is checked.

   .. dec:: Accept the known security gaps of the demo product
      :id: DEC_ARCH_ACCEPT_DEMO_GAPS
      :status: accepted
      :decides: ARCH_AUTH_SERVICE, RISK_AUTH_TRANSPORT, RISK_LOCKOUT_RACE, RISK_LOCKOUT_ENUM, RISK_AUDIT_READ_UNGUARDED
      :safety_relevant: false
      :security_relevant: true

      **Context**

      The architecture review found four security gaps: no required
      transport encryption, a possible race on the failure counter, account
      enumeration through the lockout response, and an unguarded audit read
      interface. The product content is test data that will be removed
      later (plan 002, user).

      **Alternatives**

      Mitigate each gap with new requirements and specifications — effort on
      content that will be removed. Keep the risks open — blocks every
      release (CI 2).

      **Consequences**

      The four risks are accepted for the demo product and stay documented;
      a real product would have to mitigate them, starting with the
      transport encryption (high severity).

      **Rationale**

      Accepting is chosen because the content is throwaway test data; the
      user delegated content decisions (plan 002).

.. arch:: Login Lockout Guard
   :id: ARCH_LOCKOUT_GUARD
   :fulfills: REQ_LOCKOUT
   :trust_boundary: false
   :safety_relevant: false
   :security_relevant: true

   **Responsibility**

   The Login Lockout Guard is the component responsible for enforcing the
   per-account lockout required by ``REQ_LOCKOUT``: it keeps a
   consecutive-failed-attempt counter and a lock-until timestamp for each
   account, and is the sole place that decides whether an account is
   currently locked out. The Authentication Service consults the Guard
   before it checks a submitted credential and reports every failed or
   successful check back to the Guard; while an account is locked out, the
   Authentication Service rejects the login attempt without checking the
   credential, as ``REQ_LOCKOUT`` requires.

   **Interfaces**

   - An internal "check lockout" interface, called by the Authentication
     Service before it checks credentials, that accepts an account
     identifier and returns whether that account is currently locked out.
   - An internal "record failed attempt" interface, called by the
     Authentication Service after a failed credential check, that
     increments the account's consecutive-failure counter and, once the
     counter reaches 5, locks the account until 15 minutes after that
     failure (``DEC_REQ_LOCKOUT_LIMITS``).
   - An internal "record success" interface, called by the Authentication
     Service after a successful credential check, that resets the
     account's consecutive-failure counter, so that only *consecutive*
     failures count towards a lockout.

   None of these interfaces is reachable directly from outside the
   product; the untrusted account identifier and credential already cross
   the trust boundary at the Authentication Service's login interface
   (``ARCH_AUTH_SERVICE``), which is the sole caller of the Guard.

   .. dec:: Separate the Login Lockout Guard from the Authentication Service
      :id: DEC_ARCH_LOCKOUT_SEPARATION
      :status: accepted
      :safety_relevant: false
      :security_relevant: true

      **Context**

      ``REQ_LOCKOUT`` needs a place to track each account's consecutive
      failed-attempt counter and lock-until time, in addition to the
      credential check the Authentication Service already performs.

      **Alternatives**

      Add the counter and lock-until timestamp directly to the
      Authentication Service (``ARCH_AUTH_SERVICE``) instead of a separate
      component — keeps a single component, but mixes credential
      verification with failure-tracking and lockout state, and makes it
      harder to change or reuse the lockout policy on its own.

      **Consequences**

      The Authentication Service calls the Guard's internal interfaces
      instead of tracking failures itself; changing the lockout policy
      (limits, duration, storage) touches only the Guard, not the
      Authentication Service.

      **Rationale**

      A separate Guard is chosen because it keeps credential verification
      and lockout enforcement as two distinct responsibilities, matching
      the one-responsibility-per-element principle this architecture
      already follows for the Authentication Service.

.. arch:: Audit Logger
   :id: ARCH_AUDIT_LOGGER
   :fulfills: REQ_LOG
   :trust_boundary: false
   :safety_relevant: false
   :security_relevant: true

   **Responsibility**

   The Audit Logger is the component responsible for recording the audit
   trail required by ``REQ_LOG``: it appends one structured record for
   every login attempt the Authentication Service completes, whether the
   credential check succeeded or failed (``DEC_REQ_LOG_ALL_ATTEMPTS``), and
   it is the sole place the trail is written to or read from
   (``SPEC_AUDIT``).

   **Interfaces**

   - An internal "record attempt" interface, called by the Authentication
     Service after every login attempt, that accepts the account
     identifier, the outcome (success or failure) and a timestamp, and
     appends a new, immutable record to the audit trail.
   - An internal "read trail" interface that returns the recorded entries
     in the order they were appended, for an administrator investigating
     suspicious activity (``US_AUDIT``).

   Neither interface is reachable directly from outside the product; the
   untrusted account identifier already crosses the trust boundary at the
   Authentication Service's login interface (``ARCH_AUTH_SERVICE``), which
   is the sole caller of the "record attempt" interface.

   .. dec:: Separate the Audit Logger from the Authentication Service
      :id: DEC_ARCH_AUDIT_SEPARATION
      :status: accepted
      :safety_relevant: false
      :security_relevant: true

      **Context**

      ``REQ_LOG`` needs a place to store and later read one record per
      login attempt, in addition to the credential check the
      Authentication Service already performs.

      **Alternatives**

      Record attempts directly inside the Authentication Service instead
      of a separate component — keeps a single component, but mixes
      credential verification with the audit record's format and storage
      (``SPEC_AUDIT``), and makes it harder to change the log's format or
      storage without touching authentication logic.

      **Consequences**

      The Authentication Service calls the Audit Logger's "record
      attempt" interface after every attempt instead of writing records
      itself; changing the record format or storage
      (``DEC_AUDIT_FORMAT``) touches only the Audit Logger.

      **Rationale**

      A separate Audit Logger is chosen because it keeps credential
      verification and audit recording as two distinct responsibilities,
      matching the one-responsibility-per-element principle this
      architecture already follows for the Login Lockout Guard
      (``DEC_ARCH_LOCKOUT_SEPARATION``).
