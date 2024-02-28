import fitz  # PyMuPDFをインポート
import os

input_dir = 'input'
output_dir = 'output'

# 入力フォルダ内の全てのPDFファイルを検索
for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        input_path = os.path.join(input_dir, filename)
        doc = fitz.open(input_path)

        # PDFの各ページに対して処理
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()

            # 出力ファイルのパスを生成（ファイル名_ページ番号.ppm）
            output_path = os.path.join(output_dir, f"{filename[:-4]}_page{page_num + 1}.ppm")
            pix.save(output_path)

        doc.close()

print("PDFから画像への変換が完了しました。")
