from datetime import datetime
from enum import Enum
from typing import List

from pydantic import (
    AliasPath,
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
)
from pydantic.alias_generators import to_camel


class ReadingFrequencyType(Enum):
    RAW_INTERVAL = "RAW_INTERVAL"
    FIVE_MIN_INTERVAL = "FIVE_MIN_INTERVAL"
    FIFTEEN_MIN_INTERVAL = "FIFTEEN_MIN_INTERVAL"
    THIRTY_MIN_INTERVAL = "THIRTY_MIN_INTERVAL"
    HOUR_INTERVAL = "HOUR_INTERVAL"
    DAY_INTERVAL = "DAY_INTERVAL"
    WEEK_INTERVAL = "WEEK_INTERVAL"
    MONTH_INTERVAL = "MONTH_INTERVAL"
    QUARTER_INTERVAL = "QUARTER_INTERVAL"
    DAILY = "DAILY"
    POINT_IN_TIME = "POINT_IN_TIME"


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
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class UtilityFilter(EdfModel):
    model_config = ConfigDict(use_enum_values=True)
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


class CostType(Enum):
    STANDING_CHARGE_COST = "STANDING_CHARGE_COST"
    CONSUMPTION_COST = "CONSUMPTION_COST"


class Cost(EdfModel):
    amount: float = Field(
        ..., validation_alias=AliasPath("costInclTax", "estimatedAmount")
    )
    currency: str = Field(
        ..., validation_alias=AliasPath("costInclTax", "costCurrency")
    )
    type: CostType


class ReadingType(Enum):
    GAS = "GasFiltersOutput"
    ELECTRICITY = "ElectricityFiltersOutput"


class Reading(EdfModel):
    start_at: datetime = Field(..., validation_alias=AliasPath("node", "startAt"))
    end_at: datetime = Field(..., validation_alias=AliasPath("node", "endAt"))
    unit: str = Field(..., validation_alias=AliasPath("node", "unit"))
    value: float = Field(..., validation_alias=AliasPath("node", "value"))
    costs: List[Cost] = Field(
        ..., validation_alias=AliasPath("node", "metaData", "statistics")
    )
    type: ReadingType = Field(
        ...,
        validation_alias=AliasPath("node", "metaData", "utilityFilters", "__typename"),
    )


class PaginatedReadings(EdfModel):
    readings: List[Reading] = Field(
        ...,
        validation_alias=AliasPath("account", "properties", 0, "measurements", "edges"),
    )
    has_next_page: bool = Field(
        ...,
        validation_alias=AliasPath(
            "account", "properties", 0, "measurements", "pageInfo", "hasNextPage"
        ),
    )

    @property
    def electricity(self) -> List[Reading]:
        return self._filter_readings(ReadingType.ELECTRICITY)

    @property
    def gas(self) -> List[Reading]:
        return self._filter_readings(ReadingType.GAS)

    def _filter_readings(self, reading_type: ReadingType) -> List[Reading]:
        return [reading for reading in self.readings if reading.type == reading_type]
