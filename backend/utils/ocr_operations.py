import os
import cv2
import pytesseract
from backend.utils.file_operations import create_directory, write_data


def preprocess_image(file_directory, file_cache):
    if not os.path.exists(file_directory):
        return None, f"Preprocessor: File directory {file_directory} does not exist"
    if not os.path.exists(file_cache):
        return None, f"Preprocessor: File directory {file_cache} does not exist"

    files = os.listdir(file_directory)
    for file in files:
        try:
            img = cv2.imread(os.path.join(file_directory, file))
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

            # We save the image to cache/filecache
            # cv2.imwrite(os.path.join(FILE_CACHE, "image.jpg"), invert)

            cache_path = os.path.join(file_cache, file)
            cv2.imwrite(cache_path, invert)

            path = os.path.join(file_directory, file_cache)
            data, error = extract_text(path), None
            if error:
                return None, error

            result, error = write_data(directory=file_cache, image_name=file, file_name="data.txt", data=data)

            if error:
                return None, error
        except Exception as e:
            return None, f"An error has occurred: {e}"

        """
        @:parameter file_directory: Path to File
        Pre-processes images
        """


"""
Extracts text using TesseractOCR
"""


def extract_text(image_path):
    try:
        # Use pytesseract to get data
        text = pytesseract.image_to_string(image_path, lang='eng', config='--psm 6')

        if not text:
            return None, None

        return text, None
    except Exception as e:
        return None, f"An error has occurred: {e}"
