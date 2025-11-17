import os
import shutil
import aiofiles
from pathlib import Path
from fastapi import UploadFile
from app.config.settings import settings


class StorageEngine:
    def __init__(self, base_path: str = None):
        self.base_path = base_path or settings.STORAGE_PATH
        Path(self.base_path).mkdir(parents=True, exist_ok=True)
    
    def get_user_storage_path(self, user_id: int) -> str:
        user_path = os.path.join(self.base_path, str(user_id))
        Path(user_path).mkdir(parents=True, exist_ok=True)
        return user_path
    
    async def save_file(self, file: UploadFile, user_id: int, filename: str) -> str:
        user_path = self.get_user_storage_path(user_id)
        file_path = os.path.join(user_path, filename)
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        return file_path
    
    def delete_file(self, file_path: str) -> bool:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    def get_file_size(self, file_path: str) -> int:
        if os.path.exists(file_path):
            return os.path.getsize(file_path)
        return 0
    
    def move_file(self, old_path: str, new_path: str) -> bool:
        try:
            Path(os.path.dirname(new_path)).mkdir(parents=True, exist_ok=True)
            shutil.move(old_path, new_path)
            return True
        except Exception as e:
            print(f"Error moving file: {e}")
            return False
    
    def calculate_user_storage(self, user_id: int) -> int:
        user_path = self.get_user_storage_path(user_id)
        total_size = 0
        
        for dirpath, dirnames, filenames in os.walk(user_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if os.path.exists(file_path):
                    total_size += os.path.getsize(file_path)
        
        return total_size


storage_engine = StorageEngine()
