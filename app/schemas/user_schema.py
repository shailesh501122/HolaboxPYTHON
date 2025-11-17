from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    is_verified: bool
    plan_type: str
    storage_used: int
    total_uploads: int
    last_login: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class StorageInfo(BaseModel):
    storage_used: int
    storage_limit: int
    storage_percentage: float
    plan_type: str
