from pathlib import Path
from typing import List

from src.client import get_paginated_readings
from src.factories import get_variables
from src.models import PaginatedReadings, Reading, Settings


class ReadingsCursor:
    def __init__(self, settings: Settings, query_file_path: Path) -> None:
        self.settings = settings
        self.query_file_path = query_file_path
        self._paginated_readings: PaginatedReadings | None = None

    def next_page(self) -> bool:
        variables = get_variables(self.settings)
        self._paginated_readings = get_paginated_readings(
            self.settings.url, self.settings.jwt, self.query_file_path, variables
        )
        return self._paginated_readings.has_next_page

    @property
    def gas_readings(self) -> List[Reading]:
        return self._paginated_readings.gas

    @property
    def electricity_readings(self) -> List[Reading]:
        return self._paginated_readings.electricity
