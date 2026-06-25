import allure


class FillField:
    """Fill a form field identified by CSS selector."""

    def __init__(self, selector: str, value: str):
        self._selector = selector
        self._value = value

    def perform_as(self, actor) -> None:
        with allure.step(f"Fill '{self._selector}' with '{self._value}'"):
            page = actor.ability.page
            page.fill(self._selector, self._value)
