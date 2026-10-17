from app.security.security import (
    SecurityManager,
    UserRole,
    RiskLevel,
)
from app.security.executor import ActionExecutor


class FakeAuditLogger:
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


def test_create_file_cannot_be_downgraded_to_low_risk():
    executor = make_executor()
    calls = []

    result = executor.execute(
        "create file",
        UserRole.OWNER,
        RiskLevel.LOW,
        lambda: calls.append("ran"),
    )

    assert result is False
    assert calls == []
    assert executor.audit.entries[-1]["risk"] == "medium"
    assert executor.audit.entries[-1]["result"] == "blocked"


def test_password_extraction_remains_blocked():
    executor = make_executor()
    calls = []

    result = executor.execute(
        "extract password",
        UserRole.OWNER,
        RiskLevel.LOW,
        lambda: calls.append("ran"),
    )

    assert result is False
    assert calls == []
    assert executor.audit.entries[-1]["risk"] == "blocked"
    assert executor.audit.entries[-1]["result"] == "blocked"

def test_high_risk_action_cannot_be_downgraded_to_medium():
    executor = make_executor()
    calls = []

    result = executor.execute(
        "delete file",
        UserRole.OWNER,
        RiskLevel.MEDIUM,
        lambda: calls.append("ran"),
        confirmed=True,
    )

    assert result is False
    assert calls == []
    assert executor.audit.entries[-1]["risk"] == "high"
    assert executor.audit.entries[-1]["result"] == "blocked"


def test_unknown_action_requires_high_risk_confirmation():
    executor = make_executor()
    calls = []

    result = executor.execute(
        "unregistered action",
        UserRole.OWNER,
        RiskLevel.LOW,
        lambda: calls.append("ran"),
    )

    assert result is False
    assert calls == []
    assert executor.audit.entries[-1]["risk"] == "high"
    assert executor.audit.entries[-1]["result"] == "blocked"
