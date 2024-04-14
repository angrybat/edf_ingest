from datetime import UTC, datetime, timezone

from pydantic_core import TzInfo

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


def test_headers_maps_to_dict() -> None:
    headers = Headers(jwt=JWT)

    actual = headers.model_dump(by_alias=True)

    expected = {"Authorization": f"JWT {JWT}"}

    assert expected == actual


def test_variables_maps_to_dict() -> None:
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


def test_paginated_readings_maps_from_dict() -> None:
    readings_response = {
        "account": {
            "properties": [
                {
                    "measurements": {
                        "edges": [
                            {
                                "node": {
                                    "startAt": "2024-01-11T00:00:00+00:00",
                                    "endAt": "2024-01-11T01:00:00+00:00",
                                    "unit": "kwh",
                                    "value": "33.333333333333333333333333333333",
                                    "metaData": {
                                        "statistics": [
                                            {
                                                "type": "STANDING_CHARGE_COST",
                                                "costInclTax": {
                                                    "estimatedAmount": "10.50",
                                                    "costCurrency": "GBP",
                                                },
                                            },
                                            {
                                                "type": "CONSUMPTION_COST",
                                                "costInclTax": {
                                                    "estimatedAmount": "69.49",
                                                    "costCurrency": "GBP",
                                                },
                                            },
                                        ],
                                        "utilityFilters": {
                                            "__typename": "GasFiltersOutput"
                                        },
                                    },
                                }
                            },
                            {
                                "node": {
                                    "startAt": "2024-01-11T23:00:00+00:00",
                                    "endAt": "2024-01-12T00:00:00+00:00",
                                    "unit": "kwh",
                                    "value": "76.432113454",
                                    "metaData": {
                                        "statistics": [
                                            {
                                                "type": "STANDING_CHARGE_COST",
                                                "costInclTax": {
                                                    "estimatedAmount": "40.53",
                                                    "costCurrency": "GBP",
                                                },
                                            },
                                            {
                                                "type": "CONSUMPTION_COST",
                                                "costInclTax": {
                                                    "estimatedAmount": "209.54",
                                                    "costCurrency": "GBP",
                                                },
                                            },
                                        ],
                                        "utilityFilters": {
                                            "__typename": "ElectricityFiltersOutput"
                                        },
                                    },
                                }
                            },
                        ],
                        "pageInfo": {"hasNextPage": False},
                    },
                }
            ]
        }
    }

    paginated_readings = PaginatedReadings(**readings_response)

    expected = PaginatedReadings(
        readings=[
            Reading(
                start_at=datetime(
                    year=2024,
                    month=1,
                    day=11,
                    tzinfo=timezone.utc,
                ),
                end_at=datetime(
                    year=2024,
                    month=1,
                    day=11,
                    hour=1,
                    tzinfo=timezone.utc,
                ),
                unit="kwh",
                value=33.333333333333333333333333333333,
                costs=[
                    Cost(
                        amount=10.50, currency="GBP", type=CostType.STANDING_CHARGE_COST
                    ),
                    Cost(amount=69.49, currency="GBP", type=CostType.CONSUMPTION_COST),
                ],
                type=ReadingType.GAS,
            ),
            Reading(
                start_at=datetime(
                    year=2024,
                    month=1,
                    day=11,
                    hour=23,
                    tzinfo=timezone.utc,
                ),
                end_at=datetime(
                    year=2024,
                    month=1,
                    day=12,
                    tzinfo=timezone.utc,
                ),
                unit="kwh",
                value=76.432113454,
                costs=[
                    Cost(
                        amount=40.53, currency="GBP", type=CostType.STANDING_CHARGE_COST
                    ),
                    Cost(
                        amount=209.54,
                        currency="GBP",
                        type=CostType.CONSUMPTION_COST,
                    ),
                ],
                type=ReadingType.ELECTRICITY,
            ),
        ],
        has_next_page=False,
    )
    assert expected == paginated_readings


def test_gas_readings_returns_only_readings_of_type_gas() -> None:
    gas_reading = Reading(
        start_at=datetime(
            year=2024,
            month=1,
            day=11,
            tzinfo=timezone.utc,
        ),
        end_at=datetime(
            year=2024,
            month=1,
            day=11,
            hour=1,
            tzinfo=timezone.utc,
        ),
        unit="kwh",
        value=33.333333333333333333333333333333,
        costs=[
            Cost(amount=10.50, currency="GBP", type=CostType.STANDING_CHARGE_COST),
            Cost(amount=69.49, currency="GBP", type=CostType.CONSUMPTION_COST),
        ],
        type=ReadingType.GAS,
    )
    paginated_readings = PaginatedReadings(
        readings=[
            gas_reading,
            Reading(
                start_at=datetime(
                    year=2024,
                    month=1,
                    day=11,
                    hour=23,
                    tzinfo=timezone.utc,
                ),
                end_at=datetime(
                    year=2024,
                    month=1,
                    day=12,
                    tzinfo=timezone.utc,
                ),
                unit="kwh",
                value=76.432113454,
                costs=[
                    Cost(
                        amount=40.53, currency="GBP", type=CostType.STANDING_CHARGE_COST
                    ),
                    Cost(
                        amount=209.54,
                        currency="GBP",
                        type=CostType.CONSUMPTION_COST,
                    ),
                ],
                type=ReadingType.ELECTRICITY,
            ),
        ],
        has_next_page=False,
    )

    gas_readings = paginated_readings.gas

    assert [gas_reading] == gas_readings
