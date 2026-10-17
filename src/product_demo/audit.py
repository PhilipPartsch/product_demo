"""Structured, append-only audit records of authentication events."""

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class AuditRecord:
    timestamp: str
    user: str
    event: str
    success: bool


# @Append-only audit log, IMPL_AUDIT, impl, [SPEC_AUDIT], false, true
class AuditLog:
    """Append-only log: records can be added and read, never changed."""

    def __init__(self) -> None:
        self._lines: list[str] = []

    def append(self, user: str, event: str, success: bool) -> AuditRecord:
        record = AuditRecord(
            timestamp=datetime.now(timezone.utc).isoformat(),
            user=user,
            event=event,
            success=success,
        )
        self._lines.append(json.dumps(asdict(record), sort_keys=True))
        return record

    def records(self) -> list[AuditRecord]:
        return [AuditRecord(**json.loads(line)) for line in self._lines]
