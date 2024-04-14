from pathlib import Path

from src.client import get_paginated_readings

env_file_path = Path("env.json")
query_file_path = Path("src/get_measurements.graphql")

readings = get_paginated_readings(env_file_path, query_file_path)

with open("output.json", "w") as output_file:
    output_file.write(readings.model_dump_json())
