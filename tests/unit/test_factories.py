from json import dump
from pathlib import Path
from tempfile import TemporaryDirectory

from src.factories import get_authorized_client, get_settings
from src.models import Headers, Settings
from tests.unit.constants import ACCOUNT_NUMBER, JWT, URL


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

        assert client.transport.url == URL

    def test_headers_is_set(self) -> None:
        client = get_authorized_client(url=URL, jwt=JWT)

        assert client.transport.headers == Headers(jwt=JWT).model_dump(by_alias=True)
