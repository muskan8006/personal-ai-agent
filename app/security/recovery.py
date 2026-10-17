from app.security.security import SecurityState

from app.security.audit import AuditLogger
from app.security.authentication import AuthenticationManager


class RecoveryManager:

    def __init__(self, security):
        self.security = security
        self.audit = AuditLogger()
        self.authentication = AuthenticationManager()

    def begin_recovery(self):

        if not self.security.is_locked():
            print("Recovery not required.")
            return False

        self.security.unlock()

        print(
            "RECOVERY MODE | "
            "Owner authentication required."
        )

        self.audit.log(
            action="Begin Recovery",
            role="unknown",
            risk="high",
            result="recovery_started"
        )

        return True

    def verify_owner(self, pin: str):

        if self.security.state != SecurityState.RECOVERY:
            print(
                "Recovery session is not active."
            )
            return False

        role = self.authentication.authenticate_owner(pin)

        if role.value == "blocked":

            self.security.lock()

            print(
                "SECURITY LOCKED | "
                "Too many authentication failures."
            )

            self.audit.log(
                action="Authentication Lockout",
                role=role.value,
                risk="blocked",
                result="locked"
            )

            return False

        if role.value != "owner":

            print(
                "RECOVERY FAILED | "
                "Owner authentication failed."
            )

            self.audit.log(
                action="Owner Authentication",
                role=role.value,
                risk="high",
                result="verification_failed"
            )

            return False

        self.security.arm()

        print(
            "RECOVERY SUCCESS | "
            "Security system armed."
        )

        self.audit.log(
            action="Owner Authentication",
            role=role.value,
            risk="high",
            result="verification_success"
        )

        return True