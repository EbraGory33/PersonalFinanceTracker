from fastapi import Depends, HTTPException
from datetime import datetime

from app.services.auth_service import authenticate_user
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.bank import CreateBankAccountRequest

from app.utils.plaid_client import client, encrypt_id, decrypt_id  # Initialized PlaidApi instance
from plaid.model.accounts_get_request import AccountsGetRequest

from app.utils.database import get_db

from app.models.user import User
from app.models.bank import Bank
from app.schemas.bank import BankResponse, BanksResponse

from app.services.auth_service import authenticate_user
from app.services.transaction_service import get_transactions, getTransactionsByBank
import asyncio


async def getBank(
    # bank_id: int,
    shareableId: str,
    db: Session
):
    # print(f"bank_id : {bank_id}")

    bank = db.query(Bank).filter(Bank.shareable_id == shareableId).first()
    
    # print(f"bank : {bank}")

    if not bank:
        raise HTTPException(
            status_code=404,
            detail="Bank not found"
        )
    
    return bank

async def getBanks(current_user: User, db: Session):
    banks = db.query(Bank).filter(Bank.user_id == current_user.id).all()
    # print(f"banks : {banks}")
    bank_responses = [BankResponse.model_validate(bank) for bank in banks]
    # print(f"bank_responses : {bank_responses}")
    return BanksResponse(banks=bank_responses)

# async def getAccount(current_user: User, Bank_ID: int, db: Session):
async def getAccount(current_user: User, shareableId: str, db: Session):
    shareableId
    try:
        bank = await getBank(shareableId, db)
        
        decrypted_token = decrypt_id(bank.access_token)
                
        # print("decrypted_token:", decrypted_token)

        accountsResponse = client.accounts_get({
            "access_token" : decrypted_token
        })
        
        # print("accountsResponse : ", accountsResponse)

        target_account_id = bank.account_id

        accountData = next(
            (acct for acct in accountsResponse["accounts"] if acct["account_id"] == target_account_id),
            None
        )
        # print("account_Data : ", accountData)
        

        institution = get_institution(accountsResponse['item']['institution_id'])
        # institution = get_institution(accountsResponse.data.item.institution_id)
        # print("institution : ", institution)



        # 4. Get Plaid transactions
        # transactions_response = await client.transactions_sync(
        #     TransactionsSyncRequest(access_token=bank.access_token)
        # )

        transactions_response = await get_transactions(decrypted_token,target_account_id)


        # print("transactions_response : ", transactions_response)

        # 5. Get transfer transactions (e.g. from internal DB)
        transfer_transactions_raw = await getTransactionsByBank(current_user,bank, db)
        # print("transfer_transactions_raw : ", transfer_transactions_raw)
        
        transfer_transactions = [
            {
                "id": tx.id,
                "name": tx.category,
                "amount": tx.amount,
                "date": tx.date.isoformat(),
                "paymentChannel": "internal",
                "category": tx.category,
                "type": "debit" if tx.sender_bank_id == bank.id else "credit"
            }
            for tx in transfer_transactions_raw
        ]

        # print("transfer_transactions : ", transfer_transactions)

        # 6. Account object
        account = {
            "id": accountData.account_id,
            "availableBalance": accountData.balances.available,
            "currentBalance": accountData.balances.current,
            "institutionId": institution.institution_id,
            "name": accountData.name,
            "officialName": accountData.official_name,
            "mask": accountData.mask,
            "type": str(accountData.type),
            "subtype": str(accountData.subtype),
            "bankId": bank.id,
            "shareableId": bank.shareable_id,
        }
        # print("account : ",account)

        # 7. Merge + sort transactions
        all_transactions = transactions_response + transfer_transactions
        # print("all_transactions : ",all_transactions)
        all_transactions.sort(key=lambda tx: tx["date"], reverse=True)
        # print("sorted_all_transactions : ",all_transactions)
        
        return {
                "data": account,
                "transactions": all_transactions
            }

    except Exception as e:
            print(f"Error getting account: {e}")
            raise HTTPException(status_code=500, detail=f"Could not fetch account data : {e}")

async def getAccounts(current_user: User, db: Session):
    try:
        # print("calling getAccounts")
        banks_response = await getBanks(current_user, db)
        # banks_response = current_user.banks
        banks = banks_response.banks
        banks_by_account_id = {b.account_id: b for b in banks}
        # print("banks : ", banks)
        
        accounts = []
        
        async def process_bank(bank):
            # print("Single Bank: ", bank)
            # print("access_token:", bank.access_token)

            decrypted_token = decrypt_id(bank.access_token)
            
            # print("decrypted_token:", decrypted_token)

            accountsResponse = client.accounts_get({
                "access_token" : decrypted_token
            })
            # print("accountsResponse : ", accountsResponse)
            
            for accountData in accountsResponse["accounts"]:
                matching_bank = banks_by_account_id[accountData.account_id]  # Fast, O(1)


                if not matching_bank:
                    # Handle missing link gracefully
                    continue

                
                
                # print(f"TEST account: {accountData}")

                institution = get_institution(accountsResponse['item']['institution_id'])
                # print("institution : ", institution)
                
                account = {
                    "id": accountData.account_id,
                    "availableBalance": accountData.balances.available,
                    "currentBalance": accountData.balances.current,
                    "institutionId": institution.institution_id,
                    "name": accountData.name,
                    "officialName": accountData.official_name,
                    "mask": accountData.mask,
                    "type": str(accountData.type),
                    "subtype": str(accountData.subtype),
                    "bankId": matching_bank.id,
                    "shareableId": matching_bank.shareable_id,
                }
                # print("account : ",account)
                # print("Type od account : ",type(account))
                accounts.append(account)
            
        # accounts = await asyncio.gather(*(process_bank(bank) for bank in {b.bank_id: b for b in banks or []}.values()))
        await asyncio.gather(*(process_bank(bank) for bank in {b.bank_id: b for b in banks or []}.values()))

        # print("accounts : ",accounts) 
        
        totalBanks = len(accounts)
        # print("totalBanks : ",totalBanks) 

        totalCurrentBalance = sum(account["currentBalance"] or 0 for account in accounts)
        # print("totalCurrentBalance : ",totalCurrentBalance) 

        return {
            "accounts": accounts,
            "totalBanks": totalBanks,
            "totalCurrentBalance": totalCurrentBalance
        }

    except Exception as e:
        print("Error getting Accounts:", e)
        raise HTTPException(status_code=500, detail=f"Could not get Accounts : {e}")

# TODO: verify InstitutionsGetByIdRequest
from plaid.model.institutions_get_by_id_request import  InstitutionsGetByIdRequest
from plaid.model.country_code import CountryCode

# Get bank info
def get_institution(institution_id: str):
    """
    Fetch institution details from Plaid API using institution ID.
    """
    try:
        institution_response = client.institutions_get_by_id(
            InstitutionsGetByIdRequest(
                institution_id=institution_id,
                country_codes=[CountryCode('US')],
            )
        )

        institution = institution_response.institution
        # print ("Institution: ",institution)
        
        # TODO: parsify return
        return institution

    except Exception as e:
        print("Error getting institution:", e)
        raise HTTPException(status_code=500, detail=f"Could not fetch institution info: {e}")

################################################################################################

async def create_bank_account(
    request: CreateBankAccountRequest,
    currentuser,
    db: Session
):
    if not currentuser:
        raise HTTPException(status_code=404, detail="User not found")

    # Optionally encrypt access token
    encrypted_token = encrypt_id(request['access_token'])


    new_bank_account = Bank(
        user_id=request['user_id'],
        bank_id=request['bank_id'],
        account_id=request['account_id'],
        access_token=encrypted_token,
        funding_source_url=request['funding_source_url'],
        shareable_id=request['shareable_id']
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