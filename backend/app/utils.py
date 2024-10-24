import os
from werkzeug.datastructures import FileStorage

def get_unique_filename(original_filename: str, upload_folder: str) -> str:
    """Generates a unique filename by appending a counter if the file already exists.

    Args:
        original_filename (str): The original filename.
        upload_folder (str): The folder where the file will be saved.

    Returns:
        str: A unique filename that does not exist in the upload folder.
    """
    filename, file_extension = os.path.splitext(original_filename)
    file_path = os.path.join(upload_folder, original_filename)

    counter = 1
    while os.path.exists(file_path):
        new_filename = f"{filename} ({counter}){file_extension}"
        file_path = os.path.join(upload_folder, new_filename)
        counter += 1

    return file_path

def save_file(file: FileStorage, upload_folder: str) -> str:
    """Saves the uploaded file to the specified folder, renaming if the file already exists.

    Args:
        file (FileStorage): The file to be saved.
        upload_folder (str): The folder where the file will be saved.

    Returns:
        str: The path of the saved file.
    """
    
    # Ensure the upload folder exists
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Get a unique filename
    unique_file_path = get_unique_filename(file.filename, upload_folder)

    # Save the file
    file.save(unique_file_path)
    
    return unique_file_path
