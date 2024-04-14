from pathlib import Path

from src.client import get_account_number, get_credentials, get_paginated_readings
from src.constants import (
    ACCOUNT_NUMBER_QUERY_FILE_PATH,
    ENV_FILE_PATH,
    GET_READINGS_QUERY_FILE_PATH,
)
from src.factories import get_readings_variables, get_settings
from src.models import Credentials, PaginatedReadings


def test_can_retrieve_paginated_readings() -> None:
    env_file_path = Path(ENV_FILE_PATH)
    settings = get_settings(env_file_path)
    account_number = get_account_number(
        settings.url, settings.jwt, ACCOUNT_NUMBER_QUERY_FILE_PATH
    )
    variables = get_readings_variables(settings, account_number)
    paginated_readings = get_paginated_readings(
        settings.url, settings.jwt, GET_READINGS_QUERY_FILE_PATH, variables
    )

    assert isinstance(paginated_readings, PaginatedReadings)


def test_can_retrieve_credentials() -> None:
    env_file_path = Path(ENV_FILE_PATH)
    settings = get_settings(env_file_path)

    credentials = get_credentials(
        settings.url, settings.email_address, settings.password
    )

    assert isinstance(credentials, Credentials)
