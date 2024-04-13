from json import dump
from pathlib import Path
from tempfile import TemporaryDirectory

from gql import gql

from src.factories import get_authorized_client, get_query, get_settings
from src.models import Headers, Settings
from tests.unit.constants import ACCOUNT_NUMBER, JWT, QUERY_STRING, URL


class TestGetSettings:
    def test_settings_can_be_read_from_file(self) -> None:
        with TemporaryDirectory() as temp_dir:
            env_file_path = Path(temp_dir) / "env.json"
            with open(env_file_path, "w") as env_file:
                dump(
                    {"jwt": JWT, "url": URL, "account_number": ACCOUNT_NUMBER}, env_file
                )

            settings = get_settings(env_file_path)

        expected = Settings(account_number=ACCOUNT_NUMBER, jwt=JWT, url=URL)
        assert expected == settings


class TestGetAuthorizedClient:
    def test_url_is_set(self) -> None:
        client = get_authorized_client(url=URL, jwt=JWT)

        assert client.transport.url == URL  # type: ignore

    def test_headers_is_set(self) -> None:
        client = get_authorized_client(url=URL, jwt=JWT)

        headers_dict = Headers(jwt=JWT).model_dump(by_alias=True)
        assert client.transport.headers == headers_dict  # type: ignore


class TestGetQuery:
    def test_string_is_returned(self) -> None:
        with TemporaryDirectory() as temp_dir:
            query_file_path = Path(temp_dir) / "query.graphql"
            with open(query_file_path, "w") as query_file:
                query_file.write(QUERY_STRING)

            query = get_query(query_file_path)

        expected = gql(QUERY_STRING)
        assert expected == query
