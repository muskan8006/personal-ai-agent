from app.agent.command_router import CommandRouter
from app.security.security import SecurityManager, UserRole, RiskLevel
from app.security.executor import ActionExecutor
from app.tools.app_launcher import AppLauncher
from app.tools.file_manager import FileManager
from app.tools.playwright_browser import PlaywrightBrowser
from app.memory.memory_manager import MemoryManager


class CommandExecutor:

    def __init__(self):
        self.router = CommandRouter()
        self.security = SecurityManager()
        self.security.arm()

        self.executor = ActionExecutor(self.security)
        self.apps = AppLauncher()
        self.files = FileManager()
        self.browser = PlaywrightBrowser()
        self.memory = MemoryManager()

    def execute(
        self,
        command: str,
        role: UserRole = UserRole.OWNER,
        confirmed: bool = False
    ):
        routed = self.router.route(command)

        if routed is None:
            print("UNKNOWN COMMAND | Action not executed.")
            return False

        action = routed["action"]
        params = routed["params"]

        # OPEN CHROME
        if action == "open chrome":
            return self.executor.execute(
                action_name=action,
                role=role,
                risk=RiskLevel.LOW,
                action_function=lambda: self.apps.open_app("chrome"),
                confirmed=confirmed
            )

        # OPEN NOTEPAD
        if action == "open notepad":
            return self.executor.execute(
                action_name=action,
                role=role,
                risk=RiskLevel.LOW,
                action_function=lambda: self.apps.open_app("notepad"),
                confirmed=confirmed
            )

        # OPEN CALCULATOR
        if action == "open calculator":
            return self.executor.execute(
                action_name=action,
                role=role,
                risk=RiskLevel.LOW,
                action_function=lambda: self.apps.open_app("calculator"),
                confirmed=confirmed
            )

        # OPEN EXPLORER
        if action == "open explorer":
            return self.executor.execute(
                action_name=action,
                role=role,
                risk=RiskLevel.LOW,
                action_function=lambda: self.apps.open_app("explorer"),
                confirmed=confirmed
            )

        # CREATE FILE
        if action == "create file":
            filename = params["filename"]

            return self.executor.execute(
                action_name=action,
                role=role,
                risk=RiskLevel.MEDIUM,
                action_function=lambda: self.files.create_file(filename),
                confirmed=confirmed
            )

        # READ FILE
        if action == "read file":
            filename = params["filename"]
            result = self.files.read_file(filename)

            if result is None:
                return False

            print("\n--- FILE CONTENT ---")
            print(result)
            print("--- END FILE ---\n")
            return True

        # REMEMBER INFORMATION
        if action == "remember":
            key = params["key"]
            value = params["value"]

            return self.executor.execute(
                action_name=action,
                role=role,
                risk=RiskLevel.MEDIUM,
                action_function=lambda: self.memory.remember(key, value),
                confirmed=confirmed
            )

        # RECALL INFORMATION
        if action == "recall":
            key = params["key"]

            return self.executor.execute(
                action_name=action,
                role=role,
                risk=RiskLevel.LOW,
                action_function=lambda: self.memory.recall(key) is not None,
                confirmed=confirmed
            )

        # LIST SAVED MEMORIES

        # LIST SAVED MEMORIES
        if action == "list memories":
            return self.executor.execute(
                action_name=action,
                role=role,
                risk=RiskLevel.LOW,
                action_function=self.memory.list_memories,
                confirmed=confirmed
            )


        # FORGET A MEMORY
        if action == "forget":
            key = params["key"]

            return self.executor.execute(
                action_name=action,
                role=role,
                risk=RiskLevel.MEDIUM,
                action_function=lambda: self.memory.forget(key),
                confirmed=confirmed
            )

        # GOOGLE SEARCH
        if action == "google search":
            query = params["query"]

            try:
                self.browser.start()

                return self.executor.execute(
                    action_name=action,
                    role=role,
                    risk=RiskLevel.LOW,
                    action_function=lambda: self.browser.google_search(query),
                    confirmed=confirmed
                )
            finally:
                self.browser.close()

        # READ WEBPAGE
        if action == "read webpage":
            try:
                if self.browser.page is None:
                    print("Browser is not running.")
                    return False

                return self.executor.execute(
                    action_name=action,
                    role=role,
                    risk=RiskLevel.LOW,
                    action_function=lambda: self.browser.read_page(),
                    confirmed=confirmed
                )

            except Exception as error:
                print(f"Webpage reading error: {error}")
                return False

        print(f"UNSUPPORTED ACTION | {action}")
        return False
