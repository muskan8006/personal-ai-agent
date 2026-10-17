from app.security.security import (
    SecurityState,
    RiskLevel,
)


class ThreatMonitor:

    def __init__(self, security_manager, lock_callback=None):
        self.security = security_manager
        self.lock_callback = lock_callback
        self.suspicion_score = 0

    def record_event(self, risk: RiskLevel):

        if risk == RiskLevel.LOW:
            return

        if risk == RiskLevel.MEDIUM:
            self.suspicion_score += 1

        elif risk == RiskLevel.HIGH:
            self.suspicion_score += 2

        elif risk == RiskLevel.BLOCKED:
            self.suspicion_score += 3

        print(
            f"Suspicion score: {self.suspicion_score}"
        )

        if self.suspicion_score >= 5:

            self.security.state = SecurityState.SUSPICIOUS

            print(
                "WARNING | Suspicious activity detected."
            )

            if self.lock_callback:
                self.lock_callback()

    def reset(self):

        self.suspicion_score = 0

        if self.security.state == SecurityState.SUSPICIOUS:
            self.security.state = SecurityState.ARMED