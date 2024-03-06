import subprocess
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from fastapi.responses import FileResponse
import os


app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# 数値やその他のデータを受け取るためのPydanticモデル
class Item(BaseModel):
    pages: int


@app.post("/upload-pdf/")
async def upload_pdf(pdf_file: UploadFile = File(...)):
    UPLOAD_DIR = "uploads"
    file_path = os.path.join(UPLOAD_DIR, pdf_file.filename)

    with open(file_path, "wb") as f:
        f.write(await pdf_file.read())

    # コマンドラインツールを呼び出す
    cmd = ["python", "pdf_to_dxf.py", UPLOAD_DIR, "output_folder"]
    subprocess.run(cmd, check=True)  # エラーチェックを有効にする

    # ダウンロード用エンドポイントにリダイレクト
    return {"message": "PDF uploaded and converted successfully"}


@app.get("/download-dxf/")
async def download_dxf():
    dxf_file_path = "output_folder/converted.dxf"
    return FileResponse(dxf_file_path, filename="converted.dxf")
