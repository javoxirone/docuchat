from fastapi import UploadFile
from fastapi.exceptions import HTTPException

from .constants import (
    ALLOWED_CONTENT_TYPES,
    ALLOWED_EXTENSIONS,
    EXTENSION_TO_CONTENT_TYPE,
)
from .exceptions import NoFileNameError
from .utils import get_file_extension


def is_file_supported(file: UploadFile) -> bool:
    if file.filename is None or file.content_type is None:
        return False
    try:
        extension = get_file_extension(file.filename)
    except NoFileNameError as e:
        raise HTTPException(400, detail=str(e)) from e
    return extension in ALLOWED_EXTENSIONS and file.content_type in ALLOWED_CONTENT_TYPES


def is_extension_corresponds_to_mime_type(file: UploadFile) -> bool:
    if file.filename is None or file.content_type is None:
        return False
    try:
        extension = get_file_extension(file.filename)
    except NoFileNameError as e:
        raise HTTPException(400, detail=str(e)) from e
    expected_content_type = EXTENSION_TO_CONTENT_TYPE.get(extension)
    return expected_content_type == file.content_type


async def validate_mime_type(file: UploadFile) -> UploadFile:
    if file.content_type is None:
        raise HTTPException(400, detail="File must have a content type")
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(400, detail="File must be either in pdf or txt format")
    return file


async def validate_extension(file: UploadFile) -> UploadFile:
    try:
        extension = get_file_extension(file.filename)
    except NoFileNameError as e:
        raise HTTPException(400, detail=str(e)) from e
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, detail="File must be either in pdf or txt format")
    return file


async def validate_content(file: UploadFile) -> UploadFile:
    header = await file.read(5)
    if file.content_type == "application/pdf":
        if not header.startswith(b"%PDF-"):
            raise HTTPException(400, detail="File content is not valid PDF format")
    elif file.content_type == "text/plain":
        try:
            header.decode("utf-8")
        except UnicodeDecodeError as e:
            raise HTTPException(400, detail="File content is not valid TXT format") from e
        finally:
            await file.seek(0)  # Reset the file pointer to the beginning after reading
    await file.seek(0)  # Reset the file pointer to the beginning after reading
    return file


async def validate_file(file: UploadFile) -> UploadFile:
    if is_file_supported(file) is False:
        raise HTTPException(400, detail="File must be either in pdf or txt format")
    if is_extension_corresponds_to_mime_type(file) is False:
        raise HTTPException(400, detail="File extension does not match the MIME type")
    handled_file = await validate_mime_type(file)
    handled_file = await validate_extension(handled_file)
    handled_file = await validate_content(handled_file)
    return handled_file
