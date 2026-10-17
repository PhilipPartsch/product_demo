.. _report-risks:

Risks
=====

Risks link the needs they affect (``affects``) and, once mitigated, the needs
that mitigate them (``mitigated_by``) — each link with a hash condition on the
target's fingerprint. When a target changes after the risk was evaluated,
the build reports ``needs.link_condition_failed``: the risk is stale and is
re-evaluated (``review-risk``), then signed off again with
``python3 scripts/refresh_risk_links.py <RISK_ID>``. Stale risks are reported
on ``main`` and block a release.

Open risks
----------

.. needtable::
   :filter: type == "risk" and status == "open"
   :columns: id, title, risk_category, severity, likelihood, affects
   :style: table

Risks without a mitigation
--------------------------

Open or mitigated risks that name no mitigating need.

.. needtable::
   :filter: type == "risk" and status in ["open", "mitigated"] and len(mitigated_by) == 0
   :columns: id, title, status, severity
   :style: table

Security and safety risks
-------------------------

.. needtable::
   :filter: type == "risk" and (risk_category in ["security", "safety"] or security_relevant or safety_relevant)
   :columns: id, title, status, risk_category, severity, likelihood
   :style: table

All risks
---------

.. needtable::
   :filter: type == "risk"
   :columns: id, title, status, risk_category, severity, likelihood, affects, mitigated_by
   :style: table
