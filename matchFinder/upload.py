from flask import (
	Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for, abort)
import os
from werkzeug.utils import secure_filename
import imghdr
from . import matchCalculator

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.csv', '.txt']

bp = Blueprint('upload', __name__, url_prefix='/upload')

@bp.route('/')
def index():
	return render_template('upload.html')

@bp.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        assignments = matchCalculator.calculateMatch(uploaded_file)
        print(assignments)
    return redirect(url_for('upload.index'))
