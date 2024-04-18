from src.client import (
    get_account_number,
    get_authorization_tokens,
    get_paginated_readings,
    refresh_authorization_tokens,
)
from src.constants import ENV_FILE_PATH
from src.factories import get_readings_variables, get_settings
from src.models import AuthorizationTokens, PaginatedReadings


def test_can_retrieve_paginated_readings() -> None:
    env_file_path = ENV_FILE_PATH
    settings = get_settings(env_file_path)

    authorization_tokens = get_authorization_tokens(
        settings.url,
        settings.email_address,
        settings.password,
        settings.get_jwt_query_file_path,
    )
    account_number = get_account_number(
        settings.url,
        authorization_tokens.jwt,
        settings.get_account_number_query_file_path,
    )
    variables = get_readings_variables(settings, account_number)
    paginated_readings = get_paginated_readings(
        settings.url,
        authorization_tokens.jwt,
        settings.get_readings_query_file_path,
        variables,
    )

    assert isinstance(paginated_readings, PaginatedReadings)


def test_can_refresh_authorization_tokens() -> None:
    env_file_path = ENV_FILE_PATH
    settings = get_settings(env_file_path)
    authorization_tokens = get_authorization_tokens(
        settings.url,
        settings.email_address,
        settings.password,
        settings.get_jwt_query_file_path,
    )

    refreshed_tokens = refresh_authorization_tokens(
        settings.url,
        authorization_tokens.refresh_token,
        settings.get_jwt_query_file_path,
    )

    assert isinstance(refreshed_tokens, AuthorizationTokens)
