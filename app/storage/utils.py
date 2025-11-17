import mimetypes


def get_mime_type(filename: str) -> str:
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or "application/octet-stream"


def is_video(mime_type: str) -> bool:
    return mime_type.startswith("video/") if mime_type else False


def is_image(mime_type: str) -> bool:
    return mime_type.startswith("image/") if mime_type else False
