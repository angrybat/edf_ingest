from pathlib import Path

from src.factories import get_authorized_client, get_query
from src.models import PaginatedReadings, Variables


def get_paginated_readings(
    url: str,
    jwt: str,
    query_file_path: Path,
    variables: Variables,
) -> PaginatedReadings:
    client = get_authorized_client(jwt, url)
    query = get_query(query_file_path)
    response = client.execute(
        query, variable_values=variables.model_dump(by_alias=True)
    )
    return PaginatedReadings(**response)


def get_account_name(url: str, jwt: str, query_file_path: Path) -> str:
    client = get_authorized_client(jwt, url)
    query = get_query(query_file_path)
    response = client.execute(query)
    return response["viewer"]["accounts"][0]["number"]
