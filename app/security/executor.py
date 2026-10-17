from app.security.security import (
    SecurityManager,
    UserRole,
    RiskLevel,
)
from app.security.audit import AuditLogger
from app.security.risk_policy import RiskPolicy


class ActionExecutor:

    def __init__(self, security: SecurityManager):
        self.security = security
        self.audit = AuditLogger()
        self.last_status = None

    def execute(
        self,
        action_name: str,
        role: UserRole,
        risk: RiskLevel,
        action_function,
        confirmed: bool = False,
    ) -> bool:

        # Reset status for every new execution.
        self.last_status = None

        # 1. Validate inputs.
        if not isinstance(action_name, str) or not action_name.strip():
            print("BLOCKED | Invalid action name")
            self.last_status = "blocked"
            return False

        if not isinstance(role, UserRole):
            print("BLOCKED | Invalid user role")
            self.last_status = "blocked"
            return False

        if not isinstance(risk, RiskLevel):
            print("BLOCKED | Invalid risk level")
            self.last_status = "blocked"
            return False

        if not callable(action_function):
            print("BLOCKED | Invalid action function")
            self.last_status = "blocked"
            return False

        # 2. Central risk policy is the source of truth.
        policy_risk = RiskPolicy.get_risk(action_name)
        effective_risk = policy_risk

        # 3. Reject risk mismatches.
        if risk != policy_risk:
            print(f"BLOCKED | Risk mismatch for {action_name}")
            self.last_status = "blocked"

            self.audit.log(
                action=action_name,
                role=role.value,
                risk=policy_risk.value,
                result="blocked",
            )
            return False

        # 4. Block prohibited actions.
        if effective_risk == RiskLevel.BLOCKED:
            print(f"BLOCKED | {action_name}")
            self.last_status = "blocked"

            self.audit.log(
                action=action_name,
                role=role.value,
                risk=effective_risk.value,
                result="blocked",
            )
            return False

        # 5. Check permissions.
        allowed = self.security.check_permission(
            role,
            effective_risk,
        )

        if not allowed:
            print(f"BLOCKED | {action_name}")
            self.last_status = "blocked"

            self.audit.log(
                action=action_name,
                role=role.value,
                risk=effective_risk.value,
                result="blocked",
            )
            return False

        # 6. Require explicit confirmation for medium/high risk.
        if self.security.requires_confirmation(effective_risk):
            if confirmed is not True:
                print(f"CONFIRMATION REQUIRED | {action_name}")
                self.last_status = "confirmation_required"

                self.audit.log(
                    action=action_name,
                    role=role.value,
                    risk=effective_risk.value,
                    result="confirmation_required",
                )
                return False

        # 7. Execute only after all checks pass.
        try:
            result = action_function()

            if result is False:
                print(f"FAILED | {action_name}")
                self.last_status = "failed"

                self.audit.log(
                    action=action_name,
                    role=role.value,
                    risk=effective_risk.value,
                    result="failed",
                )
                return False

            print(f"EXECUTED | {action_name}")
            self.last_status = "executed"

            self.audit.log(
                action=action_name,
                role=role.value,
                risk=effective_risk.value,
                result="executed",
            )
            return True

        except Exception as error:
            print(f"ERROR | {action_name} | {error}")
            self.last_status = "error"

            self.audit.log(
                action=action_name,
                role=role.value,
                risk=effective_risk.value,
                result="error",
            )
            return False
