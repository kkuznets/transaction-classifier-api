from enum import Enum
from datetime import datetime
from sqlmodel import SQLModel, Field
import uuid


class CategoryURLChoices(Enum):
    RETAIL = "retail"
    GROCERIES = "groceries"
    UTILITIES = "utilities"
    TRAVEL = "travel"


class CategoryChoices(Enum):
    RETAIL = "Retail"
    GROCERIES = "Groceries"
    UTILITIES = "Utilities"
    TRAVEL = "Travel"


class TransactionBase(SQLModel):
    transactionId: uuid.UUID
    amount: float
    counterpartName: str
    transactionTimeUtc: datetime
    transactionType: str


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase, table=True):
    id: int = Field(default=None, primary_key=True)
    category: CategoryChoices
