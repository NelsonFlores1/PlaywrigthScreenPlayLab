"""Step definitions for the fund transfer scenario using Screenplay Pattern.

Maps Spanish Gherkin steps to Screenplay Tasks, Interactions, and Questions.
Validates: Requirements 6.1, 6.2, 6.5, 9.4, 12.1-12.5
"""

import allure
from pytest_bdd import when, then, parsers

from screenplay.actors.actor import Actor
from screenplay.interactions.navigate_to import NavigateTo
from screenplay.tasks.transfer_funds import TransferFunds
from screenplay.questions.is_transfer_successful import IsTransferSuccessful


# Module-level state to share data between steps
_transfer_state: dict = {}


@allure.feature("Transferencia de Fondos")
@when(parsers.parse('el usuario navega a la opción "{option}"'))
def navigate_to_transfer_funds(actor: Actor, option: str):
    """Navigate to the Transfer Funds page."""
    actor.attempts_to(NavigateTo("transfer.htm"))


@when("selecciona la cuenta origen")
def select_source_account(actor: Actor):
    """Select the first available account as the source (origin) account.

    Reads dropdown options from the page and stores the selected account
    for use in the transfer confirmation step.
    """
    page = actor.ability.page
    from_options = page.locator("#fromAccountId option")
    from_options.first.wait_for(state="attached")
    first_account = from_options.first.get_attribute("value")
    page.select_option("#fromAccountId", first_account)
    _transfer_state["from_account"] = first_account


@when("selecciona la cuenta destino")
def select_destination_account(actor: Actor):
    """Select the second available account as the destination account.

    Reads dropdown options and picks the second option to ensure it
    differs from the source account when possible.
    """
    page = actor.ability.page
    to_options = page.locator("#toAccountId option")
    to_options.first.wait_for(state="attached")
    option_count = to_options.count()

    if option_count > 1:
        second_account = to_options.nth(1).get_attribute("value")
    else:
        second_account = to_options.first.get_attribute("value")

    page.select_option("#toAccountId", second_account)
    _transfer_state["to_account"] = second_account


@when(parsers.parse('ingresa un monto válido "{amount}"'))
def enter_transfer_amount(actor: Actor, amount: str):
    """Store the transfer amount for the confirmation step."""
    _transfer_state["amount"] = amount


@when("confirma la transferencia")
def confirm_transfer(actor: Actor):
    """Execute the fund transfer using the TransferFunds Task."""
    amount = _transfer_state.get("amount", "100")
    from_account = _transfer_state.get("from_account", "")
    to_account = _transfer_state.get("to_account", "")
    actor.attempts_to(TransferFunds(amount, from_account, to_account))


@then("el sistema muestra el mensaje de transferencia exitosa")
def verify_transfer_success_message(actor: Actor):
    """Verify that the transfer was successful using the IsTransferSuccessful Question."""
    assert actor.asks_about(IsTransferSuccessful()), (
        "Expected 'Transfer Complete' success message was not displayed."
    )
