"""converter pdf files to dxf files"""

import asyncio
import os
import argparse
from pdf_to_svg import pdf_to_svg

INKSCAPE_DIR = "/usr/bin/inkscape"


async def convert_svg_to_dxf(svg_file, dxf_file):
    """converter svg files to dxf files on inkscape"""
    process = await asyncio.create_subprocess_exec(
        INKSCAPE_DIR, svg_file, "--export-type=dxf", "-o", dxf_file
    )
    await process.wait()  # プロセスの終了を待つ
    print("SVGをDXFへ変換しました。")


async def extract_and_convert(pdf_file, output_dir):
    """pdf files throw pdf_to_svg"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_to_svg(pdf_file, output_dir)

    svg_files = [f for f in os.listdir(output_dir) if f.endswith(".svg")]

    for svg_file_name in svg_files:
        svg_file_path = os.path.join(output_dir, svg_file_name)
        dxf_file_name = f"{os.path.splitext(svg_file_name)[0]}.dxf"
        dxf_file_path = os.path.join(output_dir, dxf_file_name)

        await convert_svg_to_dxf(svg_file_path, dxf_file_path)


def parse_pages_arg(pages_arg):
    """Recognize the specified page"""
    page_numbers = []
    for part in pages_arg.split(","):
        if "-" in part:
            start, end = map(int, part.split("-"))
            page_numbers.extend(range(start - 1, end))
        else:
            page_numbers.append(int(part) - 1)
    return page_numbers


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract SVGs from PDF and convert to DXF."
    )
    parser.add_argument("pdf_file", type=str, help="Input PDF file")
    parser.add_argument("output_dir", type=str, help="Output directory")
    parser.add_argument(
        "-p",
        "--pages",
        type=str,
        help="Comma-separated page numbers or page ranges to extract (1-indexed)",
        default=None,
    )
    args = parser.parse_args()

    pages = parse_pages_arg(args.pages) if args.pages is not None else None
    extract_and_convert(args.pdf_file, args.output_dir)
