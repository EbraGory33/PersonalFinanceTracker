"""
Module: utils.jwt_handler
Description:
    Provides utility functions for creating and verifying JWT tokens for authentication.

Functions:
    create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        Creates a JWT access token with optional expiration time.
    
    verify_token(token: str) -> dict | None:
        Verifies a JWT token and returns its payload if valid, otherwise returns None.
"""

from jose import JWTError, jwt
from datetime import datetime, timezone, timedelta
from app.core.config import settings


SECRET_KEY = settings.ACCESS_TOKEN_SECRET
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token with an expiration time.

    Args:
        data (dict): The payload data to include in the token.
                     Typically contains user identification info (e.g., user_id).
        expires_delta (timedelta, optional): Custom expiration time for the token.
                                             Defaults to `ACCESS_TOKEN_EXPIRE_MINUTES`.

    Returns:
        str: The encoded JWT token as a string.

    Example:
        >>> token = create_access_token({"sub": "123"})
        >>> print(token)
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    """
    Verify and decode a JWT token.

    Args:
        token (str): The JWT token string to verify.

    Returns:
        dict | None: The decoded payload if the token is valid, otherwise None.

    Raises:
        None: This function catches JWT errors internally and returns None for invalid tokens.

    Example:
        >>> payload = verify_token(token)
        >>> if payload:
        ...     print("Valid token:", payload)
        ... else:
        ...     print("Invalid token")
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
