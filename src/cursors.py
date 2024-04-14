from pathlib import Path

from src.client import get_paginated_readings
from src.factories import get_variables
from src.models import Settings


class ReadingsCursor:
    def __init__(self, settings: Settings, query_file_path: Path) -> None:
        self.settings = settings
        self.query_file_path = query_file_path

    def next_page(self) -> bool:
        variables = get_variables(self.settings)
        paginated_readings = get_paginated_readings(
            self.settings.url, self.settings.jwt, self.query_file_path, variables
        )
        return paginated_readings.has_next_page
