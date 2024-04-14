from pathlib import Path

from src.client import get_paginated_readings
from src.factories import get_settings, get_utility_filters
from src.models import Variables

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

readings = get_paginated_readings(
    settings.url, settings.jwt, query_file_path, variables
)

with open("output.json", "w") as output_file:
    output_file.write(readings.model_dump_json())
