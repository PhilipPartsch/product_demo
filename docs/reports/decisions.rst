.. _report-decisions:

Decisions
=========

Every decision is nested inside the need it decides and links to it with
``decides`` (written automatically). User stories, requirements,
specifications and test specifications each need at least one decision
(schema rule ``dec-present``). A decision whose parent changed after its
review shows up as ``outdated`` in ``ubc agent verdict-check`` and is
re-reviewed with ``review-decision``.

Proposed decisions
------------------

Not yet accepted: allowed on ``main``, blocking for a release.

.. needtable::
   :filter: type == "dec" and status == "proposed"
   :columns: id, title, decides, parent
   :style: table

Needs without a decision
------------------------

.. needtable::
   :filter: type in ["us", "req", "spec", "test_spec"] and len(decides_back) == 0
   :columns: id, title, type
   :style: table

Decision log
------------

.. needtable::
   :filter: type == "dec"
   :columns: id, title, status, decides, parent, security_relevant, safety_relevant
   :style: table
