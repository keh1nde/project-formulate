from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file part")
            # Send error exception
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        # Send error exception
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)




# I still want to include errors for certain exceptions (ex. uploading files that are not supported)

if __name__ == '__main__':
    pass
