"""Delete last session"""

import shutil
import os


def delete_files_in_directory(directory):
    """test"""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except OSError as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def scheduled_deletion():
    """test"""
    directory_to_clean_1 = "uploads"
    delete_files_in_directory(directory_to_clean_1)
    directory_to_clean_2 = "output_folder"
    delete_files_in_directory(directory_to_clean_2)


if __name__ == "__main__":
    scheduled_deletion()
