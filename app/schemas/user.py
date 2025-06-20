from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.utils.enums import UserRole


class UserBase(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True


class UserCreateRequest(UserBase):
    full_name: Optional[str]
    username: str = Field(..., min_length=3, max_length=20)
    phone_number: str
    password: str = Field(..., min_length=8)
    email: EmailStr
    is_active: bool = True
    role: UserRole = UserRole.USER


class UserUpdateMeRequest(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None


class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = True
    role: Optional[UserRole] = None


class UserItemResponse(UserBase):
    uuid: UUID
    full_name: Optional[str]
    username: str
    email: EmailStr
    phone_number: Optional[str]
    is_active: bool
    role: str
    last_login: Optional[datetime]
