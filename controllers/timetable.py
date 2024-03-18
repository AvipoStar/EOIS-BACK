import datetime
import os
from fastapi import UploadFile, File


def uploadPDFFile(file: UploadFile = File(...), date: str = ""):
    file_name = f"{date}.pdf"
    file_path = f"uploads/{file_name}"

    with open(file_path, "wb") as f:
        contents = file.file.read()
        f.write(contents)

    return file_path

def downloadPDFFile():
    today = datetime.date.today()
    formatted_date = today.strftime("%d.%m.%Y")
    file_path = os.path.join("uploads", f"{formatted_date}.pdf")
    print(f'file_path {file_path}')
    if not os.path.exists(file_path):
        return {"error": "Файл не найден"}
    with open(file_path, 'rb') as file:
        pdf_data = file.read().decode('utf-8', errors='ignore')
    return pdf_data