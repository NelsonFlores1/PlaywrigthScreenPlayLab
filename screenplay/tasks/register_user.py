import allure

from screenplay.interactions.fill_field import FillField
from screenplay.interactions.click_element import ClickElement


class RegisterUser:
    """Task to register a new user on ParaBank."""

    FIELDS = {
        "first_name": "input[id='customer.firstName']",
        "last_name": "input[id='customer.lastName']",
        "address": "input[id='customer.address.street']",
        "city": "input[id='customer.address.city']",
        "state": "input[id='customer.address.state']",
        "zip_code": "input[id='customer.address.zipCode']",
        "phone": "input[id='customer.phoneNumber']",
        "ssn": "input[id='customer.ssn']",
        "username": "input[id='customer.username']",
        "password": "input[id='customer.password']",
        "confirm_password": "input[id='repeatedPassword']",
    }
    REGISTER_BUTTON = "input[value='Register']"

    def __init__(self, user_data: dict):
        self._user_data = user_data
        self._username = user_data.get("username", "unknown")

    def perform_as(self, actor) -> None:
        with allure.step(f"Register user {self._username}"):
            for field_key, selector in self.FIELDS.items():
                actor.attempts_to(
                    FillField(selector, self._user_data[field_key])
                )
            actor.attempts_to(ClickElement(self.REGISTER_BUTTON))
            actor.ability.page.wait_for_load_state("networkidle")
