"""pdf or png or pdf converter"""

import io
import os
import shutil
import zipfile
from PIL import Image
import aiofiles
import fitz


async def converter_files(get_files, output_files, quality_number, uuid_name):
    """pdf and png converter function"""
    # 出力フォルダが存在しない場合は作成
    if not os.path.exists(output_files):
        os.makedirs(output_files)

    # 出力ファイル名のリストを初期化
    converted_files = []

    # 入力フォルダ内の全ファイルに対して処理
    for image_file in os.listdir(get_files):
        file_path = os.path.join(get_files, image_file)
        output_file_name = f"{uuid_name}_{image_file}"
        output_path = os.path.join(output_files, output_file_name)

        # JPEGファイルの場合
        if image_file.lower().endswith((".jpg", ".jpeg")):
            async with aiofiles.open(file_path, "rb") as f:
                data = await f.read()
            img = Image.open(io.BytesIO(data))
            jpg_quality = int(quality_number)
            img.save(output_path, "JPEG", quality=jpg_quality)

        # PNGファイルの場合
        elif image_file.lower().endswith(".png"):
            async with aiofiles.open(file_path, "rb") as f:
                data = await f.read()
            img = Image.open(io.BytesIO(data))
            img = img.quantize(colors=256)
            img.save(output_path, "PNG", optimize=True)
        converted_files.append(output_path)

    zip_path = os.path.join(output_files, f"{str(uuid_name)}.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file in converted_files:
            zipf.write(
                file, arcname=os.path.basename(file).replace(f"{uuid_name}_", "")
            )
            os.remove(file)


async def pdf_capacity_converter(
    input_folder, output_folder, compression_level, uuid_name
):
    """compress pdf function"""
    temp_folder = os.path.join(output_folder, "temp")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    for pdf_file in os.listdir(input_folder):
        if pdf_file.endswith(".pdf"):
            new_pdf_path = os.path.join(input_folder, str(uuid_name) + pdf_file)
            old_pdf_path = os.path.join(input_folder, pdf_file)
            os.rename(old_pdf_path, new_pdf_path)

    for pdf_file in os.listdir(input_folder):
        if pdf_file.startswith(str(uuid_name)) and pdf_file.endswith(".pdf"):
            doc = fitz.open(os.path.join(input_folder, pdf_file))
            images = []
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                zoom = float(compression_level)
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                output_file = f"temp_{page_num}.png"
                img_path = os.path.join(temp_folder, output_file)
                img.save(img_path)  # 同期的に保存

                async with aiofiles.open(img_path, "rb") as file:
                    img_data = await file.read()  # ファイルの内容を非同期で読み込む

                image = Image.open(io.BytesIO(img_data)).convert("RGB")
                images.append(image)

            doc.close()

            if images:
                output_pdf = os.path.splitext(pdf_file)[0] + "_compressed.pdf"
                output_path = os.path.join(output_folder, output_pdf)
                images[0].save(output_path, save_all=True, append_images=images[1:])

            for image_file in os.listdir(temp_folder):
                os.remove(os.path.join(temp_folder, image_file))

    shutil.rmtree(temp_folder)

    final_files = [
        f for f in os.listdir(output_folder) if f.endswith("_compressed.pdf")
    ]
    with zipfile.ZipFile(os.path.join(output_folder, f"{uuid_name}.zip"), "w") as zipf:
        for file in final_files:
            zipf.write(
                os.path.join(output_folder, file), arcname=file[len(str(uuid_name)) :]
            )
            os.remove(os.path.join(output_folder, file))
