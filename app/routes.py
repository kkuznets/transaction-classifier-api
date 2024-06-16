from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel import Session, func, select

from app.db import get_session
from app.dependencies import (
    get_category,
    get_counterpart_name,
    get_end_date,
    get_start_date,
)
from app.helpers import build_query
from app.models import (
    CategorySummary,
    CategoryURLChoices,
    CounterpartsPerCategory,
    Transaction,
    TransactionCreate,
)
from app.utils import classify_transaction

router = APIRouter()


# Endpoint to get all transactions with optional filters
@router.get(
    "/transactions",
    summary="All transactions",
)
async def transactions(
    counterpart_name: Optional[str] = Depends(get_counterpart_name),
    category: Optional[CategoryURLChoices] = Depends(get_category),
    start_date: Optional[datetime] = Depends(get_start_date),
    end_date: Optional[datetime] = Depends(get_end_date),
    session: Session = Depends(get_session),
) -> list[Transaction]:
    query = build_query(
        select(Transaction), counterpart_name, category, start_date, end_date
    )
    transactions = session.exec(query).all()
    return transactions


# Endpoint to get a transaction by its transaction_id (not unique)
@router.get(
    "/transactions/{transaction_id}",
    summary="Transaction(s) by transaction_id",
)
async def get_transaction_by_id(
    transaction_id: UUID = Path(
        ...,
        title="Transaction ID",
        description="The unique identifier for the transaction",
        example="d290f1ee-6c54-4b01-90e6-d701748f0851",
    ),
    session: Session = Depends(get_session),
) -> List[Transaction]:
    query = select(Transaction).where(Transaction.transaction_id == transaction_id)
    result = session.exec(query).all()
    # Check if the transaction exists or if result is empty
    if not result:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return result


# Endpoint to get a summary of categories within a date range
@router.get("/categories-summary", summary="Categories summary")
async def categories_summary(
    category: Optional[CategoryURLChoices] = Depends(get_category),
    start_date: Optional[datetime] = Depends(get_start_date),
    end_date: Optional[datetime] = Depends(get_end_date),
    session: Session = Depends(get_session),
) -> List[CategorySummary]:
    base_query = select(
        Transaction.category,
        func.count(Transaction.id).label("transaction_count"),
        func.sum(Transaction.amount).label("total_amount"),
    ).group_by(Transaction.category)
    query = build_query(
        base_query, category=category, start_date=start_date, end_date=end_date
    )
    results = session.exec(query).all()
    return [
        {
            "category": result.category,
            "transaction_count": result.transaction_count,
            "total_amount": result.total_amount,
        }
        for result in results
    ]


# Endpoint to get unique counterparts per category within a date range
@router.get("/counterparts-per-category", summary="Counterparts per category")
async def counterparts_per_category(
    category: Optional[CategoryURLChoices] = Depends(get_category),
    start_date: Optional[datetime] = Depends(get_start_date),
    end_date: Optional[datetime] = Depends(get_end_date),
    session: Session = Depends(get_session),
) -> List[CounterpartsPerCategory]:
    base_query = (
        select(Transaction.category, Transaction.counterpart_name)
        .distinct(Transaction.counterpart_name)
        .group_by(Transaction.category, Transaction.counterpart_name)
    )
    query = build_query(
        base_query, category=category, start_date=start_date, end_date=end_date
    )
    results = session.exec(query).all()

    unique_counterparts = {
        category: [
            result.counterpart_name for result in results if result.category == category
        ]
        for category in set(result.category for result in results)
    }

    return [
        {"category": category, "unique_counterparts": counterparts}
        for category, counterparts in unique_counterparts.items()
    ]


# Endpoint to create a new transaction
@router.post("/transactions", summary="Create a transaction")
async def create_transaction(
    transaction_data: TransactionCreate, session: Session = Depends(get_session)
) -> Transaction:
    transaction = Transaction(
        **transaction_data.model_dump(),
        category=classify_transaction(transaction_data),
    )
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction
