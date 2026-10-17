import ctypes


class WindowsControl:

    def lock_screen(self) -> bool:
        try:
            result = ctypes.windll.user32.LockWorkStation()

            if result:
                print("Windows screen locked.")
                return True

            print("Failed to lock Windows.")
            return False

        except Exception as error:
            print(f"Windows lock error: {error}")
            return False