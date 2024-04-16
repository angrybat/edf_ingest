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
    def __init__(
        self,
        settings: Settings,
        account_number: str,
        authorization_tokens: AuthorizationTokens,
    ) -> None:
        self.variables = get_readings_variables(settings, account_number)
        self.url = settings.url
        self.email_address = (settings.email_address,)
        self.password = (settings.password,)
        self.authorization_tokens = authorization_tokens
        self.query_file_path = settings.get_readings_query_file_path
        self._paginated_readings: PaginatedReadings | None = None

    def next_page(self) -> bool:
        if (
            datetime.now(tz=timezone.utc) > self.authorization_tokens.expires_at
            and datetime.now(tz=timezone.utc)
            > self.authorization_tokens.refresh_expires_in
        ):
            self.authorization_tokens = get_authorization_tokens(
                self.url, self.email_address, self.password
            )
        if datetime.now(tz=timezone.utc) > self.authorization_tokens.expires_at:
            self.authorization_tokens = refresh_authorization_tokens(
                self.url, self.authorization_tokens.refresh_expires_in
            )
        self._paginated_readings = get_paginated_readings(
            self.url,
            self.authorization_tokens.jwt,
            self.query_file_path,
            self.variables,
        )
        self.variables.after = self._paginated_readings.cursor
        return self._paginated_readings.has_next_page

    @property
    def gas_readings(self) -> List[Reading]:
        return self._paginated_readings.gas

    @property
    def electricity_readings(self) -> List[Reading]:
        return self._paginated_readings.electricity
