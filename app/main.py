from app.agent.command_executor import CommandExecutor
def main():
    print("=" * 40)
    print("       PERSONAL AI AGENT")
    print("=" * 40)
    print("Type 'exit' to stop the agent.")
    print()

    agent = CommandExecutor()
    pending_command = None

    while True:
        try:
            command = input("You: ").strip()

        except (KeyboardInterrupt, EOFError):
            print("\nAgent stopped.")
            break

        if not command:
            continue

        if command.lower() in ("exit", "quit", "bye"):
            print("Agent: Goodbye.")
            break

        # HANDLE PENDING CONFIRMATION
        if pending_command is not None:

            if command.lower() in (
                "yes", "y", "haan", "ha", "confirm"
            ):
                confirmed_command = pending_command
                pending_command = None

                print("Agent: Confirmation received.")

                result = agent.execute(
                    confirmed_command,
                    confirmed=True,
                )

                if result:
                    print("Agent: Done.")
                else:
                    print("Agent: Action failed or was blocked.")

                continue

            if command.lower() in (
                "no", "n", "nahi", "cancel"
            ):
                print("Agent: Action cancelled.")
                pending_command = None
                continue

            print("Agent: Please answer yes or no.")
            continue

        # EXECUTE COMMAND
        result = agent.execute(command)

        # CHECK STATUS SAFELY
        executor = getattr(agent, "executor", None)
        status = getattr(executor, "last_status", None)

        # CONFIRM ONLY WHEN THE EXECUTOR REQUESTS IT

        # CHECK CONFIRMATION STATUS
        executor = getattr(agent, "executor", None)
        status = getattr(executor, "last_status", None)

        routed = agent.router.route(command)

        # Real executor must explicitly request confirmation.
        confirmation_needed = status == "confirmation_required"

        # Compatibility fallback for test doubles that do not
        # expose executor status. Keep this limited to known actions.
        if executor is None and result is False:
            confirmation_needed = (
                routed is not None
                and routed["action"] in (
                    "create file",
                    "remember",
                    "forget",
                )
            )

        if confirmation_needed:
            if (
                routed is not None
                and routed["action"] in (
                    "create file",
                    "remember",
                    "forget",
                )
            ):
                pending_command = command
                action = routed["action"]
                params = routed["params"]

                print("\nAgent: Confirmation required.")

                if action == "create file":
                    print("Action: Create file")
                    print(f"File: {params['filename']}")

                elif action == "remember":
                    print("Action: Save memory")
                    print(f"Key: {params['key']}")
                    print(f"Value: {params['value']}")

                elif action == "forget":
                    print("Action: Delete saved memory")
                    print(f"Memory key: {params['key']}")

                print("Confirm? (yes/no)")

        elif not result:
            print("Agent: Action was not completed.")



if __name__ == "__main__":
    main()
