from flask import (
	Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for, abort, current_app as app)
import json
import numpy as np
import os
from . import matchCalculator
from werkzeug.utils import secure_filename
from matchFinder.models import teilnehmer
from . import db

bp = Blueprint('results', __name__, url_prefix='/results')

@bp.route('/')
def index():
    return render_template('404.html')

@bp.route('present', methods=['POST'])
def present():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        assignments = matchCalculator.calculateFromCSV(uploaded_file)
        print(assignments)
    return render_template('results.html', data=assignments)