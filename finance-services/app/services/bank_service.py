from fastapi import Depends, HTTPException, Request, status
from app.models.bank import Bank


async def create_plaid_link_token():
    return True

async def exchange_public_token():
    return True

async def get_user_banks():
    return True