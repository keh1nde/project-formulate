import os
import cv2
import pytesseract

# I don't know how it's going to go yet, but I'm thinking:
# First, we import the safe files from /uploads, which contains the pictures for use by this algorithm

# Second, we pass it through a function that cleans up each file one by one, saving them to a cache that
# will be located at /ocr/file-cache. They will only be used here before they're destroyed after use.

# Then, we will begin scanning the files for text data. The data retrieved from the images will be saved
# to separate files somewhere in the backend, which when needed can be passed to the frontend for copy
# and pasting, or sent by email.

# When all files have been processed and sent, /file-cache will be either cleared, but not deleted or
# cleared and deleted.

# Implementation:

#

uploads_dir = 'backend/app/uploads'
dir_name = 'file-cache'
try:
    os.mkdir(dir_name)
    print('Cache successfully created')
except FileExistsError:
    print("The cache has already been created.")
except PermissionError:
    print(f"The cache cannot be created, please check permissions")
except Exception as e:
    print(f"An error has occurred: '{e}'")

# Load each file and perform pre-processing. Save to cache
files = os.listdir(uploads_dir)

for file in files:
    img = cv2.imread(os.path.join(uploads_dir, file))
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
    cv2.imwrite(os.path.join(dir_name, "image.jpg"), invert)

    # Use pytesseract to get data
    text = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')

    # We save the text data to another directory (to be done).

    # The files in file-cache will stay there to allow data to be viewed/fetched manually if needed.
    # On close, the directory will be destroyed.