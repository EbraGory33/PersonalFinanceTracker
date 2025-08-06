from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from typing import List


class TransferRequest(BaseModel):
    source_funding_source_url: str
    destination_funding_source_url: str
    amount: str


class TransactionParams(BaseModel):
    name: Optional[str] = None
    amount: float
    sender_id: int  # = Field(..., alias="senderId")
    receiver_id: int  # = Field(..., alias="receiverId")
    email: Optional[EmailStr] = None
    category: Optional[str] = None
    pending: Optional[bool] = True
    sender_bank_id: Optional[int]  # = Field(None, alias="senderBankId")
    receiver_bank_id: Optional[int]  # = Field(None, alias="receiverBankId")
    date: Optional[datetime] = None
    channel: Optional[str] = None

    model_config = {"from_attributes": True}


class TransactionResponse(BaseModel):
    id: int
    name: str
    sender_id: int
    receiver_id: int
    amount: float
    date: datetime
    type: Optional[str] = None
    category: Optional[str] = None
    pending: Optional[bool] = False
    sender_bank_id: Optional[int] = None
    receiver_bank_id: Optional[int] = None

    model_config = {"from_attributes": True}


class TransactionsResponse(BaseModel):
    transactions: List[TransactionResponse]

    model_config = {"from_attributes": True}


class CreateBankAccountRequest(BaseModel):
    user_id: str
    bank_id: str
    account_id: str
    access_token: str
    funding_source_url: str
    shareable_id: Optional[str]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "userId": "user_123456",
                "bankId": "bank_xyz",
                "accountId": "acc_78910",
                "accessToken": "access-sandbox-abc123",
                "fundingSourceUrl": "https://api.dwolla.com/funding-sources/xyz",
                "shareableId": "abc-def-ghi",
            }
        }
