import allure


class IsTransferSuccessful:
    """Question: Did the fund transfer complete successfully?"""

    def answered_by(self, actor) -> bool:
        with allure.step("Check if transfer was successful"):
            return actor.ability.page.is_visible("text=Transfer Complete")
