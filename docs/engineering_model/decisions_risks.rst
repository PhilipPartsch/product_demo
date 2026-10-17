.. _engineering-decisions-risks:

Decisions and risks
===================

Decisions and risks are recorded while the other needs are authored: each
stage skill hands a complete payload to ``record-dec`` or ``record-risk``.

Decisions
---------

- A decision (``dec``) lives **nested inside** the need it decides and
  decides it automatically (``decides`` is copied from the parent). A
  decision outside a need is a schema violation (``dec-nested``).
- Every user story, requirement, specification and test specification needs
  at least one decision (``dec-present``); on architecture elements
  decisions are optional.
- Status: ``proposed`` → ``accepted`` → ``superseded``. A proposed decision
  is allowed on ``main`` and blocks a release.
- **Kept up to date by reviews:** when a decision's parent changes, the
  decision's review verdict becomes ``outdated`` (the ``decisions`` stage
  has trace edges along ``decides``) and it is re-reviewed with
  ``review-decision``. Editing a decision also re-reviews its parent, whose
  text contains it.

Risks
-----

- A risk (``risk``) lives in ``risks.rst`` and links the needs it
  ``affects`` and, once mitigated, the needs it is ``mitigated_by``
  (requirements, architecture elements, specifications, test
  specifications, decisions).
- Status: ``open`` → ``mitigated`` / ``accepted`` → ``closed``. A mitigated
  risk names its mitigation; an accepted risk is decided by an accepted
  decision. An open risk is allowed on ``main`` and blocks a release.
- **Kept up to date by hash conditions:** each link carries the target's
  fingerprint at the last evaluation, ``SPEC_HASH[fp=="…"]``. When the
  target changes, the build reports ``needs.link_condition_failed``: the
  risk is stale. Re-evaluate it (``review-risk``), update it if needed, then
  sign it off again:

  .. code-block:: bash

     python3 scripts/refresh_risk_links.py RISK_SCRYPT_PARAMS

  A stale risk is reported on ``main`` and blocks a release.

Overviews
---------

:ref:`report-decisions` and :ref:`report-risks` list proposed decisions,
needs without a decision, the decision log, open risks, risks without a
mitigation and the security / safety risks.
