# ===================================================
# Imports
# ===================================================

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from datetime import date, datetime

from app.utils.jwt_handler import verify_token
from app.models.user import User
from app.schemas.auth import UserResponse, SignupRequest, SigninRequest
from app.utils.database import get_db
from app.utils.dwolla import create_dwolla_customer, extractCustomerIdFromUrl

# ===================================================
# Initialization
# ===================================================

ph = PasswordHasher()
key = Fernet.generate_key()  # In production, load from secure vault
cipher = Fernet(key)

# ===================================================
# Function: authenticate_user
# ===================================================


async def authenticate_user(request: Request, db: Session = Depends(get_db)):
    """
    Authenticate the user by verifying the JWT token stored in the request cookies.
    """
    token = request.cookies.get("jwt")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access denied: No token found.",
        )

    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access denied: Token invalid or expired.",
        )

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload.",
        )

    try:
        user = db.query(User).filter(User.id == user_id).first()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while retrieving user.",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred during authentication.",
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user


# ===================================================
# Function: register_user
# ===================================================


async def register_user(user: SignupRequest, db: Session) -> UserResponse:
    """
    Register a new user by securely processing sensitive fields, saving the user to the database,
    and creating a corresponding Dwolla customer.
    """

    hashed_password = ph.hash(user.password)
    encrypted_ssn = cipher.encrypt(user.ssn.encode()).decode() if user.ssn else None

    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password,
        ssn=encrypted_ssn,
        address1=user.address1,
        city=user.city,
        state=user.state,
        postal_code=user.postal_code,
        date_of_birth=user.date_of_birth,
    )
    print(f"user.address1==>{user.address1}")
    print(f"db_user.address1==>{db_user.address1}")
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        dwolla_payload = {
            "firstName": db_user.first_name,
            "lastName": db_user.last_name,
            "email": db_user.email,
            "type": "personal",
            "address1": db_user.address1,
            "city": db_user.city,
            "state": db_user.state,
            "postalCode": db_user.postal_code,
            "dateOfBirth": db_user.date_of_birth,
            "ssn": user.ssn if user.ssn else None,
        }

        dwollaCustomerUrl = await create_dwolla_customer(dwolla_payload)

        if not dwollaCustomerUrl:
            raise Exception("Error creating Dwolla customer")

        dwollaCustomerId = extractCustomerIdFromUrl(dwollaCustomerUrl)

        db_user.dwolla_customer_url = dwollaCustomerUrl
        db_user.dwolla_customer_id = dwollaCustomerId
        db.commit()

    except Exception as e:
        db.rollback()

        if db_user.id:
            try:
                db.delete(db_user)
                db.commit()
            except SQLAlchemyError as delete_error:
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Dwolla failed and user delete also failed: {delete_error}",
                )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to complete registration: {str(e)}",
        )

    return UserResponse.model_validate(db_user)


# ===================================================
# Function: validate_user_credentials
# ===================================================


async def validate_user_credentials(data: SigninRequest, db: Session) -> UserResponse:
    """
    Validate user credentials by verifying the email and password against stored data.
    """
    try:
        user = db.query(User).filter(User.email == data.email).first()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving user.",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred: {e}",
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password.",
        )

    try:
        ph.verify(user.hashed_password, data.password)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password.",
        )

    return UserResponse.model_validate(user)
