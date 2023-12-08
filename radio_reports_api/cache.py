from os import path, remove, makedirs, rmdir

from radio_reports.settings import CACHE_ROOT
from radio_reports_api.utils import unique_str


def save_file_to_cache(file, filename=None):
    _, file_extension = path.splitext(file.name)
    if filename is not None:
        filename = f"{unique_str()}{file_extension}"
    filepath = path.join(CACHE_ROOT, filename)

    with open(filepath, 'wb+') as destination: # write the file
        for chunk in file.chunks():
            destination.write(chunk)

    return filename, filepath

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
