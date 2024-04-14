from json import dump
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from gql import gql

from src.constants import DATETIME_FORMAT, QUERY_FILE_PATH
from src.factories import (
    get_authorized_client,
    get_query,
    get_settings,
    get_utility_filters,
)
from src.models import ElectricityFilter, GasFilter, Headers, Settings
from tests.unit.constants import (
    ACCOUNT_NUMBER,
    ELECTRICITY_READING_FREQUENCY,
    END_AT,
    FIRST,
    GAS_READING_FREQUENCY,
    JWT,
    QUERY_STRING,
    START_AT,
    URL,
)


class TestGetSettings:
    def test_settings_can_be_read_from_file(self) -> None:
        with TemporaryDirectory() as temp_dir:
            env_file_path = Path(temp_dir) / "env.json"
            settings_file_contents = {
                "jwt": JWT,
                "url": URL,
                "account_number": ACCOUNT_NUMBER,
                "start_at": START_AT.strftime(DATETIME_FORMAT),
                "end_at": END_AT.strftime(DATETIME_FORMAT),
                "first": FIRST,
                "gas_reading_frequency": GAS_READING_FREQUENCY.value,
                "electricity_reading_frequency": ELECTRICITY_READING_FREQUENCY.value,
                "query_file_path": str(QUERY_FILE_PATH),
            }
            with open(env_file_path, "w") as env_file:
                dump(settings_file_contents, env_file)

            settings = get_settings(env_file_path)

        expected = Settings(
            account_number=ACCOUNT_NUMBER,
            jwt=JWT,
            url=URL,
            start_at=START_AT,
            end_at=END_AT,
            first=FIRST,
            gas_reading_frequency=GAS_READING_FREQUENCY,
            electricity_reading_frequency=ELECTRICITY_READING_FREQUENCY,
            query_file_path=QUERY_FILE_PATH,
        )
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


class TestGetUtilityFilters:
    def test_returns_gas_and_electricity_filters(self) -> None:
        settings = Settings(
            account_number=ACCOUNT_NUMBER,
            jwt=JWT,
            url=URL,
            start_at=START_AT,
            end_at=END_AT,
            first=FIRST,
            gas_reading_frequency=GAS_READING_FREQUENCY,
            electricity_reading_frequency=ELECTRICITY_READING_FREQUENCY,
        )

        utility_filters = get_utility_filters(settings)

        expected = [
            ElectricityFilter(reading_frequency_type=ELECTRICITY_READING_FREQUENCY),
            GasFilter(reading_frequency_type=GAS_READING_FREQUENCY),
        ]
        assert expected == utility_filters

    def test_returns_electricity_filter(self) -> None:
        settings = Settings(
            account_number=ACCOUNT_NUMBER,
            jwt=JWT,
            url=URL,
            start_at=START_AT,
            end_at=END_AT,
            first=FIRST,
            electricity_reading_frequency=ELECTRICITY_READING_FREQUENCY,
        )

        utility_filters = get_utility_filters(settings)

        expected = [
            ElectricityFilter(reading_frequency_type=ELECTRICITY_READING_FREQUENCY),
        ]
        assert expected == utility_filters

    def test_returns_gas_filter(self) -> None:
        settings = Settings(
            account_number=ACCOUNT_NUMBER,
            jwt=JWT,
            url=URL,
            start_at=START_AT,
            end_at=END_AT,
            first=FIRST,
            gas_reading_frequency=GAS_READING_FREQUENCY,
        )

        utility_filters = get_utility_filters(settings)

        expected = [
            GasFilter(reading_frequency_type=GAS_READING_FREQUENCY),
        ]
        assert expected == utility_filters

    def test_throws_exception(self) -> None:
        settings = Settings(
            account_number=ACCOUNT_NUMBER,
            jwt=JWT,
            url=URL,
            start_at=START_AT,
            end_at=END_AT,
            first=FIRST,
        )

        with pytest.raises(ValueError):
            _ = get_utility_filters(settings)
