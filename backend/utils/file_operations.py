import os
from flask import request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "/uploads"
CACHE_FOLDER = "cache/file-cache"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

"""
@:parameter filename
Determines if the file is safe
"""


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


"""
@:parameter upload_dir: Chosen directory for the uploads folder
@:parameter file_cache: Chosen directory for the file-cache folder
Creates a cache directory located in /backend
"""


def create_directory(file_cache):
    try:
        os.mkdir(file_cache)
        print('Cache successfully created')
    except FileExistsError:
        print("The cache already exists")
    except PermissionError:
        print(f"The cache cannot be created, please check permissions")
    except Exception as e:
        print(f"An error has occurred: '{e}'")


"""

@:parameter directory
Destroys selected directory.
"""


def cleanup_cache(directory):
    try:
        os.remove(directory)
    except FileExistsError:
        print("Cache does not exist")
    except PermissionError:
        print("Unable to clean up, please check permissions")
    except Exception as e:
        print(f"An error has occurred: {e}")

