import uuid
from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


# Model for the category choices in the query parameters
class CategoryURLChoices(str, Enum):
    RETAIL = "retail"
    GROCERIES = "groceries"
    UTILITIES = "utilities"
    TRAVEL = "travel"

# Model for the category choices in the database
class CategoryChoices(str, Enum):
    RETAIL = "Retail"
    GROCERIES = "Groceries"
    UTILITIES = "Utilities"
    TRAVEL = "Travel"

# Model for the /categories-summary route response
class CategorySummary(SQLModel):
    category: str
    transaction_count: int
    total_amount: float

    class Config:
        json_schema_extra = {
            "example": {
                "category": "Retail",
                "transaction_count": 5,
                "total_amount": -150.00,
            }
        }

# Model for the /counterparts-per-category route response
class CounterpartsPerCategory(SQLModel):
    category: str
    unique_counterparts: list[str]

    class Config:
        json_schema_extra = {
            "example": {
                "category": "Groceries",
                "unique_counterparts": ["Walmart", "Whole Foods"],
            }
        }

#  Model for the transaction data. ID is generated on the database side automatically
class TransactionBase(SQLModel):
    transaction_id: uuid.UUID
    amount: float
    counterpart_name: str
    transaction_time_utc: datetime = Field(index=True)
    transaction_type: str

# Don't need to include any additional fields to create a transaction
class TransactionCreate(TransactionBase):
    pass

#  Model and table for the transaction data with the ID included (for database queries)
class Transaction(TransactionBase, table=True):
    id: int = Field(default=None, primary_key=True)
    category: CategoryChoices

    class Config:
        json_schema_extra = {
            "example": {
                "transaction_id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
                "amount": -50.00,
                "counterpart_name": "Walmart",
                "transaction_time_utc": "2025-08-11T03:44:38.035695Z",
                "transaction_type": "CARD_TRANSACTION",
                "category": "Retail",
            }
        }
