# ================================================
# Imports
# ================================================

import asyncio

from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import Depends, HTTPException

from plaid.model.transactions_sync_request import TransactionsSyncRequest

from app.services.auth_service import authenticate_user
from app.utils.plaid_client import client, encrypt_id, decrypt_id
from app.models.user import User
from app.models.bank import Bank
from app.models.transactions import Transaction
from app.schemas.transaction import (
    TransactionParams,
    TransactionResponse,
    TransactionsResponse,
)

# ================================================
# Transaction Queries
# ================================================


async def get_transactions_by_bank(current_user: User, current_bank: Bank, db: Session):
    """
    Fetch transactions associated with a user and specific bank.
    """
    try:
        transactions = (
            db.query(Transaction)
            .filter(
                or_(
                    Transaction.sender_id == current_user.id,
                    Transaction.receiver_id == current_user.id,
                ),
                or_(
                    Transaction.sender_bank_id == current_bank.id,
                    Transaction.receiver_bank_id == current_bank.id,
                ),
            )
            .all()
        )

        return [
            TransactionResponse.model_validate(transaction)
            for transaction in transactions
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not get Transactions : {e}")


async def getAllTransactions(current_user: User, db: Session):
    """
    Fetch all transactions for a user.
    """
    try:
        transactions = (
            db.query(Transaction).filter(Transaction.user_id == current_user.id).all()
        )

        if not transactions:
            raise HTTPException(status_code=404, detail="Transactions not found")

        return [
            TransactionResponse.model_validate(transaction)
            for transaction in transactions
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not get Transactions : {e}")


# ================================================
# Create Transactions
# ================================================


async def createTransactions(
    request: TransactionParams, currentuser: User, db: Session
):
    """
    Create a new transaction record in the database.
    """
    try:
        if not currentuser:
            raise HTTPException(status_code=404, detail="User not found")

        new_transaction = Transaction(
            user_id=request["user_id"],
            bank_id=request["bank_id"],
            amount=request["amount"],
            date=request["date"],
            type=request["type"],
            category=request["category"],
            pending=request["pending"],
            sender_bank_id=request["sender_bank_id"],
            receiver_bank_id=request["receiver_bank_id"],
        )

        db.add(new_transaction)
        db.commit()  # <-- Fixed missing parentheses
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
        raise HTTPException(status_code=500, detail=f"Error creating transactions: {e}")


# ================================================
# Plaid API: Get Transactions
# ================================================


async def get_transactions(access_token: str, target_account_id: str):
    """
    Fetch and filter transactions from Plaid API for a specific account.
    """
    try:
        has_more = True
        cursor = None
        transactions = []

        while has_more:
            request = (
                TransactionsSyncRequest(access_token=access_token, cursor=cursor)
                if cursor
                else TransactionsSyncRequest(access_token=access_token)
            )

            print("Getting Transactions response...")
            response = client.transactions_sync(request)
            data = response.to_dict()

            added_transactions = data.get("added", [])

            for transaction in added_transactions:
                if transaction.get("account_id") == target_account_id:
                    transactions.append(
                        {
                            "id": transaction.get("transaction_id"),
                            "name": transaction.get("name"),
                            "payment_channel": transaction.get("payment_channel"),
                            "type": transaction.get("payment_channel"),
                            "account_id": transaction.get("account_id"),
                            "amount": transaction.get("amount"),
                            "pending": transaction.get("pending"),
                            "category": (
                                transaction.get("personal_finance_category", {}).get(
                                    "primary"
                                )
                                if transaction.get("personal_finance_category")
                                else ""
                            ),
                            "date": transaction.get("date"),
                            "image": transaction.get("logo_url"),
                        }
                    )

            has_more = data.get("has_more", False)
            cursor = data.get("next_cursor")

        return transactions

    except Exception as e:
        print("An error occurred while getting the transactions:", e)
        raise HTTPException(status_code=500, detail=f"Could not get transactions: {e}")
