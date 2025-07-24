from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    address1: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    date_of_birth: Optional[str] = None
    dwolla_customer_id: Optional[str] = None
    dwolla_customer_url: Optional[str] = None
    is_active: bool

    model_config = {
        "from_attributes": True
    }

class SignupRequest(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)  # Strong password validation can be added
    address1: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    date_of_birth: Optional[str] = None  # Could be validated as a date
    ssn: Optional[str] = None  # Optional for now

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "address1": "123 Main St",
                "city": "New York",
                "state": "NY",
                "postal_code": "10001",
                "date_of_birth": "1990-01-01"
            }
        }


class SigninRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePass123"
            }
        }
