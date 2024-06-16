from fastapi import FastAPI, HTTPException, Depends
from models import (
    TransactionCreate,
    Transaction,
    CategoryURLChoices,
    CategoryChoices,
)
from dependencies import (
    get_counterpart_name,
    get_category,
    get_start_date,
    get_end_date,
)
from utils import classify_transaction
from helpers import build_query
from sqlmodel import Session, select, func
from datetime import datetime
from typing import Optional
from db import get_session


app = FastAPI()


@app.get("/transactions")
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


@app.get("/categories-summary")
async def categories_summary(
    category: Optional[CategoryURLChoices] = Depends(get_category),
    start_date: Optional[datetime] = Depends(get_start_date),
    end_date: Optional[datetime] = Depends(get_end_date),
    session: Session = Depends(get_session),
):
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


@app.get("/counterparts-per-category")
async def counterparts_per_category(
    category: Optional[CategoryURLChoices] = Depends(get_category),
    start_date: Optional[datetime] = Depends(get_start_date),
    end_date: Optional[datetime] = Depends(get_end_date),
    session: Session = Depends(get_session),
):
    base_query = (
        select(Transaction.category, Transaction.counterpartName)
        .distinct(Transaction.counterpartName)
        .group_by(Transaction.category, Transaction.counterpartName)
    )
    query = build_query(
        base_query, category=category, start_date=start_date, end_date=end_date
    )
    results = session.exec(query).all()

    unique_counterparts = {
        category: [
            result.counterpartName for result in results if result.category == category
        ]
        for category in set(result.category for result in results)
    }

    return [
        {"category": category, "unique_counterparts": counterparts}
        for category, counterparts in unique_counterparts.items()
    ]


@app.post("/transactions")
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
