import hashlib
import os

from dotenv import load_dotenv

from app.security.security import UserRole


load_dotenv()


class AuthenticationManager:

    MAX_ATTEMPTS = 3

    def __init__(self):
        self.owner_pin_hash = os.getenv(
            "OWNER_PIN_HASH"
        )

        self.trusted_pin_hash = os.getenv(
            "TRUSTED_PIN_HASH"
        )

        self.failed_attempts = 0

    def _hash_pin(self, pin: str) -> str:

        return hashlib.sha256(
            pin.encode("utf-8")
        ).hexdigest()

    def authenticate(self, pin: str) -> UserRole:

        if self.failed_attempts >= self.MAX_ATTEMPTS:

            print(
                "AUTHENTICATION LOCKED | "
                "Too many failed attempts."
            )

            return UserRole.BLOCKED

        if not self.owner_pin_hash:
            print("Owner authentication not configured.")
            return UserRole.UNKNOWN

        pin_hash = self._hash_pin(pin)

        if pin_hash == self.owner_pin_hash:

            self.failed_attempts = 0

            print("Owner authentication successful.")

            return UserRole.OWNER

        if (
            self.trusted_pin_hash
            and pin_hash == self.trusted_pin_hash
        ):

            self.failed_attempts = 0

            print(
                "Trusted user authentication successful."
            )

            return UserRole.TRUSTED

        self.failed_attempts += 1

        print(
            f"Authentication failed. "
            f"Attempts: {self.failed_attempts}/"
            f"{self.MAX_ATTEMPTS}"
        )

        return UserRole.UNKNOWN

    def authenticate_owner(self, pin: str) -> UserRole:
        return self.authenticate(pin)