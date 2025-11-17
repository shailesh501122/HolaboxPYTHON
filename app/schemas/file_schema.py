from pydantic import BaseModel
from datetime import datetime


class FolderCreate(BaseModel):
    name: str
    parent_id: int | None = None


class FolderResponse(BaseModel):
    id: int
    name: str
    path: str
    parent_id: int | None
    is_deleted: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class FileUploadResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_size: int
    mime_type: str | None
    folder_id: int | None
    created_at: datetime
    
    class Config:
        from_attributes = True


class FileResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_size: int
    mime_type: str | None
    folder_id: int | None
    is_deleted: bool
    view_count: int
    download_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class FileMove(BaseModel):
    file_id: int
    target_folder_id: int | None


class FileRename(BaseModel):
    new_name: str


class FolderRename(BaseModel):
    new_name: str
