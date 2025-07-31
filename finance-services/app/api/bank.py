from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.bank_service import create_bank_account, create_plaid_link_token, exchange_public_token, get_user_banks
from app.schemas.bank import PublicTokenRequest
from app.models.user import User
# Auth Services & JWT
from app.services.auth_service import authenticate_user
from app.services.bank_service import create_bank_account
# Utility Functions
from app.utils.database import get_db
from app.utils.dwolla import add_funding_source
# App Config
from app.core.config import settings
# Plaid SDK
from app.utils.plaid_client import client,encrypt_id  # Initialized PlaidApi instance
# Plaid Link Token
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
# Plaid Token Exchange & Accounts
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.processor_token_create_request import ProcessorTokenCreateRequest

import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/bank", tags=["Bank"])

@router.post("/plaid/create_link_token")
async def create_link_token(current_user: User = Depends(authenticate_user)):
    logger.info(f"Current User ID : {current_user.id}")
    try:
        request = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(str(current_user.id)),
            client_name="Personal Finance Tracker",
            products=[Products("auth")],
            country_codes=[CountryCode("US")],
            language='en',
        )
        logger.info(f"request : {request}")
        response = client.link_token_create(request)
        logger.info(f"response : {response}")
        
        ## delete
        response_dict = response.to_dict()
        print(json.dumps(response_dict, indent=2, default=str))
        #############################################################
        logger.info(f"response_dict : {response_dict}")
        logger.info(f"link_token : {response.link_token}")
        return {"link_token": response.link_token}
    except Exception as e:
        print(e)

@router.post("/plaid/exchange_public_token")
async def exchange_public_token(
    payload: PublicTokenRequest,
    current_user: User = Depends(authenticate_user),
    db: Session = Depends(get_db)
):
    ACH_ELIGIBLE_SUBTYPES = ["checking", "savings"]
    try:
        # Step 1: Exchange public token for access token and item ID
        request = ItemPublicTokenExchangeRequest(public_token=payload.public_token)
        response = client.item_public_token_exchange(request)
        response_data = response.to_dict()
        # print("Response Data:",response_data)

        access_token = response_data["access_token"]
        print("Access Token:", access_token)

        item_id = response_data["item_id"]
        # print("Item ID:", item_id)
        
        # # log or save access_token to DB for user
        # print("Response Data:",response_data)
        # print("Access Token:", access_token)
        # print("Item ID:", item_id)

        # Step 2: Get accounts using access token
        accounts_request = AccountsGetRequest(access_token=access_token)
        # print("Accounts request:",accounts_request)
        
        accounts_response = client.accounts_get(accounts_request)
        # print("Accounts response:",accounts_response)

        accounts_data = accounts_response.to_dict()
        print("Accounts data:",accounts_data)
        
        accounts = accounts_data.get("accounts", [])
        
        if not accounts:
            raise HTTPException(status_code=400, detail="No accounts found for the user")
        
        bank_creation_messages = []

        for account in accounts:
            print("Account data:",account)
            
            account_type = account["type"]
            account_subtype = account["subtype"]

            account_id = account["account_id"]
            print("Account ID:", account_id)
            
            bank_name = account["name"]
            print("Bank Name:", bank_name)

            # Skip unsupported accounts if absolutely invalid (very rare edge case)
            if not account_type or not account_subtype:
                continue

            # CASE 1: ACH-Eligible Account (checking/savings)
            if account_type == "depository" and account_subtype in ACH_ELIGIBLE_SUBTYPES:
                
                # 3. Create processor token for Dwolla

                processor_request = ProcessorTokenCreateRequest(
                    access_token=access_token,
                    account_id=account_id,
                    processor="dwolla"  # Just a string
                )
                processor_token_response = client.processor_token_create(processor_request).to_dict()
                processor_token = processor_token_response["processor_token"]

                print("processor_token_response:", processor_token_response)

                # 4. Create Dwolla funding source (O)
                funding_source_url = add_funding_source(
                    current_user.dwolla_customer_id,
                    processor_token,
                    bank_name
                )

                print("funding_source_url: ", funding_source_url)

                if not funding_source_url:
                    raise Exception("Failed to create Dwolla funding source")

            else:
                print(f"Storing non-ACH account: {account_type} ({account_subtype})")
                funding_source_url = None  # No Dwolla integration for these
            
            # 5. Create bank account in your system (O)
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
                db
            )
            bank_creation_messages.append({
                "account_id": account_id,
                "bank_name": bank_name,
                **BankMessage
            })
        
        return {
            "public_token_exchange": "complete",
            "banks_created": bank_creation_messages
        }
    
    except Exception as e:
        print("Error exchanging public token:", e)
        raise HTTPException(status_code=500, detail=f"Could not exchange public token : {e}")






@router.post("/link")
async def link_bank():
    return await create_plaid_link_token()

@router.post("/exchange")
async def exchange_token():
    return await exchange_public_token()

@router.get("/banks")
async def list_banks():
    return await get_user_banks()
