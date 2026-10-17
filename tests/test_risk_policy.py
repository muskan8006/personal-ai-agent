
from app.security.security import RiskLevel
from app.security.risk_policy import RiskPolicy


def test_create_file_is_medium_risk():
    assert RiskPolicy.get_risk("create file") == RiskLevel.MEDIUM


def test_delete_file_is_high_risk():
    assert RiskPolicy.get_risk("delete file") == RiskLevel.HIGH


def test_password_extraction_is_blocked():
    assert RiskPolicy.get_risk("extract password") == RiskLevel.BLOCKED


def test_unknown_action_defaults_to_high_risk():
    assert RiskPolicy.get_risk("unknown action") == RiskLevel.HIGH


def test_action_name_ignores_case():
    assert RiskPolicy.get_risk("CREATE FILE") == RiskLevel.MEDIUM


def test_action_name_ignores_surrounding_whitespace():
    assert RiskPolicy.get_risk("  create file  ") == RiskLevel.MEDIUM


def test_empty_action_defaults_to_high_risk():
    assert RiskPolicy.get_risk("") == RiskLevel.HIGH
