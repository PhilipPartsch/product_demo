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

   **Preconditions**

   None (the hashing functions have no state).

   **Inputs and steps**

   1. Hash the password ``s3cret`` twice.
   2. Verify ``s3cret`` against the first hash.
   3. Verify ``wrong`` against the first hash.

   **Pass criteria**

   - The two hashes differ (a fresh salt per hash).
   - Step 2 succeeds, step 3 fails.

   .. dec:: Test with the real scrypt, no mock
      :id: DEC_TSPEC_HASH_REAL
      :status: accepted
      :safety_relevant: false
      :security_relevant: true

      **Context**

      The test could replace scrypt with a fast fake.

      **Alternatives**

      A mocked hash — faster, but would not show that the real parameters
      work.

      **Consequences**

      Each run computes real scrypt hashes (milliseconds).

      **Rationale**

      The real function is chosen because the specification is about the
      real hash.

.. test_spec:: Audit record test
   :id: TSPEC_AUDIT
   :verifies: SPEC_AUDIT
   :test_level: unit
   :safety_relevant: false
   :security_relevant: true

   **Preconditions**

   An empty audit log.

   **Inputs and steps**

   1. Append a successful and a failed login of ``alice``.
   2. Read the records.
   3. Try to change the user of the first record.

   **Pass criteria**

   - Two records are returned, in order, with success ``true`` then
     ``false``.
   - Step 3 fails with an error (records cannot be changed).

   .. dec:: Check append-only through immutable records
      :id: DEC_TSPEC_AUDIT_IMMUTABLE
      :status: accepted
      :safety_relevant: false
      :security_relevant: true

      **Context**

      Append-only can be checked on the log or on its records.

      **Alternatives**

      Checking that the log has no delete method — says nothing about
      changing a record.

      **Consequences**

      The test relies on records being immutable; a log that allows
      replacing records would need an extra check.

      **Rationale**

      Immutable records are checked because changing a record is the likely
      way to falsify the trail.

.. test_spec:: Login lockout test
   :id: TSPEC_LOCKOUT
   :verifies: SPEC_LOCKOUT
   :test_level: unit
   :safety_relevant: false
   :security_relevant: true

   **Preconditions**

   A login guard with a controllable clock and no previous attempts.

   **Inputs and steps**

   1. Five failed attempts for account ``alice``.
   2. One attempt for ``alice`` with the correct password.
   3. One attempt for account ``bob`` with the correct password.
   4. Advance the clock by 899 seconds; one attempt for ``alice`` with the
      correct password; advance by 1 more second; one more attempt.
   5. New guard: four failed attempts, one success, four failed attempts,
      one success for ``alice``.

   **Pass criteria**

   - Step 2 is rejected and the password is not checked.
   - Step 3 succeeds (other accounts are not locked).
   - In step 4 the first attempt is rejected (still locked) and the second
     succeeds (the lock has ended after exactly 900 seconds).
   - The test uses the specified values (5, 900 s) literally, not the
     code's constants, so a mismatch between code and specification fails.
   - In step 5 both successes are accepted (a success resets the counter,
     so no lock happens).

   .. dec:: Test with a fake clock instead of waiting
      :id: DEC_TSPEC_LOCKOUT_CLOCK
      :status: accepted
      :safety_relevant: false
      :security_relevant: false

      **Context**

      The lock lasts 900 seconds; a test must check its end.

      **Alternatives**

      Sleeping in the test — 15 minutes per run. Lowering the duration for
      tests — the tested value would differ from the specified one.

      **Consequences**

      The guard takes its time source as a parameter; the test controls it.

      **Rationale**

      A fake clock is chosen because it tests the specified 900 seconds in
      no time.
