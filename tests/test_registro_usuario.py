"""Test module for user registration and account opening scenarios.

Validates: Requirements 3.1, 3.2, 4.1, 4.2, 9.2, 9.4
"""
from pytest_bdd import scenarios

# Import step definitions so pytest-bdd can discover them
from steps.registro_steps import *  # noqa: F401, F403

# Load all scenarios from the feature file
scenarios("registro_usuario.feature")
