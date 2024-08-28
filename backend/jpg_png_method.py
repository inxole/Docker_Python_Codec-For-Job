"""pdf to dxf converter script"""

import os
from shutil import copyfileobj
from typing import List
import uuid
from fastapi import File, HTTPException, UploadFile, Form, status
from fastapi.responses import FileResponse
from converter_files import converter_files
from fastapi import APIRouter


router = APIRouter()


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


toggleJPGPNG_instance = ToggleJPGPNG()


@router.post("/upload_jpg_or_png/")
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

    raise HTTPException(status_code=status.HTTP_423_LOCKED,
                        detail="anyone using")


@router.get("/download-jpg-and-png/{file_uuid}")
async def download_jpg_and_png_zip(file_uuid):
    """get download jpg and png in zip files"""
    zip_file_path = "converter_output/" + file_uuid + ".zip"

    if not os.path.exists(zip_file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )

    return FileResponse(path=zip_file_path, filename="converter_files.zip")
