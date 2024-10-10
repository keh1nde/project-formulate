from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from backend.utils.file_operations import allowed_file, create_directory, cleanup_cache, save_uploaded_file
from backend.utils.ocr_operations import preprocess_image, extract_text

app = Flask(__name__)

file_cache = '/cache/file-history'


@app.route('/upload', method=['POST'])
def handle_file():
    if request.method == 'POST':
        file_path, error = save_uploaded_file()
    if error:
        return error

    # Preprocessing
    processed_image_path = preprocess_image(file_path)






# I still want to include errors for certain exceptions (ex. uploading files that are not supported)
