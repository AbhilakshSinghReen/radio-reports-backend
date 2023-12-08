from os import path, remove, makedirs, rmdir
from uuid import uuid4
from time import time

from radio_reports.settings import CACHE_ROOT


def save_file_to_cache(file, filename=None):
    _, file_extension = path.splitext(file.name)
    if filename is not None:
        filename = f"{uuid4()}_{round(time() * 1000)}{file_extension}"
    filepath = path.join(CACHE_ROOT, filename)

    with open(filepath, 'wb+') as destination: # write the file
        for chunk in file.chunks():
            destination.write(chunk)

    return filename

def delete_from_cache(file_or_folder_name):
    file_or_folder_path = path.join(CACHE_ROOT, file_or_folder_name)

    if path.exists(file_or_folder_path):
        if path.isdir(file_or_folder_path):
            try:
                rmdir(file_or_folder_path)
            except:
                print(f"Failed to delete directory {file_or_folder_name} from the cache.")
        else:
            try:
                remove(file_or_folder_path)
            except:
                print(f"Failed to delete file {file_or_folder_name} from the cache.")

def create_folder_in_cache(folder_name):
    folder_path = path.join(CACHE_ROOT, folder_name)

    if path.exists(folder_path):
        return False
    
    makedirs(folder_path)
    return folder_path
