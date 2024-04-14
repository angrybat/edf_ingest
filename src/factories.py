from json import load
from pathlib import Path
from typing import List

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from graphql import DocumentNode

from src.models import ElectricityFilter, GasFilter, Headers, Settings, Variables


def get_settings(file_path: Path) -> Settings:
    with open(file_path) as file:
        json = load(file)
        return Settings(**json)


def get_variables(settings: Settings, account_number: str) -> Variables:
    return Variables(
        account_number=account_number,
        start_at=settings.start_at,
        end_at=settings.end_at,
        first=settings.first,
        utility_filters=get_utility_filters(settings),
    )


def get_authorized_client(jwt: str, url: str) -> Client:
    headers = Headers(jwt=jwt)
    transport = AIOHTTPTransport(url=url, headers=headers.model_dump(by_alias=True))
    return Client(transport=transport, fetch_schema_from_transport=True)


def get_query(file_path: Path) -> DocumentNode:
    with open(file_path) as file:
        return gql(file.read())


def get_utility_filters(settings: Settings) -> List[GasFilter | ElectricityFilter]:
    if settings.gas_reading_frequency and settings.electricity_reading_frequency:
        return [
            ElectricityFilter(
                reading_frequency_type=settings.electricity_reading_frequency
            ),
            GasFilter(reading_frequency_type=settings.gas_reading_frequency),
        ]
    if settings.electricity_reading_frequency:
        return [
            ElectricityFilter(
                reading_frequency_type=settings.electricity_reading_frequency
            )
        ]
    if settings.gas_reading_frequency:
        return [GasFilter(reading_frequency_type=settings.gas_reading_frequency)]
    raise ValueError(
        """
        Neither gas_reading_frequency or electricity_reading_frequency at least one of
         these need to be set.
        """
    )
