from datetime import datetime

from src.models import ElectricityFilter, GasFilter, ReadingFrequencyType, Variables


def test_variables_maps_to_dict() -> None:
    account_number = "account_number"
    first = 10
    gas_filter_frequency = ReadingFrequencyType.MONTH_INTERVAL
    electricity_filter_frequency = ReadingFrequencyType.DAY_INTERVAL
    variables = Variables(
        account_number=account_number,
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
        "accountNumber": account_number,
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