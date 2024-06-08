import os

def file_exists(file_path: str) -> bool:
    return os.path.exists(file_path)
