import webbrowser
from urllib.parse import urlparse


class BrowserTool:

    ALLOWED_SCHEMES = {"http", "https"}

    def open_url(self, url: str) -> bool:

        url = url.strip()

        try:
            parsed = urlparse(url)

            if parsed.scheme not in self.ALLOWED_SCHEMES:
                print("Blocked: only HTTP/HTTPS URLs are allowed.")
                return False

            if not parsed.netloc:
                print("Invalid URL.")
                return False

            webbrowser.open(url)

            print(f"Browser opened: {url}")
            return True

        except Exception as error:
            print(f"Browser error: {error}")
            return False