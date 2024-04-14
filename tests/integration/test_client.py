from pathlib import Path

from src.client import get_paginated_readings
from src.factories import get_settings, get_utility_filters
from src.models import PaginatedReadings, Variables


def test_api_call_does_not_throw_error():
    env_file_path = Path("env.json")
    query_file_path = Path("src/get_measurements.graphql")
    settings = get_settings(env_file_path)
    variables = Variables(
        account_number=settings.account_number,
        start_at=settings.start_at,
        end_at=settings.end_at,
        first=settings.first,
        utility_filters=get_utility_filters(settings),
    )
    paginated_readings = get_paginated_readings(
        settings.url, settings.jwt, query_file_path, variables
    )

    assert isinstance(paginated_readings, PaginatedReadings)
