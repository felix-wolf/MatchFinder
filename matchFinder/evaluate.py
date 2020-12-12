from flask import (
    Blueprint, Flask, render_template, request, current_app as app)
from werkzeug.utils import secure_filename
import os
from . import database_helper
from . import matchCalculator

bp = Blueprint('evaluate', __name__, url_prefix='/evaluate')

@bp.route('/')
def index():
	verteilungen = database_helper.get_all_verteilungen()
	print(verteilungen)
	return render_template('evaluate.html', verteilungen=verteilungen)


@bp.route('csv_upload', methods=['POST'])
def csv_upload():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        assignments = matchCalculator.calculateFromCSV(uploaded_file)
        print(assignments)
    return render_template('results.html', data=assignments)