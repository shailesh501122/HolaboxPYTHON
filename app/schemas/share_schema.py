from pydantic import BaseModel
from datetime import datetime


class ShareCreate(BaseModel):
    file_id: int
    password: str | None = None
    expiry_hours: int | None = None


class ShareResponse(BaseModel):
    id: int
    share_token: str
    file_id: int
    expires_at: datetime | None
    view_count: int
    download_count: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ShareAccess(BaseModel):
    password: str | None = None


class ShareStats(BaseModel):
    share_token: str
    view_count: int
    download_count: int
    is_active: bool
    expires_at: datetime | None
