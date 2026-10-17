from dataclasses import FrozenInstanceError

import pytest

from product_demo.audit import AuditLog


def test_record_written_per_login_attempt(record_property):
    record_property("executes", "TSPEC_AUDIT")
    log = AuditLog()
    log.append("alice", "login", success=True)
    log.append("alice", "login", success=False)
    records = log.records()
    assert [r.success for r in records] == [True, False]
    with pytest.raises(FrozenInstanceError):
        records[0].user = "mallory"
