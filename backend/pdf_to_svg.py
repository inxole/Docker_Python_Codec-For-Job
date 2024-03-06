import fitz  # PyMuPDF
import subprocess
import os
import shutil

def pdf_to_svg(pdf_file_path, output_folder, pages=None):
    # 一時的にPPMファイルを保存するフォルダを作成
    temp_folder = os.path.join(output_folder, "temp_ppm")
    os.makedirs(temp_folder, exist_ok=True)
    
    doc = fitz.open(pdf_file_path)

    # ページが指定されていない場合、全ページを処理
    if pages is None:
        pages_process = range(len(doc))
    else:
        pages_process = [pages]
    
    # 指定されたページに対して処理
    for page_num in pages_process:
        if page_num < len(doc):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()

            # 一時フォルダ内にPPMファイルを保存
            temp_output_path = os.path.join(temp_folder, f"{os.path.splitext(os.path.basename(pdf_file_path))[0]}_page{page_num + 1}.ppm")
            pix.save(temp_output_path)

    doc.close()

    # 一時フォルダ内の全てのPPMファイルをSVGに変換
    for filename in os.listdir(temp_folder):
        if filename.endswith(".ppm"):
            input_path = os.path.join(temp_folder, filename)
            output_path = os.path.join(output_folder, filename.replace('.ppm', '.svg'))

            # Potraceコマンドを構築
            command = f"potrace {input_path} -s -o {output_path}"

            # コマンドを実行
            subprocess.run(command, shell=True)

    # 一時フォルダを削除
    shutil.rmtree(temp_folder)

    print("PDFからSVGへの変換が完了しました。")
