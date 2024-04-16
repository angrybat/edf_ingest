from datetime import datetime, timezone
from typing import List
from unittest.mock import patch

import pytest
from freezegun import freeze_time
from pytest import fixture

from src.cursors import ReadingsCursor
from src.models import AuthorizationTokens, PaginatedReadings, Reading, Settings
from tests.unit.constants import (
    ACCOUNT_NUMBER,
    CURSOR,
    ELECTRICITY_READING_FREQUENCY,
    EMAIL_ADDRESS,
    END_AT,
    EXPIRES_AT,
    FIRST,
    GAS_READING_FREQUENCY,
    JWT,
    PASSWORD,
    REFRESH_EXPIRES_IN,
    REFRESH_TOKEN,
    START_AT,
    URL,
)


@fixture
def authorization_tokens() -> AuthorizationTokens:
    return AuthorizationTokens(
        jwt=JWT,
        expires_at=EXPIRES_AT,
        refresh_token=REFRESH_TOKEN,
        refresh_expires_in=REFRESH_EXPIRES_IN,
    )


@fixture
def readings_cursor(authorization_tokens: AuthorizationTokens) -> ReadingsCursor:
    settings = Settings(
        email_address=EMAIL_ADDRESS,
        password=PASSWORD,
        jwt=JWT,
        url=URL,
        start_at=START_AT,
        end_at=END_AT,
        first=FIRST,
        gas_reading_frequency=GAS_READING_FREQUENCY,
        electricity_reading_frequency=ELECTRICITY_READING_FREQUENCY,
    )
    return ReadingsCursor(settings, ACCOUNT_NUMBER, authorization_tokens)


class TestReadingsCursor:
    @patch("src.cursors.get_paginated_readings")
    @freeze_time(datetime(2024, 3, 1, tzinfo=timezone.utc))
    @pytest.mark.parametrize(
        "expected",
        [True, False],
        ids=["has_next_page_is_true", "has_next_page_is_false"],
    )
    def test_next_page_return_value(
        self,
        mock_get_paginated_readings,
        readings_cursor: ReadingsCursor,
        expected: bool,
    ) -> None:
        mock_get_paginated_readings.return_value = PaginatedReadings(
            readings=[], has_next_page=expected, cursor=CURSOR
        )

        assert expected == readings_cursor.next_page()

    @patch("src.cursors.get_paginated_readings")
    @freeze_time(datetime(2024, 3, 1, tzinfo=timezone.utc))
    def test_next_page_updates_gas_readings(
        self,
        mock_get_paginated_readings,
        readings_cursor: ReadingsCursor,
        paginated_readings: PaginatedReadings,
        gas_readings: List[Reading],
    ) -> None:
        mock_get_paginated_readings.return_value = paginated_readings

        readings_cursor.next_page()

        assert gas_readings == readings_cursor.gas_readings

    @patch("src.cursors.get_paginated_readings")
    @freeze_time(datetime(2024, 3, 1, tzinfo=timezone.utc))
    def test_next_page_updates_electricity_readings(
        self,
        mock_get_paginated_readings,
        readings_cursor: ReadingsCursor,
        paginated_readings: PaginatedReadings,
        electricity_readings: List[Reading],
    ) -> None:
        mock_get_paginated_readings.return_value = paginated_readings

        readings_cursor.next_page()

        assert electricity_readings == readings_cursor.electricity_readings

    @patch("src.cursors.get_paginated_readings")
    @freeze_time(datetime(2024, 3, 1, tzinfo=timezone.utc))
    def test_next_page_updates_the_after_variable_to_the_end_cursor(
        self,
        mock_get_paginated_readings,
        readings_cursor: ReadingsCursor,
        paginated_readings: PaginatedReadings,
    ) -> None:
        mock_get_paginated_readings.return_value = paginated_readings

        readings_cursor.next_page()

        assert CURSOR == readings_cursor.variables.after

    @patch("src.cursors.refresh_authorization_tokens")
    @patch("src.cursors.get_paginated_readings")
    @freeze_time(datetime(2024, 4, 1, 1, 2, 0, tzinfo=timezone.utc))
    def test_calls_refresh_authorization_tokens_when_jwt_has_expired(
        self,
        mock_get_paginated_readings,
        mock_refresh_authorization_tokens,
        readings_cursor: ReadingsCursor,
        paginated_readings: PaginatedReadings,
    ) -> None:
        refreshed_tokens = AuthorizationTokens(
            jwt="RefreshedJwt",
            expires_at=datetime(2024, 5, 1, 1, tzinfo=timezone.utc),
            refresh_token="RefreshedRefreshToken",
            refresh_expires_in=datetime(2024, 5, 5, tzinfo=timezone.utc),
        )
        mock_get_paginated_readings.return_value = paginated_readings
        mock_refresh_authorization_tokens.return_value = refreshed_tokens

        readings_cursor.next_page()

        assert refreshed_tokens.jwt == readings_cursor.jwt

    @patch("src.cursors.get_authorization_tokens")
    @patch("src.cursors.refresh_authorization_tokens")
    @patch("src.cursors.get_paginated_readings")
    @freeze_time(datetime(2024, 5, 1, tzinfo=timezone.utc))
    def test_calls_get_authorization_tokens_when_jwt_and_refresh_token_has_expired(
        self,
        mock_get_paginated_readings,
        mock_refresh_authorization_tokens,
        mock_get_authorization_tokens,
        readings_cursor: ReadingsCursor,
        paginated_readings: PaginatedReadings,
    ) -> None:
        refreshed_tokens = AuthorizationTokens(
            jwt="RefreshedJwt",
            expires_at=datetime(2024, 5, 1, 1, tzinfo=timezone.utc),
            refresh_token="RefreshedRefreshToken",
            refresh_expires_in=datetime(2024, 5, 5, tzinfo=timezone.utc),
        )
        new_authorization_tokens = AuthorizationTokens(
            jwt="NewJwt",
            expires_at=datetime(2024, 7, 1, 1, tzinfo=timezone.utc),
            refresh_token="NewRefreshToken",
            refresh_expires_in=datetime(2024, 7, 5, tzinfo=timezone.utc),
        )
        mock_get_paginated_readings.return_value = paginated_readings
        mock_refresh_authorization_tokens.return_value = refreshed_tokens
        mock_get_authorization_tokens.return_value = new_authorization_tokens

        readings_cursor.next_page()

        assert new_authorization_tokens.jwt == readings_cursor.jwt
