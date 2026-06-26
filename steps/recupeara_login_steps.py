import allure
from pytest_bdd import given, when, then, parsers
from screenplay.actors.actor import Actor
from screenplay.interactions.navigate_to import NavigateTo
from screenplay.questions.is_credentials_displayed import IsCredentialsDisplayed
from screenplay.tasks.recuperar_login import RecuperaLogin
from steps.test_data_helper import static_user_data

# --- Registration Steps ---
@allure.feature("Recuperar Login")
@given("el usuario navega a la pagina de recuperacion de login")
def navigate_to_forgot(actor: Actor):
    """Navigate to the ParaBank registration page."""
    actor.attempts_to(NavigateTo("lookup.htm"))


@allure.feature("Recuperar Login")
@when("completa el formulario de búsqueda con sus datos personales")
def fill_search_form(actor: Actor):
    """Fill the registration form with randomly generated test data."""
    user_data = static_user_data()
    actor.attempts_to(RecuperaLogin(user_data))


@allure.feature("Recuperar Login")
@when("hace clic en el botón Find My Login Info")
def click_find_button(actor: Actor):
    """Click the Register button to submit the form.

    Note: The RegisterUser task already clicks the Register button,
    so this step is a no-op to preserve Gherkin compatibility.
    """
    pass


@allure.feature("Recuperar Login")
@then("el sistema muestra las credenciales recuperadas")
def verify_result_success(actor: Actor):
    """Verify that the registration was successful."""
    assert actor.asks_about(IsCredentialsDisplayed()), (
        "Login recovery failed: Credential not displayed on the page."
    )
