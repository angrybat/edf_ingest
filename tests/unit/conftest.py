from datetime import datetime, timezone
from decimal import Decimal
from typing import List

from pytest import fixture

from src.models import Cost, CostType, PaginatedReadings, Reading, ReadingType
from tests.unit.constants import CURSOR


@fixture
def gas_readings() -> List[Reading]:
    return [
        Reading(
            start_at=datetime(2024, 1, 11, 0, 0, tzinfo=timezone.utc),
            end_at=datetime(2024, 1, 12, 0, 0, tzinfo=timezone.utc),
            unit="kwh",
            value=Decimal("49.754585606701326"),
            costs=[
                Cost(
                    amount=Decimal("91.91140781918034"),
                    currency="GBP",
                    type=CostType.STANDING_CHARGE_COST,
                ),
                Cost(
                    amount=Decimal("3.9241057679550884"),
                    currency="GBP",
                    type=CostType.CONSUMPTION_COST,
                ),
            ],
            type=ReadingType.GAS,
        ),
        Reading(
            start_at=datetime(2024, 1, 12, 0, 0, tzinfo=timezone.utc),
            end_at=datetime(2024, 1, 13, 0, 0, tzinfo=timezone.utc),
            unit="kwh",
            value=Decimal("82.87448481198764"),
            costs=[
                Cost(
                    amount=Decimal("73.78014397278886"),
                    currency="GBP",
                    type=CostType.STANDING_CHARGE_COST,
                ),
                Cost(
                    amount=Decimal("89.57461582198445"),
                    currency="GBP",
                    type=CostType.CONSUMPTION_COST,
                ),
            ],
            type=ReadingType.GAS,
        ),
        Reading(
            start_at=datetime(2024, 1, 13, 0, 0, tzinfo=timezone.utc),
            end_at=datetime(2024, 1, 14, 0, 0, tzinfo=timezone.utc),
            unit="kwh",
            value=Decimal("26.0325834943407"),
            costs=[
                Cost(
                    amount=Decimal("70.48907190813418"),
                    currency="GBP",
                    type=CostType.STANDING_CHARGE_COST,
                ),
                Cost(
                    amount=Decimal("39.97638710056837"),
                    currency="GBP",
                    type=CostType.CONSUMPTION_COST,
                ),
            ],
            type=ReadingType.GAS,
        ),
        Reading(
            start_at=datetime(2024, 1, 14, 0, 0, tzinfo=timezone.utc),
            end_at=datetime(2024, 1, 15, 0, 0, tzinfo=timezone.utc),
            unit="kwh",
            value=Decimal("60.973307823432"),
            costs=[
                Cost(
                    amount=Decimal("54.15493726904323"),
                    currency="GBP",
                    type=CostType.STANDING_CHARGE_COST,
                ),
                Cost(
                    amount=Decimal("60.93476258953893"),
                    currency="GBP",
                    type=CostType.CONSUMPTION_COST,
                ),
            ],
            type=ReadingType.GAS,
        ),
    ]


@fixture
def electricity_readings() -> List[Reading]:
    return [
        Reading(
            start_at=datetime(2024, 1, 11, 0, 0, tzinfo=timezone.utc),
            end_at=datetime(2024, 1, 12, 0, 0, tzinfo=timezone.utc),
            unit="kwh",
            value=Decimal("94.10837814392384"),
            costs=[
                Cost(
                    amount=Decimal("25.255747036638244"),
                    currency="GBP",
                    type=CostType.STANDING_CHARGE_COST,
                ),
                Cost(
                    amount=Decimal("25.581227231256353"),
                    currency="GBP",
                    type=CostType.CONSUMPTION_COST,
                ),
            ],
            type=ReadingType.ELECTRICITY,
        ),
        Reading(
            start_at=datetime(2024, 1, 12, 0, 0, tzinfo=timezone.utc),
            end_at=datetime(2024, 1, 13, 0, 0, tzinfo=timezone.utc),
            unit="kwh",
            value=Decimal("5.781684051845659"),
            costs=[
                Cost(
                    amount=Decimal("82.80427671543171"),
                    currency="GBP",
                    type=CostType.STANDING_CHARGE_COST,
                ),
                Cost(
                    amount=Decimal("46.41564806162006"),
                    currency="GBP",
                    type=CostType.CONSUMPTION_COST,
                ),
            ],
            type=ReadingType.ELECTRICITY,
        ),
        Reading(
            start_at=datetime(2024, 1, 13, 0, 0, tzinfo=timezone.utc),
            end_at=datetime(2024, 1, 14, 0, 0, tzinfo=timezone.utc),
            unit="kwh",
            value=Decimal("31.281634430543235"),
            costs=[
                Cost(
                    amount=Decimal("9.805394767961195"),
                    currency="GBP",
                    type=CostType.STANDING_CHARGE_COST,
                ),
                Cost(
                    amount=Decimal("74.80780318455047"),
                    currency="GBP",
                    type=CostType.CONSUMPTION_COST,
                ),
            ],
            type=ReadingType.ELECTRICITY,
        ),
    ]


@fixture
def paginated_readings(
    gas_readings: List[Reading], electricity_readings: List[Reading]
) -> PaginatedReadings:
    return PaginatedReadings(
        readings=gas_readings + electricity_readings, has_next_page=False, cursor=CURSOR
    )
