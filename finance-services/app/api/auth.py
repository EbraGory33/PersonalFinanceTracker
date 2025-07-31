# ─────────────────────────────────────────────────────────────────────────────
# 🚀 FastAPI Core
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse

# 📦 Database & ORM
from sqlalchemy.orm import Session

# 📦 Pydantic Schemas
from app.schemas.auth import (
    UserResponse,
    SignupRequest,
    SigninRequest,
    PublicTokenRequest
)

# 👤 Models
from app.models.user import User

# 🔐 Auth Services & JWT
from app.services.auth_service import (
    register_user,
    authenticate_user,
    validate_user_credentials
)
from app.services.bank_service import create_bank_account
from app.utils.jwt_handler import create_access_token

# 🛠️ Utility Functions
from app.utils.database import get_db
from app.utils.dwolla import add_funding_source

# ⚙️ App Config
from app.core.config import settings

# ─────────────────────────────────────────────────────────────────────────────
# 💰 Plaid SDK
from app.utils.plaid_client import client,encrypt_id  # Initialized PlaidApi instance

# 🏦 Plaid Link Token
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode

# 🔄 Plaid Token Exchange & Accounts
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.processor_token_create_request import ProcessorTokenCreateRequest



router = APIRouter(prefix="/auth", tags=["Auth"])

max_age = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    data: SignupRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists."
        )
    
    user = await register_user(data, db)
    access_token = create_access_token({"user_Id": str(user.id)})
    response = JSONResponse(content=user.model_dump())
    response.set_cookie(
        key="jwt",
        value=access_token,
        httponly=True,
        secure=settings.SECURE_COOKIE,  # True in production
        samesite=settings.SAME_SITE,    # "none" for prod, "lax" for dev
        max_age=max_age,
        path="/"
    )
    return response

@router.post("/signin", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def signin(
    data: SigninRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    user = await validate_user_credentials(data,db)
    access_token = create_access_token({"user_Id": str(user.id)})
    print(f"Secure or Not:{settings.SECURE_COOKIE}")
    print(f"SameSite:{settings.SAME_SITE}")
    response = JSONResponse(content=user.model_dump())
    response.set_cookie(
        key="jwt",
        value=access_token,
        httponly=True,
        secure=settings.SECURE_COOKIE,  # True in production,
        samesite=settings.SAME_SITE,    # "none" for prod, "lax" for dev 
        max_age=max_age,
        path="/"
    )
    return response
    
@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    response.delete_cookie(
        key="jwt",
        path="/"
    )
    return {"message": "Logout successful"}

@router.get("/authenticate", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_profile(current_user: User = Depends(authenticate_user)):
    return current_user

## delete
import json

@router.post("/plaid/create_link_token")
async def create_link_token(current_user: User = Depends(authenticate_user)):
    try:
        request = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(current_user.id), # Replace with actual user ID
            client_name="Your App Name",
            products=[Products("auth")],
            country_codes=[CountryCode("US")],
            language='en',
        )
        response = client.link_token_create(request)
        
        ## delete
        response_dict = response.to_dict()
        print(json.dumps(response_dict, indent=2))
        #############################################################

        return {"link_token": response.link_token}
    except Exception as e:
        print(e)

@router.post("/plaid/exchange_public_token")
async def exchange_public_token(
    payload: PublicTokenRequest,
    current_user: User = Depends(authenticate_user),
    db: Session = Depends(get_db)
):
    try:
        # Step 1: Exchange public token for access token and item ID
        request = await ItemPublicTokenExchangeRequest(public_token=payload.public_token)
        response = await client.item_public_token_exchange(request)
        response_data = response.to_dict()
        
        access_token = response_data["access_token"]
        item_id = response_data["item_id"]
        
        # log or save access_token to DB for user
        print("Response Data:",response_data)
        print("Access Token:", access_token)
        print("Item ID:", item_id)

        # Step 2: Get accounts using access token
        accounts_request = AccountsGetRequest(access_token=access_token)
        accounts_response = client.accounts_get(accounts_request)
        accounts_data = accounts_response.to_dict()
        
        account_id = accounts_data["account_id"]
        bank_name = accounts_data["name"]
        
        print("Accounts data:",accounts_data)
        print("Account ID:", access_token)
        print("Bank Name:", bank_name)


        # 3. Create processor token for Dwolla (O)

        processor_request = ProcessorTokenCreateRequest(
            access_token=access_token,
            account_id=account_id,
            processor="dwolla"  # Just a string
        )
        processor_token_response = client.processor_token_create(processor_request).to_dict()
        processor_token = processor_token_response["processor_token"]

        # 4. Create Dwolla funding source (O)
        funding_source_url = await add_funding_source({
            "dwolla_customer_id": current_user.dwolla_customer_id,
            "processor_token": processor_token,
            "bank_name": bank_name
        })

        if not funding_source_url:
            raise Exception("Failed to create Dwolla funding source")

        
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

        return {
            "public_token_exchange": "complete",
            "Create_Bank_Message": BankMessage
        }
    
    except Exception as e:
        print("Error exchanging public token:", e)
        raise HTTPException(status_code=500, detail=f"Could not exchange public token : {e}")