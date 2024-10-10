import os
from flask import request
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
        return None, 'Backend: File does not exist, please check name'
    elif not os.path.exists(destination):
        return None, 'Backend: Path does not exist'
    else:
        return os.rename(file_name, destination), None

# Add file history methods
