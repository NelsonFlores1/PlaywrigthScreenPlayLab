import allure


class SelectOption:
    """Select an option from a dropdown by value."""

    def __init__(self, selector: str, value: str):
        self._selector = selector
        self._value = value

    def perform_as(self, actor) -> None:
        with allure.step(f"Select '{self._value}' from '{self._selector}'"):
            actor.ability.page.select_option(self._selector, self._value)
