from pathlib import Path

from src.client import get_account_name, get_paginated_readings
from src.constants import ACCOUNT_NAME_QUERY_FILE_PATH, QUERY_FILE_PATH
from src.factories import get_settings, get_variables
from src.models import PaginatedReadings


def test_api_call_does_not_throw_error() -> None:
    env_file_path = Path("env.json")
    settings = get_settings(env_file_path)
    variables = get_variables(settings)
    paginated_readings = get_paginated_readings(
        settings.url, settings.jwt, QUERY_FILE_PATH, variables
    )

    assert isinstance(paginated_readings, PaginatedReadings)


def test_get_account_name_does_not_return_an_empty_string() -> None:
    env_file_path = Path("env.json")
    settings = get_settings(env_file_path)
    account_name = get_account_name(
        settings.url, settings.jwt, ACCOUNT_NAME_QUERY_FILE_PATH
    )

    assert "" != account_name
