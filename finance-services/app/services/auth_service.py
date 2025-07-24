"""
Authentication and User Management Service

This module provides core authentication-related functionalities for the FastAPI application,
including user registration, user authentication via JWT tokens, and credential validation.

Functions:
- authenticate_user: Validates JWT token from request cookies and returns the authenticated user.
- register_user: Registers a new user by hashing the password, encrypting sensitive data (SSN), 
  and saving to the database.
- validate_user_credentials: Verifies user login credentials against stored data and returns the user.

Dependencies:
- SQLAlchemy for database interaction.
- argon2 PasswordHasher for secure password hashing and verification.
- cryptography Fernet for encrypting sensitive information like SSN.
- FastAPI HTTPException for handling API errors.
"""


from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.utils.jwt_handler import verify_token
from app.models.user import User
from app.schemas.auth import UserResponse, SignupRequest, SigninRequest
from sqlalchemy.orm import Session
from app.utils.database import get_db

from app.schemas.auth import SignupRequest
from argon2 import PasswordHasher
from cryptography.fernet import Fernet

ph = PasswordHasher()
key = Fernet.generate_key()  # In production, load from secure vault
cipher = Fernet(key)

async def authenticate_user(request: Request, db: Session = Depends(get_db)):
    """
    Authenticate the user by verifying the JWT token stored in the request cookies.

    Args:
        request (Request): FastAPI Request object containing the incoming HTTP request.
        db (Session): SQLAlchemy database session dependency.

    Returns:
        User: The authenticated User object fetched from the database.

    Raises:
        HTTPException: 
            - 401 Unauthorized if JWT token is missing or invalid.
            - 404 Not Found if the user decoded from the token does not exist.
            - 500 Internal Server Error if database retrieval or unexpected errors occur.

    Example:
        # Usage in a route
        @router.get("/authenticate", response_model=UserResponse, status_code=status.HTTP_200_OK)
        async def get_profile(current_user: User = Depends(authenticate_user)):
            return current_user
    """
    
    token = request.cookies.get("jwt")
    
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied: No token found.")

    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied: Token invalid or expired.")

    user_id = payload.get("user_Id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload.")

    try:
        user = db.query(User).filter(User.id == user_id).first()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while retrieving user."
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred during authentication."
        )

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    return user

async def register_user(user: SignupRequest, db: Session) -> UserResponse:
    """
    Register a new user by hashing the password and encrypting sensitive fields,
    then saving the user data to the database.

    Args:
        user (SignupRequest): Pydantic model containing user registration data.
        db (Session): SQLAlchemy database session.

    Returns:
        UserResponse: The newly created user data excluding sensitive information.

    Raises:
        HTTPException:
            - 409 Conflict if a user with the same email already exists.
            - 500 Internal Server Error if database or unexpected errors occur.
    """
    # Hash password
    hashed_password = ph.hash(user.password)
    
    # Encrypt SSN if provided
    encrypted_ssn = cipher.encrypt(user.ssn.encode()).decode() if user.ssn else None
    try:
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
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    
    except IntegrityError as e:
        db.rollback()
        # Assuming email uniqueness constraint error, customize as needed
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists."
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while creating user."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred:{e}"
        )

    return UserResponse.model_validate(db_user)

async def validate_user_credentials(data: SigninRequest, db: Session) -> UserResponse:
    """
    Validate user credentials by verifying the email and password against stored data.

    Args:
        data (SigninRequest): Pydantic model with user's email and password.
        db (Session): SQLAlchemy database session.

    Returns:
        UserResponse: The authenticated user's data.

    Raises:
        HTTPException:
            - 400 Bad Request if email or password is invalid.
            - 500 Internal Server Error if database or unexpected errors occur.
    """
    
    try:
        user = db.query(User).filter(User.email == data.email).first()
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while creating user."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred:{e}"
        )
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    try:
        ph.verify(user.hashed_password, data.password)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    
    return UserResponse.model_validate(user)