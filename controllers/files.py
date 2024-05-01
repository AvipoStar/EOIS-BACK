from fastapi import APIRouter, File, UploadFile
import os
import hashlib

router = APIRouter()


def calculate_file_hash(file_content):
    hash_object = hashlib.md5()
    hash_object.update(file_content)
    return hash_object.hexdigest()


async def uploadUserPhoto(file: UploadFile = File(...)):
    file_content = await file.read()
    file_hash = calculate_file_hash(file_content)
    file_extension = os.path.splitext(file.filename)[1]
    file_path = os.path.join('Documents/UserPhoto/', f"{file_hash}{file_extension}")

    # Проверяем существует ли файл с таким хэшем
    if not os.path.exists(file_path):
        with open(file_path, "wb") as f:
            f.write(file_content)
        return {"filePath": file_path}
    else:
        return {"filePath": file_path}

async def uploadTaskmanagerFile(file: UploadFile = File(...)):
    file_content = await file.read()
    file_hash = calculate_file_hash(file_content)
    file_extension = os.path.splitext(file.filename)[1]
    file_path = os.path.join('Documents/TaskmanagerFiles/', f"{file_hash}{file_extension}")

    # Проверяем существует ли файл с таким хэшем
    if not os.path.exists(file_path):
        with open(file_path, "wb") as f:
            f.write(file_content)
        return {"filePath": file_path}
    else:
        return {"filePath": file_path}
