import base64

def image_file_path_to_base64_url(image_file_path: str) -> str:
    with open(image_file_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        extension = image_file_path.split('.')[-1]
        return f"data:image/{'jpeg' if extension == 'jpg' else extension};base64,{image_base64}"

def buffer_to_base64_url(buffer: bytes) -> str:
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/png;base64,{image_base64}"
