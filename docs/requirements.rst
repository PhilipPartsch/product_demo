.. _full-reqs:

Requirements
============

.. req:: User authentication
   :id: REQ_AUTH
   :status: <<[var.platform == "windows"]: win_auth, default_auth>>
   :platform_note: Built for <{ var.platform }>

   The system shall authenticate users before granting access.
   ``status`` resolves per build variant; ``platform_note`` embeds variant data.

.. req:: Audit logging
   :id: REQ_LOG

   The system shall record an audit trail of authentication events.
