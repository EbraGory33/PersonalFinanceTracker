# ================================================
# Imports
# ================================================

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from typing import Optional
import logging
import json
import traceback

# ========== Models ==========
from app.models.user import User
from app.models.bank import Bank

# ========== Schemas ==========
from app.schemas.bank import (
    PublicTokenRequest,
    BankResponse,
    BanksResponse,
)

# ========== Services ==========
from app.services.auth_service import authenticate_user
from app.services.bank_service import (
    create_bank_account,
    getAccount,
    getAccounts,
)

# ========== Utilities ==========
from app.utils.database import get_db
from app.utils.dwolla import add_funding_source
from app.utils.plaid_client import client, encrypt_id
from app.core.config import settings

# ========== Plaid Models ==========
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest,
)
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.processor_token_create_request import ProcessorTokenCreateRequest


# ================================================
# Router Config
# ================================================

router = APIRouter(prefix="/bank", tags=["Bank"])
logger = logging.getLogger(__name__)


# ================================================
# Plaid Routes
# ================================================


@router.post("/plaid/create_link_token")
async def create_link_token(current_user: User = Depends(authenticate_user)):
    logger.info(f"Creating link token for user ID: {current_user.id}")
    try:
        request = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(str(current_user.id)),
            client_name="Personal Finance Tracker",
            products=[Products(p) for p in settings.PLAID_PRODUCT],
            country_codes=[CountryCode("US")],
            language="en",
        )

        response = client.link_token_create(request)
        logger.info(f"Link token created: {response.link_token}")
        return {"link_token": response.link_token}
    except Exception as e:
        logger.error(f"Error creating link token: {e}")
        raise HTTPException(status_code=500, detail="Failed to create Plaid link token")


@router.post("/plaid/exchange_public_token")
async def exchange_public_token(
    payload: PublicTokenRequest,
    current_user: User = Depends(authenticate_user),
    db: Session = Depends(get_db),
):
    ACH_ELIGIBLE_SUBTYPES = ["checking", "savings"]
    try:
        # Exchange public token for access token
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=payload.public_token
        )
        exchange_response = client.item_public_token_exchange(
            exchange_request
        ).to_dict()

        access_token = exchange_response["access_token"]
        item_id = exchange_response["item_id"]

        # Get account info from Plaid
        accounts_response = client.accounts_get(
            AccountsGetRequest(access_token=access_token)
        ).to_dict()

        accounts = accounts_response.get("accounts", [])
        if not accounts:
            raise HTTPException(status_code=400, detail="No accounts found for user")

        bank_creation_messages = []

        for account in accounts:
            account_id = account["account_id"]
            account_type = account["type"]
            account_subtype = account["subtype"]
            bank_name = account["name"]

            if not account_type or not account_subtype:
                continue

            # Handle ACH-eligible accounts
            funding_source_url = None
            if (
                account_type == "depository"
                and account_subtype in ACH_ELIGIBLE_SUBTYPES
            ):
                processor_request = ProcessorTokenCreateRequest(
                    access_token=access_token,
                    account_id=account_id,
                    processor="dwolla",
                )
                processor_token = client.processor_token_create(
                    processor_request
                ).to_dict()["processor_token"]
                funding_source_url = add_funding_source(
                    current_user.dwolla_customer_id,
                    processor_token,
                    bank_name,
                )
                if not funding_source_url:
                    raise Exception("Failed to create Dwolla funding source")

            # Create bank in DB
            BankMessage = await create_bank_account(
                {
                    "user_id": current_user.id,
                    "bank_id": item_id,
                    "account_id": account_id,
                    "access_token": access_token,
                    "funding_source_url": funding_source_url,
                    "shareable_id": encrypt_id(account_id),
                },
                current_user,
                db,
            )

            bank_creation_messages.append(
                {"account_id": account_id, "bank_name": bank_name, **BankMessage}
            )

        return {
            "public_token_exchange": "complete",
            "banks_created": bank_creation_messages,
        }

    except Exception as e:
        logger.error(f"Error exchanging public token: {e}")
        raise HTTPException(
            status_code=500, detail=f"Could not exchange public token: {str(e)}"
        )


# ================================================
# Bank Retrieval Routes
# ================================================


@router.get("/userBanks", response_model=BanksResponse)
async def get_user_banks(
    current_user: User = Depends(authenticate_user),
    db: Session = Depends(get_db),
):
    banks = db.query(Bank).filter(Bank.user_id == current_user.id).all()
    bank_responses = [BankResponse.model_validate(bank) for bank in banks]
    return BanksResponse(banks=bank_responses)


@router.get("/getBank", response_model=BankResponse)
async def get_bank_by_shareable_id(
    shareableId: str,
    current_user: User = Depends(authenticate_user),
    db: Session = Depends(get_db),
):
    bank = db.query(Bank).filter(Bank.shareable_id == shareableId).first()
    if not bank or bank.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Bank not found")
    return bank


# ================================================
# Account-Specific Routes
# ================================================


@router.get("/getAccounts")
async def get_all_user_accounts(
    current_user: User = Depends(authenticate_user),
    db: Session = Depends(get_db),
):
    return await getAccounts(current_user, db)


@router.get("/getAccount")
async def get_single_user_account(
    shareableId: str,
    current_user: User = Depends(authenticate_user),
    db: Session = Depends(get_db),
):
    try:
        return await getAccount(current_user, shareableId, db)
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"Error fetching account: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "type": type(e).__name__,
                "trace": tb,
            },
        )
