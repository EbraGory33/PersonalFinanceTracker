from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.bank import CreateBankAccountRequest
from app.models.bank import Bank
from app.utils.plaid_client import encrypt_id


async def create_plaid_link_token():
    return True

async def exchange_public_token():
    return True

async def get_user_banks():
    return True

async def create_bank_account(
    request: CreateBankAccountRequest,
    currentuser,
    db: Session
):
    if not currentuser:
        raise HTTPException(status_code=404, detail="User not found")

    # Optionally encrypt access token
    encrypted_token = encrypt_id(request.access_token)

    new_bank_account = Bank(
        user_id=request.user_id,
        bank_id=request.bank_id,
        account_id=request.account_id,
        access_token=encrypted_token,
        funding_source_url=request.funding_source_url,
        sharable_id=request.shareable_id
    )

    db.add(new_bank_account)
    db.commit()
    db.refresh(new_bank_account)

    return {
        "message": "Bank account created successfully.",
        "bank_account": {
            "id": new_bank_account.id,
            "user_id": new_bank_account.user_id,
            "bank_id": new_bank_account.bank_id,
            "account_id": new_bank_account.account_id,
            "funding_source_url": new_bank_account.funding_source_url,
            "sharable_id": new_bank_account.sharable_id,
        }
    }

  