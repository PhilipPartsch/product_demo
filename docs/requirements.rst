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

.. req:: Audit logging
   :id: REQ_LOG
   :satisfies: US_AUDIT
   :safety_relevant: false
   :security_relevant: true

   The system shall record an audit trail of authentication events.
