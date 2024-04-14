from typing import List

from src.client import get_paginated_readings
from src.factories import get_variables
from src.models import PaginatedReadings, Reading, Settings


class ReadingsCursor:
    def __init__(self, settings: Settings) -> None:
        self.variables = get_variables(settings)
        self.url = settings.url
        self.jwt = settings.jwt
        self.query_file_path = settings.query_file_path
        self._paginated_readings: PaginatedReadings | None = None

    def next_page(self) -> bool:
        self._paginated_readings = get_paginated_readings(
            self.url,
            self.jwt,
            self.query_file_path,
            self.variables,
        )
        self.variables.start_at = sorted(
            [reading.end_at for reading in self._paginated_readings.readings],
            reverse=True,
        )[0]
        return self._paginated_readings.has_next_page

    @property
    def gas_readings(self) -> List[Reading]:
        return self._paginated_readings.gas

    @property
    def electricity_readings(self) -> List[Reading]:
        return self._paginated_readings.electricity
