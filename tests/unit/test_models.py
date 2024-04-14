from datetime import datetime
from json import load
from typing import List

from pytest import fixture

from src.models import (
    ElectricityFilter,
    GasFilter,
    Headers,
    PaginatedReadings,
    Reading,
    ReadingFrequencyType,
    Variables,
)
from tests.unit.constants import ACCOUNT_NUMBER, CURSOR, JWT


class TestHeaders:
    def test_maps_to_dict(self) -> None:
        headers = Headers(jwt=JWT)

        actual = headers.model_dump(by_alias=True)

        expected = {"Authorization": f"JWT {JWT}"}

        assert expected == actual


class TestVariable:
    def test_maps_to_dict(self) -> None:
        first = 10
        gas_filter_frequency = ReadingFrequencyType.MONTH_INTERVAL
        electricity_filter_frequency = ReadingFrequencyType.DAY_INTERVAL
        variables = Variables(
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
