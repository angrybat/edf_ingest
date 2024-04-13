from json import load
from pathlib import Path

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

env_file_path = Path("env.json")
with open(env_file_path) as env_file:
    settings = load(env_file)

URL = settings["url"]
JWT = settings["jwt"]

HEADERS = {"Authorization": f"JWT {JWT}"}
transport = AIOHTTPTransport(url=URL, headers=HEADERS)

client = Client(transport=transport, fetch_schema_from_transport=True)

params = {
    "accountNumber": settings["account_number"],
    "startAt": "2024-01-11T00:00:00.000Z",
    "endAt": "2024-01-12T00:00:00.000Z",
    "first": 48,
    "utilityFilters": [
        {"electricityFilters": {"readingFrequencyType": "HOUR_INTERVAL"}}
    ],
}

query = gql(
    "query getMeasurements($accountNumber: String!, $first: Int!, $utilityFilters: [UtilityFiltersInput!], $startAt: DateTime, $endAt: DateTime) {\n  account(accountNumber: $accountNumber) {\n    properties {\n      measurements(\n        first: $first\n        utilityFilters: $utilityFilters\n        startAt: $startAt\n        endAt: $endAt\n      ) {\n        edges {\n          node {\n            value\n            ... on IntervalMeasurementType {\n              startAt\n              endAt\n              value\n              metaData {\n                statistics {\n                  type\n                  costInclTax {\n                    estimatedAmount\n                    __typename\n                  }\n                  __typename\n                }\n                __typename\n              }\n              __typename\n            }\n            metaData {\n              utilityFilters {\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"  # noqa: E501
)

result = client.execute(query, variable_values=params)
print(result)
