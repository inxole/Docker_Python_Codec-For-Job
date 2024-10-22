"""join pdf files"""

import os
import zipfile
import fitz


async def pdf_tie(pdf_dir, output_dir, uuid_name):
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
