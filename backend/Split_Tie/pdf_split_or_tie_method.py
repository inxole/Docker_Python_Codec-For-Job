"""Script to split and combine pdf"""

import os
import uuid
from typing import List
from fastapi import HTTPException, UploadFile, status, APIRouter, Form, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from Split_Tie.split_pdf import pdf_split
from Split_Tie.tie_pdf import pdf_tie


router = APIRouter()


class Item(BaseModel):
    """Pydantic model add pages"""
    pages: str


class PdfFileToggle:
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


pdfFileStateToggler = PdfFileToggle()


@router.post("/upload-pdf-split/")
async def upload_pdf_split(pdf_file: UploadFile = File(...), pages: str = Form(...)):
    """uvicorn uploads post - 分割"""
    if pdfFileStateToggler.not_using():
        pdfFileStateToggler.catch()

        upload_dir = "uploads"
        files_id = uuid.uuid4()
        file_save_path = os.path.join(upload_dir, pdf_file.filename)

        with open(file_save_path, "wb") as file_writer:
            file_writer.write(await pdf_file.read())

        output = "output_folder"
        await pdf_split(file_save_path, output, pages, files_id)

        # 入力フォルダ内の全ファイルを削除
        for file_name in os.listdir("uploads"):
            file_path = os.path.join("uploads", file_name)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)

        pdfFileStateToggler.releace()

        return {"message": files_id, "number": pages}

    raise HTTPException(status_code=status.HTTP_423_LOCKED,
                        detail="anyone using")


@router.post("/upload-pdf-tie/")
async def upload_pdf_tie(files: List[UploadFile] = File(...)):
    """複数のPDFファイルを結合するためのエンドポイント"""
    if pdfFileStateToggler.not_using():
        pdfFileStateToggler.catch()

        upload_dir = "uploads"
        files_id = uuid.uuid4()
        file_paths = []

        # 各ファイルを保存
        for pdf_file in files:
            file_save_path = os.path.join(upload_dir, pdf_file.filename)
            file_paths.append(file_save_path)
            with open(file_save_path, "wb") as file_writer:
                file_writer.write(await pdf_file.read())

        output = "output_folder"
        await pdf_tie(upload_dir, output, files_id)

        # 入力フォルダ内の全ファイルを削除
        for file_name in os.listdir("uploads"):
            file_path = os.path.join("uploads", file_name)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)

        pdfFileStateToggler.releace()

        return {"message": files_id}

    raise HTTPException(status_code=status.HTTP_423_LOCKED,
                        detail="anyone using")


@router.get("/download-pdf-SoT-zip/{file_uuid}")
async def download_result_zip(file_uuid):
    """get download zip files"""
    zip_file_path = "output_folder/" + file_uuid + ".zip"

    if not os.path.exists(zip_file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    return FileResponse(path=zip_file_path, filename="result_pdf_files.zip")
