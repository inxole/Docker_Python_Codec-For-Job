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


class ToggleTransDXF:
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


class ToggleJPGPNG:
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


class TogglePDF:
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


class Opinion(BaseModel):
    """test"""

    id: str
    content: str


toggleDXF_instance = ToggleTransDXF()
toggleJPGPNG_instance = ToggleJPGPNG()
togglePDF_instance = TogglePDF()


@app.post("/upload-pdf/")
async def upload_pdf(upload_pdf_file: UploadFile = File(...), pages: str = Form(...)):
    """uvicorn uploads post"""

    if toggleDXF_instance.not_using():
        toggleDXF_instance.catch()

        upload_dir = "uploads"
        files_id = uuid.uuid4()
        file_save_path = os.path.join(upload_dir, upload_pdf_file.filename)

        with open(file_save_path, "wb") as file_writer:
            file_writer.write(await upload_pdf_file.read())

        output = "output_folder"
        await extract_and_convert(upload_dir, output, pages, files_id)

        toggleDXF_instance.releace()

        return {"message": files_id, "number": pages}

    raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="anyone using")


@app.get("/download-dxf-zip/{file_uuid}")
async def download_dxf_zip(file_uuid):
    """get download zip files"""
    zip_file_path = "output_folder/" + file_uuid + ".zip"

    if not os.path.exists(zip_file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )

    return FileResponse(path=zip_file_path, filename="dxf_files.zip")


@app.post("/upload_jpg_or_png/")
async def converter_jpg_png_files(
    files: List[UploadFile] = File(...), quality_number: str = Form(...)
):
    """jpg and png compression function"""
    if toggleJPGPNG_instance.not_using():
        toggleJPGPNG_instance.catch()

        file_paths = []
        for file in files:
            file_path = f"converter_upload/{file.filename}"
            with open(file_path, "wb") as buffer:
                copyfileobj(file.file, buffer)
            file_paths.append(file_path)

        files_id = uuid.uuid4()
        await converter_files(
            get_files="converter_upload",
            output_files="converter_output",
            quality_number=quality_number,
            uuid_name=files_id,
        )

        toggleJPGPNG_instance.releace()

        return {"message": files_id, "number": quality_number}

    raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="anyone using")


@app.get("/download-jpg-and-png/{file_uuid}")
async def download_jpg_and_png_zip(file_uuid):
    """get download jpg and png in zip files"""
    zip_file_path = "converter_output/" + file_uuid + ".zip"

    if not os.path.exists(zip_file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )

    return FileResponse(path=zip_file_path, filename="converter_files.zip")


@app.post("/pdf_for_compression/")
async def converter_pdf(upload_pdf_for_converter: UploadFile = File(...)):
    """pdf compression functions"""
    if togglePDF_instance.not_using():
        togglePDF_instance.catch()

        input_path = f"converter_upload/{upload_pdf_for_converter.filename}"
        with open(input_path, "wb") as buffer:
            copyfileobj(upload_pdf_for_converter.file, buffer)

        files_id = uuid.uuid4()
        await pdf_capacity_converter(
            input_folder="converter_upload",
            output_folder="converter_output",
            compression_level=1.5,
            uuid_name=files_id,
        )

        togglePDF_instance.releace()
        return {"message": files_id}

    raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="anyone using")


@app.get("/download-pdf/{file_uuid}")
async def download_pdf(file_uuid):
    """get download pdf in zip files"""
    zip_file_path = "converter_output/" + file_uuid + ".zip"

    if not os.path.exists(zip_file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )

    return FileResponse(path=zip_file_path, filename="converter_files.zip")


def save_opinion(opinion: Opinion):
    """test"""
    with open("opinions.txt", "a", encoding="utf-8") as file:
        file.write(f"{opinion.id}:{opinion.content}\n")


def load_opinions():
    """test"""
    opinions = []
    try:
        with open("opinions.txt", "r", encoding="utf-8") as file:
            for line in file:
                opinion_id, content = line.strip().split(":")
                opinions.append(Opinion(id=opinion_id, content=content))
    except FileNotFoundError:
        pass
    return opinions


@app.post("/opinions/")
def create_opinion(opinion: Opinion):
    """test"""
    opinion.id = str(uuid.uuid4())
    save_opinion(opinion)
    return opinion


@app.get("/opinions/")
def read_opinions():
    """test"""
    return load_opinions()


@app.delete("/opinions/{opinion_id}")
def delete_opinion(opinion_id: str):
    """test"""
    opinions = load_opinions()
    opinions = [opinion for opinion in opinions if opinion.id != opinion_id]
    with open("opinions.txt", "w", encoding="utf-8") as file:
        for opinion in opinions:
            file.write(f"{opinion.id}:{opinion.content}\n")
    return {"message": "Opinion deleted"}
