import allure
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class NavigateTo:
    """Navigate the browser to a path relative to base URL."""

    def __init__(self, path: str, timeout: int = 30000):
        self._path = path
        self._timeout = timeout

    def perform_as(self, actor) -> None:
        with allure.step(f"Navigate to {self._path}"):
            ability = actor.ability
            target_url = f"{ability.base_url}/{self._path}"
            try:
                ability.page.goto(target_url, timeout=self._timeout)
                ability.page.wait_for_load_state("networkidle")
            except PlaywrightTimeoutError:
                raise TimeoutError(
                    f"Navigation failed: URL '{target_url}' unreachable "
                    f"after {self._timeout}ms."
                )
