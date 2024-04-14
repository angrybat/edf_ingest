from pathlib import Path

import pytest

from src.client import get_paginated_readings
from src.models import PaginatedReadings


def test_api_call_does_not_throw_error():
    env_file_path = Path("env.json")
    query_file_path = Path("src/get_measurements.graphql")

    paginated_readings = get_paginated_readings(env_file_path, query_file_path)

    assert isinstance(paginated_readings, PaginatedReadings)
