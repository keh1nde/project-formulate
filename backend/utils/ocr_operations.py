import os
import cv2
import pytesseract
from backend.utils.file_operations import create_directory, create_archive_directory, write_data, move_to

def processing(identifier, queue_path, edited_image_directory, image_save_directory, raw_directory):
    try:
        files = os.listdir(queue_path)
        while len(files) != 0:
            for file in files:
                # Before processing starts, a copy of the file should be sent to image_save_directory

                img = file
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

                cv2.imwrite(raw_directory, invert)

                os.remove(file) # The file is processed, so we remove it from the queue

        files = os.listdir(edited_image_directory)
        amount_processed = 0 # We don't want to remove files from edited_image_directory, so we use this as an alternative
        while amount_processed != len(files):
            for file in files:
                text = pytesseract.image_to_string(file, lang='eng', config='--psm6')
                # Once write_data is amended, we call it using the identifier, text, and text_save_directory

                amount_processed += 1

        return "Success", None # For the frontend, it will allow handle_submit() to call handle_history()

    except identifier is None:
        return None, f"Backend (preprocessor): The save identifier {identifier} is missing."
    except FileNotFoundError:
        return None, "Backend (preprocessor): A file or directory was not found. Please try again later."
    except PermissionError:
        return None, ("Backend (preprocessor): Unable to complete pre-processing."
                      " Please check your permissions and try again.")
    except Exception as e:
        return None, f"Backend (preprocessor): An error has occurred: {e}"
