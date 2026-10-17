import re
class CommandRouter:

    def route(self, command: str):

        if not isinstance(command, str):
            return None

        command = command.strip().lower()

        if not command:
            return None

        # OPEN CHROME
        if (
            "open chrome" in command
            or "chrome kholo" in command
            or "chrome open" in command
        ):
            return {"action": "open chrome", "params": {}}

        # OPEN NOTEPAD
        if (
            "open notepad" in command
            or "notepad kholo" in command
            or "notepad open" in command
        ):
            return {"action": "open notepad", "params": {}}

        # OPEN CALCULATOR
        if (
            "open calculator" in command
            or "calculator kholo" in command
            or "calculator open" in command
        ):
            return {"action": "open calculator", "params": {}}

        # OPEN FILE EXPLORER
        if (
            "open explorer" in command
            or "explorer kholo" in command
            or "file explorer kholo" in command
        ):
            return {"action": "open explorer", "params": {}}

        # CREATE FILE
        create_file_patterns = [
            r"file banao (.+)",
            r"create file (.+)",
            r"file create karo (.+)",
        ]

        for pattern in create_file_patterns:
            match = re.fullmatch(pattern, command)

            if match:
                filename = match.group(1).strip()

                if filename:
                    return {
                        "action": "create file",
                        "params": {"filename": filename}
                    }

        # READ WEBPAGE
        if (
            "read webpage" in command
            or "webpage read karo" in command
            or "page read karo" in command
            or "page padho" in command
            or "webpage padho" in command
        ):
            return {"action": "read webpage", "params": {}}

        # READ FILE
        read_file_patterns = [
            r"read file (.+)",
            r"file read karo (.+)",
            r"(.+\.txt) read karo",
        ]

        for pattern in read_file_patterns:
            match = re.fullmatch(pattern, command)

            if match:
                filename = match.group(1).strip()

                if filename:
                    return {
                        "action": "read file",
                        "params": {"filename": filename}
                    }

        # GOOGLE SEARCH
        search_patterns = [
            r"google search (.+)",
            r"google par search karo (.+)",
            r"google pe search karo (.+)",
            r"search karo (.+)",
        ]

        for pattern in search_patterns:
            match = re.fullmatch(pattern, command)

            if match:
                query = match.group(1).strip()

                if query:
                    return {
                        "action": "google search",
                        "params": {"query": query}
                    }

        # LIST SAVED MEMORIES
        if command in (
            "what do you remember",
            "show memories",
            "list memories",
            "meri memories dikhao",
            "kya yaad hai",
        ):
            return {
                "action": "list memories",
                "params": {}
            }

        # FORGET A MEMORY
        forget_patterns = [
            r"forget my (.+)",
            r"forget (.+)",
            r"bhool jao my (.+)",
            r"meri (.+) bhool jao",
        ]

        for pattern in forget_patterns:
            match = re.fullmatch(pattern, command)

            if match:
                key = match.group(1).strip()

                if key:
                    return {
                        "action": "forget",
                        "params": {"key": key}
                    }

        # REMEMBER INFORMATION
        remember_patterns = [
            r"remember my (.+?) is (.+)",
            r"remember (.+?) is (.+)",
            r"yaad rakho my (.+?) is (.+)",
        ]

        for pattern in remember_patterns:
            match = re.fullmatch(pattern, command)

            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()

                if key and value:
                    return {
                        "action": "remember",
                        "params": {
                            "key": key,
                            "value": value
                        }
                    }

        # RECALL INFORMATION
        recall_patterns = [
            r"what is my (.+)",
            r"what's my (.+)",
            r"mere (.+) kya hai",
            r"batao my (.+)",
        ]

        for pattern in recall_patterns:
            match = re.fullmatch(pattern, command)

            if match:
                key = match.group(1).strip()

                if key:
                    return {
                        "action": "recall",
                        "params": {"key": key}
                    }

        return None
