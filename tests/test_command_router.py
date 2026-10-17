from app.agent.command_router import CommandRouter
def test_create_file_extracts_filename():
    router = CommandRouter()

    result = router.route("create file notes.txt")

    assert result == {
        "action": "create file",
        "params": {"filename": "notes.txt"},
    }


def test_remember_extracts_key_and_value():
    router = CommandRouter()

    result = router.route("remember my city is Lucknow")

    assert result == {
        "action": "remember",
        "params": {
            "key": "city",
            "value": "lucknow",
        },
    }


def test_forget_extracts_memory_key():
    router = CommandRouter()

    result = router.route("forget my city")

    assert result == {
        "action": "forget",
        "params": {"key": "city"},
    }


def test_unknown_command_returns_none():
    router = CommandRouter()

    assert router.route("do something unknown") is None


def test_empty_command_returns_none():
    router = CommandRouter()

    assert router.route("   ") is None


def test_non_string_command_returns_none():
    router = CommandRouter()

    assert router.route(None) is None
