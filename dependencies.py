from fastapi import Query
from typing import Optional
from datetime import datetime
from models import CategoryURLChoices


def get_counterpart_name(
    counterpart_name: Optional[str] = Query(
        None,
        title="Counterpart Name",
        description="Partial match for counterpart name (case insensitive)",
        examples=["Example Counterpart Name"],
    )
) -> Optional[str]:
    return counterpart_name


def get_category(
    category: Optional[CategoryURLChoices] = Query(
        None,
        title="Category",
        description="Filter by category",
        examples=[list(CategoryURLChoices)[0].value],
    )
) -> Optional[CategoryURLChoices]:
    return category


def get_start_date(
    start_date: Optional[datetime] = Query(
        None,
        title="Start Date",
        description="Filter by start date or datetime",
        examples=["2025-08-11T03:44:38.035695Z"],
    )
) -> Optional[datetime]:
    return start_date


def get_end_date(
    end_date: Optional[datetime] = Query(
        None,
        title="End Date",
        description="Filter by end date or datetime",
        examples=["2025-08-11T03:44:38.035695Z"],
    )
) -> Optional[datetime]:
    return end_date
