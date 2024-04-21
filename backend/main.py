"""pdf to dxf converter script"""

import os
from shutil import copyfileobj
from typing import List
import uuid
from fastapi import FastAPI, File, HTTPException, UploadFile, Form, status
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from converter_files import converter_files, pdf_capacity_converter
from pdf_to_dxf import extract_and_convert


app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:8000",
]

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    """Pydantic model add pages"""

    pages: int


class Toggle:
    """Change state Toggle"""

    def __init__(self):
        self.state = True

    def releace(self):
        """No catch pdf files"""
        self.state = True

    def catch(self):
        """Catch pdf files"""
        self.state = False

    def not_using(self):
        """Get state"""
        return self.state


toggle_instance = Toggle()


@app.post("/upload-pdf/")
async def upload_pdf(upload_pdf_file: UploadFile = File(...), pages: str = Form(...)):
    """uvicorn uploads post"""

    if toggle_instance.not_using():

        toggle_instance.catch()

        upload_dir = "uploads"
        files_id = uuid.uuid4()
        file_save_path = os.path.join(upload_dir, upload_pdf_file.filename)

        with open(file_save_path, "wb") as file_writer:
            file_writer.write(await upload_pdf_file.read())

        output = "output_folder"
        await extract_and_convert(upload_dir, output, pages, files_id)

        toggle_instance.releace()

        return {"message": files_id, "number": pages}

    raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="anyone using")


@app.get("/download-dxf-zip/{file_uuid}")
async def download_dxf_zip(file_uuid):
    """get download zip files"""
    zip_file_path = "output_folder/" + file_uuid + ".zip"

    return FileResponse(path=zip_file_path, filename="dxf_files.zip")


@app.post("/upload_jpg_or_png/")
async def converter_jpg_png_files(
    files: List[UploadFile] = File(...), quality_number: str = Form(...)
):
    """jpg and png compression function"""
    file_paths = []
    for file in files:
        file_path = f"converter_upload/{file.filename}"
        with open(file_path, "wb") as buffer:
            copyfileobj(file.file, buffer)
        file_paths.append(file_path)

    files_id = uuid.uuid4()
    converter_files(
        get_files="converter_upload",
        output_files="converter_output",
        quality_number=quality_number,
        uuid_name=files_id,
    )

    return {"file_names": files_id, "number": quality_number}


@app.get("/download-jpg-and-png/{file_uuid}")
async def download_jpg_and_png_zip(file_uuid):
    """get download jpg and png in zip files"""
    zip_file_path = "converter_output/" + file_uuid + ".zip"

    return FileResponse(path=zip_file_path, filename="converter_files.zip")


@app.post("/pdf_for_compression/")
async def converter_pdf(
    upload_pdf_for_converter: UploadFile = File(...), zoom_number: str = Form(...)
):
    """pdf compression functions"""
    input_path = f"converter_upload/{upload_pdf_for_converter.filename}"
    with open(input_path, "wb") as buffer:
        copyfileobj(upload_pdf_for_converter.file, buffer)

    pdf_capacity_converter(
        input_folder="converter_upload",
        output_folder="converter_output",
        compression_level=zoom_number,
    )

    return {
        "message": f"Processed {upload_pdf_for_converter.filename}",
        "number": zoom_number,
    }


@app.get("/download-pdf/{file_uuid}")
async def download_pdf(file_uuid: str):
    """PDFファイルをダウンロードする"""
    output_folder = "converter_output"
    pdf_file_path = f"{output_folder}/{file_uuid}.pdf"

    return FileResponse(path=pdf_file_path, filename=f"{file_uuid}.pdf")
