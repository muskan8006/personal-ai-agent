from datetime import datetime
from pathlib import Path
import hashlib
import json


class AuditLogger:
    def __init__(self):
        self.log_directory = Path("logs")
        self.log_directory.mkdir(parents=True, exist_ok=True)

        self.log_file = self.log_directory / "security.log"
        self.hash_file = self.log_directory / "security.hash"

        self.checkpoint_file = (
            Path.home()
            / "AppData"
            / "Local"
            / "PersonalAIAgent"
            / "security"
            / "audit_checkpoint.json"
        )

    def _read_checkpoint(self) -> dict | None:
        if not self.checkpoint_file.exists():
            return None

        try:
            with self.checkpoint_file.open(
                "r", encoding="utf-8-sig"
            ) as file:
                checkpoint = json.load(file)

            if not isinstance(checkpoint, dict):
                return None

            if type(checkpoint.get("version")) is not int:
                return None
            if checkpoint["version"] != 1:
                return None

            if type(checkpoint.get("entry_count")) is not int:
                return None
            if checkpoint["entry_count"] < 0:
                return None

            if not isinstance(checkpoint.get("last_hash"), str):
                return None

            return checkpoint

        except (OSError, json.JSONDecodeError):
            return None

    def _write_checkpoint(
        self,
        entry_count: int,
        last_hash: str,
    ) -> None:
        self.checkpoint_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        checkpoint = {
            "version": 1,
            "entry_count": entry_count,
            "last_hash": last_hash,
        }

        temporary_file = self.checkpoint_file.with_suffix(".tmp")

        temporary_file.write_text(
            json.dumps(checkpoint, indent=2),
            encoding="utf-8",
        )

        temporary_file.replace(self.checkpoint_file)

    def _get_previous_hash(self) -> str:
        if not self.hash_file.exists():
            return "GENESIS"

        return self.hash_file.read_text(
            encoding="utf-8"
        ).strip()

    def _calculate_hash(
        self,
        log_entry: str,
        previous_hash: str,
    ) -> str:
        data = previous_hash + log_entry

        return hashlib.sha256(
            data.encode("utf-8")
        ).hexdigest()

    def log(
        self,
        action: str,
        role: str,
        risk: str,
        result: str,
    ) -> None:
        # Refuse to append when an existing audit trail is invalid.
        if self.log_file.exists() and self.log_file.stat().st_size > 0:
            if not self.verify_integrity():
                raise RuntimeError(
                    "Audit integrity check failed; refusing to append."
                )

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        log_entry = (
            f"{timestamp} | "
            f"{result.upper()} | "
            f"{role} | "
            f"{risk} | "
            f"{action}"
        )

        previous_hash = self._get_previous_hash()
        current_hash = self._calculate_hash(
            log_entry,
            previous_hash,
        )

        with self.log_file.open(
            "a",
            encoding="utf-8",
        ) as file:
            file.write(
                f"{log_entry} | HASH={current_hash}\n"
            )

        self.hash_file.write_text(
            current_hash,
            encoding="utf-8",
        )

        # Intentionally do not rewrite the checkpoint automatically.
        # Checkpoint advancement needs a separately verified,
        # explicit policy to avoid silently accepting tampering.

    def verify_integrity(self) -> bool:
        if not self.log_file.exists():
            print("TAMPERED | No security log found")
            return False

        lines = self.log_file.read_text(
            encoding="utf-8"
        ).splitlines()

        if not lines:
            print("TAMPERED | Audit log is empty")
            return False

        previous_hash = "GENESIS"

        for line_number, line in enumerate(lines, start=1):
            if "| HASH=" not in line:
                print(
                    f"TAMPERED | Missing hash at line {line_number}"
                )
                return False

            log_entry, stored_hash = line.rsplit(
                " | HASH=",
                1,
            )

            expected_hash = self._calculate_hash(
                log_entry,
                previous_hash,
            )

            if stored_hash != expected_hash:
                print(f"TAMPERED | Line {line_number}")
                return False

            previous_hash = stored_hash

        current_hash = self._get_previous_hash()

        if current_hash != previous_hash:
            print("TAMPERED | Hash state mismatch")
            return False

        checkpoint = self._read_checkpoint()

        if checkpoint is None:
            print("TAMPERED | Missing or invalid checkpoint")
            return False

        if checkpoint["entry_count"] != len(lines):
            print("TAMPERED | Checkpoint entry count mismatch")
            return False

        if checkpoint["last_hash"] != previous_hash:
            print("TAMPERED | Checkpoint hash mismatch")
            return False

        print("INTEGRITY OK | Log and checkpoint are valid.")
        return True
