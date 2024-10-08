"""pdf to dxf converter script"""

import os
import uuid
from fastapi import File, HTTPException, UploadFile, Form, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pdf_to_dxf import extract_and_convert
from fastapi import APIRouter


router = APIRouter()


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


toggleDXF_instance = ToggleTransDXF()


@router.post("/upload-pdf/")
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

        # 入力フォルダ内の全ファイルを削除
        for file_name in os.listdir("uploads"):
            file_path = os.path.join("uploads", file_name)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)

        toggleDXF_instance.releace()

        return {"message": files_id, "number": pages}

    raise HTTPException(status_code=status.HTTP_423_LOCKED,
                        detail="anyone using")


@router.get("/download-dxf-zip/{file_uuid}")
async def download_dxf_zip(file_uuid):
    """get download zip files"""
    zip_file_path = "output_folder/" + file_uuid + ".zip"

    if not os.path.exists(zip_file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )

    return FileResponse(path=zip_file_path, filename="dxf_files.zip")
