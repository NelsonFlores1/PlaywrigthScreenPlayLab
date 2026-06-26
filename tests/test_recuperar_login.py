"""Test module for login recovery
"""
from pytest_bdd import scenarios

# Import step definitions so pytest-bdd can discover them
from steps.recupeara_login_steps import *  # noqa: F401, F403

# Load all scenarios from the feature file
scenarios("recuperar_login.feature")
