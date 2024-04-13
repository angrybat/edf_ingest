from json import dump
from pathlib import Path
from tempfile import TemporaryDirectory

from src.factories import get_authorized_client, get_settings
from src.models import Headers, Settings

URL = "http://localhost:8008"
JWT = "ThisIsAJwt"


class TestGetSettings:
    def test_settings_can_be_read_from_file(self) -> None:
        jwt = "ThisIsAJwt"
        url = "http://localhost:8008"
        account_number = "account_number"
        with TemporaryDirectory() as temp_dir:
            env_file_path = Path(temp_dir) / "env.json"
            with open(env_file_path, "w") as env_file:
                dump(
                    {"jwt": jwt, "url": url, "account_number": account_number}, env_file
                )

            settings = get_settings(env_file_path)

        expected = Settings(account_number=account_number, jwt=jwt, url=url)
        assert expected == settings


class TestGetAuthorizedClient:
    def test_url_is_set(self) -> None:
        client = get_authorized_client(url=URL, jwt=JWT)

        assert client.transport.url == URL

    def test_headers_is_set(self) -> None:
        client = get_authorized_client(url=URL, jwt=JWT)

        assert client.transport.headers == Headers(jwt=JWT).model_dump(by_alias=True)
