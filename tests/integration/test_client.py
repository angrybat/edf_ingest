from pathlib import Path

from src.client import get_paginated_readings
from src.factories import get_settings, get_variables
from src.models import PaginatedReadings


def test_api_call_does_not_throw_error():
    env_file_path = Path("env.json")
    query_file_path = Path("src/get_measurements.graphql")
    settings = get_settings(env_file_path)
    variables = get_variables(settings)
    paginated_readings = get_paginated_readings(
        settings.url, settings.jwt, query_file_path, variables
    )

    assert isinstance(paginated_readings, PaginatedReadings)
