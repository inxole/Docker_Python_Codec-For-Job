"""Script to split and combine pdf"""

import os
import uuid
import zipfile
import fitz
from fastapi import HTTPException, UploadFile, status, APIRouter, Form, File
from fastapi.responses import FileResponse
from pydantic import BaseModel


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


@router.post("/upload-pdf-separate_or_join/")
async def upload_pdf(pdf_file: UploadFile = File(...), pages: str = Form(...), mode: str = Form(...)):
    """uvicorn uploads post - 分割 or 結合"""
    if pdfFileStateToggler.not_using():
        pdfFileStateToggler.catch()

        upload_dir = "uploads"
        files_id = uuid.uuid4()
        file_save_path = os.path.join(upload_dir, pdf_file.filename)

        with open(file_save_path, "wb") as file_writer:
            file_writer.write(await pdf_file.read())

        output = "output_folder"
        if mode == "split":
            await pdf_separate(upload_dir, output, pages, files_id)
        elif mode == "join":
            await pdf_join(upload_dir, output, files_id)

        # 入力フォルダ内の全ファイルを削除
        for file_name in os.listdir("uploads"):
            file_path = os.path.join("uploads", file_name)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)

        pdfFileStateToggler.releace()

        return {"message": files_id, "number": pages}

    raise HTTPException(status_code=status.HTTP_423_LOCKED,
                        detail="anyone using")


@router.get("/download-pdf-SoJ-zip/{file_uuid}")
async def download_result_zip(file_uuid):
    """get download zip files"""
    zip_file_path = "output_folder/" + file_uuid + ".zip"

    if not os.path.exists(zip_file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    return FileResponse(path=zip_file_path, filename="result_pdf_files.zip")


def parse_pages_arg(pages_str):
    """parse_pages"""
    # 結果を格納するリスト
    pages = []

    # カンマで分割して個々の範囲またはページを解析
    for part in pages_str.split(","):
        if "-" in part:
            # ハイフンがあれば範囲として処理
            start, end = map(int, part.split("-"))
            pages.extend(range(start, end + 1))
        else:
            # 単一のページ番号を追加
            pages.append(int(part))

    return pages


async def pdf_separate(pdf_file, output_dir, pages, uuid_name):
    """pdf separate function"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    specified_pages = parse_pages_arg(pages)

    # Open the original PDF
    pdf_document = fitz.open(pdf_file)

    # Create a new PDF for the specified pages
    new_pdf_document = fitz.open()

    for page_num in specified_pages:
        new_pdf_document.insert_pdf(
            pdf_document, from_page=page_num - 1, to_page=page_num - 1)

    # Save the new PDF
    new_pdf_path = os.path.join(output_dir, f"{uuid_name}_extracted.pdf")
    new_pdf_document.save(new_pdf_path)

    # Close the documents
    pdf_document.close()
    new_pdf_document.close()

    # Create a ZIP file
    zip_file_path = os.path.join(output_dir, f"{uuid_name}.zip")
    with zipfile.ZipFile(zip_file_path, "w") as zipf:
        result_pdf_files = [
            f
            for f in os.listdir(output_dir)
            if f.startswith(str(uuid_name)) and f.endswith(".pdf")
        ]
        for result_pdf_file in result_pdf_files:
            pdf_file_path = os.path.join(output_dir, result_pdf_file)
            arcname = result_pdf_file[len(str(uuid_name)) + 1:]
            zipf.write(pdf_file_path, arcname=arcname)
            os.remove(pdf_file_path)


async def pdf_join(pdf_dir, output_dir, uuid_name):
    """pdf join function"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create a new PDF for the joined files
    merged_pdf_document = fitz.open()

    # Find all the PDF files in the upload directory
    for file_name in os.listdir(pdf_dir):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, file_name)
            pdf_document = fitz.open(pdf_path)

            # Insert all pages from the current PDF
            merged_pdf_document.insert_pdf(pdf_document)
            pdf_document.close()

    # Save the merged PDF
    new_pdf_path = os.path.join(output_dir, f"{uuid_name}_merged.pdf")
    merged_pdf_document.save(new_pdf_path)
    merged_pdf_document.close()

    # Create a ZIP file
    zip_file_path = os.path.join(output_dir, f"{uuid_name}.zip")
    with zipfile.ZipFile(zip_file_path, "w") as zipf:
        result_pdf_files = [
            f
            for f in os.listdir(output_dir)
            if f.startswith(str(uuid_name)) and f.endswith(".pdf")
        ]
        for result_pdf_file in result_pdf_files:
            pdf_file_path = os.path.join(output_dir, result_pdf_file)
            arcname = result_pdf_file[len(str(uuid_name)) + 1:]
            zipf.write(pdf_file_path, arcname=arcname)
            os.remove(pdf_file_path)
