import json
from app.security.audit import AuditLogger
def make_test_logger(tmp_path):
    logger = AuditLogger()

    # Keep every test artifact inside pytest's temporary directory.
    logger.log_directory = tmp_path
    logger.log_file = tmp_path / "security.log"
    logger.hash_file = tmp_path / "security.hash"
    logger.checkpoint_file = tmp_path / "audit_checkpoint.json"

    return logger


def write_checkpoint(logger):
    """Create a checkpoint for the current test log."""
    lines = logger.log_file.read_text(
        encoding="utf-8"
    ).splitlines()

    if not lines:
        raise ValueError("Cannot checkpoint an empty audit log")

    last_hash = lines[-1].rsplit(" | HASH=", 1)[1]

    checkpoint = {
        "version": 1,
        "entry_count": len(lines),
        "last_hash": last_hash,
    }

    logger.checkpoint_file.write_text(
        json.dumps(checkpoint, indent=2),
        encoding="utf-8",
    )


def test_valid_audit_log_passes_integrity_check(tmp_path):
    logger = make_test_logger(tmp_path)

    logger.log(
        action="create file",
        role="owner",
        risk="medium",
        result="executed",
    )

    write_checkpoint(logger)

    assert logger.verify_integrity() is True


def test_tampered_audit_log_fails_integrity_check(tmp_path):
    logger = make_test_logger(tmp_path)

    logger.log(
        action="create file",
        role="owner",
        risk="medium",
        result="executed",
    )

    write_checkpoint(logger)

    content = logger.log_file.read_text(encoding="utf-8")
    logger.log_file.write_text(
        content.replace("create file", "delete file"),
        encoding="utf-8",
    )

    # Do not update the checkpoint after tampering.
    assert logger.verify_integrity() is False


def test_modified_hash_state_fails_integrity_check(tmp_path):
    logger = make_test_logger(tmp_path)

    logger.log(
        action="create file",
        role="owner",
        risk="medium",
        result="executed",
    )

    write_checkpoint(logger)

    logger.hash_file.write_text(
        "invalid-hash",
        encoding="utf-8",
    )

    assert logger.verify_integrity() is False


def test_deleted_last_audit_entry_fails_integrity_check(tmp_path):
    logger = make_test_logger(tmp_path)

    logger.log(
        action="create file",
        role="owner",
        risk="medium",
        result="executed",
    )
    write_checkpoint(logger)

    logger.log(
        action="delete file",
        role="owner",
        risk="high",
        result="executed",
    )
    write_checkpoint(logger)

    lines = logger.log_file.read_text(
        encoding="utf-8"
    ).splitlines()

    # Remove the last entry without updating the checkpoint.
    logger.log_file.write_text(
        lines[0] + "\n",
        encoding="utf-8",
    )

    assert logger.verify_integrity() is False


def test_deleted_middle_audit_entry_fails_integrity_check(tmp_path):
    logger = make_test_logger(tmp_path)

    for action in ("create file", "remember", "delete file"):
        logger.log(
            action=action,
            role="owner",
            risk="medium",
            result="executed",
        )
        write_checkpoint(logger)

    lines = logger.log_file.read_text(
        encoding="utf-8"
    ).splitlines()

    del lines[1]

    # Do not update the checkpoint after deleting an entry.
    logger.log_file.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    assert logger.verify_integrity() is False
