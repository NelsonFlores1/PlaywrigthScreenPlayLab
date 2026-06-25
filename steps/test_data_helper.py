"""Helper module for generating random test data for ParaBank registration."""

import uuid
import random


def generate_user_data() -> dict:
    """Generate random user registration data with a unique username.

    Returns:
        Dictionary with keys matching RegisterUser Task expected input:
        first_name, last_name, address, city, state, zip_code, phone, ssn,
        username, password, confirm_password.
    """
    unique_id = uuid.uuid4().hex[:8]
    password = f"Test{unique_id}!"

    return {
        "first_name": f"Test{unique_id[:4]}",
        "last_name": f"User{unique_id[4:]}",
        "address": f"{random.randint(100, 9999)} Main St",
        "city": "Springfield",
        "state": "IL",
        "zip_code": f"{random.randint(10000, 99999)}",
        "phone": f"{random.randint(1000000000, 9999999999)}",
        "ssn": f"{random.randint(100000000, 999999999)}",
        "username": f"user_{unique_id}",
        "password": password,
        "confirm_password": password,
    }
