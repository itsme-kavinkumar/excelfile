from fastapi import APIRouter
from fastapi.responses import HTMLResponse
router = APIRouter()

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import shutil
import os
router=APIRouter()
REPO_PATH = "https://github.com/itsme-kavinkumar/fastapi-Crud"
UPLOAD_DIR = "uploads"

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    print('-----',file.filename)
    file_path = os.path.join(REPO_PATH, UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

@router.get("/upload")
async def get_upload_form():
    content = """
    <html>
    <head>
        <title>File Upload</title>
    </head>
    <body>
        <h1>Upload File</h1>
        <form action="/upload/" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit">
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=content)
