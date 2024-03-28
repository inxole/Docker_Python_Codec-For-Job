"""pdf to dxf converter script"""

import os
import subprocess
import uuid
from zipfile import ZipFile
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from clear_files import clear_directory
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


# 数値やその他のデータを受け取るためのPydanticモデル
class Item(BaseModel):
    """pydantic model add pages"""

    pages: int


@app.post("/upload-pdf/")
async def upload_pdf(upload_pdf_file: UploadFile = File(...), pages: int = Form(...)):
    """uvicorn uploads post"""
    # 既存のファイルを削除
    clear_directory("uploads")
    clear_directory("output_folder")

    upload_dir = "uploads"
    files_id = uuid.uuid4()
    file_save_path = os.path.join(upload_dir, str(files_id) + ".pdf")

    with open(file_save_path, "wb") as file_writer:
        file_writer.write(await upload_pdf_file.read())

    # コマンドラインツールを呼び出す
    # cmd = ["python", "pdf_to_dxf.py", upload_dir, "output_folder", "-p", str(pages)]
    # subprocess.run(cmd, check=True)  # エラーチェックを有効にする
    output = "output_folder"
    extract_and_convert(upload_dir, output)

    # ダウンロード用エンドポイントにリダイレクト
    return {"message": files_id, "number": pages}


@app.get("/download-dxf-zip/")
async def download_dxf_zip():
    """get downloads zip files"""
    output_folder = "output_folder"
    zip_file_path = "output_folder/dxf_files.zip"

    # ZIPファイルを作成
    with ZipFile(zip_file_path, "w") as zipf:
        for root, _, files in os.walk(output_folder):
            for file in files:
                if file.endswith(".dxf"):
                    # .dxfファイルのみをZIPに追加
                    zipf.write(os.path.join(root, file), arcname=file)

    # ZIPファイルをレスポンスとして返す
    return FileResponse(path=zip_file_path, filename="dxf_files.zip")
