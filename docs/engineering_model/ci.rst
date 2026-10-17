.. _engineering-ci:

CI gates
========

Two pipelines (GitHub Actions). Both run the tests first, because the test
results are needs, then lint and build the documentation with ubc and with
Sphinx.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Check
     - CI 1 — pull request / push to ``main``
     - CI 2 — ``release/*`` and tags ``v*``
   * - tests (``ubc script tests``)
     - must pass
     - must pass
   * - lint / build (``ubc check``, ``ubc build html``, Sphinx ``-W``)
     - no warning or error
     - no warning or error
   * - schema violations
     - block
     - block
   * - schema completeness (``info``)
     - allowed
     - none (``ubc check --deny info``)
   * - stale risks (``needs.link_condition_failed``)
     - reported
     - block
   * - workflow config (``ubc agent config-validate``, ``doctor``)
     - must be ok
     - must be ok
   * - structural gaps
     - no new gaps (ratchet against ``.pharaoh/gaps-baseline.json``)
     - none (``ubc agent gaps``)
   * - reviews (``ubc agent verdict-check``)
     - no failing verdict
     - every verdict present, fresh and passing
   * - decisions / risks status
     - ``proposed`` / ``open`` allowed
     - not allowed (``release_disallow_status``)
   * - skill copies (``scripts/mirror_skills.py --check``)
     - in sync
     - in sync

The gates on top of ``ubc agent`` are in ``scripts/ci_gates.py``
(``gaps``, ``verdicts``, ``schema-json``, ``stale-risks``, each with
``--tier main`` or ``--tier release``). ``ubc agent release-check`` is not
used: it counts missing reviews and open statuses as gaps and its baseline
cannot be captured from a failing state (plan 999 PH-20).

On ``main``, stale risks are reported but do not fail: CI 1 sets
``CI_TIER=main`` (read by ``conf.py``) and adds
``needs.link_condition_failed`` to ubc's ``lint.ignore``. Locally both
toolchains fail on a stale risk.

Workflows: ``.github/workflows/ci-main.yml`` (CI 1), ``ci-release.yml``
(CI 2), shared setup ``.github/actions/setup/action.yml`` (ubc pinned via
``UBC_VERSION``, uv, graphviz).

Run the same checks locally from ``docs/``: ``ubc script ci`` (tests, lint,
build), ``ubc script sphinx``, and the gates from the repository root, e.g.
``python3 scripts/ci_gates.py gaps --tier main``.
