"""Shared login step definitions using Screenplay Pattern.

Validates: Requirements 1.1, 1.2, 7.4, 9.4, 12.1-12.5
"""
import allure
from pytest_bdd import given, when, then, parsers

from screenplay.actors.actor import Actor
from screenplay.interactions.navigate_to import NavigateTo
from screenplay.tasks.login import Login
from screenplay.questions.is_logged_in import IsLoggedIn


@allure.feature("Autenticación")
@given("el usuario se encuentra en la página de login de ParaBank")
def navigate_to_login_page(actor: Actor):
    """Navigate the browser to the ParaBank login page."""
    actor.attempts_to(NavigateTo("index.htm"))


@when(
    parsers.parse('ingresa el usuario "{username}" y la contraseña "{password}"'),
    target_fixture="login_result",
)
def enter_credentials(actor: Actor, username: str, password: str):
    """Fill in credentials and submit the login form."""
    actor.attempts_to(Login(username, password))


@then("el sistema muestra el dashboard de la cuenta")
def verify_dashboard_displayed(actor: Actor):
    """Assert that the user is logged in and the account dashboard is visible."""
    assert actor.asks_about(IsLoggedIn()), (
        "Login failed: the account dashboard is not displayed."
    )
