import allure


class IsRegistrationSuccessful:
    """Question: Was the user registration successful?"""

    SUCCESS_TEXT = "Your account was created successfully"

    def answered_by(self, actor) -> bool:
        with allure.step("Check if registration was successful"):
            return actor.ability.page.is_visible(f"text={self.SUCCESS_TEXT}")
