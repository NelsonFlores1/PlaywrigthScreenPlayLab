import allure
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class ClickElement:
    """Click an element identified by CSS selector."""

    def __init__(self, selector: str, timeout: int = 10000):
        self._selector = selector
        self._timeout = timeout

    def perform_as(self, actor) -> None:
        with allure.step(f"Click element '{self._selector}'"):
            try:
                actor.ability.page.click(self._selector, timeout=self._timeout)
            except PlaywrightTimeoutError:
                raise TimeoutError(
                    f"Click failed: element '{self._selector}' not found "
                    f"on page '{actor.ability.page.url}'"
                )
