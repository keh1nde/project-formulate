import os
import cv2
import pytesseract


UPLOAD_DIR = 'backend/app/uploads'
DIR_NAME = 'file-cache'
try:
    os.mkdir(DIR_NAME)
    print('Cache successfully created')
except FileExistsError:
    print("The cache has already been created.")
except PermissionError:
    print(f"The cache cannot be created, please check permissions")
except Exception as e:
    print(f"An error has occurred: '{e}'")

# Load each file and perform pre-processing. Save to cache
files = os.listdir(UPLOAD_DIR)

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
    cv2.imwrite(os.path.join(DIR_NAME, "image.jpg"), invert)

    # Use pytesseract to get data
    text = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')

    # We save the text data to another directory (to be done).

    # The files in file-cache will stay there to allow data to be viewed/fetched manually if needed.
    # On close, the directory will be destroyed.