import subprocess
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os

app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-pdf/")
async def upload_pdf(pdf_file: UploadFile):
    file_path = os.path.join(UPLOAD_DIR, pdf_file.filename)
    with open(file_path, "wb") as f:
        f.write(pdf_file.file.read())

    # コマンドラインツールを呼び出す
    cmd = ["python", "pdf_to_dxf.py", file_path, "output_folder"]
    subprocess.run(cmd, check=True)  # エラーチェックを有効にする

    # ダウンロード用エンドポイントにリダイレクト
    return {"message": "PDF uploaded and converted successfully"}

@app.get("/download-dxf/")
async def download_dxf():
    dxf_file_path = "path/to/converted.dxf"  # 変換後のDXFファイルのパスを指定
    return FileResponse(dxf_file_path, filename="converted.dxf")
