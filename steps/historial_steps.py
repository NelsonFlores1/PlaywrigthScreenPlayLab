"""Step definitions for the account history scenario (historial_cuenta.feature).

Uses Screenplay Pattern with Actor fixture.
Validates: Requirements 2.1, 2.2, 2.3, 7.4, 6.5, 12.1-12.5, 9.4
"""

import allure
from pytest_bdd import when, then

from screenplay.actors.actor import Actor
from screenplay.tasks.view_account_history import ViewAccountHistory
from screenplay.questions.is_transaction_history_visible import IsTransactionHistoryVisible
from screenplay.questions.get_transactions import GetTransactions


@allure.feature("Historial de Cuenta")
@when("el usuario selecciona una cuenta desde el listado")
def select_account_from_list(actor: Actor):
    """Select the first account from the accounts overview list."""
    actor.attempts_to(ViewAccountHistory(0))


@then("el sistema muestra el historial de transacciones")
def verify_transaction_history_visible(actor: Actor):
    """Assert that the transaction history table is visible."""
    assert actor.asks_about(IsTransactionHistoryVisible()), (
        "Transaction history table is not visible after selecting an account."
    )


@then("se visualizan los movimientos realizados en la cuenta")
def verify_transaction_data_completeness(actor: Actor):
    """Verify that transactions are present and each has date and description.

    Retrieves the list of transactions and asserts:
    - At least one transaction exists
    - Each transaction has a non-empty date
    - Each transaction has a non-empty description
    """
    transactions = actor.asks_about(GetTransactions())

    assert len(transactions) > 0, (
        "No transactions found in the account history. "
        "Expected at least one transaction to be displayed."
    )

    for i, transaction in enumerate(transactions):
        assert transaction["date"], (
            f"Transaction at index {i} has an empty date field."
        )
        assert transaction["description"], (
            f"Transaction at index {i} has an empty description field."
        )
