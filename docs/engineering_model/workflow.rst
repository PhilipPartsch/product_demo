.. _engineering-workflow:

Engineering workflow
====================

Needs are authored and reviewed stage by stage with ``ubc agent``
(``[workflow]`` in ``ubproject.toml``). Each stage produces one need type,
links it to its parent, and is reviewed against a quality pack before the
next stage starts.

Stages
------

.. list-table::
   :header-rows: 1
   :widths: 14 11 22 18 18 17

   * - Stage
     - Produces
     - Links to (trace gate)
     - Author skill
     - Review skill
     - File (in ``docs/``)
   * - ``user_stories``
     - ``us``
     - —
     - ``draft-us``
     - ``review-feat``
     - ``user_stories.rst``
   * - ``reqs``
     - ``req``
     - ``satisfies`` → ``us``
     - ``draft-requirement``
     - ``review-requirement``
     - ``requirements.rst``
   * - ``specs``
     - ``spec``
     - ``refines`` → ``req``
     - ``draft-spec``
     - ``review-spec``
     - ``specifications.rst``
   * - ``code``
     - ``impl``
     - ``implements`` → ``spec``
     - ``draft-impl``
     - —
     - ``../src``
   * - ``test_specs``
     - ``test_spec``
     - ``verifies`` → ``spec``
     - ``draft-test-spec``
     - ``review-test-spec``
     - ``verification.rst``
   * - ``decisions``
     - ``dec``
     - ``decides`` (for staleness only)
     - ``record-dec``
     - ``review-decision``
     - nested in the parent
   * - ``risks``
     - ``risk``
     - — (hash-conditioned links)
     - ``record-risk``
     - ``review-risk``
     - ``risks.rst``

Test results have no stage: ``ubc script tests`` runs pytest and writes the
JUnit XML that Sphinx-Test-Reports turns into test-result needs.

Driving the loop
----------------

.. code-block:: bash

   cd docs
   ubc agent status            # state of every stage
   ubc agent next              # the next action (author / review / fix)
   ubc agent prompt            # that action as an instruction for an agent
   ubc agent run               # execute it with the headless runner ([agent.runner])
   ubc agent gaps              # missing links and reviews
   ubc agent verdict-check     # missing / failing / outdated reviews

Every author skill first proposes an outline (the needs, their links, the
decisions and risks it will record) and waits for approval. Changes stay
uncommitted for review.

Skills
------

All skills live in ``.agents/skills/`` and are copied to ``.claude/skills/``
and ``.github/agents/`` by ``scripts/mirror_skills.py`` (``--check`` in CI).

- **Stage skills** (``draft-us``, ``draft-requirement``, ``draft-spec``,
  ``draft-impl``, ``draft-test-spec``) state their incoming and outgoing
  needs, the template, the status rule (only decisions and risks have a
  status), append-only editing, and when to record a decision or a risk.
- **Recording skills** (``record-dec``, ``record-risk``) only render a
  complete hand-over payload (``.agents/templates/handover/``) — no research,
  no judgment.
- **Review skills** (``review-*``) score a need against its quality pack
  (``docs/quality/*.toml``) and submit a verdict.

``draft-requirement`` and ``draft-impl`` carry this project's pattern under
the profile's names; unused profile skills were removed. Never run
``ubc agent update`` in the repository: it would restore them (plan 998
§4.7).

Templates
---------

One template per need type in ``.agents/templates/`` (``us.rst``,
``req.rst``, ``spec.rst``, ``test_spec.rst``, ``dec.rst``, ``risk.rst``,
``impl.py``, ``test.py``).

Quality packs
-------------

.. list-table::
   :header-rows: 1
   :widths: 18 82

   * - Type
     - Pack and its axes
   * - ``us``
     - ``quality/us.toml``: parent fit, single user capability, user
       observable, no mechanism leak, naming clarity, **no overlap** (must
       score 2), decisions documented
   * - ``req``
     - ``quality/req.toml``: parent fit, atomicity, verifiability,
       unambiguity, comprehensibility, feasibility, decisions documented
   * - ``spec``
     - ``quality/spec.toml``: as ``req``, judged one level down
   * - ``test_spec``
     - ``quality/test_spec.toml``: parent fit, pass criteria, spec coverage,
       reproducibility, decisions documented
   * - ``dec``
     - ``quality/dec.toml``: context present (required), alternatives
       listed, consequences present, rationale quality
   * - ``risk``
     - ``quality/risk.toml``: cause and effect, rating justified, affected
       complete, mitigation fit
