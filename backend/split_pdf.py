import os
import zipfile
import fitz

def parse_pages_arg(pages_str):
    """parse_pages"""
    pages = []
    for part in pages_str.split(","):
        if "-" in part:
            start, end = map(int, part.split("-"))
            pages.append(list(range(start, end + 1)))
        else:
            pages.append([int(part)])
    return pages

async def pdf_split(pdf_file, output_dir, pages, uuid_name):
    """pdf separate function"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    specified_pages_list = parse_pages_arg(pages)

    # Open the original PDF
    pdf_document = fitz.open(pdf_file)

    result_pdf_files = []
    base_filename = os.path.splitext(os.path.basename(pdf_file))[0]

    for idx, specified_pages in enumerate(specified_pages_list):
        # Create a new PDF for the specified pages
        new_pdf_document = fitz.open()

        for page_num in specified_pages:
            new_pdf_document.insert_pdf(
                pdf_document, from_page=page_num - 1, to_page=page_num - 1)

        # Save the new PDF
        new_pdf_path = os.path.join(output_dir, f"{base_filename}_{idx + 1}.pdf")
        new_pdf_document.save(new_pdf_path)
        result_pdf_files.append(new_pdf_path)

        # Close the new PDF document
        new_pdf_document.close()

    # Close the original PDF document
    pdf_document.close()

    # Create a ZIP file
    zip_file_path = os.path.join(output_dir, f"{uuid_name}.zip")
    with zipfile.ZipFile(zip_file_path, "w") as zipf:
        for result_pdf_file in result_pdf_files:
            arcname = os.path.basename(result_pdf_file)
            zipf.write(result_pdf_file, arcname=arcname)
            os.remove(result_pdf_file)