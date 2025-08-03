from fastapi import Depends, HTTPException
from app.services.auth_service import authenticate_user
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.utils.plaid_client import client, encrypt_id, decrypt_id  # Initialized PlaidApi instance
from plaid.model.transactions_sync_request import TransactionsSyncRequest

from app.models.user import User
from app.models.bank import Bank
from app.models.transactions import Transaction

from app.schemas.transaction import TransactionParams, TransactionResponse, TransactionsResponse
import asyncio

# TODO: Transaction sneder and reciever
async def getTransactionsByBank(current_user: User, current_bank: Bank, db: Session):
    try:
        # transactions = db.query(Transaction).filter(
        #         Transaction.user_id == current_user.id,
        #         Transaction.bank_id == current_bank.id
        #     ).all()
        
        transactions = db.query(Transaction).filter(
            Transaction.user_id == current_user.id,
            or_(
                Transaction.sender_bank_id == current_bank.id,
                Transaction.receiver_bank_id == current_bank.id
            )
        ).all()

        # print(f"Transaction : {transactions}")
        transactions_responses = [TransactionResponse.model_validate(transaction) for transaction in transactions]
        # print(f"transactions_responses : {transactions_responses}")
        
        return transactions_responses
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not get Transactions : {e}")

async def getAllTransactions(current_user: User, db: Session):
    try:
        transactions = db.query(Transaction).filter(Transaction.user_id == current_user.id).all()

        # print(f"Transaction : {transactions}")
        transactions_responses = [TransactionsResponse.model_validate(transaction) for transaction in transactions]
        # print(f"transactions_responses : {transactions_responses}")
        
        if not transactions:
                raise HTTPException(
                status_code=404,
                detail="Transactions not found"
                )

        # print(f"Transaction : {transactions}")
        transactions_responses = [TransactionResponse.model_validate(transaction) for transaction in transactions]
        # print(f"transactions_responses : {transactions_responses}")    
        
        return transactions_responses

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not get Transactions : {e}")
################################################## ####################################################################################################
async def createTransactions(
    request: TransactionParams, 
    currentuser, 
    db: Session
):
    try:    
        if not currentuser:
            raise HTTPException(status_code=404, detail="User not found")

        new_transaction = Transaction(
            user_id=request['user_id'],
            bank_id=request['bank_id'],
            amount = request['amount'],
            date = request['date'],
            type = request['type'],
            category = request['category'],
            pending = request['pending'],
            sender_bank_id = request['sender_bank_id'],
            receiver_bank_id = request['receiver_bank_id'],
        )

        db.add(new_transaction)
        db.commit
        db.refresh(new_transaction)


        return {
            "transaction": {
                "id": new_transaction.id,
                "user_id": new_transaction.user_id,
                "bank_id": new_transaction.bank_id,
                "amount": new_transaction.amount,
                "date": new_transaction.date,
                "type": new_transaction.type,
                "category": new_transaction.category,
                "pending": new_transaction.pending,
                "sender_bank_id": new_transaction.sender_bank_id,
                "receiver_bank_id": new_transaction.receiver_bank_id,
            }
        }
    except Exception as e:
        print("Error creating transactions:", e)
        raise HTTPException(status_code=500, detail=f"Error creating transactions: : {e}")
    


async def get_transactions(access_token: str,target_account_id: str):
    try:
        has_more = True
        cursor = None
        transactions = []

        while has_more:
            # request = TransactionsSyncRequest(
            #     access_token=access_token,
            #     cursor=cursor  # initially None; will be updated in loop
            # )

            if cursor:
                request = TransactionsSyncRequest(
                    access_token=access_token,
                    cursor=cursor
                )
            else:
                request = TransactionsSyncRequest(
                    access_token=access_token
                )
            
            print("Gettin Transactions response : ")

            response = client.transactions_sync(request)
            data = response.to_dict()

            print("Transactions response data : ", data)

            # Add new transactions (only "added"; others are "modified" or "removed")
            added_transactions = data.get("added", [])


            print("Added Transactions data : ", added_transactions)

            for transaction in added_transactions:
                if transaction.get("account_id") == target_account_id:
                    transactions.append({
                        "id": transaction.get("transaction_id"),
                        "name": transaction.get("name"),
                        "paymentChannel": transaction.get("payment_channel"),
                        "type": transaction.get("payment_channel"),  # same as above
                        "accountId": transaction.get("account_id"),
                        "amount": transaction.get("amount"),
                        "pending": transaction.get("pending"),
                        "category": transaction.get("category")[0] if transaction.get("category") else "",
                        "date": transaction.get("date"),
                        "image": transaction.get("logo_url")  # Note: This may require a different source
                    })
            print("Transactions : ", transactions)

            has_more = data.get("has_more", False)
            # print("has_more : ", has_more)

            cursor = data.get("next_cursor")
            

        return transactions

    except Exception as e:
        print("An error occurred while getting the transactions:", e)
        raise HTTPException(status_code=500, detail=f"Could not get transactions: {e}")