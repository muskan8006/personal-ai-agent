import pytest
from app.security.security import (
    SecurityManager,
    SecurityState,
    UserRole,
    RiskLevel,
)
@pytest.fixture
def security():
    manager = SecurityManager()
    manager.arm()
    return manager


def test_disarmed_state_blocks_actions():
    manager = SecurityManager()

    assert manager.check_permission(
        UserRole.OWNER, RiskLevel.LOW
    ) is False


def test_armed_owner_can_run_low_risk(security):
    assert security.check_permission(
        UserRole.OWNER, RiskLevel.LOW
    ) is True


def test_unknown_user_cannot_run_medium_risk(security):
    assert security.check_permission(
        UserRole.UNKNOWN, RiskLevel.MEDIUM
    ) is False


def test_trusted_user_cannot_run_high_risk(security):
    assert security.check_permission(
        UserRole.TRUSTED, RiskLevel.HIGH
    ) is False


def test_blocked_action_is_rejected(security):
    assert security.check_permission(
        UserRole.OWNER, RiskLevel.BLOCKED
    ) is False


def test_locked_state_blocks_actions(security):
    security.lock()

    assert security.check_permission(
        UserRole.OWNER, RiskLevel.LOW
    ) is False


def test_recovery_state_blocks_actions(security):
    security.unlock()

    assert security.get_state() == SecurityState.RECOVERY.value
    assert security.check_permission(
        UserRole.OWNER, RiskLevel.LOW
    ) is False


def test_invalid_role_is_rejected(security):
    assert security.check_permission(
        "owner", RiskLevel.LOW
    ) is False


def test_medium_risk_requires_confirmation(security):
    assert security.requires_confirmation(RiskLevel.MEDIUM) is True


def test_low_risk_does_not_require_confirmation(security):
    assert security.requires_confirmation(RiskLevel.LOW) is False
