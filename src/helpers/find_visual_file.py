import glob
from typing import Optional

file_cache = {}

def find_visual_file(output_file: str) -> Optional[str]:
    if output_file in file_cache:
        return file_cache[output_file]

    file_extension = output_file.split('.')[-1]
    file_name_without_extension = output_file.rsplit('.', 1)[0]
    image_files = glob.glob(f"{file_name_without_extension}.{{png,jpg,jpeg,svg,webp}}", recursive=False)

    image_file = image_files[0] if image_files else None
    file_cache[output_file] = image_file
    return image_file
