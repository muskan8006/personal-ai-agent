from app.security.security import (
    SecurityManager,
    UserRole,
    RiskLevel,
)
from app.security.executor import ActionExecutor


class FakeAuditLogger:
    """Avoid changing the real security logs during tests."""

    def __init__(self):
        self.entries = []

    def log(self, action, role, risk, result):
        self.entries.append({
            "action": action,
            "role": role,
            "risk": risk,
            "result": result,
        })


def make_executor():
    security = SecurityManager()
    security.arm()

    executor = ActionExecutor(security)
    executor.audit = FakeAuditLogger()

    return executor


def test_medium_risk_action_does_not_run_without_confirmation():
    executor = make_executor()
    calls = []

    result = executor.execute(
        "create file",
        UserRole.OWNER,
        RiskLevel.MEDIUM,
        lambda: calls.append("ran"),
    )

    assert result is False
    assert calls == []
    assert executor.audit.entries[-1]["result"] == "confirmation_required"


def test_medium_risk_action_runs_after_confirmation():
    executor = make_executor()
    calls = []

    result = executor.execute(
        "create file",
        UserRole.OWNER,
        RiskLevel.MEDIUM,
        lambda: calls.append("ran"),
        confirmed=True,
    )

    assert result is True
    assert calls == ["ran"]
    assert executor.audit.entries[-1]["result"] == "executed"


def test_blocked_action_does_not_run():
    executor = make_executor()
    calls = []

    result = executor.execute(
        "extract password",
        UserRole.OWNER,
        RiskLevel.BLOCKED,
        lambda: calls.append("ran"),
    )

    assert result is False
    assert calls == []
    assert executor.audit.entries[-1]["result"] == "blocked"


def test_action_exception_is_handled():
    executor = make_executor()

    def failing_action():
        raise RuntimeError("test failure")

    result = executor.execute(
        "create file",
        UserRole.OWNER,
        RiskLevel.MEDIUM,
        failing_action,
        confirmed=True,
    )

    assert result is False
    assert executor.audit.entries[-1]["result"] == "error"

def test_confirmation_requires_exact_boolean_true():
    executor = make_executor()
    calls = []

    result = executor.execute(
        "create file",
        UserRole.OWNER,
        RiskLevel.MEDIUM,
        lambda: calls.append("ran"),
        confirmed=1,
    )

    assert result is False
    assert calls == []
    assert executor.last_status == "confirmation_required"
    assert executor.audit.entries[-1]["result"] == "confirmation_required"
