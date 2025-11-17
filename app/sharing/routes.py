from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
from app.config.database import get_db
from app.schemas.share_schema import ShareCreate, ShareResponse, ShareAccess, ShareStats
from app.common.models import File
from app.users.models import User
from app.common.helpers import get_current_user
from app.sharing.service import create_share_link, verify_share_access
from app.sharing.models import Share

router = APIRouter(prefix="/shares", tags=["Sharing"])


@router.post("/", response_model=ShareResponse, status_code=status.HTTP_201_CREATED)
def create_share(
    share_data: ShareCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    file = db.query(File).filter(
        File.id == share_data.file_id,
        File.user_id == current_user.id
    ).first()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    share = create_share_link(
        share_data.file_id,
        current_user.id,
        share_data.password,
        share_data.expiry_hours,
        db
    )
    
    return share


@router.get("/my-shares", response_model=list[ShareResponse])
def get_my_shares(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    shares = db.query(Share).filter(Share.user_id == current_user.id).all()
    return shares


@router.get("/{share_token}/access")
def access_shared_file(
    share_token: str,
    share_access: ShareAccess,
    db: Session = Depends(get_db)
):
    share = verify_share_access(share_token, share_access.password, db)
    
    if share is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Share not found or expired"
        )
    
    if share is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    
    share.view_count += 1
    db.commit()
    
    file = db.query(File).filter(File.id == share.file_id).first()
    
    return {
        "file_id": file.id,
        "filename": file.original_filename,
        "file_size": file.file_size,
        "mime_type": file.mime_type
    }


@router.get("/{share_token}/download")
def download_shared_file(
    share_token: str,
    password: str | None = None,
    db: Session = Depends(get_db)
):
    share = verify_share_access(share_token, password, db)
    
    if share is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Share not found or expired"
        )
    
    if share is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    
    file = db.query(File).filter(File.id == share.file_id).first()
    
    if not os.path.exists(file.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File does not exist"
        )
    
    share.download_count += 1
    db.commit()
    
    return FileResponse(
        path=file.file_path,
        filename=file.original_filename,
        media_type=file.mime_type
    )


@router.delete("/{share_id}")
def delete_share(
    share_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    share = db.query(Share).filter(
        Share.id == share_id,
        Share.user_id == current_user.id
    ).first()
    
    if not share:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Share not found"
        )
    
    share.is_active = False
    db.commit()
    
    return {"message": "Share deleted successfully"}
