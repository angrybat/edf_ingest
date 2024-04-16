from pathlib import Path

from src.constants import GET_JWT_QUERY_FILE_PATH
from src.factories import get_authorized_client, get_client, get_query
from src.models import (
    AuthorizationVariables,
    Credentials,
    GetReadingsVariables,
    PaginatedReadings,
)


def get_paginated_readings(
    url: str,
    jwt: str,
    query_file_path: Path,
    variables: GetReadingsVariables,
) -> PaginatedReadings:
    client = get_authorized_client(jwt, url)
    query = get_query(query_file_path)
    response = client.execute(
        query, variable_values=variables.model_dump(by_alias=True)
    )
    return PaginatedReadings(**response)


def get_account_number(url: str, jwt: str, query_file_path: Path) -> str:
    client = get_authorized_client(jwt, url)
    query = get_query(query_file_path)
    response = client.execute(query)
    return response["viewer"]["accounts"][0]["number"]


def get_credentials(url: str, email_address: str, password: str) -> Credentials:
    client = get_client(url)
    variables = AuthorizationVariables(email=email_address, password=password)
    query = get_query(GET_JWT_QUERY_FILE_PATH)
    response = client.execute(
        query, variable_values=variables.model_dump(by_alias=True)
    )
    return Credentials(**response)
