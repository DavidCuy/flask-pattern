import os
from typing import Any, List

from .local import LocalStorage

class NotInListDiskException(Exception):
    DISKS = ["local"]
    def __init__(self, message: str=f"Notification disk not in list [{ ', '.join(DISKS) }]") -> None:
        self.message = message
        super().__init__(self.message)

class Storage:
    def __init__(self, disk: str, unit: str = "default") -> None:
        self.disk = disk
        self.unit = unit
        if self.disk == "local":
            self.storageManager = LocalStorage()
        else:
            raise NotInListDiskException()
    
    def select_unit(self, unit: str) -> 'Storage':
        self.unit = unit
        return self
    
    def list(self, path: str = "") -> List[str]:
        return self.storageManager.list_files(path)
    
    def get(self, path: str) -> str:
        return self.storageManager.get(path)
    
    def put(self, path: str, content: bytes) -> bool:
        return self.storageManager.put(path, content)
    
    def delete(self, path: str) -> None:
        return self.storageManager.delete(path)
    