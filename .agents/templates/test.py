# pytest test realising one test specification. The `executes` property
# becomes the link from the test result (Sphinx-Test-Reports) to the test
# specification; `ubc script tests` writes tests/_results/junit.xml.


def test_{{what_is_checked}}(record_property):
    record_property("executes", "TSPEC_{{NAME}}")
    {{arrange}}
    {{act}}
    assert {{pass criterion}}
