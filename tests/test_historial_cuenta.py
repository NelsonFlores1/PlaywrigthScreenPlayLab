"""Test module for account history scenarios.

Wires pytest-bdd scenarios from historial_cuenta.feature to step definitions.
Validates: Requirements 2.1, 2.2, 2.3, 9.2, 9.4
"""
from pytest_bdd import scenarios

# Import step definitions so pytest-bdd can discover them
from steps.login_steps import *  # noqa: F401, F403
from steps.historial_steps import *  # noqa: F401, F403

# Load all scenarios from the feature file
scenarios("historial_cuenta.feature")
