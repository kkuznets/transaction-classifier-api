from datetime import datetime
from typing import Optional

from sqlalchemy import String, cast
from sqlmodel.sql.expression import Select

from app.models import CategoryURLChoices, Transaction


# Build a query with optional filters
def build_query(
    base_query: Select,
    counterpart_name: Optional[str] = None,
    category: Optional[CategoryURLChoices] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> Select:
    if counterpart_name:
        base_query = base_query.where(
            cast(Transaction.counterpart_name, String).ilike(f"%{counterpart_name}%")
        )
    if category:
        base_query = base_query.where(
            cast(Transaction.category, String).ilike(f"%{category.value}%")
        )
    if start_date:
        base_query = base_query.where(Transaction.transaction_time_utc >= start_date)
    if end_date:
        base_query = base_query.where(Transaction.transaction_time_utc <= end_date)
    return base_query
