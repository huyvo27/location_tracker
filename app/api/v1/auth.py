from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.dependencies.db import get_db
from app.schemas.response import Response
from app.schemas.token import Token
from app.schemas.user import UserRegisterRequest
from app.services.user import UserService

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login", response_model=Response[Token])
async def login(form_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    API Login User
    Authenticate user with username and password, and return an access token.
    """
    user = await UserService(db).authenticate(
        username=form_data.username, password=form_data.password
    )

    await user.update(db=db, last_login=datetime.now(timezone.utc))
    toke_data = {"sub": user.uuid_str}

    return Response.success({"access_token": create_access_token(data=toke_data)})


@router.post("/logout", response_model=Response[None])
async def logout():
    """
    API Logout User
    This endpoint is a placeholder for logout functionality.
    Actual logout logic may involve token invalidation or session management.
    """
    return Response.success(data=None)


@router.post("/register", response_model=Response[Token])
async def register(user_data: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    """
    API Register User
    Create a new user and return an access token.
    """
    new_user = await UserService(db=db).register_user(user_data=user_data)

    toke_data = {"sub": new_user.uuid_str}
    return Response.success({"access_token": create_access_token(data=toke_data)})
