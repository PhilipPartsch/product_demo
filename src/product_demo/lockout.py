"""Lock an account after repeated failed logins."""

from collections.abc import Callable
from dataclasses import dataclass
import time

MAX_FAILURES = 5
LOCK_SECONDS = 900


@dataclass
class _State:
    failures: int = 0
    locked_until: float = 0.0


# @Login lockout guard, IMPL_LOCKOUT, impl, [SPEC_LOCKOUT], false, true
class LoginGuard:
    """Rejects logins for an account after consecutive failed attempts."""

    def __init__(self, clock: Callable[[], float] = time.monotonic) -> None:
        self._clock = clock
        self._states: dict[str, _State] = {}

    def attempt(self, account: str, check_password: Callable[[], bool]) -> bool:
        """Return True if the login succeeds; never check a locked account."""
        state = self._states.setdefault(account, _State())
        if self._clock() < state.locked_until:
            return False
        if check_password():
            state.failures = 0
            return True
        state.failures += 1
        if state.failures >= MAX_FAILURES:
            state.locked_until = self._clock() + LOCK_SECONDS
            state.failures = 0
        return False
