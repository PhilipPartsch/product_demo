.. _full-us:

User Stories
============

.. us:: Secure login
   :id: US_LOGIN
   :safety_relevant: false
   :security_relevant: true

   As a user, I want to log in with my password, so that only I can access
   my account.

   .. dec:: Password login only
      :id: DEC_US_LOGIN_SCOPE
      :status: accepted
      :safety_relevant: false
      :security_relevant: true

      **Context**

      Users could log in with a password or through an external identity
      provider.

      **Alternatives**

      Single sign-on with an external provider — needs an integration the
      product does not have.

      **Consequences**

      Only accounts with a password are covered; single sign-on would be a
      new user story.

      **Rationale**

      Password login is chosen because it is the only login the product
      offers.

.. us:: Traceable account activity
   :id: US_AUDIT
   :safety_relevant: false
   :security_relevant: true

   As an administrator, I want a record of authentication events, so that I
   can investigate suspicious activity.

   .. dec:: Audit only authentication events
      :id: DEC_US_AUDIT_SCOPE
      :status: accepted
      :safety_relevant: false
      :security_relevant: true

      **Context**

      An audit trail could cover every user action or only authentication.

      **Alternatives**

      All user actions — far more data, and the product has no other actions
      yet.

      **Consequences**

      Only login attempts are traceable; other actions need a new user
      story.

      **Rationale**

      Authentication events are chosen because suspicious activity starts at
      login.

.. us:: Protection against password guessing
   :id: US_LOCKOUT
   :safety_relevant: false
   :security_relevant: true

   As a user, I want my account to be protected against repeated password
   guessing, so that an attacker cannot find my password by trying many.

   .. dec:: Protect per account, not per network address
      :id: DEC_US_LOCKOUT_SCOPE
      :status: accepted
      :safety_relevant: false
      :security_relevant: true

      **Context**

      Password guessing can be limited per account or per network address of
      the caller.

      **Alternatives**

      Per network address — needs network information the product does not
      have, and attackers rotate addresses.

      **Consequences**

      Guessing against one account is limited; spreading guesses over many
      accounts is not covered by this story.

      **Rationale**

      Per-account protection is chosen because it needs only the account
      name and protects each user directly.
