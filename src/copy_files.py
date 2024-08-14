import os
import shutil


def copy_static_files(source_dir="static", destination_dir="public"):
    if not os.path.exists(destination_dir):
        os.mkdir(destination_dir)

    clear_directory(destination_dir)
    recursive_copy(source_dir, destination_dir)


def recursive_copy(source_dir, destination_dir):
    os.makedirs(destination_dir, exist_ok=True)

    for item in os.listdir(source_dir):
        src_path = os.path.join(source_dir, item)
        dst_path = os.path.join(destination_dir, item)

        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)
        else:
            recursive_copy(src_path, dst_path)


def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
