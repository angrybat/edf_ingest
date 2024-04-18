from datetime import datetime, timezone
from typing import List

from src.client import (
    get_authorization_tokens,
    get_paginated_readings,
    refresh_authorization_tokens,
)
from src.factories import get_readings_variables
from src.models import AuthorizationTokens, PaginatedReadings, Reading, Settings


class ReadingsCursor:
    _paginated_readings: PaginatedReadings | None = None

    def __init__(
        self,
        settings: Settings,
        account_number: str,
        authorization_tokens: AuthorizationTokens,
    ) -> None:
        self.variables = get_readings_variables(settings, account_number)
        self.url = settings.url
        self.email_address = settings.email_address
        self.password = settings.password
        self.get_readings_query_file_path = settings.get_readings_query_file_path
        self.get_jwt_query_file_path = settings.get_jwt_query_file_path
        self._set_token_properties(authorization_tokens)

    @property
    def gas_readings(self) -> List[Reading]:
        return self._paginated_readings.gas

    @property
    def electricity_readings(self) -> List[Reading]:
        return self._paginated_readings.electricity

    def next_page(self) -> bool:
        self._refresh_authorization_tokens()
        self._paginated_readings = get_paginated_readings(
            self.url,
            self.jwt,
            self.get_readings_query_file_path,
            self.variables,
        )
        self.variables.after = self._paginated_readings.cursor
        return self._paginated_readings.has_next_page

    def _refresh_authorization_tokens(self) -> None:
        if authorization_tokens := self._get_authorization_tokens():
            self._set_token_properties(authorization_tokens)

    def _get_authorization_tokens(self) -> AuthorizationTokens | None:
        if datetime.now(tz=timezone.utc) > self.jwt_expires_at:
            if datetime.now(tz=timezone.utc) > self.refresh_token_expires_at:
                return get_authorization_tokens(
                    self.url,
                    self.email_address,
                    self.password,
                    self.get_jwt_query_file_path,
                )
            return refresh_authorization_tokens(self.url, self.refresh_token)
        return None

    def _set_token_properties(self, authorization_tokens) -> None:
        self.jwt = authorization_tokens.jwt
        self.jwt_expires_at = authorization_tokens.expires_at
        self.refresh_token = authorization_tokens.refresh_token
        self.refresh_token_expires_at = authorization_tokens.refresh_expires_in
