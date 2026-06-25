import allure

from screenplay.interactions.fill_field import FillField
from screenplay.interactions.click_element import ClickElement


class Login:
    """Task to authenticate a user against ParaBank."""

    USERNAME_INPUT = "input[name='username']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BUTTON = "input[value='Log In']"

    def __init__(self, username: str, password: str):
        if not username or not username.strip():
            raise ValueError("Username is required and cannot be empty.")
        if not password or not password.strip():
            raise ValueError("Password is required and cannot be empty.")
        self._username = username
        self._password = password

    def perform_as(self, actor) -> None:
        with allure.step(f"Login as {self._username}"):
            actor.attempts_to(
                FillField(self.USERNAME_INPUT, self._username),
                FillField(self.PASSWORD_INPUT, self._password),
                ClickElement(self.LOGIN_BUTTON),
            )
            actor.ability.page.wait_for_load_state("networkidle")
