# ================================================
# Imports
# ================================================

import traceback

# FastAPI
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse

# SQLAlchemy
from sqlalchemy.orm import Session

# Schemas
from app.schemas.auth import (
    UserResponse,
    SignupRequest,
    SigninRequest,
)

# Models
from app.models.user import User

# Services
from app.services.auth_service import (
    register_user,
    authenticate_user,
    validate_user_credentials,
)

# Utils
from app.utils.jwt_handler import create_access_token
from app.utils.database import get_db

# Config
from app.core.config import settings


# ================================================
# Router Configuration
# ================================================

router = APIRouter(prefix="/auth", tags=["Auth"])
max_age = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60


# ================================================
# Routes
# ================================================


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def signup(
    data: SignupRequest, response: Response, db: Session = Depends(get_db)
):
    try:
        if db.query(User).filter(User.email == data.email).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists.",
            )
        print(f"data.first_name==>{data.first_name}")
        print(f"data.address1==>{data.address1}")
        user = await register_user(data, db)
        access_token = create_access_token({"user_id": str(user.id)})

        response = JSONResponse(content=user.model_dump())
        response.set_cookie(
            key="jwt",
            value=access_token,
            httponly=True,
            secure=settings.SECURE_COOKIE,
            samesite=settings.SAME_SITE,
            max_age=max_age,
            path="/",
        )
        return response

    except Exception as e:
        tb = traceback.format_exc()
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "type": type(e).__name__,
                "trace": tb,
            },
        )


@router.post("/signin", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def signin(
    data: SigninRequest, response: Response, db: Session = Depends(get_db)
):
    try:
        user = await validate_user_credentials(data, db)
        access_token = create_access_token({"user_id": str(user.id)})

        print(f"Secure or Not: {settings.SECURE_COOKIE}")
        print(f"SameSite: {settings.SAME_SITE}")

        response = JSONResponse(content=user.model_dump())
        response.set_cookie(
            key="jwt",
            value=access_token,
            httponly=True,
            secure=settings.SECURE_COOKIE,
            samesite=settings.SAME_SITE,
            max_age=max_age,
            path="/",
        )
        return response

    except Exception as e:
        tb = traceback.format_exc()
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "type": type(e).__name__,
                "trace": tb,
            },
        )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    response.delete_cookie(key="jwt", path="/")
    return {"message": "Logout successful"}


@router.get(
    "/authenticate", response_model=UserResponse, status_code=status.HTTP_200_OK
)
async def get_profile(current_user: User = Depends(authenticate_user)):
    return current_user
