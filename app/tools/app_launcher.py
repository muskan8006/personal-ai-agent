import subprocess


class AppLauncher:

    ALLOWED_APPS = {
        "chrome": [
            "cmd",
            "/c",
            "start",
            "",
            "chrome"
        ],

        "notepad": [
            "notepad.exe"
        ],

        "calculator": [
            "calc.exe"
        ],

        "explorer": [
            "explorer.exe"
        ],
    }

    def open_app(self, app_name: str) -> bool:

        app_name = app_name.lower().strip()

        if app_name not in self.ALLOWED_APPS:
            print(
                f"App not allowed: {app_name}"
            )
            return False

        try:
            subprocess.Popen(
                self.ALLOWED_APPS[app_name],
                shell=False
            )

            print(
                f"Application opened: {app_name}"
            )

            return True

        except Exception as error:
            print(
                f"Failed to open {app_name}: {error}"
            )
            return False