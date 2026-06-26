import allure
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from screenplay.interactions.fill_field import FillField
from screenplay.interactions.click_element import ClickElement


class RecuperaLogin:
    """Task to find login."""

    FIRST_NAME = "input[id='firstName']"
    LAST_NAME = "input[id='lastName']"
    ADDRESS = "input[id='address.street']"
    CITY = "input[id='address.city']"
    STATE = "input[id='address.state']"
    ZIP_CODE = "input[id='address.zipCode']"
    SSN = "input[id='ssn']"
    FIND_LOGIN_BUTTON = "input[value='Find My Login Info']"
    SUCCESS_MESSAGE = "text=Bill Payment Complete"

    def __init__(self, user_data: dict):
        self._user_data = user_data

    def perform_as(self, actor) -> None:
        with allure.step(f"Find login info for {self._user_data.get('first_name', 'user')}"):
            actor.attempts_to(
                FillField(self.FIRST_NAME, self._user_data["first_name"]),
                FillField(self.LAST_NAME, self._user_data["last_name"]),
                FillField(self.ADDRESS, self._user_data["address"]),
                FillField(self.CITY, self._user_data["city"]),
                FillField(self.STATE, self._user_data["state"]),
                FillField(self.ZIP_CODE, self._user_data["zip_code"]),
                FillField(self.SSN, self._user_data["ssn"]),
                ClickElement(self.FIND_LOGIN_BUTTON),
            )
            actor.ability.page.wait_for_load_state("networkidle")
