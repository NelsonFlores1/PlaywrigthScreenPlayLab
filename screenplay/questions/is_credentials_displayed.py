import allure


class IsCredentialsDisplayed:
    """Question: Are the  recovered login?"""

    SUCCESS_TEXT = "Your account was created successfully"

    def answered_by(self, actor) -> bool:
        with allure.step("Check if recovered credencial displayed"):
            page= actor.ability.page
            if not  page.locator("h1").is_visible():
                return False
            
        resultado=page.locator("h1").inner_text()
        print(f"Testo Obtenido:  {resultado}")
        return "Error" in resultado
        
      