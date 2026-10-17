from enum import Enum
class UserRole(Enum):
    OWNER = "owner"
    TRUSTED = "trusted"
    UNKNOWN = "unknown"
    BLOCKED = "blocked"


class SecurityState(Enum):
    DISARMED = "disarmed"
    ARMED = "armed"
    SUSPICIOUS = "suspicious"
    LOCKED = "locked"
    RECOVERY = "recovery"


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKED = "blocked"


class SecurityManager:

    def __init__(self):
        self.state = SecurityState.DISARMED

    def arm(self):
        self.state = SecurityState.ARMED

    def disarm(self):
        self.state = SecurityState.DISARMED

    def get_state(self):
        return self.state.value

    def check_permission(
        self,
        role: UserRole,
        risk: RiskLevel
    ) -> bool:

        # Fail closed: only ARMED state allows evaluation
        if self.state != SecurityState.ARMED:
            return False

        # Reject invalid inputs
        if not isinstance(role, UserRole):
            return False

        if not isinstance(risk, RiskLevel):
            return False

        # Explicitly blocked users and actions
        if role == UserRole.BLOCKED:
            return False

        if risk == RiskLevel.BLOCKED:
            return False

        # Unknown users cannot perform medium/high-risk actions
        if role == UserRole.UNKNOWN and risk in (
            RiskLevel.MEDIUM,
            RiskLevel.HIGH,
        ):
            return False

        # Trusted users cannot perform high-risk actions
        if role == UserRole.TRUSTED and risk == RiskLevel.HIGH:
            return False

        return True

    def requires_confirmation(
        self,
        risk: RiskLevel
    ) -> bool:

        if not isinstance(risk, RiskLevel):
            return True

        return risk in (
            RiskLevel.MEDIUM,
            RiskLevel.HIGH,
        )

    def lock(self):
        self.state = SecurityState.LOCKED

    def is_locked(self):
        return self.state == SecurityState.LOCKED

    def unlock(self):
        # Recovery is not the same as authorization.
        # Explicitly arm again after recovery checks.
        self.state = SecurityState.RECOVERY
