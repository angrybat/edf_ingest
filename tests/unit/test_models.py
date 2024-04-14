from datetime import datetime, timezone
from decimal import Decimal
from json import load
from typing import List

from pytest import fixture

from src.models import (
    Cost,
    CostType,
    ElectricityFilter,
    GasFilter,
    Headers,
    PaginatedReadings,
    Reading,
    ReadingFrequencyType,
    ReadingType,
    Variables,
)
from tests.unit.constants import ACCOUNT_NUMBER, JWT


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
        }
        assert expected == actual


@fixture
def readings_response() -> dict:
    with open("tests/unit/example_response.json") as file:
        return load(file)


@fixture
def gas_readings() -> List[Reading]:
    return [
        Reading(
            start_at=datetime(2024, 1, 11, 0, 0, tzinfo=timezone.utc),
            end_at=datetime(2024, 1, 12, 0, 0, tzinfo=timezone.utc),
            unit="kwh",
            value=Decimal("49.754585606701326"),
            costs=[
                Cost(
                    amount=Decimal("91.91140781918034"),
                    currency="GBP",
                    type=CostType.STANDING_CHARGE_COST,
                ),
                Cost(
                    amount=Decimal("3.9241057679550884"),
                    currency="GBP",
                    type=CostType.CONSUMPTION_COST,
                ),
            ],
            type=ReadingType.GAS,
        ),
        Reading(
            start_at=datetime(2024, 1, 12, 0, 0, tzinfo=timezone.utc),
            end_at=datetime(2024, 1, 13, 0, 0, tzinfo=timezone.utc),
            unit="kwh",
            value=Decimal("82.87448481198764"),
            costs=[
                Cost(
                    amount=Decimal("73.78014397278886"),
                    currency="GBP",
                    type=CostType.STANDING_CHARGE_COST,
                ),
                Cost(
                    amount=Decimal("89.57461582198445"),
                    currency="GBP",
                    type=CostType.CONSUMPTION_COST,
                ),
            ],
            type=ReadingType.GAS,
        ),
        Reading(
            start_at=datetime(2024, 1, 13, 0, 0, tzinfo=timezone.utc),
            end_at=datetime(2024, 1, 14, 0, 0, tzinfo=timezone.utc),
            unit="kwh",
            value=Decimal("26.0325834943407"),
            costs=[
                Cost(
                    amount=Decimal("70.48907190813418"),
                    currency="GBP",
                    type=CostType.STANDING_CHARGE_COST,
                ),
                Cost(
                    amount=Decimal("39.97638710056837"),
                    currency="GBP",
                    type=CostType.CONSUMPTION_COST,
                ),
            ],
            type=ReadingType.GAS,
        ),
    ]


@fixture
def electricity_readings() -> List[Reading]:
    return [
        Reading(
            start_at=datetime(2024, 1, 11, 0, 0, tzinfo=timezone.utc),
            end_at=datetime(2024, 1, 12, 0, 0, tzinfo=timezone.utc),
            unit="kwh",
            value=Decimal("94.10837814392384"),
            costs=[
                Cost(
                    amount=Decimal("25.255747036638244"),
                    currency="GBP",
                    type=CostType.STANDING_CHARGE_COST,
                ),
                Cost(
                    amount=Decimal("25.581227231256353"),
                    currency="GBP",
                    type=CostType.CONSUMPTION_COST,
                ),
            ],
            type=ReadingType.ELECTRICITY,
        ),
        Reading(
            start_at=datetime(2024, 1, 12, 0, 0, tzinfo=timezone.utc),
            end_at=datetime(2024, 1, 13, 0, 0, tzinfo=timezone.utc),
            unit="kwh",
            value=Decimal("5.781684051845659"),
            costs=[
                Cost(
                    amount=Decimal("82.80427671543171"),
                    currency="GBP",
                    type=CostType.STANDING_CHARGE_COST,
                ),
                Cost(
                    amount=Decimal("46.41564806162006"),
                    currency="GBP",
                    type=CostType.CONSUMPTION_COST,
                ),
            ],
            type=ReadingType.ELECTRICITY,
        ),
        Reading(
            start_at=datetime(2024, 1, 13, 0, 0, tzinfo=timezone.utc),
            end_at=datetime(2024, 1, 14, 0, 0, tzinfo=timezone.utc),
            unit="kwh",
            value=Decimal("31.281634430543235"),
            costs=[
                Cost(
                    amount=Decimal("9.805394767961195"),
                    currency="GBP",
                    type=CostType.STANDING_CHARGE_COST,
                ),
                Cost(
                    amount=Decimal("74.80780318455047"),
                    currency="GBP",
                    type=CostType.CONSUMPTION_COST,
                ),
            ],
            type=ReadingType.ELECTRICITY,
        ),
    ]


@fixture
def paginated_readings(
    gas_readings: List[Reading], electricity_readings: List[Reading]
) -> PaginatedReadings:
    return PaginatedReadings(
        readings=gas_readings + electricity_readings,
        has_next_page=False,
    )


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
