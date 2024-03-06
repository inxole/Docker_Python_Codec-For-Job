import subprocess
from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from fastapi.responses import FileResponse
import os
from pdf_to_dxf import extract_and_convert


app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# 数値やその他のデータを受け取るためのPydanticモデル
class Item(BaseModel):
    pages: int


@app.post("/upload-pdf/")
async def upload_pdf(pdf_file: UploadFile = File(...), pages: int = Form(...)):
    UPLOAD_DIR = "/app/uploads"
    file_path = os.path.join(UPLOAD_DIR, pdf_file.filename)

    with open(file_path, "wb") as f:
        f.write(await pdf_file.read())

    # PDFファイルをDXFに変換する関数の呼び出し
    extract_and_convert(file_path, "/app/output_folder", pages)

    # ダウンロード用エンドポイントにリダイレクト
    return {"message": "PDF uploaded and converted successfully", "number": pages}


@app.get("/download-dxf/")
async def download_dxf():
    dxf_file_path = "/app/output_folder/converted.dxf"
    return FileResponse(dxf_file_path, filename="converted.dxf")
