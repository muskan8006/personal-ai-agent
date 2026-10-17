from playwright.sync_api import sync_playwright


class PlaywrightBrowser:

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    def start(self):
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False
        )

        self.page = self.browser.new_page()

        # Increase timeout from default 30 seconds
        self.page.set_default_timeout(10000)
        self.page.set_default_navigation_timeout(60000)

        print("Browser started.")

    def open_url(self, url: str) -> bool:

        if self.page is None:
            print("Browser is not started.")
            return False

        if not url.startswith(("http://", "https://")):
            print("Blocked: invalid URL scheme.")
            return False

        try:
            response = self.page.goto(
                url,
                wait_until="commit",
                timeout=60000
            )

            print(f"Opened: {url}")

            if response:
                print(f"HTTP status: {response.status}")

            print(f"Title: {self.page.title()}")

            return True

        except Exception as error:
            print(f"Browser error: {error}")
            return False

    def google_search(self, query: str) -> bool:

        if self.page is None:
            print("Browser is not started.")
            return False

        query = query.strip()

        if not query:
            print("Search query cannot be empty.")
            return False

        try:
            self.page.goto(
                "https://www.google.com",
                wait_until="commit",
                timeout=60000
            )

            search_box = self.page.locator(
                "textarea[name='q'], input[name='q']"
            ).first

            search_box.fill(query)
            search_box.press("Enter")

            self.page.wait_for_load_state(
                "domcontentloaded",
                timeout=30000
            )

            print(f"Search completed: {query}")
            print(f"Title: {self.page.title()}")

            return True

        except Exception as error:
            print(f"Search error: {error}")
            return False

    def read_page(self, max_chars: int = 3000):

        if self.page is None:
            print("Browser is not started.")
            return None

        try:
            self.page.wait_for_selector(
                "body",
                timeout=15000
            )

            text = self.page.locator("body").inner_text()

            text = " ".join(text.split())

            if len(text) > max_chars:
                text = text[:max_chars] + "..."

            print("\n--- PAGE CONTENT ---")
            print(text)
            print("--- END CONTENT ---\n")

            return text

        except Exception as error:
            print(f"Page reading error: {error}")
            return None

    def close(self):

        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()

        self.browser = None
        self.page = None
        self.playwright = None

        print("Browser closed.")