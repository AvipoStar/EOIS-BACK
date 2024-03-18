from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from controllers.timetable import uploadPDFFile, downloadPDFFile

router = APIRouter()

@router.post("/upload", tags=["Timetable"])
async def upload_PDF(file: UploadFile = File(...), date: str = ""):
    newfile = uploadPDFFile(file, date)
    return newfile

@router.get("/download", tags=["Timetable"])
def download_PDF():
    file = downloadPDFFile()
    return file