from json import load
from pathlib import Path

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from graphql import DocumentNode

from src.models import Headers, Settings


def get_settings(file_path: Path) -> Settings:
    with open(file_path) as file:
        json = load(file)
        return Settings(**json)


def get_authorized_client(jwt: str, url: str) -> Client:
    headers = Headers(jwt=jwt)
    transport = AIOHTTPTransport(url=url, headers=headers.model_dump(by_alias=True))
    return Client(transport=transport, fetch_schema_from_transport=True)


def get_query(file_path: Path) -> DocumentNode:
    with open(file_path) as file:
        return gql(file.read())
