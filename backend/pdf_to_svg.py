import fitz  # PyMuPDF
import os

input_folder = "input"
output_folder = "output"


def pdf_to_svg(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_folder, filename)
            doc = fitz.open(input_path)

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                svg = page.get_svg_image()
                output_path = os.path.join(
                    output_folder,
                    f"{os.path.splitext(filename)[0]}_page_{page_num}.svg",
                )
                with open(output_path, "w") as svg_file:
                    svg_file.write(svg)

            print(f"{filename} was successfully converted to SVG.")
            doc.close()

