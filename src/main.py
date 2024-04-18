from pathlib import Path

from src.client import get_account_number, get_authorization_tokens
from src.cursors import ReadingsCursor
from src.factories import get_settings


def get_readings_cursor(settings_file_path: Path) -> Path:
    settings = get_settings(settings_file_path)
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
    return ReadingsCursor(settings, account_number, authorization_tokens)
