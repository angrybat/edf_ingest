from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel


class ReadingFrequencyType(Enum):
    THIRTY_MIN_INTERVAL = "THIRTY_MIN_INTERVAL"
    HOUR_INTERVAL = "HOUR_INTERVAL"
    DAY_INTERVAL = "DAY_INTERVAL"
    WEEK_INTERVAL = "WEEK_INTERVAL"
    MONTH_INTERVAL = "MONTH_INTERVAL"
    YEAR_INTERVAL = "YEAR_INTERVAL"


class UtilityFilter(BaseModel):
    reading_frequency_type: ReadingFrequencyType


class GasFilter(BaseModel):
    gas_filters: UtilityFilter


class ElectricityFilter(BaseModel):
    electricity_filter: UtilityFilter


class Variables(BaseModel):
    account_number: str
    start_at: datetime
    end_at: datetime
    first: int
    utility_filters: List[GasFilter | ElectricityFilter]
