"""pdf to dxf converter script"""

import os
from shutil import copyfileobj
import uuid
from fastapi import File, HTTPException, UploadFile,  status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from Converter.converter_files import pdf_capacity_converter
from fastapi import APIRouter


router = APIRouter()


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


togglePDF_instance = TogglePDF()


@router.post("/pdf_for_compression/")
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

        # 入力フォルダ内の全ファイルを削除
        for file_name in os.listdir("converter_upload"):
            file_path = os.path.join("converter_upload", file_name)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)

        togglePDF_instance.releace()
        return {"message": files_id}

    raise HTTPException(status_code=status.HTTP_423_LOCKED,
                        detail="anyone using")


@router.get("/download-pdf/{file_uuid}")
async def download_pdf(file_uuid):
    """get download pdf in zip files"""
    zip_file_path = "converter_output/" + file_uuid + ".zip"

    if not os.path.exists(zip_file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )

    return FileResponse(path=zip_file_path, filename="converter_files.zip")
