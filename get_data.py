from json import dump
from pathlib import Path

from src.factories import get_authorized_client, get_query, get_settings
from src.models import GasFilter, Variables

# get sensitive data from env file
env_file_path = Path("env.json")
query_file_path = Path("src/get_measurements.graphql")
settings = get_settings(env_file_path)

# Create authorized client
client = get_authorized_client(jwt=settings.jwt, url=settings.url)

# Define variables and query
variables = Variables(
    account_number=settings.account_number,
    start_at=settings.start_at,
    end_at=settings.end_at,
    first=settings.first,
    utility_filters=[GasFilter(reading_frequency_type=settings.gas_reading_frequency)],
)

query = get_query(query_file_path)

# get data
result = client.execute(query, variable_values=variables.model_dump(by_alias=True))

# output to file
with open("output.json", "w") as output_file:
    dump(result, output_file)
