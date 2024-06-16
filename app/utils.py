import os

from dotenv import load_dotenv
from fastapi import HTTPException
from openai import OpenAI

from app.models import CategoryChoices, TransactionCreate

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


def classify_transaction(transaction: TransactionCreate) -> CategoryChoices:
    prompt = f"""
    Classify the following transaction into one of the categories:
    {', '.join([cat.value for cat in CategoryChoices])}.
    Transaction details:
        counterpart name = {transaction.counterpart_name},
        amount = {transaction.amount},
        transaction type = {transaction.transaction_type}
    Answer with the category name only.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that classifies transactions.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=10,
        n=1,
        stop=None,
        temperature=0.5,
    )
    category = response.choices[0].message.content.strip()
    if category.upper() not in CategoryChoices.__members__:
        raise HTTPException(
            status_code=400, detail="Unable to classify the transaction category."
        )
    return category.upper()
