import os

from flask import Flask, render_template, request, redirect, url_for, jsonify
from backend.utils.file_operations import allowed_file, create_directory, cleanup_cache, save_uploaded_file, move_to
from backend.utils.ocr_operations import preprocess_image, extract_text

app = Flask(__name__)

FILE_CACHE = '/cache/file-history'
UPLOAD_CACHE = '/cache/upload-cache'
QUEUE_CACHE = '/cache/queue-cache'
TF_SAVE = '/cache/text-file_save'


@app.route('/init', method=['POST'])
def initialize():
    pass


@app.route('/upload', method=['POST'])
def handle_file():
    if request.method == 'POST':
        file_path, error = save_uploaded_file(destination=UPLOAD_CACHE)
        if error:
            return generate_error_response(error)
    handle_processing()


def handle_processing():
    global FILE_CACHE, QUEUE_CACHE, TF_SAVE, UPLOAD_CACHE
    """ Error handling """
    if not QUEUE_CACHE or not UPLOAD_CACHE:
        return generate_error_response('Backend: No uploads found')
    if not TF_SAVE or not FILE_CACHE:
        return generate_error_response('Backend: Cache not properly initialized. Try again')

    """ Move files from UPLOAD to QUEUE"""
    files = os.listdir(UPLOAD_CACHE)
    for file in files:
        file = os.path.basename(file)
        file, error = move_to(file, QUEUE_CACHE)
        if error:
            return generate_error_response(error)

    """ Begin processing files """
    files = os.listdir(QUEUE_CACHE)
    for file in files:
        preprocess_image(file)
    # Return success


@app.route('/display', method=['GET'])
def handle_display():
    pass


""" This method will return the images and text from the helper files once they exist"""


@app.route('/history', method=['GET'])
def handle_history():
    pass


def generate_error_response(message):
    return jsonify({'success': False, 'error': message}), 400


"""Returns a JSON response for errors"""


