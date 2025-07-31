from pydantic import BaseModel, Field
from typing import Optional


class CreateBankAccountRequest(BaseModel):
    user_id: str = Field(..., alias="userId")
    bank_id: str = Field(..., alias="bankId")
    account_id: str = Field(..., alias="accountId")
    access_token: str = Field(..., alias="accessToken")
    funding_source_url: str = Field(..., alias="fundingSourceUrl")
    shareable_id: Optional[str] = Field(None, alias="shareableId")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "userId": "user_123456",
                "bankId": "bank_xyz",
                "accountId": "acc_78910",
                "accessToken": "access-sandbox-abc123",
                "fundingSourceUrl": "https://api.dwolla.com/funding-sources/xyz",
                "shareableId": "abc-def-ghi"
            }
        }
