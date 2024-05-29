from fastapi import APIRouter, File, UploadFile
from starlette.responses import JSONResponse
import os
import hashlib
import uuid

from controllers.files import uploadUserPhoto, uploadTaskmanagerFile

router = APIRouter()


def calculate_file_hash(file_content):
    hash_object = hashlib.md5()
    hash_object.update(file_content)
    return hash_object.hexdigest()


@router.post("/uploadUserPhoto", tags=["Files"])
async def upload_user_photo(file: UploadFile = File(...)):
    result = await uploadUserPhoto(file)
    return result


@router.post("/uploadTaskmanagerFiles", tags=["Files"])
async def upload_taskmanager_file(file: UploadFile = File(...)):
    result = await uploadTaskmanagerFile(file)
    return result
