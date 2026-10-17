import builtins
from app import main as main_module


class FakeRouter:
    def route(self, command):
        if command == "create file notes.txt":
            return {
                "action": "create file",
                "params": {"filename": "notes.txt"},
            }
        return None


class FakeAgent:
    def __init__(self):
        self.router = FakeRouter()
        self.calls = []

    def execute(self, command, confirmed=False):
        self.calls.append((command, confirmed))

        if command == "create file notes.txt" and not confirmed:
            return False

        return True


def run_main_with_inputs(monkeypatch, inputs):
    agent = FakeAgent()
    responses = iter(inputs)

    monkeypatch.setattr(
        main_module,
        "CommandExecutor",
        lambda: agent,
    )
    monkeypatch.setattr(
        builtins,
        "input",
        lambda prompt="": next(responses),
    )

    main_module.main()
    return agent


def test_yes_confirms_pending_action(monkeypatch):
    agent = run_main_with_inputs(
        monkeypatch,
        ["create file notes.txt", "yes", "exit"],
    )

    assert agent.calls == [
        ("create file notes.txt", False),
        ("create file notes.txt", True),
    ]


def test_no_cancels_pending_action(monkeypatch):
    agent = run_main_with_inputs(
        monkeypatch,
        ["create file notes.txt", "no", "exit"],
    )

    assert agent.calls == [
        ("create file notes.txt", False),
    ]


def test_unrelated_input_does_not_execute_while_pending(monkeypatch):
    agent = run_main_with_inputs(
        monkeypatch,
        ["create file notes.txt", "open chrome", "no", "exit"],
    )

    assert agent.calls == [
        ("create file notes.txt", False),
    ]