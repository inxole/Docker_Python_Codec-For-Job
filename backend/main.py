import os
import subprocess
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from fastapi.responses import FileResponse
from zipfile import ZipFile
from clear_files import clear_directory


app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# 数値やその他のデータを受け取るためのPydanticモデル
class Item(BaseModel):
    pages: int


@app.post("/upload-pdf/")
async def upload_pdf(pdf_file: UploadFile = File(...), pages: int = Form(...)):

    # 既存のファイルを削除
    clear_directory("uploads")
    clear_directory("output_folder")

    UPLOAD_DIR = "uploads"
    file_path = os.path.join(UPLOAD_DIR, pdf_file.filename)

    with open(file_path, "wb") as f:
        f.write(await pdf_file.read())

    # コマンドラインツールを呼び出す
    cmd = ["python", "pdf_to_dxf.py", UPLOAD_DIR, "output_folder", "-p", str(pages)]
    subprocess.run(cmd, check=True)  # エラーチェックを有効にする

    # ダウンロード用エンドポイントにリダイレクト
    return {"message": "PDF uploaded and converted successfully", "number": pages}


@app.get("/download-dxf-zip/")
async def download_dxf_zip():
    output_folder = "output_folder"
    zip_file_path = "output_folder/dxf_files.zip"

    # ZIPファイルを作成
    with ZipFile(zip_file_path, "w") as zipf:
        for root, dirs, files in os.walk(output_folder):
            for file in files:
                if file.endswith(".dxf"):
                    # .dxfファイルのみをZIPに追加
                    zipf.write(os.path.join(root, file), arcname=file)

    # ZIPファイルをレスポンスとして返す
    return FileResponse(path=zip_file_path, filename="dxf_files.zip")
