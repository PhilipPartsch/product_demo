Verification
============

Test specifications
-------------------

.. test_spec:: Password hashing test
   :id: TSPEC_HASH
   :verifies: SPEC_HASH
   :test_level: unit
   :safety_relevant: false
   :security_relevant: true

   Verifies that a stored password is a salted, memory-hard hash and that
   login succeeds for valid credentials.

.. test_spec:: Audit record test
   :id: TSPEC_AUDIT
   :verifies: SPEC_AUDIT
   :test_level: unit
   :safety_relevant: false
   :security_relevant: true

   Verifies that a structured, append-only audit record is written for each
   login attempt.
