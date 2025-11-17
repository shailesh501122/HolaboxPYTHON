from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.user_schema import UserResponse, UserUpdate, StorageInfo
from app.users.models import User
from app.common.helpers import get_current_user
from app.users.service import get_user_storage_info

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserResponse)
def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    
    if user_update.email is not None:
        existing = db.query(User).filter(
            User.email == user_update.email,
            User.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        current_user.email = user_update.email
    
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/storage", response_model=StorageInfo)
def get_storage_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_user_storage_info(current_user, db)
