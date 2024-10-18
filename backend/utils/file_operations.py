import os
import shutil
import json
from flask import request
import time
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "cache/uploads"
CACHE_FOLDER = "cache/file-history"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def create_directory(file_directory):
    """
    Creates a cache directory located in /backend
    This function initializes directories only.
    """
    try:
        os.mkdir(file_directory)
        return None
    except FileExistsError:
        return "The directory already exists"
    except PermissionError:
        return f"This directory cannot be created, please check permissions"
    except Exception as e:
        return f"An error has occurred: '{e}'"


def save_uploaded_file(destination):
    """ Saves uploaded files in queue """
    create_directory(destination) # Remove
    if 'file' not in request.files:
        return None, 'No file found.'
    file = request.files['file']
    if file.filename == '':
        return None, 'No file selected.'
    if not allowed_file(file.filename):
        return None, 'Path contains a file that is not allowed.'
    # Securing filename
    filename = secure_filename(file.filename)
    file_path = os.path.join(destination, filename)

    file.save(file_path)

    return file_path, None


def allowed_file(filename):
    """
    Determines if the file is safe
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def initialize_cache():
    """Initializes a cache for use with the backend"""
    required_root_files = ['file-queue', 'file-uploads', 'tf_save']
    try:
        error = create_directory("cache")
        if error:
            return error
        for root_file in required_root_files:
            n_path = os.path.join("cache", root_file)
            os.makedirs(n_path)
        return None
    except Exception as e:
        return f"An error has occurred: {e}"


def cleanup_cache(directory):
    """Destroys cache on app close."""
    try:
        if os.path.exists(directory):
            files = os.listdir(directory)
            if not files:
                os.rmdir(directory)
                return None
            else:
                with shutil.rmtree:
                    shutil.rmtree(directory)
                return None

        os.rmdir(directory)
    except FileNotFoundError:
        return "Directory does not exist"
    except PermissionError:
        return "Unable to clean up, please check permissions"
    except Exception as e:
        return f"An error has occurred: {e}"


def move_to(file_directory, destination):
    """Moves specified file into specified directory"""
    if not os.path.exists(file_directory):
        return None, f'Backend: Path {file_directory }does not exist, try again.'
    elif not os.path.exists(destination):
        return None, f'Backend: Path {destination} does not exist'
    else:
        return os.rename(file_directory, destination), None


""" History getters and setters """


def create_archive_directory(destination, dir_name):
    """Creates and returns an archive directory for use with history."""
    try:
        required_path_files = ['image-save', 'relation.txt', 'main.txt']

        if dir_name is None:
            dir_name = 'Untitled'
        current_time = time.strftime("%Y-%m-%d_%H-%M")
        directory_name = f"{dir_name}_{current_time}"

        n_path = os.path.join(destination, directory_name)

        os.makedirs(n_path)

        for file in required_path_files:
            os.makedirs(file)
            f = open(file, "a")
            if file is not required_path_files[0]:
                f.write(f"File created {current_time}")
                f.write(f"File edited {current_time}")

        return n_path, None
    except FileExistsError:
        current_time = time.strftime("%Y-%m-%d_%H-%M")
        directory_name = f"{dir_name}_{current_time}"
        n_path = os.path.join(destination, directory_name)
        return n_path, None
    except PermissionError:
        return None, "Cannot create path, please check permissions"
    except Exception as e:
        return None, f"An error has occurred: {e}"


def read_image_history(image_directory):
    try:
        files = os.listdir(image_directory)
        image_files = [file for file in files if file.endswith(('.png', '.jpg', '.jpeg'))]
        return image_files, None
    except FileNotFoundError:
        return None, 'This is not a image history directory.'
    except PermissionError:
        return None, 'Cannot complete operation, please check permissions'
    except Exception as e:
        return None, f"An Error has occurred: {e}"


def write_data(file_history, image_name, text_file_name, save_name):
    create_archive_directory(file_history, save_name) # Create new save
    """When the pre-processor & processor are done with their work, they will write to the file cache using
    this helper file"""
    try:
        path = os.path.join(file_history, 'relation.txt')
        with open(file_history, 'w') as file:
            json.dump(image_name, text_file_name)
        return None, None
    except FileNotFoundError:
        return None, "A directory does not exist. Please check all and try again."
    except PermissionError:
        return None, "Cannot write data, please check permissions and try again"
    except Exception as e:
        return None, f"An error has occurred: {e}"


def read_data(directory):
    try:
        files = os.path.join(directory, 'data.txt')
        # Parse the file for details
    except FileNotFoundError:
        return None, "No data.txt found in directory"
    except PermissionError:
        return None, 'Cannot complete operation, please check permissions'
    except Exception as e:
        return None, f"An error has occurred: {e}"


def read_details(directory):
    try:
        files = os.path.join(directory, 'main.txt')
        # Parse the file for details
    except FileNotFoundError:
        print(f'Directory used: {directory}')
        return None, "No main.txt found in directory."
    except PermissionError:
        return None, 'Cannot complete operation, please check permissions'
    except Exception as e:
        return None, f"An error has occurred: {e}"


