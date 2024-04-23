from datetime import datetime, timezone
from json import dump
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from freezegun import freeze_time

from src.constants import (
    DATETIME_FORMAT,
    GET_ACCOUNT_NUMBER_QUERY_FILE_PATH,
    GET_JWT_QUERY_FILE_PATH,
    GET_READINGS_QUERY_FILE_PATH,
)
from src.cursors import ReadingsCursor
from src.main import get_readings, get_readings_cursor
from src.models import (
    AuthorizationTokens,
    Cost,
    CostType,
    Reading,
    Readings,
    ReadingType,
    Settings,
)
from tests.unit.constants import (
    ACCOUNT_NUMBER,
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


class TestGetReadingsCursor:
    @patch("src.main.get_authorization_tokens")
    @patch("src.main.get_account_number")
    def test_creates_cursor_from_file(
        self, mock_get_account_number: Mock, mock_get_authorization_tokens: Mock
    ) -> None:
        with TemporaryDirectory() as temp_dir:
            env_file_path = Path(temp_dir) / "env.json"
            authorization_tokens = AuthorizationTokens(
                jwt=JWT,
                expires_at=EXPIRES_AT,
                refresh_token=REFRESH_TOKEN,
                refresh_expires_in=REFRESH_EXPIRES_IN,
            )
            settings_file_contents = {
                "email_address": EMAIL_ADDRESS,
                "password": PASSWORD,
                "url": URL,
                "start_at": START_AT.strftime(DATETIME_FORMAT),
                "end_at": END_AT.strftime(DATETIME_FORMAT),
                "first": FIRST,
                "gas_reading_frequency": GAS_READING_FREQUENCY.value,
                "electricity_reading_frequency": ELECTRICITY_READING_FREQUENCY.value,
                "get_readings_query_file_path": str(GET_READINGS_QUERY_FILE_PATH),
                "get_jwt_query_file_path": str(GET_JWT_QUERY_FILE_PATH),
                "get_account_number_query_file_path": str(
                    GET_ACCOUNT_NUMBER_QUERY_FILE_PATH
                ),
            }
            mock_get_account_number.return_value = ACCOUNT_NUMBER
            mock_get_authorization_tokens.return_value = authorization_tokens
            with open(env_file_path, "w") as env_file:
                dump(settings_file_contents, env_file)

            readings_cursor = get_readings_cursor(env_file_path)

        settings = Settings(
            email_address=EMAIL_ADDRESS,
            password=PASSWORD,
            url=URL,
            start_at=START_AT,
            end_at=END_AT,
            first=FIRST,
            gas_reading_frequency=GAS_READING_FREQUENCY,
            electricity_reading_frequency=ELECTRICITY_READING_FREQUENCY,
            get_account_number_query_file_path=GET_ACCOUNT_NUMBER_QUERY_FILE_PATH,
            get_jwt_query_file_path=GET_JWT_QUERY_FILE_PATH,
            get_readings_query_file_path=GET_READINGS_QUERY_FILE_PATH,
        )
        expected = ReadingsCursor(
            settings=settings,
            account_number=ACCOUNT_NUMBER,
            authorization_tokens=authorization_tokens,
        )
        assert expected.variables == readings_cursor.variables
        assert expected.url == readings_cursor.url
        assert expected.email_address == readings_cursor.email_address
        assert expected.password == readings_cursor.password
        assert (
            expected.get_readings_query_file_path
            == readings_cursor.get_readings_query_file_path
        )
        assert (
            expected.get_jwt_query_file_path == readings_cursor.get_jwt_query_file_path
        )
        assert expected.jwt == readings_cursor.jwt
        assert expected.jwt_expires_at == readings_cursor.jwt_expires_at
        assert expected.refresh_token == readings_cursor.refresh_token
        assert (
            expected.refresh_token_expires_at
            == readings_cursor.refresh_token_expires_at
        )


class TestGetReadings:
    def test_correct_readings_are_returned(self) -> None:
        gas_readings = [
            Reading(
                start_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
                end_at=datetime(2024, 1, 2, tzinfo=timezone.utc),
                unit="kwh",
                value=1,
                costs=[
                    Cost(amount=10, currency="GBP", type=CostType.CONSUMPTION_COST),
                    Cost(amount=10, currency="GBP", type=CostType.STANDING_CHARGE_COST),
                ],
                type=ReadingType.GAS,
            ),
            Reading(
                start_at=datetime(2024, 1, 2, tzinfo=timezone.utc),
                end_at=datetime(2024, 1, 3, tzinfo=timezone.utc),
                unit="kwh",
                value=2,
                costs=[
                    Cost(amount=20, currency="GBP", type=CostType.CONSUMPTION_COST),
                    Cost(amount=20, currency="GBP", type=CostType.STANDING_CHARGE_COST),
                ],
                type=ReadingType.GAS,
            ),
            Reading(
                start_at=datetime(2024, 1, 3, tzinfo=timezone.utc),
                end_at=datetime(2024, 1, 4, tzinfo=timezone.utc),
                unit="kwh",
                value=3,
                costs=[
                    Cost(amount=30, currency="GBP", type=CostType.CONSUMPTION_COST),
                    Cost(amount=30, currency="GBP", type=CostType.STANDING_CHARGE_COST),
                ],
                type=ReadingType.GAS,
            ),
            Reading(
                start_at=datetime(2024, 1, 4, tzinfo=timezone.utc),
                end_at=datetime(2024, 1, 5, tzinfo=timezone.utc),
                unit="kwh",
                value=4,
                costs=[
                    Cost(amount=40, currency="GBP", type=CostType.CONSUMPTION_COST),
                    Cost(amount=40, currency="GBP", type=CostType.STANDING_CHARGE_COST),
                ],
                type=ReadingType.GAS,
            ),
            Reading(
                start_at=datetime(2024, 1, 5, tzinfo=timezone.utc),
                end_at=datetime(2024, 1, 6, tzinfo=timezone.utc),
                unit="kwh",
                value=5,
                costs=[
                    Cost(amount=50, currency="GBP", type=CostType.CONSUMPTION_COST),
                    Cost(amount=50, currency="GBP", type=CostType.STANDING_CHARGE_COST),
                ],
                type=ReadingType.GAS,
            ),
            Reading(
                start_at=datetime(2024, 1, 6, tzinfo=timezone.utc),
                end_at=datetime(2024, 1, 7, tzinfo=timezone.utc),
                unit="kwh",
                value=6,
                costs=[
                    Cost(amount=60, currency="GBP", type=CostType.CONSUMPTION_COST),
                    Cost(amount=60, currency="GBP", type=CostType.STANDING_CHARGE_COST),
                ],
                type=ReadingType.GAS,
            ),
        ]
        electricity_readings = [
            Reading(
                start_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
                end_at=datetime(2024, 1, 2, tzinfo=timezone.utc),
                unit="kwh",
                value=1,
                costs=[
                    Cost(amount=10, currency="GBP", type=CostType.CONSUMPTION_COST),
                    Cost(amount=10, currency="GBP", type=CostType.STANDING_CHARGE_COST),
                ],
                type=ReadingType.ELECTRICITY,
            ),
            Reading(
                start_at=datetime(2024, 1, 2, tzinfo=timezone.utc),
                end_at=datetime(2024, 1, 3, tzinfo=timezone.utc),
                unit="kwh",
                value=2,
                costs=[
                    Cost(amount=20, currency="GBP", type=CostType.CONSUMPTION_COST),
                    Cost(amount=20, currency="GBP", type=CostType.STANDING_CHARGE_COST),
                ],
                type=ReadingType.ELECTRICITY,
            ),
            Reading(
                start_at=datetime(2024, 1, 3, tzinfo=timezone.utc),
                end_at=datetime(2024, 1, 4, tzinfo=timezone.utc),
                unit="kwh",
                value=3,
                costs=[
                    Cost(amount=30, currency="GBP", type=CostType.CONSUMPTION_COST),
                    Cost(amount=30, currency="GBP", type=CostType.STANDING_CHARGE_COST),
                ],
                type=ReadingType.ELECTRICITY,
            ),
            Reading(
                start_at=datetime(2024, 1, 4, tzinfo=timezone.utc),
                end_at=datetime(2024, 1, 5, tzinfo=timezone.utc),
                unit="kwh",
                value=4,
                costs=[
                    Cost(amount=40, currency="GBP", type=CostType.CONSUMPTION_COST),
                    Cost(amount=40, currency="GBP", type=CostType.STANDING_CHARGE_COST),
                ],
                type=ReadingType.ELECTRICITY,
            ),
            Reading(
                start_at=datetime(2024, 1, 5, tzinfo=timezone.utc),
                end_at=datetime(2024, 1, 6, tzinfo=timezone.utc),
                unit="kwh",
                value=5,
                costs=[
                    Cost(amount=50, currency="GBP", type=CostType.CONSUMPTION_COST),
                    Cost(amount=50, currency="GBP", type=CostType.STANDING_CHARGE_COST),
                ],
                type=ReadingType.ELECTRICITY,
            ),
            Reading(
                start_at=datetime(2024, 1, 6, tzinfo=timezone.utc),
                end_at=datetime(2024, 1, 7, tzinfo=timezone.utc),
                unit="kwh",
                value=6,
                costs=[
                    Cost(amount=60, currency="GBP", type=CostType.CONSUMPTION_COST),
                    Cost(amount=60, currency="GBP", type=CostType.STANDING_CHARGE_COST),
                ],
                type=ReadingType.ELECTRICITY,
            ),
        ]
        mock_cursor = MagicMock()
        type(mock_cursor).gas_readings = PropertyMock(
            side_effect=[gas_readings[0:2], gas_readings[2:4], gas_readings[4:]]
        )
        type(mock_cursor).electricity_readings = PropertyMock(
            side_effect=[
                electricity_readings[0:2],
                electricity_readings[2:4],
                electricity_readings[4:],
            ]
        )
        mock_cursor.next_page = Mock(side_effect=[True, True, False])

        readings = get_readings(mock_cursor)

        expected = Readings(gas=gas_readings, electricity=electricity_readings)
        assert expected == readings
