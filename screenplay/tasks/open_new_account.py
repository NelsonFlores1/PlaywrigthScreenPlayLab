import allure
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from screenplay.interactions.select_option import SelectOption
from screenplay.interactions.click_element import ClickElement


class OpenNewAccount:
    """Task to open a new bank account."""

    ACCOUNT_TYPE_DROPDOWN = "#type"
    SUBMIT_BUTTON = "input[value='Open New Account']"
    NEW_ACCOUNT_ID = "#newAccountId"
    ACCOUNT_TYPES = {"CHECKING": "0", "SAVINGS": "1"}

    def __init__(self, account_type: str):
        self._account_type = account_type.upper()

    def perform_as(self, actor) -> None:
        with allure.step(f"Open new {self._account_type} account"):
            value = self.ACCOUNT_TYPES[self._account_type]
            actor.attempts_to(
                SelectOption(self.ACCOUNT_TYPE_DROPDOWN, value),
                ClickElement(self.SUBMIT_BUTTON),
            )
            try:
                actor.ability.page.wait_for_selector(
                    self.NEW_ACCOUNT_ID, timeout=10000
                )
            except PlaywrightTimeoutError:
                raise TimeoutError(
                    f"Account creation failed: '{self.NEW_ACCOUNT_ID}' "
                    f"not found within 10s on page '{actor.ability.page.url}'"
                )
