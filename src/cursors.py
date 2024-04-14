from typing import List

from src.client import get_paginated_readings
from src.factories import get_variables
from src.models import PaginatedReadings, Reading, Settings


class ReadingsCursor:
    def __init__(self, settings: Settings, account_number: str) -> None:
        self.variables = get_variables(settings, account_number)
        self.url = settings.url
        self.jwt = settings.jwt
        self.query_file_path = settings.get_readings_query_file_path
        self._paginated_readings: PaginatedReadings | None = None

    def next_page(self) -> bool:
        self._paginated_readings = get_paginated_readings(
            self.url,
            self.jwt,
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
