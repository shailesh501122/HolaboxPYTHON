import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.sharing.models import Share
from app.common.models import File
from app.auth.hashing import hash_password, verify_password


def create_share_link(file_id: int, user_id: int, password: str | None, expiry_hours: int | None, db: Session):
    share_token = secrets.token_urlsafe(32)
    
    expires_at = None
    if expiry_hours:
        expires_at = datetime.utcnow() + timedelta(hours=expiry_hours)
    
    password_hash = None
    if password:
        password_hash = hash_password(password)
    
    share = Share(
        share_token=share_token,
        file_id=file_id,
        user_id=user_id,
        password_hash=password_hash,
        expires_at=expires_at
    )
    
    db.add(share)
    db.commit()
    db.refresh(share)
    return share


def verify_share_access(share_token: str, password: str | None, db: Session):
    share = db.query(Share).filter(
        Share.share_token == share_token,
        Share.is_active == True
    ).first()
    
    if not share:
        return None
    
    if share.expires_at and share.expires_at < datetime.utcnow():
        return None
    
    if share.password_hash and not password:
        return False
    
    if share.password_hash and not verify_password(password, share.password_hash):
        return False
    
    return share
