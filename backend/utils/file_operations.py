import os
from flask import request, jsonify
import time
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "cache/uploads"
CACHE_FOLDER = "cache/file-history"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

"""
@:parameter upload_dir: Chosen directory for the uploads folder
@:parameter file_cache: Chosen directory for the file-cache folder
Creates a cache directory located in /backend
"""


def create_directory(file_directory):
    try:
        os.mkdir(file_directory)
        print('Cache successfully created')
    except FileExistsError:
        print("The directory already exists")
    except PermissionError:
        print(f"This directory cannot be created, please check permissions")
    except Exception as e:
        print(f"An error has occurred: '{e}'")


"""
Saves uploaded files in queue
"""


def save_uploaded_file(destination):
    create_directory(destination)
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


"""
@:parameter filename
Determines if the file is safe
"""


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


"""

@:parameter directory
Destroys selected directory.
"""


def cleanup_cache(directory):
    try:
        os.remove(directory)
    except FileExistsError:
        print("Directory does not exist")
    except PermissionError:
        print("Unable to clean up, please check permissions")
    except Exception as e:
        print(f"An error has occurred: {e}")


"""

Moves specified file into specified directory
"""


def move_to(file_name, destination):
    if not os.path.exists(file_name):
        return None, 'Backend: Path does not exist, please check name'
    elif not os.path.exists(destination):
        return None, 'Backend: Path does not exist'
    else:
        return os.rename(file_name, destination), None


""" History getters and setters """

"""
Creates and returns an archive directory for use with history.
"""


def create_archive_directory(destination, dir_name):
    try:
        required_path_files = ['image-cache', 'data.txt', 'main.txt']
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


def write_data(directory, image_name, file_name, data):
    """When the pre-processor & processor are done with their work, they will write to the file cache using
    this helper file"""
    try:
        f = open(directory, "a")
        f.write(f"Image: {image_name}\n")
        f.write(f"Extracted Text for {image_name}: ")
        f.write(f"{data}\n")
        return directory, None
    except FileNotFoundError:
        return None, "Directory does not exist"
    except PermissionError:
        return None, "Cannot complete operations, please check permissions"
    except Exception as e:
        return None, f"An error has occurred: {e}"


def read_details(directory):
    try:
        files = os.path.join(directory, 'main.txt')
        # Parse the file for details
    except FileNotFoundError:
        return None, "No main.txt found in directory."
    except PermissionError:
        return None, 'Cannot complete operation, please check permissions'
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
