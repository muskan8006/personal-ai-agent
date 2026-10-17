from pathlib import Path


class FileManager:

    def __init__(self):
        self.workspace = Path("workspace")
        self.workspace.mkdir(exist_ok=True)

    def _safe_path(self, filename: str) -> Path:
        path = (self.workspace / filename).resolve()

        workspace_path = self.workspace.resolve()

        if workspace_path not in path.parents:
            raise ValueError("Unsafe file path")

        return path

    def create_file(self, filename: str, content: str = "") -> bool:
        try:
            path = self._safe_path(filename)

            if path.exists():
                print(f"File already exists: {filename}")
                return False

            path.write_text(content, encoding="utf-8")

            print(f"File created: {filename}")
            return True

        except Exception as error:
            print(f"File creation failed: {error}")
            return False

    def read_file(self, filename: str):
        try:
            path = self._safe_path(filename)

            if not path.exists():
                print(f"File not found: {filename}")
                return None

            content = path.read_text(encoding="utf-8")

            print(f"File read: {filename}")
            return content

        except Exception as error:
            print(f"File reading failed: {error}")
            return None

    def list_files(self):
        try:
            files = [
                file.name
                for file in self.workspace.iterdir()
                if file.is_file()
            ]

            print("Files:", files)
            return files

        except Exception as error:
            print(f"Could not list files: {error}")
            return []