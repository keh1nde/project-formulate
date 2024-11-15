import shutil
from flask import request
import time
from werkzeug.utils import secure_filename
import os

# <<< Begin Directory Operations >>>
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
# <<< End Directory Operations >>>

# <<< Begin Cache Operations >>>

def initialize_cache():
    dir_name = "cache"
    """Initializes a cache for use with the backend"""
    required_root_files = ['file-queue', 'file-uploads', 'tf_save']
    try:
        error = create_directory(dir_name)
        if error:
            return error
        for root_file in required_root_files:
            n_path = os.path.join(dir_name, root_file)
            os.makedirs(n_path)
        return None
    except Exception as e:
        return f"An error has occurred: {e}"

def cleanup_cache():
    """Destroys cache on app close."""
    try:
        if os.path.exists("cache"):
            files = os.listdir("cache")
            if not files:
                os.rmdir("cache")
                return None
            else:
                with shutil.rmtree:
                    shutil.rmtree("cache")
                return None

        os.rmdir("cache")
    except FileNotFoundError:
        return "Directory does not exist"
    except PermissionError:
        return "Unable to clean up, please check permissions"
    except Exception as e:
        return f"An error has occurred: {e}"

def create_archive_directory(destination, dir_name):
    """Creates and returns an archive directory for use with history."""
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
# <<< End Cache Operations >>>

# <<< Begin File Read Operations >>>

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

def read_data(directory): #  Needs to be rewritten using JSON
    try:
        files = os.path.join(directory, 'data.txt')
        # Parse the file for details
    except FileNotFoundError:
        return None, "No data.txt found in directory"
    except PermissionError:
        return None, 'Cannot complete operation, please check permissions'
    except Exception as e:
        return None, f"An error has occurred: {e}"

def read_details(directory): # Needs to be rewritten using YAML
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

# <<< End File Read Operations >>>

# <<< Begin File Write Operations >>>

def write_data(directory, image_name, file_name, data): # Needs to be rewritten with JSON
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

# <<< End File Write Operations >>>

# <<< Begin Auxiliary Operations >>>
def move_to(file_name, destination):
    """Moves specified file into specified directory"""
    if not os.path.exists(file_name):
        return None, 'Backend: Path does not exist, please check name'
    elif not os.path.exists(destination):
        return None, 'Backend: Path does not exist'
    else:
        return os.rename(file_name, destination), None

def allowed_file(filename):
    allowed_extension = {'png', 'jpg', 'jpeg', 'gif'}
    """
    Determines if the file is safe
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extension

def save_uploaded_file(destination): # Should be moved to a save related area
    """ Saves uploaded files in queue """
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

