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
class SecurityManager:
    def __init__(self):
        self.state = SecurityState.DISARMED
    def arm(self):
        self.state = SecurityState.ARMED
    def disarm(self):
        self.state = SecurityState.DISARMED
    def get_state(self):
        return self.state.value