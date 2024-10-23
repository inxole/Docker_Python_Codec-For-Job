"""Script to split and combine pdf"""

import os
import uuid
from fastapi import HTTPException, UploadFile, status, APIRouter, Form, File
from fastapi.responses import FileResponse
from movie_cutout import extract_frame


router = APIRouter()


class FlvFileToggle:
    """Change state Toggle"""

    def __init__(self):
        self.state = True

    def releace(self):
        """No catch flv files"""
        self.state = True

    def catch(self):
        """Catch flv files"""
        self.state = False

    def not_using(self):
        """Get state"""
        return self.state


flvFileStateToggler = FlvFileToggle()


@router.post("/upload-flv/")
async def upload_flv(flv_file: UploadFile = File(...), seconds: int = Form(...)):
    """uvicorn uploads flv"""
    if flvFileStateToggler.not_using():
        flvFileStateToggler.catch()

        upload_dir = "uploads"
        files_id = uuid.uuid4()
        file_save_path = os.path.join(upload_dir, flv_file.filename)

        with open(file_save_path, "wb") as file_writer:
            file_writer.write(await flv_file.read())

        output = "output_folder"
        extract_frame(file_save_path, output, seconds, uuid_name=files_id)

        # 入力フォルダ内の全ファイルを削除
        for file_name in os.listdir("uploads"):
            file_path = os.path.join("uploads", file_name)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)

        flvFileStateToggler.releace()

        return {"message": files_id, "time": seconds}

    raise HTTPException(status_code=status.HTTP_423_LOCKED,
                        detail="anyone using")


@router.get("/download-flv-zip/{file_uuid}")
async def download_result_flv_zip(file_uuid):
    """get download zip files"""
    zip_file_path = "output_folder/" + file_uuid + ".zip"

    if not os.path.exists(zip_file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    return FileResponse(path=zip_file_path, filename="result_pdf_files.zip")
