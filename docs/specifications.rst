.. _full-specs:

Specifications
==============

.. spec:: Password hashing
   :id: SPEC_HASH
   :refines: REQ_AUTH
   :safety_relevant: false
   :security_relevant: true

   Passwords shall be stored using a salted, memory-hard hash.

.. spec:: Structured audit records
   :id: SPEC_AUDIT
   :refines: REQ_LOG
   :safety_relevant: false
   :security_relevant: true

   Each audit record shall be a structured, append-only entry.
