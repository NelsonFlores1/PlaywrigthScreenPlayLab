from playwright.sync_api import Page


class BrowseTheWeb:
    """Ability that grants an Actor access to a browser page."""

    DEFAULT_BASE_URL = "https://parabank.parasoft.com/parabank"

    def __init__(self, page: Page, base_url: str | None = None):
        self._page = page
        self._base_url = base_url or self.DEFAULT_BASE_URL

    @property
    def page(self) -> Page:
        """The Playwright Page instance."""
        return self._page

    @property
    def base_url(self) -> str:
        """The base URL for navigation."""
        return self._base_url
