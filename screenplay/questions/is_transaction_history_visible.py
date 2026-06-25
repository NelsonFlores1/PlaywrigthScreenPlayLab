import allure
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class IsTransactionHistoryVisible:
    """Question: Is the transaction history table visible?"""

    TRANSACTION_TABLE = "#transactionTable"

    def answered_by(self, actor) -> bool:
        with allure.step("Check if transaction history is visible"):
            try:
                actor.ability.page.wait_for_selector(
                    self.TRANSACTION_TABLE, state="visible", timeout=10000
                )
                return True
            except PlaywrightTimeoutError:
                return False
