from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from app.config.database import get_db
from app.users.models import User
from app.common.models import File
from app.common.helpers import get_admin_user
from app.common.storage_engine import storage_engine

router = APIRouter(prefix="/admin", tags=["Admin"])


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    plan_type: str
    storage_used: int
    is_active: bool
    is_admin: bool
    
    class Config:
        from_attributes = True


@router.get("/users", response_model=list[UserResponse])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.post("/users/{user_id}/suspend")
def suspend_user(
    user_id: int,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = False
    db.commit()
    
    return {"message": f"User {user.username} suspended successfully"}


@router.post("/users/{user_id}/activate")
def activate_user(
    user_id: int,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = True
    db.commit()
    
    return {"message": f"User {user.username} activated successfully"}


@router.post("/users/{user_id}/reset-storage")
def reset_user_storage(
    user_id: int,
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    actual_storage = storage_engine.calculate_user_storage(user.id)
    user.storage_used = actual_storage
    db.commit()
    
    return {
        "message": "Storage recalculated",
        "storage_used": actual_storage
    }


@router.get("/stats")
def get_server_stats(
    admin_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    total_files = db.query(File).count()
    total_storage = db.query(User).with_entities(func.sum(User.storage_used)).scalar() or 0
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_files": total_files,
        "total_storage_bytes": total_storage
    }
