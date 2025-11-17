from sqlalchemy.orm import Session
from app.common.models import File, Folder
from app.users.models import User
from datetime import datetime
from app.common.helpers import check_storage_available


def create_folder(name: str, parent_id: int | None, user: User, db: Session):
    parent_path = ""
    if parent_id:
        parent = db.query(Folder).filter(
            Folder.id == parent_id,
            Folder.user_id == user.id,
            Folder.is_deleted == False
        ).first()
        if not parent:
            return None
        parent_path = parent.path
    
    folder_path = f"{parent_path}/{name}" if parent_path else f"/{name}"
    
    folder = Folder(
        name=name,
        path=folder_path,
        parent_id=parent_id,
        user_id=user.id
    )
    db.add(folder)
    db.commit()
    db.refresh(folder)
    return folder


def get_user_files(user_id: int, folder_id: int | None, include_deleted: bool, db: Session):
    query = db.query(File).filter(File.user_id == user_id)
    
    if folder_id:
        query = query.filter(File.folder_id == folder_id)
    else:
        query = query.filter(File.folder_id.is_(None))
    
    if not include_deleted:
        query = query.filter(File.is_deleted == False)
    
    return query.all()


def get_user_folders(user_id: int, parent_id: int | None, include_deleted: bool, db: Session):
    query = db.query(Folder).filter(Folder.user_id == user_id)
    
    if parent_id:
        query = query.filter(Folder.parent_id == parent_id)
    else:
        query = query.filter(Folder.parent_id.is_(None))
    
    if not include_deleted:
        query = query.filter(Folder.is_deleted == False)
    
    return query.all()


def soft_delete_file(file_id: int, user: User, db: Session):
    file = db.query(File).filter(
        File.id == file_id,
        File.user_id == user.id,
        File.is_deleted == False
    ).first()
    
    if file:
        file.is_deleted = True
        file.deleted_at = datetime.utcnow()
        
        user.storage_used = max(0, user.storage_used - file.file_size)
        
        db.commit()
        return True
    return False


def restore_file(file_id: int, user: User, db: Session):
    file = db.query(File).filter(
        File.id == file_id,
        File.user_id == user.id,
        File.is_deleted == True
    ).first()
    
    if not file:
        return False
    
    if not check_storage_available(user, file.file_size):
        return None
    
    file.is_deleted = False
    file.deleted_at = None
    
    user.storage_used += file.file_size
    
    db.commit()
    return True
