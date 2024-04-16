from datetime import datetime, timezone
from json import load
from typing import List

from pytest import fixture

from src.models import (
    Credentials,
    ElectricityFilter,
    GasFilter,
    GetReadingsVariables,
    Headers,
    PaginatedReadings,
    Reading,
    ReadingFrequencyType,
    RefreshTokenVariables,
    UsernamePasswordVariables,
)
from tests.unit.constants import (
    ACCOUNT_NUMBER,
    CURSOR,
    EMAIL_ADDRESS,
    JWT,
    PASSWORD,
    REFRESH_TOKEN,
    URL,
)


class TestHeaders:
    def test_maps_to_dict(self) -> None:
        headers = Headers(jwt=JWT)

        actual = headers.model_dump(by_alias=True)

        expected = {"Authorization": f"JWT {JWT}"}

        assert expected == actual


class TestGetReadingsVariable:
    def test_maps_to_dict(self) -> None:
        first = 10
        gas_filter_frequency = ReadingFrequencyType.MONTH_INTERVAL
        electricity_filter_frequency = ReadingFrequencyType.DAY_INTERVAL
        variables = GetReadingsVariables(
            account_number=ACCOUNT_NUMBER,
            start_at=datetime(
                year=2024,
                month=4,
                day=13,
                hour=12,
                minute=32,
                second=45,
                microsecond=123000,
            ),
            end_at=datetime(
                year=2025,
                month=3,
                day=23,
                hour=11,
                minute=26,
                second=49,
                microsecond=456000,
            ),
            first=first,
            utility_filters=[
                GasFilter(reading_frequency_type=gas_filter_frequency),
                ElectricityFilter(reading_frequency_type=electricity_filter_frequency),
            ],
            after=CURSOR,
        )

        actual = variables.model_dump(by_alias=True)

        expected = {
            "accountNumber": ACCOUNT_NUMBER,
            "startAt": "2024-04-13T12:32:45.123Z",
            "endAt": "2025-03-23T11:26:49.456Z",
            "first": first,
            "utilityFilters": [
                {"gasFilters": {"readingFrequencyType": gas_filter_frequency.value}},
                {
                    "electricityFilters": {
                        "readingFrequencyType": electricity_filter_frequency.value
                    }
                },
            ],
            "after": CURSOR,
        }
        assert expected == actual


@fixture
def readings_response() -> dict:
    with open("tests/unit/example_response.json") as file:
        return load(file)


class TestUsernamePasswordVariables:
    def test_maps_to_dict(self) -> None:
        variables = UsernamePasswordVariables(email=EMAIL_ADDRESS, password=PASSWORD)

        actual = variables.model_dump(by_alias=True)

        expected = {"input": {"email": EMAIL_ADDRESS, "password": PASSWORD}}
        assert expected == actual


class TestRefreshTokenVariables:
    def test_maps_to_dict(self) -> None:
        variables = RefreshTokenVariables(refresh_token=REFRESH_TOKEN)

        actual = variables.model_dump(by_alias=True)

        expected = {"input": {"refreshToken": REFRESH_TOKEN}}
        assert expected == actual


class TestPaginatedReadings:
    def test_maps_from_dict(
        self, paginated_readings: PaginatedReadings, readings_response: dict
    ) -> None:
        actual = PaginatedReadings(**readings_response)

        assert paginated_readings == actual

    def test_gas_returns_only_readings_of_type_gas(
        self, paginated_readings: PaginatedReadings, gas_readings: List[Reading]
    ) -> None:
        assert gas_readings == paginated_readings.gas

    def test_electricity_returns_only_readings_of_type_electricity(
        self, paginated_readings: PaginatedReadings, electricity_readings: List[Reading]
    ) -> None:
        assert electricity_readings == paginated_readings.electricity


class TestCredentials:
    def test_maps_from_dict(self) -> None:
        jwt_response = {
            "obtainKrakenToken": {
                "token": JWT,
                "payload": {
                    "sub": "kraken|account-user:123",
                    "gty": "EMAIL-AND-PASSWORD",
                    "email": EMAIL_ADDRESS,
                    "tokenUse": "access",
                    "iss": URL,
                    "iat": 1711929600,
                    "exp": 1711933200,
                    "origIat": 1711929600,
                },
                "refreshToken": REFRESH_TOKEN,
            }
        }

        credentials = Credentials(**jwt_response)

        expected = Credentials(
            jwt=JWT,
            expires_at=datetime(2024, 4, 1, 1, tzinfo=timezone.utc),
            refresh_token=REFRESH_TOKEN,
        )
        assert expected == credentials
