from fastapi import APIRouter, Depends, status, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import UserResponse, SignupRequest, SigninRequest
from app.services.auth_service import register_user, authenticate_user,validate_user_credentials
from app.utils.jwt_handler import create_access_token
from app.utils.database import get_db
from app.core.config import settings
 
router = APIRouter(prefix="/auth", tags=["Auth"])

max_age = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    data: SignupRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    user = await register_user(data, db)
    access_token = create_access_token({"user_Id": str(user.id)})
    response = JSONResponse(content=user.model_dump())
    response.set_cookie(
        key="jwt",
        value=access_token,
        httponly=True,
        secure=settings.SECURE_COOKIE,  # True in production
        samesite=settings.SAME_SITE,    # "none" for prod, "lax" for dev
        max_age=max_age,
        path="/"
    )
    return response

@router.post("/signin", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def signin(
    data: SigninRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    user = await validate_user_credentials(data,db)
    access_token = create_access_token({"user_Id": str(user.id)})
    print(f"Secure or Not:{settings.SECURE_COOKIE}")
    print(f"SameSite:{settings.SAME_SITE}")
    response = JSONResponse(content=user.model_dump())
    response.set_cookie(
        key="jwt",
        value=access_token,
        httponly=True,
        secure=settings.SECURE_COOKIE,  # True in production,
        samesite=settings.SAME_SITE,    # "none" for prod, "lax" for dev 
        max_age=max_age,
        path="/"
    )
    return response
    


@router.get("/authenticate", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_profile(current_user: User = Depends(authenticate_user)):
    return current_user

