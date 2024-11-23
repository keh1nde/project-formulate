import os

from flask import Flask, render_template, request, redirect, url_for, jsonify
from backend.utils.file_operations import create_directory, cleanup_cache, move_to, initialize_cache
# from backend.utils.ocr_operations

app = Flask(__name__)

FILE_CACHE = '/cache/file-history'
UPLOAD_CACHE = '/cache/upload-cache'
QUEUE_CACHE = '/cache/queue-cache'
TF_SAVE = '/cache/text-file_save'


@app.route('/init', method=['POST'])
def initialize():
    success, error = None, None
    """Function to initialize web app"""
    os.mkdir("cache")
    initialize_cache(FILE_CACHE)
    if success:
        pass # We send a JSON response to the frontend that cache has been generated
    if error:
        generate_error_response(error)



@app.route('/upload', method=['POST'])
def handle_file():
    error = ""
    if request.method == 'POST':
        # file_path, error = save_uploaded_file(destination=UPLOAD_CACHE)
        if error:
            return generate_error_response(error)
    handle_processing()


def handle_processing():
    error, success = None, None
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
        success, error = move_to(file, QUEUE_CACHE)
        if error:
            return generate_error_response(error)

    """ Begin processing files """
    files = os.listdir(QUEUE_CACHE)
    for file in files:
        preprocess_image(file)
    if success: # When everything without error, we pass to error display
        handle_display()


@app.route('/display', method=['GET'])
def handle_display():
    """ Handles sending of text and images for use"""
    pass


""" This method will return the images and text from the helper files once they exist"""


@app.route('/history', method=['GET'])
def handle_history():
    """ Handles history of jobs, and can call handle_display to handle work"""
    pass


def generate_error_response(message):
    return jsonify({'success': False, 'error': message}), 400


"""Returns a JSON response for errors"""


