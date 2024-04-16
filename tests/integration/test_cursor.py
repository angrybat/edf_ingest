from datetime import datetime, timezone

from freezegun import freeze_time

from src.client import get_account_number, get_authorization_tokens
from src.constants import ACCOUNT_NUMBER_QUERY_FILE_PATH, ENV_FILE_PATH
from src.cursors import ReadingsCursor
from src.factories import get_settings


@freeze_time(datetime(2024, 5, 1, tzinfo=timezone.utc))
def test_cursor_can_refresh_its_jwt() -> None:
    env_file_path = ENV_FILE_PATH
    settings = get_settings(env_file_path)

    authorization_tokens = get_authorization_tokens(
        settings.url, settings.email_address, settings.password
    )
    account_number = get_account_number(
        settings.url, authorization_tokens.jwt, ACCOUNT_NUMBER_QUERY_FILE_PATH
    )
    readings_cursor = ReadingsCursor(settings, account_number, authorization_tokens)

    readings_cursor.next_page()

    assert authorization_tokens.jwt != readings_cursor.jwt
