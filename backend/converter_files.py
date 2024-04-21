"""pdf or png or pdf converter"""

import os
import shutil
import zipfile
from PIL import Image
import fitz


def converter_files(get_files, output_files, quality_number, uuid_name):
    """pdf and png converter function"""
    # 出力フォルダが存在しない場合は作成
    if not os.path.exists(output_files):
        os.makedirs(output_files)

    # 出力ファイル名のリストを初期化
    converted_files = []

    # 入力フォルダ内の全ファイルに対して処理
    for image_file in os.listdir(get_files):
        # 画像ファイルのパスを組み立て
        file_path = os.path.join(get_files, image_file)
        # UUID名を追加した出力ファイル名
        output_file_name = f"{uuid_name}_{image_file}"
        output_path = os.path.join(output_files, output_file_name)

        # JPEGファイルの場合
        if image_file.lower().endswith((".jpg", ".jpeg")):
            with Image.open(file_path) as img:
                jpg_quality = int(quality_number)
                img.save(output_path, "JPEG", quality=jpg_quality)

        # PNGファイルの場合
        elif image_file.lower().endswith(".png"):
            with Image.open(file_path) as img:
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


def pdf_capacity_converter(input_folder, output_folder, compression_level):
    """conpress pdf function"""
    temp_folder = os.path.join(output_folder, "temp")  # 一時的にPNGを保存するフォルダ

    # 出力フォルダと一時フォルダを作成（存在しない場合）
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    # PDFをPNGに変換し、最終的なPDFに再変換
    for pdf_file in os.listdir(input_folder):
        if pdf_file.endswith(".pdf"):
            doc = fitz.open(os.path.join(input_folder, pdf_file))
            images = []
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                zoom = float(compression_level)
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                output_file = f"temp_{page_num}.png"  # 一時ファイル名
                img.save(os.path.join(temp_folder, output_file))

                img_path = os.path.join(temp_folder, output_file)
                image = Image.open(img_path).convert("RGB")
                images.append(image)

            doc.close()

            # PDFにまとめる
            if images:
                output_pdf = (
                    os.path.splitext(pdf_file)[0] + "_compressed.pdf"
                )  # 元のファイル名に基づく新しいファイル名
                output_path = os.path.join(output_folder, output_pdf)
                images[0].save(output_path, save_all=True, append_images=images[1:])

            # 使用した画像ファイルを削除
            for image_file in os.listdir(temp_folder):
                os.remove(os.path.join(temp_folder, image_file))

    # 一時フォルダを削除
    shutil.rmtree(temp_folder)
