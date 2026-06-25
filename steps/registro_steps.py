"""Step definitions for the registro_usuario.feature (user registration and account opening).

Uses the Screenplay Pattern with Actor, Tasks, Interactions, and Questions.
"""

import allure
from pytest_bdd import given, when, then, parsers

from screenplay.actors.actor import Actor
from screenplay.interactions.navigate_to import NavigateTo
from screenplay.tasks.register_user import RegisterUser
from screenplay.tasks.open_new_account import OpenNewAccount
from screenplay.questions.is_registration_successful import IsRegistrationSuccessful
from steps.test_data_helper import generate_user_data


# --- Registration Steps ---


@allure.feature("Registro")
@given("el usuario navega a la página de registro de ParaBank")
def navigate_to_registration(actor: Actor):
    """Navigate to the ParaBank registration page."""
    actor.attempts_to(NavigateTo("register.htm"))


@allure.feature("Registro")
@when("completa el formulario con datos de prueba generados")
def fill_registration_form(actor: Actor):
    """Fill the registration form with randomly generated test data."""
    user_data = generate_user_data()
    actor.attempts_to(RegisterUser(user_data))


@allure.feature("Registro")
@when("hace clic en el botón Register")
def click_register_button(actor: Actor):
    """Click the Register button to submit the form.

    Note: The RegisterUser task already clicks the Register button,
    so this step is a no-op to preserve Gherkin compatibility.
    """
    pass


@allure.feature("Registro")
@then("el sistema confirma que el usuario fue creado exitosamente")
def verify_registration_success(actor: Actor):
    """Verify that the registration was successful."""
    assert actor.asks_about(IsRegistrationSuccessful()), (
        "Registration failed: success message not displayed on the page."
    )


# --- Account Opening Steps ---


@allure.feature("Registro")
@when("el usuario navega a Open New Account")
def navigate_to_open_account(actor: Actor):
    """Navigate to the Open New Account page."""
    actor.attempts_to(NavigateTo("openaccount.htm"))


@allure.feature("Registro")
@when(parsers.parse('selecciona el tipo de cuenta "{account_type}"'), target_fixture="account_type")
def select_account_type(account_type: str):
    """Store the account type for use in the next step."""
    return account_type


@allure.feature("Registro")
@when("confirma la apertura de la cuenta")
def confirm_account_opening(actor: Actor, account_type: str):
    """Submit the account opening form with the selected account type."""
    actor.attempts_to(OpenNewAccount(account_type))


@allure.feature("Registro")
@then("el sistema crea la cuenta y muestra su número")
def verify_account_created(actor: Actor):
    """Verify the new account was created and its ID is displayed."""
    page = actor.ability.page
    page.wait_for_selector("#newAccountId", state="visible", timeout=10000)
    account_id = page.inner_text("#newAccountId")
    assert account_id, "Account creation failed: no account ID displayed."
    assert account_id.strip().isdigit(), (
        f"Account ID '{account_id}' is not a valid numeric string."
    )


@allure.feature("Registro")
@then("el entorno está listo para ejecutar los demás escenarios")
def environment_ready():
    """Confirm the environment is ready for subsequent scenarios.

    This step serves as a marker that the setup scenario completed successfully.
    No additional assertions needed beyond the previous steps passing.
    """
    pass
