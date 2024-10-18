import os
import cv2
import pytesseract
from backend.utils.file_operations import create_directory, create_archive_directory, write_data, move_to


def extract_text(image_path):
    """ Extracts text using TesseractOCR """
    try:
        text = pytesseract.image_to_string(image_path, lang='eng', config='--psm 6')

        write_data()


    except FileNotFoundError:
        return None, f"{image_path} not found."
    except PermissionError:
        return None, f"Unable to extract text from file. Please check permissions"




def preprocess_image(upload_cache, queue_cache, edited_files_directory, image_save_directory):
    error = ''
    """Moves image files from upload_cache to queue_cache, preprocesses them using Open CV, then passes them on for text extraction."""
    try:
        # Assume upload_cache = cache/file-upload
        # Assume queue_cache = cache/file-queue
        if not queue_cache:
            return None, f"File directory {queue_cache} not found."
        if not upload_cache:
            return None, f"File directory {upload_cache} not found."
        if not edited_files_directory:
            return None, f"File directory {edited_files_directory} not found."
        if not image_save_directory:
            return None, f"File directory {image_save_directory} not found."

        # Moving from uploads to cache
        files = os.listdir(upload_cache)
        for file in files:
            path = os.path.join(upload_cache, file)
            move_to(path, queue_cache)

        # Processing
        files = os.listdir(queue_cache)
        for file in files:
            img = cv2.imread(os.path.join(queue_cache, file))
            # Gray-scaling:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Gaussian Blur
            img = cv2.GaussianBlur(img, (3, 3), 0)

            # Thresholding (Using Otsu's Threshold)
            img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

            # Noise Removal using Morph Open
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=1)
            invert = 255 - opening

            save_path = os.path.join(edited_files_directory, file)
            cv2.imwrite(save_path, invert)

        # Call extract_text when all files are processed

        return None, error



    except FileNotFoundError:
        return None, f" File not found, please try again"
    except PermissionError:
        return None, "Unable to complete pre-processing. Please check your permissions and try again."
    except Exception as e:
        return None, f"An error has occurred: {e}"

