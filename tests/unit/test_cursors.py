from typing import List
from unittest.mock import patch

import pytest
from pytest import fixture

from src.constants import QUERY_FILE_PATH
from src.cursors import ReadingsCursor
from src.models import PaginatedReadings, Reading, Settings
from tests.unit.constants import (
    ACCOUNT_NUMBER,
    ELECTRICITY_READING_FREQUENCY,
    END_AT,
    FIRST,
    GAS_READING_FREQUENCY,
    JWT,
    START_AT,
    URL,
)


@fixture
def readings_cursor() -> ReadingsCursor:
    settings = Settings(
        account_number=ACCOUNT_NUMBER,
        jwt=JWT,
        url=URL,
        start_at=START_AT,
        end_at=END_AT,
        first=FIRST,
        gas_reading_frequency=GAS_READING_FREQUENCY,
        electricity_reading_frequency=ELECTRICITY_READING_FREQUENCY,
    )
    return ReadingsCursor(settings, QUERY_FILE_PATH)


class TestReadingsCursor:
    @patch("src.cursors.get_paginated_readings")
    @pytest.mark.parametrize(
        "expected",
        [True, False],
        ids=["has_next_page_is_true", "has_next_page_is_false"],
    )
    def test_next_page_return_value(
        self, mock_method, readings_cursor: ReadingsCursor, expected: bool
    ) -> None:
        mock_method.return_value = PaginatedReadings(
            readings=[], has_next_page=expected
        )

        assert expected == readings_cursor.next_page()

    @patch("src.cursors.get_paginated_readings")
    def test_next_page_updates_gas_readings(
        self,
        mock_method,
        readings_cursor: ReadingsCursor,
        paginated_readings: PaginatedReadings,
        gas_readings: List[Reading],
    ) -> None:
        mock_method.return_value = paginated_readings

        readings_cursor.next_page()

        assert gas_readings == readings_cursor.gas_readings

    @patch("src.cursors.get_paginated_readings")
    def test_next_page_updates_electricity_readings(
        self,
        mock_method,
        readings_cursor: ReadingsCursor,
        paginated_readings: PaginatedReadings,
        electricity_readings: List[Reading],
    ) -> None:
        mock_method.return_value = paginated_readings

        readings_cursor.next_page()

        assert electricity_readings == readings_cursor.electricity_readings