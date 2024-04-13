from src.clients import get_authorized_client
from src.models import Headers

URL = "http://localhost:8008"
JWT = "ThisIsAJwt"


def test_url_is_set() -> None:
    client = get_authorized_client(url=URL, jwt=JWT)

    assert client.transport.url == URL


def test_headers_is_set() -> None:
    client = get_authorized_client(url=URL, jwt=JWT)

    assert client.transport.headers == Headers(jwt=JWT).model_dump(by_alias=True)
