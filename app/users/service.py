from sqlalchemy.orm import Session
from app.users.models import User
from app.common.helpers import get_storage_limit


def get_user_storage_info(user: User, db: Session):
    storage_limit = get_storage_limit(user.plan_type)
    storage_percentage = (user.storage_used / storage_limit * 100) if storage_limit > 0 else 0
    
    return {
        "storage_used": user.storage_used,
        "storage_limit": storage_limit,
        "storage_percentage": round(storage_percentage, 2),
        "plan_type": user.plan_type
    }


def update_user_storage(user: User, file_size: int, db: Session, add: bool = True):
    if add:
        user.storage_used += file_size
    else:
        user.storage_used = max(0, user.storage_used - file_size)
    
    db.commit()
    db.refresh(user)
    return user
