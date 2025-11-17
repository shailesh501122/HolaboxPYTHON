from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File as FastAPIFile
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
import os
from app.config.database import get_db
from app.schemas.file_schema import (
    FolderCreate, FolderResponse, FileUploadResponse, FileResponse,
    FileMove, FileRename, FolderRename
)
from app.common.models import File, Folder
from app.users.models import User
from app.common.helpers import get_current_user, generate_unique_filename, check_storage_available
from app.common.storage_engine import storage_engine
from app.storage.service import create_folder, get_user_files, get_user_folders, soft_delete_file, restore_file
from app.storage.utils import get_mime_type
from app.users.service import update_user_storage

router = APIRouter(prefix="/storage", tags=["Storage"])


@router.post("/folders", response_model=FolderResponse, status_code=status.HTTP_201_CREATED)
def create_new_folder(
    folder_data: FolderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    folder = create_folder(folder_data.name, folder_data.parent_id, current_user, db)
    if not folder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent folder not found"
        )
    return folder


@router.get("/folders", response_model=list[FolderResponse])
def list_folders(
    parent_id: int | None = None,
    include_deleted: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    folders = get_user_folders(current_user.id, parent_id, include_deleted, db)
    return folders


@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    folder_id: int | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    content = await file.read()
    file_size = len(content)
    
    if not check_storage_available(current_user, file_size):
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Storage limit exceeded"
        )
    
    await file.seek(0)
    
    unique_filename = generate_unique_filename(file.filename)
    file_path = await storage_engine.save_file(file, current_user.id, unique_filename)
    
    mime_type = get_mime_type(file.filename)
    
    new_file = File(
        filename=unique_filename,
        original_filename=file.filename,
        file_path=file_path,
        file_size=file_size,
        mime_type=mime_type,
        folder_id=folder_id,
        user_id=current_user.id
    )
    
    db.add(new_file)
    update_user_storage(current_user, file_size, db, add=True)
    current_user.total_uploads += 1
    db.commit()
    db.refresh(new_file)
    
    return new_file


@router.get("/files", response_model=list[FileResponse])
def list_files(
    folder_id: int | None = None,
    include_deleted: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    files = get_user_files(current_user.id, folder_id, include_deleted, db)
    return files


@router.get("/files/{file_id}/download")
async def download_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    file = db.query(File).filter(
        File.id == file_id,
        File.user_id == current_user.id
    ).first()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    if not os.path.exists(file.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File does not exist on disk"
        )
    
    file.download_count += 1
    db.commit()
    
    return FileResponse(
        path=file.file_path,
        filename=file.original_filename,
        media_type=file.mime_type
    )


@router.delete("/files/{file_id}")
def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if soft_delete_file(file_id, current_user, db):
        return {"message": "File moved to trash"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="File not found"
    )


@router.post("/files/{file_id}/restore")
def restore_file_from_trash(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = restore_file(file_id, current_user, db)
    
    if result is True:
        return {"message": "File restored successfully"}
    elif result is None:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Cannot restore file: storage quota would be exceeded"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found in trash"
        )


@router.put("/files/{file_id}/rename")
def rename_file(
    file_id: int,
    rename_data: FileRename,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    file = db.query(File).filter(
        File.id == file_id,
        File.user_id == current_user.id
    ).first()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    file.original_filename = rename_data.new_name
    db.commit()
    
    return {"message": "File renamed successfully"}
