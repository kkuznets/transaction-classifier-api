from sqlmodel.sql.expression import Select
from datetime import datetime
from typing import Optional
from models import Transaction, CategoryURLChoices


def build_query(
    base_query: Select,
    counterpart_name: Optional[str] = None,
    category: Optional[CategoryURLChoices] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> Select:
    if counterpart_name:
        base_query = base_query.where(
            Transaction.counterpartName.ilike(f"%{counterpart_name}%")
        )
    if category:
        base_query = base_query.where(
            Transaction.category.ilike(category.value.capitalize())
        )
    if start_date:
        base_query = base_query.where(Transaction.transactionTimeUtc >= start_date)
    if end_date:
        base_query = base_query.where(Transaction.transactionTimeUtc <= end_date)
    return base_query
