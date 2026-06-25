"""Test module for fund transfer scenarios.

Wires pytest-bdd scenarios from transferencia_fondos.feature to step definitions
in login_steps and transferencia_steps.

Validates: Requirements 5.1, 5.2, 5.5, 9.2, 9.4
"""
from pytest_bdd import scenarios

# Import step definitions so pytest-bdd can discover them
from steps.login_steps import *  # noqa: F401, F403
from steps.transferencia_steps import *  # noqa: F401, F403

# Load all scenarios from the feature file
scenarios("transferencia_fondos.feature")
