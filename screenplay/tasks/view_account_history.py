import allure
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from screenplay.interactions.click_element import ClickElement


class ViewAccountHistory:
    """Task to view transaction history for a specific account."""

    ACCOUNT_LINKS = "#accountTable tbody tr td a"
    TRANSACTION_TABLE = "#transactionTable"

    def __init__(self, account_index: int = 0):
        self._account_index = account_index

    def perform_as(self, actor) -> None:
        with allure.step(f"View history for account at index {self._account_index}"):
            page = actor.ability.page
            page.wait_for_selector(self.ACCOUNT_LINKS, timeout=10000)
            links = page.query_selector_all(self.ACCOUNT_LINKS)
            if self._account_index >= len(links):
                raise IndexError(
                    f"Account index {self._account_index} out of range. "
                    f"Only {len(links)} accounts found."
                )
            links[self._account_index].click()
            page.wait_for_load_state("networkidle")
            try:
                page.wait_for_selector(
                    self.TRANSACTION_TABLE, state="visible", timeout=10000
                )
            except PlaywrightTimeoutError:
                raise TimeoutError(
                    f"Transaction table '{self.TRANSACTION_TABLE}' not visible "
                    f"within 10s on page '{page.url}'"
                )
