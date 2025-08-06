# =====================================
# IMPORTS
# =====================================
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import asyncio

# Plaid
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
from plaid.model.country_code import CountryCode

# App - Utils
from app.utils.plaid_client import client, encrypt_id, decrypt_id
from app.utils.database import get_db

# App - Services
from app.services.auth_service import authenticate_user
from app.services.transaction_service import get_transactions, get_transactions_by_bank

# App - Models
from app.models.user import User
from app.models.bank import Bank

# App - Schemas
from app.schemas.bank import (
    CreateBankAccountRequest,
    BankResponse,
    BanksResponse,
)

# =====================================
# HELPERS
# =====================================


def get_institution(institution_id: str):
    """
    Fetch institution details from Plaid API using institution ID.
    """
    try:
        institution_response = client.institutions_get_by_id(
            InstitutionsGetByIdRequest(
                institution_id=institution_id,
                country_codes=[CountryCode("US")],
            )
        )
        return institution_response.institution
    except Exception as e:
        print("Error getting institution:", e)
        raise HTTPException(
            status_code=500, detail=f"Could not fetch institution info: {e}"
        )


# =====================================
# CORE LOGIC FUNCTIONS
# =====================================


async def getBank(shareableId: str, db: Session):
    bank = db.query(Bank).filter(Bank.shareable_id == shareableId).first()
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    return bank


async def getBanks(current_user: User, db: Session):
    banks = db.query(Bank).filter(Bank.user_id == current_user.id).all()
    bank_responses = [BankResponse.model_validate(bank) for bank in banks]
    return BanksResponse(banks=bank_responses)


async def getAccount(current_user: User, shareableId: str, db: Session):
    try:
        bank = await getBank(shareableId, db)
        decrypted_token = decrypt_id(bank.access_token)
        accountsResponse = client.accounts_get({"access_token": decrypted_token})

        target_account_id = bank.account_id

        accountData = next(
            (
                acct
                for acct in accountsResponse["accounts"]
                if acct["account_id"] == target_account_id
            ),
            None,
        )

        if not accountData:
            raise HTTPException(status_code=404, detail="Account data not found")

        institution = get_institution(accountsResponse["item"]["institution_id"])

        transactions_response = await get_transactions(
            decrypted_token, target_account_id
        )

        transfer_transactions_raw = await get_transactions_by_bank(
            current_user, bank, db
        )

        transfer_transactions = [
            {
                "id": tx.id,
                "name": tx.name,
                "amount": tx.amount,
                "date": tx.date.date(),
                "payment_channel": "internal",
                "category": tx.category,
                "type": "debit" if tx.sender_bank_id == bank.id else "credit",
            }
            for tx in transfer_transactions_raw
        ]

        account = {
            "id": accountData.account_id,
            "available_balance": accountData.balances.available,
            "current_balance": accountData.balances.current,
            "institution_id": institution.institution_id,
            "name": accountData.name,
            "official_name": accountData.official_name,
            "mask": accountData.mask,
            "type": str(accountData.type),
            "subtype": str(accountData.subtype),
            "bank_id": bank.id,
            "shareable_id": bank.shareable_id,
        }

        all_transactions = transactions_response + transfer_transactions
        all_transactions.sort(key=lambda tx: tx["date"], reverse=True)

        return {"data": account, "transactions": all_transactions}

    except Exception as e:
        print(f"Error getting account: {e}")
        raise HTTPException(
            status_code=500, detail=f"Could not fetch account data : {e}"
        )


async def getAccounts(current_user: User, db: Session):
    try:
        banks_response = await getBanks(current_user, db)
        banks = banks_response.banks
        banks_by_account_id = {b.account_id: b for b in banks}

        accounts = []

        async def process_bank(bank):
            decrypted_token = decrypt_id(bank.access_token)
            accountsResponse = client.accounts_get({"access_token": decrypted_token})

            for accountData in accountsResponse["accounts"]:
                matching_bank = banks_by_account_id.get(accountData.account_id)
                if not matching_bank:
                    continue

                institution = get_institution(
                    accountsResponse["item"]["institution_id"]
                )

                account = {
                    "id": accountData.account_id,
                    "available_balance": accountData.balances.available,
                    "current_balance": accountData.balances.current,
                    "institution_id": institution.institution_id,
                    "name": accountData.name,
                    "official_name": accountData.official_name,
                    "mask": accountData.mask,
                    "type": str(accountData.type),
                    "subtype": str(accountData.subtype),
                    "bank_id": matching_bank.id,
                    "shareable_id": matching_bank.shareable_id,
                }
                accounts.append(account)

        await asyncio.gather(
            *(
                process_bank(bank)
                for bank in {b.bank_id: b for b in banks or []}.values()
            )
        )

        totalBanks = len(accounts)
        totalCurrentBalance = sum(
            account["current_balance"] or 0 for account in accounts
        )

        return {
            "accounts": accounts,
            "total_banks": totalBanks,
            "total_current_balance": totalCurrentBalance,
        }

    except Exception as e:
        print("Error getting Accounts:", e)
        raise HTTPException(status_code=500, detail=f"Could not get Accounts : {e}")


async def create_bank_account(
    request: CreateBankAccountRequest, currentuser: User, db: Session
):
    if not currentuser:
        raise HTTPException(status_code=404, detail="User not found")

    encrypted_token = encrypt_id(request["access_token"])

    new_bank_account = Bank(
        user_id=request["user_id"],
        bank_id=request["bank_id"],
        account_id=request["account_id"],
        access_token=encrypted_token,
        funding_source_url=request["funding_source_url"],
        shareable_id=request["shareable_id"],
    )

    db.add(new_bank_account)
    db.commit()
    db.refresh(new_bank_account)

    return {
        "bank_account": {
            "id": new_bank_account.id,
            "user_id": new_bank_account.user_id,
            "bank_id": new_bank_account.bank_id,
            "account_id": new_bank_account.account_id,
            "funding_source_url": new_bank_account.funding_source_url,
            "shareable_id": new_bank_account.shareable_id,
        }
    }
