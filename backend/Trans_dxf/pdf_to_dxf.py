"""converter pdf files to dxf files"""

import asyncio
import os
import zipfile
from Trans_dxf.pdf_to_svg import pdf_to_svg

INKSCAPE_DIR = "/usr/bin/inkscape"


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


async def convert_svg_to_dxf(svg_file, dxf_file):
    """converter svg files to dxf files on inkscape"""
    process = await asyncio.create_subprocess_exec(
        INKSCAPE_DIR, svg_file, "--export-type=dxf", "-o", dxf_file
    )
    await process.wait()  # プロセスの終了を待つ
    print("SVGをDXFへ変換しました。")


async def extract_and_convert(pdf_file, output_dir, pages, uuid_name):
    """Convert PDF files to SVG and then to DXF."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    specified_page = parse_pages_arg(pages)
    pdf_to_svg(pdf_file, output_dir, specified_page)

    svg_files = [f for f in os.listdir(output_dir) if f.endswith(".svg")]

    for svg_file_name in svg_files:
        svg_file_path = os.path.join(output_dir, svg_file_name)
        dxf_file_name = f"{uuid_name}_{os.path.splitext(svg_file_name)[0]}.dxf"
        dxf_file_path = os.path.join(output_dir, dxf_file_name)
        await convert_svg_to_dxf(svg_file_path, dxf_file_path)
        os.remove(svg_file_path)

    # ZIPファイルの作成
    zip_file_path = os.path.join(output_dir, f"{uuid_name}.zip")
    with zipfile.ZipFile(zip_file_path, "w") as zipf:
        dxf_files = [
            f
            for f in os.listdir(output_dir)
            if f.startswith(str(uuid_name)) and f.endswith(".dxf")
        ]
        for dxf_file in dxf_files:
            dxf_file_path = os.path.join(output_dir, dxf_file)
            arcname = dxf_file[len(str(uuid_name)) + 1 :]
            zipf.write(dxf_file_path, arcname=arcname)
            os.remove(dxf_file_path)
