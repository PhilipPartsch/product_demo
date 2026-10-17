.. _full-test-results:

Test results
============

Results of the latest pytest run (``tests/_results/junit.xml``). Each test
case links to the test specification it executes (pytest property
``executes``). This page lives next to the tests in ``tests/`` and is mounted
into the docs.

.. The ``test-file`` directive is added with the first pytest test (skill
   ``draft-test-spec``): an empty JUnit file would create test-result needs,
   and with them the workflow engine no longer treats the empty project as
   empty (plan 999 PH-24). The directive to add:

   .. test-file:: pytest results
      :file: ../tests/_results/junit.xml
      :id: TF_PYTEST
      :auto_suites:
      :auto_cases:
