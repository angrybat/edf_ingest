from pathlib import Path

from src.client import get_account_number, get_paginated_readings
from src.constants import (
    ACCOUNT_NUMBER_QUERY_FILE_PATH,
    GET_READINGS_QUERY_FILE_PATH,
)
    ACCOUNT_NUMBER_QUERY_FILE_PATH,
    GET_READINGS_QUERY_FILE_PATH,
)
from src.factories import get_settings, get_variables
from src.models import PaginatedReadings


def test_can_retrieve_paginated_readings() -> None:
    env_file_path = Path("env.json")
    settings = get_settings(env_file_path)
    account_number = get_account_number(
        settings.url, settings.jwt, ACCOUNT_NUMBER_QUERY_FILE_PATH
    )
    variables = get_variables(settings, account_number)
    paginated_readings = get_paginated_readings(
        settings.url, settings.jwt, GET_READINGS_QUERY_FILE_PATH, variables
    )

    assert isinstance(paginated_readings, PaginatedReadings)
