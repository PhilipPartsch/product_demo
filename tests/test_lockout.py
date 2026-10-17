from product_demo.lockout import LoginGuard

# Values from SPEC_LOCKOUT, written out on purpose: a test that reads the
# code's constants would stay green when code and specification disagree.
SPECIFIED_FAILURES = 5
SPECIFIED_LOCK_SECONDS = 900


class FakeClock:
    def __init__(self) -> None:
        self.now = 1000.0

    def __call__(self) -> float:
        return self.now


def test_lockout_after_five_failures(record_property):
    record_property("executes", "TSPEC_LOCKOUT")
    clock = FakeClock()
    guard = LoginGuard(clock)
    checked = []

    def wrong():
        checked.append(True)
        return False

    for _ in range(SPECIFIED_FAILURES):
        assert not guard.attempt("alice", wrong)
    # Locked: rejected even with the right password, which is not checked.
    checked.clear()
    assert not guard.attempt("alice", lambda: checked.append(True) or True)
    assert checked == []
    # Other accounts are not affected.
    assert guard.attempt("bob", lambda: True)
    # Still locked just before the window ends, open right after it.
    clock.now += SPECIFIED_LOCK_SECONDS - 1
    assert not guard.attempt("alice", lambda: True)
    clock.now += 1
    assert guard.attempt("alice", lambda: True)


def test_success_resets_the_counter(record_property):
    record_property("executes", "TSPEC_LOCKOUT")
    guard = LoginGuard(FakeClock())
    for _ in range(4):
        assert not guard.attempt("alice", lambda: False)
    assert guard.attempt("alice", lambda: True)
    for _ in range(4):
        assert not guard.attempt("alice", lambda: False)
    assert guard.attempt("alice", lambda: True)
