import allure


class IsLoggedIn:
    """Question: Is the user currently logged in?"""

    def answered_by(self, actor) -> bool:
        with allure.step("Check if user is logged in"):
            page = actor.ability.page
            if page.locator("h1.title:has-text('Accounts Overview')").is_visible():
                return True
            return page.locator("text=Welcome").first.is_visible()
