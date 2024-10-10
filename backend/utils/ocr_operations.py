import os
import cv2
import pytesseract

UPLOAD_DIR = 'backend/cache/uploads'
FILE_CACHE = '/cache/file-history'
files = os.listdir(UPLOAD_DIR)


"""

Pre-processes images
"""


def preprocess_image(file_directory):
    for file in files:
        img = cv2.imread(os.path.join(UPLOAD_DIR, file))
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

        # We save the image to ocr/filecache
        cv2.imwrite(os.path.join(FILE_CACHE, "image.jpg"), invert)

    """
    Extracts text using TesseractOCR
    """


def extract_text(image_path):
    # Use pytesseract to get data
    text = pytesseract.image_to_string(image_path, lang='eng', config='--psm 6')
    return text


# The files in file-cache will stay there to allow data to be viewed/fetched manually if needed.
# On close, the directory will be destroyed.
