import allure
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from screenplay.interactions.fill_field import FillField
from screenplay.interactions.select_option import SelectOption
from screenplay.interactions.click_element import ClickElement


class TransferFunds:
    """Task to execute a fund transfer between accounts."""

    AMOUNT_INPUT = "#amount"
    FROM_ACCOUNT_SELECT = "#fromAccountId"
    TO_ACCOUNT_SELECT = "#toAccountId"
    TRANSFER_BUTTON = "input[value='Transfer']"
    SUCCESS_MESSAGE = "text=Transfer Complete"

    def __init__(self, amount: str, from_account: str, to_account: str):
        self._amount = amount
        self._from_account = from_account
        self._to_account = to_account

    def perform_as(self, actor) -> None:
        with allure.step(f"Transfer {self._amount} from {self._from_account} to {self._to_account}"):
            actor.attempts_to(
                FillField(self.AMOUNT_INPUT, self._amount),
                SelectOption(self.FROM_ACCOUNT_SELECT, self._from_account),
                SelectOption(self.TO_ACCOUNT_SELECT, self._to_account),
                ClickElement(self.TRANSFER_BUTTON),
            )
            try:
                actor.ability.page.wait_for_selector(
                    self.SUCCESS_MESSAGE, timeout=10000
                )
            except PlaywrightTimeoutError:
                raise TimeoutError(
                    f"Transfer confirmation not received within 10s. "
                    f"URL: '{actor.ability.page.url}'"
                )
