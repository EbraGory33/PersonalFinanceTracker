from pydantic import BaseModel, Field
from typing import Optional
from app.models.user import User
from typing import List


class PublicTokenRequest(BaseModel):
    public_token: str


class BankResponse(BaseModel):
    id: int
    user_id: int
    bank_id: str
    account_id: str
    access_token: str
    funding_source_url: Optional[str]
    shareable_id: Optional[str]

    model_config = {"from_attributes": True}


class BanksResponse(BaseModel):
    banks: List[BankResponse]

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
