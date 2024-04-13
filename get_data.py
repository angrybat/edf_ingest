from datetime import datetime
from pathlib import Path

from gql import gql

from src.factories import get_authorized_client, get_settings
from src.models import GasFilter, ReadingFrequencyType, Variables

# get sensitive data from env file
env_file_path = Path("env.json")
settings = get_settings(env_file_path)

# Create authorized client
client = get_authorized_client(jwt=settings.jwt, url=settings.url)

# Define variables and query
variables = Variables(
    account_number=settings.account_number,
    start_at=datetime(year=2024, month=1, day=11),
    end_at=datetime(year=2024, month=1, day=12),
    first=48,
    utility_filters=[
        GasFilter(reading_frequency_type=ReadingFrequencyType.HOUR_INTERVAL)
    ],
)

query = gql(
    "query getMeasurements($accountNumber: String!, $first: Int!, $utilityFilters: [UtilityFiltersInput!], $startAt: DateTime, $endAt: DateTime) {\n  account(accountNumber: $accountNumber) {\n    properties {\n      measurements(\n        first: $first\n        utilityFilters: $utilityFilters\n        startAt: $startAt\n        endAt: $endAt\n      ) {\n        edges {\n          node {\n            value\n            ... on IntervalMeasurementType {\n              startAt\n              endAt\n              value\n              metaData {\n                statistics {\n                  type\n                  costInclTax {\n                    estimatedAmount\n                    __typename\n                  }\n                  __typename\n                }\n                __typename\n              }\n              __typename\n            }\n            metaData {\n              utilityFilters {\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"  # noqa: E501
)

# get data
result = client.execute(query, variable_values=variables.model_dump(by_alias=True))

# print data
print(result)
