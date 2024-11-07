"""flv or mp4 file cutout"""

import os
import zipfile
from moviepy.editor import VideoFileClip
from PIL import Image


def extract_frame(video_path, output_dir, time_in_seconds, uuid_name):
    """flv or mp4 file cutout function"""
    clip = VideoFileClip(video_path)
    frame = clip.get_frame(time_in_seconds)
    image = Image.fromarray(frame)
    # Get the base name of the video file and create the output file name
    base_name = os.path.basename(video_path)
    file_name, _ = os.path.splitext(base_name)
    output_image_path = os.path.join(output_dir, f"{file_name}.pdf")
    image.save(output_image_path, format='PDF')
    clip.close()

    # Create a ZIP file with the uuid_name
    zip_file_path = os.path.join(output_dir, f"{uuid_name}.zip")
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        zipf.write(output_image_path, os.path.basename(output_image_path))

    # Remove the original PDF file after zipping
    os.remove(output_image_path)

    return zip_file_path