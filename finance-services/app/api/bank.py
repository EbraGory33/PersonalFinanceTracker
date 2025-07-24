from fastapi import APIRouter
#from app.services.bank_service import create_plaid_link_token, exchange_public_token, get_user_banks

router = APIRouter(prefix="/bank", tags=["Bank"])
'''
@router.post("/link")
async def link_bank():
    return await create_plaid_link_token()

@router.post("/exchange")
async def exchange_token():
    return await exchange_public_token()

@router.get("/banks")
async def list_banks():
    return await get_user_banks()
'''