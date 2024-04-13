from json import dump
from pathlib import Path
from tempfile import TemporaryDirectory

from src.factories import get_settings
from src.models import Settings


def test_settings_can_be_read_from_file() -> None:
    jwt = "ThisIsAJwt"
    url = "http://localhost:8008"
    account_number = "account_number"
    with TemporaryDirectory() as temp_dir:
        env_file_path = Path(temp_dir) / "env.json"
        with open(env_file_path, "w") as env_file:
            dump({"jwt": jwt, "url": url, "account_number": account_number}, env_file)

        settings = get_settings(env_file_path)

    expected = Settings(account_number=account_number, jwt=jwt, url=url)
    assert expected == settings
