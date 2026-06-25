import allure
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class WaitForSelector:
    """Wait for an element to become visible."""

    def __init__(self, selector: str, timeout: int = 10000):
        self._selector = selector
        self._timeout = timeout

    def perform_as(self, actor) -> None:
        with allure.step(f"Wait for '{self._selector}' to be visible"):
            try:
                actor.ability.page.wait_for_selector(
                    self._selector, state="visible", timeout=self._timeout
                )
            except PlaywrightTimeoutError:
                raise TimeoutError(
                    f"Element '{self._selector}' not visible within "
                    f"{self._timeout}ms on page '{actor.ability.page.url}'"
                )
