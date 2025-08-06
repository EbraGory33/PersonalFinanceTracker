# ===================================================
# Imports
# ===================================================

# Standard Library
from datetime import datetime, timezone

# FastAPI
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

# SQLAlchemy
from sqlalchemy.orm import Session

# Schemas
from app.schemas.transaction import (
    TransactionParams,
    TransactionResponse,
    TransactionsResponse,
    TransferRequest,
)

# Models
from app.models.transactions import Transaction

# Utilities
from app.utils.database import get_db
from app.utils.dwolla import create_transfer


# ===================================================
# Router Setup
# ===================================================

router = APIRouter(prefix="/transaction", tags=["Transaction"])


# ===================================================
# Endpoints
# ===================================================


@router.post("/createTransfer", status_code=status.HTTP_201_CREATED)
async def create_transfer_endpoint(data: TransferRequest):
    print(
        "Calling create_transfer: ",
        data.source_funding_source_url,
        data.destination_funding_source_url,
        data.amount,
    )
    try:
        res = create_transfer(
            data.source_funding_source_url,
            data.destination_funding_source_url,
            data.amount,
        )
        print(f"create_transfer response: {res}")
        return res
    except Exception as err:
        print("Error transferring funds:", err)
        raise HTTPException(status_code=500, detail=f"Error transferring funds: {err}")


@router.post(
    "/createTransaction",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(data: TransactionParams, db: Session = Depends(get_db)):
    new_transaction = Transaction(
        name=data.name,
        sender_id=data.sender_id,
        receiver_id=data.receiver_id,
        sender_bank_id=data.sender_bank_id,
        receiver_bank_id=data.receiver_bank_id,
        amount=data.amount,
        type="transfer",
        category=data.category,
        channel=data.channel,
        pending=data.pending,
        date=data.date or datetime.now(timezone.utc),
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return {
        "id": new_transaction.id,
        "name": new_transaction.name,
        "email": data.email,
        "sender_id": new_transaction.sender_id,
        "receiver_id": new_transaction.receiver_id,
        "sender_bank_id": new_transaction.sender_bank_id,
        "receiver_bank_id": new_transaction.receiver_bank_id,
        "amount": new_transaction.amount,
        "type": new_transaction.type,
        "category": new_transaction.category,
        "channel": new_transaction.channel,
        "pending": (
            new_transaction.pending if new_transaction.pending is not None else True
        ),
        "date": new_transaction.date,
    }
