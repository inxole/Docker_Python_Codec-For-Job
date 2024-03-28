"""converter pdf files to svg files function"""

import os
import subprocess
import shutil
import fitz


def pdf_to_svg(input_folder, output_folder):
    """converter pdf files to svg files function"""
    # 一時的にPPMファイルを保存するフォルダを作成
    temp_folder = os.path.join(output_folder, "temp_ppm")
    os.makedirs(temp_folder, exist_ok=True)

    # 入力フォルダ内の全てのPDFファイルを検索
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_folder, filename)
            doc = fitz.open(input_path)

            # PDFの各ページに対して処理
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap()

                # 一時フォルダ内にPPMファイルを保存
                temp_output_path = os.path.join(
                    temp_folder, f"{filename[:-4]}_{page_num + 1}.ppm"
                )
                pix.save(temp_output_path)

            doc.close()

    # 一時フォルダ内の全てのPPMファイルをSVGに変換
    for filename in os.listdir(temp_folder):
        if filename.endswith(".ppm"):
            input_path = os.path.join(temp_folder, filename)
            output_path = os.path.join(output_folder, filename.replace(".ppm", ".svg"))

            # Potraceコマンドを構築
            command = f"potrace {input_path} -s -o {output_path}"

            # コマンドを実行
            subprocess.run(command, shell=True, check=True)

    # 一時フォルダを削除
    shutil.rmtree(temp_folder)
