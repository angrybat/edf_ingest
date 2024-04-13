from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_serializer
from pydantic.alias_generators import to_camel


class ReadingFrequencyType(Enum):
    THIRTY_MIN_INTERVAL = "THIRTY_MIN_INTERVAL"
    HOUR_INTERVAL = "HOUR_INTERVAL"
    DAY_INTERVAL = "DAY_INTERVAL"
    WEEK_INTERVAL = "WEEK_INTERVAL"
    MONTH_INTERVAL = "MONTH_INTERVAL"
    YEAR_INTERVAL = "YEAR_INTERVAL"


class Settings(BaseModel):
    account_number: str
    jwt: str
    url: str


class Headers(BaseModel):
    jwt: str = Field(..., exclude=True)

    @computed_field(alias="Authorization")
    @property
    def authorization(self) -> str:
        return f"JWT {self.jwt}"


class EdfModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, use_enum_values=True
    )


class UtilityFilter(EdfModel):
    reading_frequency_type: ReadingFrequencyType


class GasFilter(EdfModel):
    reading_frequency_type: ReadingFrequencyType = Field(..., exclude=True)

    @computed_field
    @property
    def gas_filters(self) -> UtilityFilter:
        return UtilityFilter(reading_frequency_type=self.reading_frequency_type)


class ElectricityFilter(EdfModel):
    reading_frequency_type: ReadingFrequencyType = Field(..., exclude=True)

    @computed_field
    @property
    def electricity_filters(self) -> UtilityFilter:
        return UtilityFilter(reading_frequency_type=self.reading_frequency_type)


class Variables(EdfModel):
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
