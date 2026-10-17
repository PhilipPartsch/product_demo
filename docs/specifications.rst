.. _full-specs:

Specifications
==============

.. spec:: Password hashing
   :id: SPEC_HASH
   :refines: REQ_AUTH
   :safety_relevant: false
   :security_relevant: true

   Passwords shall be stored using a salted, memory-hard hash: a fresh
   random salt of 16 bytes per password, stored together with the hash as
   ``<salt hex>$<hash hex>``. Verification recomputes the hash with the stored
   salt and compares in constant time.

   .. dec:: Use scrypt with N=2^14, r=8, p=1
      :id: DEC_HASH_ALGO
      :status: accepted
      :safety_relevant: false
      :security_relevant: true

      **Context**

      A memory-hard, salted password hash is required; the product uses only
      the Python standard library.

      **Alternatives**

      bcrypt — not memory-hard and not in the standard library. Argon2id —
      the recommended choice, but needs a third-party package.

      **Consequences**

      Hashes cost 16 MiB of memory each; a 16-byte random salt is stored
      with the hash. Changing the parameters later needs a rehash on login.

      **Rationale**

      scrypt is chosen because it is memory-hard and part of the standard
      library (hashlib).

.. spec:: Structured audit records
   :id: SPEC_AUDIT
   :refines: REQ_LOG
   :safety_relevant: false
   :security_relevant: true

   Each audit record shall be a structured, append-only entry with the
   fields ``timestamp`` (UTC, ISO 8601), ``user``, ``event`` and ``success``
   (true / false). Records can be appended and read, never changed or
   deleted; they are returned in the order they were appended.

   .. dec:: JSON lines in memory
      :id: DEC_AUDIT_FORMAT
      :status: accepted
      :decides: SPEC_AUDIT, RISK_AUDIT_VOLATILE
      :safety_relevant: false
      :security_relevant: true

      **Context**

      Audit records need a format and a place to live.

      **Alternatives**

      A database — durable, but adds a dependency. Plain text lines — not
      structured.

      **Consequences**

      Records are JSON objects appended in memory; they are lost on restart
      (accepted, RISK_AUDIT_VOLATILE).

      **Rationale**

      In-memory JSON lines are chosen because they are structured, append-
      only and need no dependency.

.. spec:: Failed-login counter with lockout window
   :id: SPEC_LOCKOUT
   :refines: REQ_LOCKOUT
   :safety_relevant: false
   :security_relevant: true

   A login guard keeps, per account name, the number of consecutive failed
   login attempts and the time until which the account is locked:

   - before a password is checked, an attempt for a locked account is
     rejected (the password is not checked);
   - a failed attempt increments the counter; the 5th consecutive failure
     locks the account for 900 seconds and resets the counter;
   - a successful attempt resets the counter;
   - the lock ends when 900 seconds have passed;
   - the time source is passed in, so the guard can be tested without
     waiting.

   .. dec:: Keep the lockout state in memory
      :id: DEC_LOCKOUT_STATE
      :status: accepted
      :decides: SPEC_LOCKOUT, RISK_LOCKOUT_RESTART
      :safety_relevant: false
      :security_relevant: true

      **Context**

      The counters and lock times need to be stored somewhere.

      **Alternatives**

      A persistent store (file, database) — survives restarts but adds a
      dependency the product does not have yet.

      **Consequences**

      A restart clears all counters and locks; an attacker could use a
      restart to guess again. Persisting the state is a later change.

      **Rationale**

      In-memory state is chosen because it matches the in-memory audit log
      and keeps the guard simple and testable.

