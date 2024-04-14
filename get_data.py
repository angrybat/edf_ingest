from src.client import get_paginated_readings
from src.constants import ENV_FILE_PATH, QUERY_FILE_PATH
from src.factories import get_settings, get_variables

settings = get_settings(ENV_FILE_PATH)
variables = get_variables(settings)

readings = get_paginated_readings(
    settings.url, settings.jwt, QUERY_FILE_PATH, variables
)

with open("output.json", "w") as output_file:
    output_file.write(readings.model_dump_json())
