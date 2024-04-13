from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict, field_serializer
from pydantic.alias_generators import to_camel


class ReadingFrequencyType(Enum):
    THIRTY_MIN_INTERVAL = "THIRTY_MIN_INTERVAL"
    HOUR_INTERVAL = "HOUR_INTERVAL"
    DAY_INTERVAL = "DAY_INTERVAL"
    WEEK_INTERVAL = "WEEK_INTERVAL"
    MONTH_INTERVAL = "MONTH_INTERVAL"
    YEAR_INTERVAL = "YEAR_INTERVAL"


class UtilityFilter(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    reading_frequency_type: ReadingFrequencyType

    @field_serializer("reading_frequency_type", return_type=str)
    def get_enum_string(self, reading_frequency_type: ReadingFrequencyType) -> str:
        return reading_frequency_type.value


class GasFilter(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    gas_filters: UtilityFilter


class ElectricityFilter(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    electricity_filters: UtilityFilter


class Variables(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    account_number: str
    start_at: datetime
    end_at: datetime
    first: int
    utility_filters: List[GasFilter | ElectricityFilter]

    @field_serializer(
        "start_at",
        "end_at",
        return_type=str,
    )
    def get_datetime_str(self, datetime: datetime) -> str:
        return datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
