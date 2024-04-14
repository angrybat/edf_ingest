from pathlib import Path

from src.factories import (
    get_authorized_client,
    get_query,
    get_settings,
    get_utility_filters,
)
from src.models import PaginatedReadings, Variables


def get_paginated_readings(
    settings_file_path: Path, query_file_path: Path
) -> PaginatedReadings:
    settings = get_settings(settings_file_path)
    variables = Variables(
        account_number=settings.account_number,
        start_at=settings.start_at,
        end_at=settings.end_at,
        first=settings.first,
        utility_filters=get_utility_filters(settings),
    )
    client = get_authorized_client(jwt=settings.jwt, url=settings.url)
    query = get_query(query_file_path)
    response = client.execute(
        query, variable_values=variables.model_dump(by_alias=True)
    )
    return PaginatedReadings(**response)
