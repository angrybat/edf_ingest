from pathlib import Path

from src.client import get_paginated_readings
from src.factories import get_settings, get_variables

env_file_path = Path("env.json")
query_file_path = Path("src/get_measurements.graphql")
settings = get_settings(env_file_path)
variables = get_variables(settings)

readings = get_paginated_readings(
    settings.url, settings.jwt, query_file_path, variables
)

with open("output.json", "w") as output_file:
    output_file.write(readings.model_dump_json())
