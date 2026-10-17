from app.security.security import RiskLevel
class RiskPolicy:

    ACTION_RISKS = {

        # Safe application actions
        "open chrome": RiskLevel.LOW,
        "open notepad": RiskLevel.LOW,
        "open calculator": RiskLevel.LOW,
        "open explorer": RiskLevel.LOW,

        # Browser actions
        "google search": RiskLevel.LOW,
        "open webpage": RiskLevel.LOW,
        "read webpage": RiskLevel.LOW,

        # File actions
        "create file": RiskLevel.MEDIUM,
        "read file": RiskLevel.LOW,

        # Memory actions
        "remember": RiskLevel.MEDIUM,
        "recall": RiskLevel.LOW,

        # Communication
        "send message": RiskLevel.MEDIUM,

        # High-risk actions
        "delete file": RiskLevel.HIGH,
        "delete important files": RiskLevel.HIGH,
        "lock windows": RiskLevel.HIGH,
        "automatic security lock": RiskLevel.HIGH,

        # Prohibited actions
        "extract password": RiskLevel.BLOCKED,
        "access otp": RiskLevel.BLOCKED,
        "bypass security": RiskLevel.BLOCKED,
        "list memories": RiskLevel.LOW,
        "forget": RiskLevel.MEDIUM,
    }

    @classmethod
    def get_risk(cls, action_name: str) -> RiskLevel:

        action = action_name.lower().strip()

        return cls.ACTION_RISKS.get(
            action,
            RiskLevel.HIGH
        )