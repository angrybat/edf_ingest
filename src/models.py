from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import List

from pydantic import (
    AliasPath,
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
    field_validator,
)
from pydantic.alias_generators import to_camel

from src.constants import (
    ACCOUNT_NUMBER_QUERY_FILE_PATH,
    DATETIME_FORMAT,
    GET_READINGS_QUERY_FILE_PATH,
)


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
    jwt: str
    email_address: str
    password: str
    url: str
    start_at: datetime
    end_at: datetime
    first: int
    gas_reading_frequency: ReadingFrequencyType | None = None
    electricity_reading_frequency: ReadingFrequencyType | None = None
    get_readings_query_file_path: Path = GET_READINGS_QUERY_FILE_PATH
    account_number_query_path: Path = ACCOUNT_NUMBER_QUERY_FILE_PATH


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


class GetReadingsVariables(EdfModel):
    account_number: str
    start_at: datetime
    end_at: datetime
    first: int
    utility_filters: List[GasFilter | ElectricityFilter]
    after: str = ""

    @field_serializer(
        "start_at",
        "end_at",
        return_type=str,
    )
    def get_datetime_str(self, datetime: datetime) -> str:
        return datetime.strftime(DATETIME_FORMAT)[:-3] + "Z"


class EmailAndPassword(BaseModel):
    email: str
    password: str


class AuthorizationVariables(EdfModel):
    email: str = Field(..., exclude=True)
    password: str = Field(..., exclude=True)

    @computed_field
    @property
    def input(self) -> EmailAndPassword:
        return EmailAndPassword(email=self.email, password=self.password)


class CostType(Enum):
    STANDING_CHARGE_COST = "STANDING_CHARGE_COST"
    CONSUMPTION_COST = "CONSUMPTION_COST"


class Cost(EdfModel):
    amount: Decimal = Field(
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
    value: Decimal = Field(..., validation_alias=AliasPath("node", "value"))
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
    cursor: str = Field(
        ...,
        validation_alias=AliasPath(
            "account", "properties", 0, "measurements", "pageInfo", "endCursor"
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


class Credentials(EdfModel):
    jwt: str = Field(..., validation_alias=AliasPath("obtainKrakenToken", "token"))
    expires_at: datetime = Field(
        ..., validation_alias=AliasPath("obtainKrakenToken", "payload", "exp")
    )
    refresh_token: str = Field(
        ..., validation_alias=AliasPath("obtainKrakenToken", "refreshToken")
    )
