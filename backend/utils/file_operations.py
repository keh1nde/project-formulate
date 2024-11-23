import shutil
from flask import request
import time
from werkzeug.utils import secure_filename
import os
import yaml
import json

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

def old_write_data(directory): # Needs to be rewritten using YAML
    try:
        files = os.path.join(directory, 'data.txt')
        # Parse the file for details
    except FileNotFoundError:
        return None, "No data.txt found in directory"
    except PermissionError:
        return None, 'Cannot complete operation, please check permissions'
    except Exception as e:
        return None, f"An error has occurred: {e}"

def write_config(directory, save_name, image_dir, text_dir, ): # Could "image_dir" and "text_dir" both be arrays?
    # Config file should contain the name of the file,
    # the dates in which it was created and last modified.
    try:
        config_filename = f"{directory}_image-text-map.json"

        image_text_map = {
            image_dir : text_dir
        }

        with open(config_filename, 'w') as file:
            json.dump(image_text_map, config_filename, indent=4)
    except FileNotFoundError:
        return None, "Backend (write_config): No image_text_map.json found in directory"


def load_config(directory):
    try:
        config_filename = f"{directory}_config.yaml"

        with open(config_filename, 'r') as file:
            config = yaml.safe_load(file)
        return config, False
    except not os.path.exists(directory):
        return None, ("Backend (read_config): An error has occurred whilst"
                      " attempting to open directory. Please try again later.")
    except PermissionError:
        return None, "Backend (read_config): An error has occurred, please check permissions and try again."
    except Exception as e:
        return None, f"Backend (read_config): An error has occurred: {e}"

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

